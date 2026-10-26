#Requires -Version 5.1
<# Native offline entry point. Windows PowerShell 5.1 and .NET only.
   No downloads, Python invocation, policy changes or account operations.
   JSON on stdout is for the assistant; explain results in the user's language.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][ValidateSet('install','start','scan','ingest','verify','folders','overview')][string]$Action,
    [Parameter(Mandatory=$true)][string]$Root,
    [string]$Source,
    [ValidateRange(1900,9999)][int]$Year = (Get-Date).Year,
    [ValidateSet('en','ru','de')][string]$Language = 'en',
    [ValidateSet('localized','legacy')][string]$Layout = 'localized',
    [ValidateSet('general','bookkeeping','tax-consultant')][string]$Mode = 'general',
    [string]$Period,
    [ValidateSet('codex','claude','both')][string]$Target = 'both',
    [ValidateRange(1,10000)][int]$MaxEntries = 1000,
    [ValidateRange(0,32)][int]$MaxDepth = 10,
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2
$utf8 = New-Object Text.UTF8Encoding($false, $true)
[Console]::OutputEncoding = $utf8
$limit = 50 * 1024 * 1024
$extensions = @('.pdf','.xml','.png','.jpg','.jpeg','.tif','.tiff','.csv')
$markerName = '00_admin/workspace.json'
$kitRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))

function Absolute([string]$path) {
    if ([string]::IsNullOrWhiteSpace($path) -or -not [IO.Path]::IsPathRooted($path) -or $path -match '(^|[\\/])\.\.([\\/]|$)') {
        throw 'Use an absolute local path without parent traversal.'
    }
    if ($path.StartsWith('\\') -or ($path -replace '^[A-Za-z]:','') -match ':') { throw 'Network/device paths and alternate data streams are not supported.' }
    return [IO.Path]::GetFullPath($path)
}
function Chain([string]$path, [bool]$file = $false) {
    $current = $path
    while ($current) {
        if (Test-Path -LiteralPath $current) {
            $item = Get-Item -LiteralPath $current -Force
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Linked/reparse paths are not supported: $current. Use the real location instead." }
            if ($current -eq $path -and $file) {
                if ($item.PSIsContainer) { throw 'Expected a regular file.' }
            } elseif (-not $item.PSIsContainer) { throw 'Expected a directory.' }
        }
        $current = [IO.Path]::GetDirectoryName($current)
    }
}
function Private([string]$path) {
    $current = $path
    while ($current) {
        foreach ($name in @('.git','SKILL.md','skill.md')) {
            if (Test-Path -LiteralPath (Join-Path $current $name)) { throw 'Keep business data outside Git and skill directories.' }
        }
        if ((Test-Path -LiteralPath (Join-Path $current 'HEAD')) -and (Test-Path -LiteralPath (Join-Path $current 'objects')) -and (Test-Path -LiteralPath (Join-Path $current 'refs'))) { throw 'Bare Git repository rejected.' }
        $current = [IO.Path]::GetDirectoryName($current)
    }
}
function ReadBytes([string]$path) {
    Chain $path $true
    $stream = [IO.File]::Open($path, [IO.FileMode]::Open, [IO.FileAccess]::Read, [IO.FileShare]::Read)
    try {
        if ($stream.Length -gt $limit) { throw 'File exceeds 50 MiB.' }
        $memory = New-Object IO.MemoryStream
        try { $stream.CopyTo($memory); if ($memory.Length -gt $limit) { throw 'File exceeds 50 MiB.' }; return ,$memory.ToArray() } finally { $memory.Dispose() }
    } finally { $stream.Dispose() }
}
function ReadJson([string]$path) {
    $text = $utf8.GetString((ReadBytes $path))
    # 5.1 preserves top-level arrays; 7 needs NoEnumerate to preserve []/[null].
    # Parse the original text, never embed unvalidated JSON into a wrapper.
    if ((Get-Command ConvertFrom-Json).Parameters.ContainsKey('DateKind')) {
        # ISO timestamps are fingerprinted strings; DateTime parsing loses precision.
        $parsed = ConvertFrom-Json -InputObject $text -NoEnumerate -DateKind String
    } elseif ((Get-Command ConvertFrom-Json).Parameters.ContainsKey('NoEnumerate')) {
        $parsed = ConvertFrom-Json -InputObject $text -NoEnumerate
    } else {
        $parsed = ConvertFrom-Json -InputObject $text
    }
    return ,$parsed
}
function BytesJson($value) { return ,$utf8.GetBytes((ConvertTo-Json -InputObject $value -Depth 40 -Compress) + "`n") }
function FolderLayout {
    $descriptor = Join-Path $rootPath '.workspace-layout.json'
    if (-not (Test-Path -LiteralPath $descriptor)) {
        if (Test-Path -LiteralPath (Join-Path $rootPath '.business-kit')) { throw 'Missing localized layout; preserve existing files.' }
        return $null
    }
    $record = ReadJson $descriptor
    if ($record -isnot [pscustomobject] -or (@($record.PSObject.Properties.Name | Sort-Object) -join ',') -ne 'language,schema_version' -or $record.schema_version -isnot [int] -and $record.schema_version -isnot [long] -or $record.schema_version -ne 1 -or $record.language -cnotin @('en','ru','de')) { throw 'Unsupported folder layout.' }
    $catalog = ReadJson (Join-Path $kitRoot 'assets/folder-layouts.json')
    $words = $catalog.languages.PSObject.Properties[$record.language].Value
    foreach ($prefix in $words.paths.PSObject.Properties.Name) {
        if (Test-Path -LiteralPath (Join-Path $rootPath $prefix.Split('/')[0])) { throw 'Conflicting legacy and localized folders; preserve both.' }
    }
    return @{record=$record; words=$words}
}
function WorkspacePath([string]$relative) {
    if ([IO.Path]::IsPathRooted($relative) -or $relative -match '(^|[\\/])\.\.([\\/]|$)') { throw 'Expected a relative workspace path.' }
    $info = FolderLayout
    if ($null -ne $info) {
        foreach ($property in @($info.words.paths.PSObject.Properties | Sort-Object { $_.Name.Length } -Descending)) {
            if ($relative -ceq $property.Name -or $relative.StartsWith($property.Name + '/', [StringComparison]::Ordinal)) {
                $suffix = $relative.Substring($property.Name.Length).TrimStart('/').Split('/')
                if ($property.Name -ceq '06_bookkeeping' -and $suffix.Count -ge 3) {
                    $part = $info.words.parts.PSObject.Properties[$suffix[2]]
                    if ($null -ne $part) { $suffix[2] = $part.Value }
                }
                $relative = $property.Value
                if ($suffix[0]) { $relative += '/' + ($suffix -join '/') }
                break
            }
        }
    }
    return Join-Path $rootPath $relative
}
function WorkspacePresent([string]$path) {
    foreach ($name in @($markerName,'.workspace-layout.json','.business-kit')) {
        if (Test-Path -LiteralPath (Join-Path $path $name)) { return $true }
    }
    return $false
}
function Hash([byte[]]$bytes) {
    $sha = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-','').ToLowerInvariant() } finally { $sha.Dispose() }
}
function WriteNew([string]$path, [byte[]]$bytes) {
    Chain $path $true
    $parent = [IO.Path]::GetDirectoryName($path)
    Chain $parent
    [void][IO.Directory]::CreateDirectory($parent)
    $stream = [IO.File]::Open($path, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { $stream.Write($bytes, 0, $bytes.Length); $stream.Flush($true) } finally { $stream.Dispose() }
}
function ReplaceJson([string]$path, $value) {
    Chain $path $true
    $temp = $path + '.' + [guid]::NewGuid().ToString('N') + '.tmp'
    WriteNew $temp (BytesJson $value)
    try { [IO.File]::Replace($temp, $path, [NullString]::Value) } finally { if ([IO.File]::Exists($temp)) { [IO.File]::Delete($temp) } }
}
function Now { return [DateTime]::UtcNow.ToString('o') }
function Event($name, $details) { return @{ event_id=[guid]::NewGuid().ToString('N'); recorded_at=(Now); action=$name; details=$details } }
function Audit($name, $details) {
    $path = WorkspacePath '09_audit/events.json'
    $events = ReadJson $path
    if ($events -isnot [Array] -or @($events | Where-Object { $null -eq $_ -or $_ -isnot [pscustomobject] }).Count) { throw 'Invalid audit log; preserve and inspect it.' }
    ReplaceJson $path (@($events) + (Event $name $details))
}
function Workspace {
    Chain $rootPath
    Private $rootPath
    $marker = ReadJson (WorkspacePath $markerName)
    if ($marker.schema -ne 'german-business-workspace' -or $marker.schema_version -ne 1) { throw 'Unsupported workspace; do not initialize over it.' }
    $id = [guid]::Empty
    if (-not [guid]::TryParse($marker.workspace_id, [ref]$id)) { throw 'Invalid workspace identity.' }
    if ($marker.language -notin @('en','ru','de') -or $marker.mode -notin @('general','bookkeeping','tax-consultant')) { throw 'Invalid saved preferences.' }
    $info = FolderLayout
    if ($null -ne $info -and ($null -eq $marker.PSObject.Properties['folder_layout'] -or $marker.folder_layout.schema_version -ne 1 -or $marker.folder_layout.language -cne $info.record.language)) { throw 'Folder layout does not match workspace identity.' }
    if ($null -eq $info -and $null -ne $marker.PSObject.Properties['folder_layout']) { throw 'Localized marker has no layout descriptor.' }
    return $marker
}
function Index {
    $index = ReadJson (WorkspacePath '00_admin/documents.json')
    if ($index.schema_version -ne 1 -or $index.documents -isnot [Array]) { throw 'Invalid document index.' }
    return $index
}
function Verify {
    $index = Index
    $errors = New-Object 'Collections.Generic.List[string]'
    $paths = @{}
    $ids = @{}
    foreach ($doc in $index.documents) {
        try {
            if ($doc.period -notmatch '^[1-9][0-9]{3}-(0[1-9]|1[0-2])$' -or [int]$doc.period.Substring(0,4) -lt 1900) { throw 'Invalid period.' }
            if ($doc.sha256 -cnotmatch '^[0-9a-f]{64}$' -or [string]::IsNullOrWhiteSpace($doc.document_id) -or $ids.ContainsKey($doc.document_id)) { throw 'Invalid digest or duplicate identity.' }
            $ids[$doc.document_id] = $true
            $ext = [IO.Path]::GetExtension($doc.path)
            $expected = '06_bookkeeping/' + $doc.period.Substring(0,4) + '/' + $doc.period.Substring(5,2) + '/originals/' + $doc.sha256 + $ext
            if ($ext -cnotin $extensions -or $doc.path -cne $expected -or $paths.ContainsKey($expected)) { throw 'Invalid or duplicate original path.' }
            $paths[$expected] = $true
            $bytes = ReadBytes (WorkspacePath $expected)
            if ($bytes.Length -ne $doc.size_bytes -or (Hash $bytes) -cne $doc.sha256) { throw 'Original content or size changed.' }
        } catch { $errors.Add($_.Exception.Message) }
    }
    $unindexed = 0
    $base = WorkspacePath '06_bookkeeping'
    if (Test-Path -LiteralPath $base) {
        Chain $base
        foreach ($yearDir in Get-ChildItem -LiteralPath $base -Force) {
            Chain $yearDir.FullName
            foreach ($monthDir in Get-ChildItem -LiteralPath $yearDir.FullName -Force) {
                Chain $monthDir.FullName
                $originals = WorkspacePath ('06_bookkeeping/' + $yearDir.Name + '/' + $monthDir.Name + '/originals')
                if (-not (Test-Path -LiteralPath $originals)) { continue }
                Chain $originals
                foreach ($entry in Get-ChildItem -LiteralPath $originals -Force) {
                    $relative = '06_bookkeeping/' + $yearDir.Name + '/' + $monthDir.Name + '/originals/' + $entry.Name
                    if ($entry.PSIsContainer -or ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) -or -not $paths.ContainsKey($relative)) { $unindexed++; $errors.Add('Unindexed or unsafe original: ' + $relative) }
                }
            }
        }
    }
    $state = 'ok'; if ($errors.Count) { $state = 'needs_review' }
    return @{status=$state; indexed_documents=$index.documents.Count; unindexed_originals=$unindexed; errors=@($errors.ToArray()); scope='Original integrity only; no accounting, processing assessment or tax certification.'}
}
function Install {
    if (-not [IO.Directory]::Exists($rootPath)) { throw 'Install root must be an existing user home or project directory.' }
    Chain $kitRoot
    $catalogPath = Join-Path $kitRoot 'assets/skill-set.json'
    $catalog = $utf8.GetString((ReadBytes $catalogPath)) | ConvertFrom-Json
    if (@($catalog.PSObject.Properties.Name).Count -ne 2 -or
        $null -eq $catalog.PSObject.Properties['schema_version'] -or
        $null -eq $catalog.PSObject.Properties['skills'] -or
        -not ($catalog.schema_version -is [int] -or $catalog.schema_version -is [long]) -or $catalog.schema_version -ne 1 -or
        -not ($catalog.skills -is [array])) { throw 'Unsupported skill catalog.' }
    $names = @($catalog.skills)
    if ($names.Count -lt 1 -or $names.Count -gt 32 -or $names[0] -cne 'de-business-kit') { throw 'Missing shared core in skill catalog.' }
    $seen = @{}; $packages = @{}; $allFiles = @{}
    $bundleRoot = [IO.Path]::GetDirectoryName($kitRoot)
    foreach ($name in $names) {
        if (-not ($name -is [string]) -or $name.Length -gt 64 -or
            $name -cnotmatch '\Ade-business-[a-z0-9]+(?:-[a-z0-9]+)*\z' -or $seen.ContainsKey($name)) { throw 'Invalid or duplicate skill name.' }
        $seen[$name] = $true
        $skillRoot = Join-Path $bundleRoot $name
        Chain $skillRoot
        if (-not [IO.Directory]::Exists($skillRoot)) { throw ('Missing skill: ' + $name) }
        $entryText = $utf8.GetString((ReadBytes (Join-Path $skillRoot 'SKILL.md')))
        if (-not $entryText.Replace("`r`n", "`n").StartsWith("---`nname: $name`n")) { throw ('Skill identity mismatch: ' + $name) }
        $files = New-Object 'Collections.Generic.List[object]'
        $pending = New-Object 'Collections.Generic.Stack[string]'
        $pending.Push($skillRoot)
        while ($pending.Count) {
            $directory = $pending.Pop()
            Chain $directory
            foreach ($item in Get-ChildItem -LiteralPath $directory -Force) {
                if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Linked package resource rejected.' }
                if ($item.PSIsContainer) { $pending.Push($item.FullName) } else {
                    $relative = $item.FullName.Substring($skillRoot.Length).TrimStart([char[]]'\/')
                    $file = @{relative=$relative; bytes=(ReadBytes $item.FullName)}
                    $files.Add($file)
                    $allFiles[$name + '/' + $relative.Replace('\','/')] = $file.bytes
                }
            }
        }
        if (-not $allFiles.ContainsKey($name + '/agents/openai.yaml')) { throw ('Missing skill metadata: ' + $name) }
        $packages[$name] = $files
    }
    # Resolve every local reference against the captured bundle, never the source
    # checkout or another installed skill outside this inventory.
    foreach ($key in @($allFiles.Keys)) {
        if (-not $key.EndsWith('.md')) { continue }
        foreach ($match in [regex]::Matches($utf8.GetString($allFiles[$key]), '\]\(([^)]+)\)')) {
            $link = $match.Groups[1].Value
            if ($link -match '^[a-zA-Z][a-zA-Z0-9+.-]*:' -or $link.StartsWith('#')) { continue }
            $parent = [IO.Path]::GetDirectoryName((Join-Path $bundleRoot $key))
            $resolved = [IO.Path]::GetFullPath((Join-Path $parent ($link.Split('#')[0])))
            if (-not $resolved.StartsWith($bundleRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw 'Skill reference escapes the bundle.' }
            $targetKey = $resolved.Substring($bundleRoot.Length).TrimStart([char[]]'\/').Replace('\','/')
            $found = $allFiles.ContainsKey($targetKey)
            if (-not $found) { foreach ($candidate in $allFiles.Keys) { if ($candidate.StartsWith($targetKey.TrimEnd('/') + '/', [StringComparison]::Ordinal)) { $found = $true; break } } }
            if (-not $found) { throw ('Missing skill reference: ' + $key + ' -> ' + $link) }
        }
    }
    $hosts = @($Target); if ($Target -eq 'both') { $hosts = @('codex','claude') }
    $targets = @()
    foreach ($hostName in $hosts) {
        $folder = '.agents'; if ($hostName -eq 'claude') { $folder = '.claude' }
        foreach ($name in $names) {
            $dest = Join-Path $rootPath ($folder + '/skills/' + $name)
            Chain $dest
            if ((Test-Path -LiteralPath $dest) -or $dest.StartsWith($bundleRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) { throw 'Existing installation or destination inside package; preserve it and review update separately.' }
            $targets += $dest
        }
    }
    if ($DryRun) { return @{status='preview'; destinations=$targets; files=$allFiles.Count} }
    # Publish complete staged directories with a no-overwrite move. A raced
    # destination is preserved; any completed first target stays visible.
    foreach ($dest in $targets) {
        $parent = [IO.Path]::GetDirectoryName($dest)
        Chain $parent
        [void][IO.Directory]::CreateDirectory($parent)
        $stage = Join-Path $parent ('.de-business-kit-stage-' + [guid]::NewGuid().ToString('N'))
        [void][IO.Directory]::CreateDirectory($stage)
        $skillName = [IO.Path]::GetFileName($dest)
        foreach ($file in $packages[$skillName]) { WriteNew (Join-Path $stage $file.relative) $file.bytes }
        Chain $parent
        [IO.Directory]::Move($stage, $dest)
    }
    return @{status='installed'; destinations=$targets; note='Verify skill discovery in the actual host. No permissions or execution policy changed.'}
}

$rootPath = Absolute $Root
Chain $rootPath
if ($DryRun -and $Action -ne 'install') { throw 'DryRun is supported only for install.' }
if ($Action -eq 'install') { Install | ConvertTo-Json -Depth 40; return }
Private $rootPath
if ($Action -eq 'start' -and -not (Test-Path -LiteralPath (WorkspacePath $markerName))) {
    if ((Test-Path -LiteralPath $rootPath) -and @(Get-ChildItem -LiteralPath $rootPath -Force).Count) { throw 'Start requires an empty folder or an existing workspace. Keep source files separate.' }
    [void][IO.Directory]::CreateDirectory($rootPath)
}
$lockPath = Join-Path $rootPath '.workspace.lock'
$lock = $null
try {
    # Same lock as Python writers. Read-only operations refuse active writes too.
    $lock = [IO.File]::Open($lockPath, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    # The host lets doctor tell an ended local writer from another computer's lock.
    $lockBytes = BytesJson @{pid=$PID; created_at=(Now); host=[System.Net.Dns]::GetHostName()}
    $lock.Write($lockBytes,0,$lockBytes.Length); $lock.Flush($true)
    $result = $null
    if ($Action -eq 'start' -and -not (Test-Path -LiteralPath (WorkspacePath $markerName))) {
        if (@(Get-ChildItem -LiteralPath $rootPath -Force | Where-Object { $_.Name -ne '.workspace.lock' }).Count) { throw 'Folder changed; preserve it.' }
        if ($Layout -eq 'localized') { WriteNew (Join-Path $rootPath '.workspace-layout.json') (BytesJson @{schema_version=1; language=$Language}) }
        $seed = ReadJson (Join-Path $kitRoot 'assets/workspace-seed.json')
        foreach ($property in $seed.PSObject.Properties) { WriteNew (WorkspacePath $property.Name) (BytesJson $property.Value) }
        foreach ($dir in @('00_admin/inbox','02_registration','03_banking','04_accounting',"05_tax/$Year",'06_bookkeeping','07_exports','08_correspondence','09_audit/history')) { [void][IO.Directory]::CreateDirectory((WorkspacePath $dir)) }
        WriteNew (WorkspacePath '09_audit/events.json') (BytesJson @((Event 'workspace_initialized' @{year=$Year; language=$Language; mode=$Mode; runtime='powershell'})))
        # Marker last: interrupted initialization must never look complete.
        $newMarker = @{schema='german-business-workspace'; schema_version=1; workspace_id=[guid]::NewGuid().ToString(); created_at=(Now); initial_year=$Year; language=$Language; mode=$Mode}
        if ($Layout -eq 'localized') {
            $info = FolderLayout
            $newMarker.folder_layout = $info.record
            WriteNew (Join-Path $rootPath $info.words.guide_name) ($utf8.GetBytes($info.words.guide))
            if ($env:OS -eq 'Windows_NT') {
                foreach ($hidden in @('.business-kit','.workspace-layout.json')) {
                    $hiddenPath = Join-Path $rootPath $hidden
                    [IO.File]::SetAttributes($hiddenPath, ([IO.File]::GetAttributes($hiddenPath) -bor [IO.FileAttributes]::Hidden))
                }
            }
        }
        WriteNew (WorkspacePath $markerName) (BytesJson $newMarker)
        $result = @{status='initialized'; language=$Language; mode=$Mode; setup='processing_review_not_recorded'; next='Review actual data processing; use public/synthetic data until assessed.'}
    } else {
        $marker = Workspace
        switch ($Action) {
            'start' {
                $integrity = Verify
                $result = @{status='resumed'; language=$marker.language; mode=$marker.mode; integrity=$integrity; setup='not_assessed_by_native_command'; next='Read existing profile, tasks and processing evidence; do not reset or infer approval.'}
            }
            'verify' { $result = Verify }
            'overview' {
                . (Join-Path $PSScriptRoot 'windows-overview.ps1')
                $result = NativeOverview
            }
            'folders' {
                $info = FolderLayout
                $paths = @{}
                $catalog = ReadJson (Join-Path $kitRoot 'assets/folder-layouts.json')
                foreach ($key in $catalog.languages.en.paths.PSObject.Properties.Name) {
                    $paths[$key] = (WorkspacePath $key).Substring($rootPath.TrimEnd([char[]]'\/').Length + 1).Replace('\','/')
                }
                $result = @{layout='legacy'; folder_language=$null; paths=$paths; guide=$null}
                if ($null -ne $info) { $result.layout='localized'; $result.folder_language=$info.record.language; $result.guide=$info.words.guide_name }
            }
            'ingest' {
                if ($Period -notmatch '^[1-9][0-9]{3}-(0[1-9]|1[0-2])$' -or [int]$Period.Substring(0,4) -lt 1900) { throw 'Storage period must be YYYY-MM, year 1900-9999.' }
                $inputPath = Absolute $Source
                $ext = [IO.Path]::GetExtension($inputPath).ToLowerInvariant()
                if ($ext -notin $extensions) { throw 'Unsupported format; do not import credentials or executable content.' }
                if ((Verify).status -ne 'ok') { throw 'Existing original integrity needs review; no import performed.' }
                $events = ReadJson (WorkspacePath '09_audit/events.json')
                if ($events -isnot [Array] -or @($events | Where-Object { $null -eq $_ -or $_ -isnot [pscustomobject] }).Count) { throw 'Invalid audit log.' }
                $data = ReadBytes $inputPath
                $digest = Hash $data
                $index = Index
                $existing = @($index.documents | Where-Object { $_.sha256 -ceq $digest })
                if ($existing.Count) {
                    Audit 'document_content_seen_again' @{document_id=$existing[0].document_id}
                    $result = @{status='existing_content'; document_id=$existing[0].document_id; note='Identical bytes; not a business duplicate determination.'}
                } else {
                    $relative = '06_bookkeeping/' + $Period.Substring(0,4) + '/' + $Period.Substring(5,2) + '/originals/' + $digest + $ext
                    WriteNew (WorkspacePath $relative) $data
                    $document = @{document_id='doc-' + [guid]::NewGuid().ToString('N'); sha256=$digest; size_bytes=$data.Length; original_name=[IO.Path]::GetFileName($inputPath); path=$relative; period=$Period; imported_at=(Now); status='imported'; provider_state='unknown'}
                    $index.documents = @($index.documents) + $document
                    ReplaceJson (WorkspacePath '00_admin/documents.json') $index
                    Audit 'document_imported' @{document_id=$document.document_id; sha256=$digest}
                    $result = @{status='imported'; document_id=$document.document_id; size_bytes=$data.Length; note='Storage period only; document catalog/review/posting not performed.'}
                }
            }
            'scan' {
                $sourcePath = Absolute $Source
                Chain $sourcePath
                if (-not [IO.Directory]::Exists($sourcePath)) { throw 'Source directory missing.' }
                $sep = [IO.Path]::DirectorySeparatorChar
                $left = $rootPath.TrimEnd([char[]]'\/') + $sep; $right = $sourcePath.TrimEnd([char[]]'\/') + $sep
                if ($left.StartsWith($right,[StringComparison]::OrdinalIgnoreCase) -or $right.StartsWith($left,[StringComparison]::OrdinalIgnoreCase)) { throw 'Source and workspace must not overlap.' }
                if (WorkspacePresent $sourcePath) { throw 'Resume an existing workspace instead of scanning it as a source.' }
                $entries = New-Object 'Collections.Generic.List[object]'
                $queue = New-Object 'Collections.Generic.Stack[object]'
                $queue.Push(@{path=$sourcePath; depth=0})
                $complete = $true; $candidates = 0
                while ($queue.Count -gt 0 -and $entries.Count -lt $MaxEntries) {
                    $parent = $queue.Pop()
                    Chain $parent.path
                    # Enumerate lazily: entry limit bounds metadata and memory, not just output.
                    foreach ($child in [IO.Directory]::EnumerateFileSystemEntries($parent.path)) {
                        if ($entries.Count -ge $MaxEntries) { $complete=$false; break }
                        $item = Get-Item -LiteralPath $child -Force
                        $row = @{path=$child.Substring($right.Length).Replace('\','/'); status='skipped'; reason=$null}
                        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { $row.reason='link_or_reparse_point' }
                        elseif ($item.Name.StartsWith('.') -or ($item.Attributes -band [IO.FileAttributes]::Hidden)) { $row.reason='hidden_entry' }
                        elseif ($item.PSIsContainer) {
                            if (WorkspacePresent $child) { $row.reason='existing_workspace' }
                            elseif ($parent.depth -ge $MaxDepth) { $row.reason='depth_limit'; $complete=$false }
                            else { $row.status='directory'; $queue.Push(@{path=$child; depth=$parent.depth+1}) }
                        } elseif ($item.Extension.ToLowerInvariant() -notin $extensions) { $row.reason='unsupported_or_credential' }
                        elseif ($item.Length -gt $limit) { $row.reason='file_too_large' }
                        else { $row.status='candidate'; $row.size_bytes=$item.Length; $candidates++ }
                        $entries.Add($row)
                    }
                }
                if ($queue.Count) { $complete=$false }
                $result = @{status='preview'; source_folder=$sourcePath; candidates=$candidates; entries=@($entries.ToArray()); traversal_complete=$complete; max_entries=$MaxEntries; max_depth=$MaxDepth; scope='Metadata only. No import, source-content reads, tax classification or cloud-residency verification.'}
            }
        }
    }
    ConvertTo-Json -InputObject $result -Depth 40
} finally {
    if ($null -ne $lock) { $lock.Dispose(); [IO.File]::Delete($lockPath) }
}
