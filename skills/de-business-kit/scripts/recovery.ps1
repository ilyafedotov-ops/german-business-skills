[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][ValidateSet('backup','verify','restore')][string]$Action,
    [string]$Root,
    [string]$Destination,
    [string]$Backup
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2
$utf8 = New-Object Text.UTF8Encoding($false, $true)
[Console]::OutputEncoding = $utf8
$lockName = '.workspace.lock'

function Chain([string]$path, [bool]$file=$false) {
    $current=$path
    while ($current) {
        if (Test-Path -LiteralPath $current) {
            $item=Get-Item -LiteralPath $current -Force
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Linked/reparse paths are not supported.' }
            if ($current -eq $path -and $file) { if ($item.PSIsContainer) { throw 'Expected a regular file.' } }
            elseif (-not $item.PSIsContainer) { throw 'Expected a directory.' }
        }
        $current=[IO.Path]::GetDirectoryName($current)
    }
}
function Location([string]$path) {
    if ([string]::IsNullOrWhiteSpace($path) -or -not [IO.Path]::IsPathRooted($path) -or $path -match '(^|[\\/])\.\.([\\/]|$)' -or $path.StartsWith('\\') -or ($path -replace '^[A-Za-z]:','') -match ':') { throw 'Use an absolute local directory path without parent traversal.' }
    $full=[IO.Path]::GetFullPath($path).TrimEnd([char[]]'\/'); Chain $full
    $current=$full
    while ($current) {
        foreach ($name in @('.git','SKILL.md','skill.md')) { if (Test-Path -LiteralPath (Join-Path $current $name)) { throw 'Keep recovery data outside Git and skill directories.' } }
        if ((Test-Path -LiteralPath (Join-Path $current 'HEAD')) -and (Test-Path -LiteralPath (Join-Path $current 'objects')) -and (Test-Path -LiteralPath (Join-Path $current 'refs'))) { throw 'Bare Git repository rejected.' }
        $current=[IO.Path]::GetDirectoryName($current)
    }
    return $full
}
function Fresh([string]$path,[string]$outside) {
    $full=Location $path
    $separator=[IO.Path]::DirectorySeparatorChar
    if ($full.Equals($outside,[StringComparison]::OrdinalIgnoreCase) -or $full.StartsWith($outside+$separator,[StringComparison]::OrdinalIgnoreCase) -or $outside.StartsWith($full+$separator,[StringComparison]::OrdinalIgnoreCase)) { throw 'Recovery destinations must be outside the source tree.' }
    if (Test-Path -LiteralPath $full) { throw 'Destination already exists; choose a new private directory.' }
    if (-not [IO.Directory]::Exists([IO.Path]::GetDirectoryName($full))) { throw 'Destination parent must already exist.' }
    return $full
}
function Relative([string]$value) {
    if ([string]::IsNullOrWhiteSpace($value) -or $value.StartsWith('/') -or $value.Contains('\')) { throw 'Invalid backup member path.' }
    foreach ($part in $value.Split('/')) {
        if (-not $part -or $part -in @('.','..') -or $part.EndsWith(' ') -or $part.EndsWith('.') -or $part -match '[\x00-\x1f<>:"|?*]' -or $part -match '^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\.|$)') { throw 'Backup member is not a safe portable path.' }
    }
    return $value
}
function Key([string]$value) { return $value.Normalize([Text.NormalizationForm]::FormC).ToUpperInvariant() }
function Json([string]$path) {
    Chain $path $true
    $stream=[IO.File]::Open($path,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::Read)
    try {
        if ($stream.Length -gt 50*1024*1024) { throw 'Manifest or workspace marker exceeds 50 MiB.' }
        $reader=New-Object IO.StreamReader($stream,$utf8,$false)
        try { $text=$reader.ReadToEnd() } finally { $reader.Dispose() }
    } finally { $stream.Dispose() }
    $options=@{InputObject=$text}
    if ((Get-Command ConvertFrom-Json).Parameters.ContainsKey('NoEnumerate')) { $options.NoEnumerate=$true }
    if ((Get-Command ConvertFrom-Json).Parameters.ContainsKey('DateKind')) { $options.DateKind='String' }
    return ,(ConvertFrom-Json @options)
}
function WriteNew([string]$path,[byte[]]$bytes) {
    Chain $path $true
    $stream=[IO.File]::Open($path,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
    try { $stream.Write($bytes,0,$bytes.Length); $stream.Flush($true) } finally { $stream.Dispose() }
}
function FileRecord([string]$path,[string]$copy='') {
    Chain $path $true
    $source=[IO.File]::Open($path,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::Read)
    $sha=[Security.Cryptography.SHA256]::Create(); $output=$null
    try {
        $before=Get-Item -LiteralPath $path -Force; $length=$source.Length; $modified=$before.LastWriteTimeUtc.Ticks
        if ($copy) { Chain $copy $true; $output=[IO.File]::Open($copy,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None) }
        $buffer=New-Object byte[] (1024*1024); [long]$total=0
        while (($count=$source.Read($buffer,0,$buffer.Length)) -gt 0) {
            [void]$sha.TransformBlock($buffer,0,$count,$null,0); $total+=$count
            if ($null -ne $output) { $output.Write($buffer,0,$count) }
        }
        [void]$sha.TransformFinalBlock((New-Object byte[] 0),0,0)
        if ($null -ne $output) { $output.Flush($true) }
        $after=Get-Item -LiteralPath $path -Force
        if ($total -ne $length -or $after.Length -ne $length -or $after.LastWriteTimeUtc.Ticks -ne $modified) { throw 'Source changed during copy; preserve partial destination.' }
        return @{sha256=([BitConverter]::ToString($sha.Hash)).Replace('-','').ToLowerInvariant(); size_bytes=$total}
    } finally { if ($null -ne $output) { $output.Dispose() }; $sha.Dispose(); $source.Dispose() }
}
function Inventory([string]$path,[bool]$excludeLock=$false) {
    Chain $path
    if (-not [IO.Directory]::Exists($path)) { throw 'Backup files directory is missing.' }
    $dirs=New-Object 'Collections.Generic.List[string]'; $files=New-Object 'Collections.Generic.List[object]'; $seen=@{}
    $pending=New-Object 'Collections.Generic.Stack[string]'; $pending.Push($path)
    while ($pending.Count) {
        $directory=$pending.Pop(); Chain $directory
        foreach ($entry in Get-ChildItem -LiteralPath $directory -Force) {
            $relative=$entry.FullName.Substring($path.Length).TrimStart([char[]]'\/').Replace('\','/')
            if ($excludeLock -and $relative -ceq $lockName) { continue }
            [void](Relative $relative); $key=Key $relative
            if ($seen.ContainsKey($key)) { throw 'Case or Unicode-colliding backup paths.' }; $seen[$key]=$true
            if ($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Linked/reparse backup members rejected.' }
            if ($entry.PSIsContainer) { $dirs.Add($relative); $pending.Push($entry.FullName) }
            else { $record=FileRecord $entry.FullName; $record.path=$relative; $files.Add($record) }
        }
    }
    return @{directories=@($dirs.ToArray()); files=@($files.ToArray())}
}
function SameInventory($left,$right) {
    if ($left.directories.Count -ne $right.directories.Count -or $left.files.Count -ne $right.files.Count) { return $false }
    $directories=@{}; foreach ($path in $left.directories) { $directories[$path]=$path }
    foreach ($path in $right.directories) { if (-not $directories.ContainsKey($path) -or $directories[$path] -cne $path) { return $false } }
    $files=@{}; foreach ($file in $left.files) { $files[$file.path]=$file }
    foreach ($file in $right.files) {
        if (-not $files.ContainsKey($file.path)) { return $false }; $other=$files[$file.path]
        if ($other.path -cne $file.path -or $other.sha256 -cne $file.sha256 -or $other.size_bytes -ne $file.size_bytes) { return $false }
    }
    return $true
}
function Workspace([string]$path) {
    # Reuse native marker/layout validation rather than inventing another contract.
    $mapped=& (Join-Path $PSScriptRoot 'windows.ps1') -Action folders -Root $path | ConvertFrom-Json
    if ($null -eq $mapped -or $null -eq $mapped.PSObject.Properties['paths']) { throw 'Invalid workspace folder mapping.' }
}
function Manifest([string]$path) {
    $value=Json (Join-Path $path 'manifest.json')
    $expected='backup_id,created_at,directories,excluded_paths,files,schema,schema_version'
    if ($value -isnot [pscustomobject] -or (@($value.PSObject.Properties.Name | Sort-Object) -join ',') -cne $expected -or $value.schema -cne 'german-business-backup' -or ($value.schema_version -isnot [int] -and $value.schema_version -isnot [long]) -or $value.schema_version -ne 1) { throw 'Unsupported backup manifest.' }
    $id=[guid]::Empty
    if (-not [guid]::TryParse($value.backup_id,[ref]$id) -or $value.created_at -isnot [string] -or -not $value.created_at -or $value.excluded_paths -isnot [Array] -or $value.excluded_paths.Count -ne 1 -or $value.excluded_paths[0] -cne $lockName -or $value.directories -isnot [Array] -or $value.files -isnot [Array]) { throw 'Invalid backup metadata or members.' }
    $seen=@{}; $dirs=@{}; $paths=New-Object 'Collections.Generic.List[string]'
    foreach ($directory in $value.directories) { if ($directory -isnot [string]) { throw 'Invalid backup directory.' }; [void](Relative $directory); $dirs[$directory]=$true; $paths.Add($directory) }
    foreach ($file in $value.files) {
        if ($file -isnot [pscustomobject] -or (@($file.PSObject.Properties.Name | Sort-Object) -join ',') -cne 'path,sha256,size_bytes' -or $file.path -isnot [string] -or $file.sha256 -isnot [string] -or $file.sha256 -cnotmatch '^[0-9a-f]{64}$' -or ($file.size_bytes -isnot [int] -and $file.size_bytes -isnot [long]) -or $file.size_bytes -lt 0) { throw 'Invalid backup file record.' }
        [void](Relative $file.path); $paths.Add($file.path)
    }
    foreach ($member in $paths) {
        $key=Key $member
        if ($seen.ContainsKey($key) -or $member -ceq $lockName) { throw 'Duplicate, colliding or excluded backup member.' }; $seen[$key]=$true
        $parent=$member
        while ($parent.Contains('/')) {
            $parent=$parent.Substring(0,$parent.LastIndexOf('/'))
            if (-not $dirs.ContainsKey($parent)) { throw 'Unlisted backup parent directory.' }
        }
    }
    return $value
}
function VerifyBackup([string]$path,[bool]$withManifest=$false) {
    $path=Location $path
    if (-not [IO.Directory]::Exists($path) -or (@(Get-ChildItem -LiteralPath $path -Force | ForEach-Object { $_.Name } | Sort-Object) -join ',') -cne 'files,manifest.json') { throw 'Backup must contain only manifest.json and files/.' }
    $value=Manifest $path; $actual=Inventory (Join-Path $path 'files')
    if (-not (SameInventory $value $actual)) { throw 'Backup members are missing, unexpected or changed.' }
    Workspace (Join-Path $path 'files')
     $checked=@{status='verified'; backup_id=$value.backup_id; file_count=$value.files.Count; directory_count=$value.directories.Count; excluded_paths=@($lockName); scope='Complete workspace bytes and paths; excludes active lock. No encryption or accounting correctness assessment.'}
    if ($withManifest) { return @{result=$checked; manifest=$value} }
    return $checked
}
try {
    if ($Action -eq 'verify') { $result=VerifyBackup $Backup }
    elseif ($Action -eq 'backup') {
        $rootPath=Location $Root; Workspace $rootPath; $target=Fresh $Destination $rootPath
        $lock=Join-Path $rootPath $lockName; $token=$utf8.GetBytes(([guid]::NewGuid().ToString()))
        WriteNew $lock $token
        try {
            $inventory=Inventory $rootPath $true
            [void](New-Item -ItemType Directory -Path $target -ErrorAction Stop); $data=Join-Path $target 'files'; [void][IO.Directory]::CreateDirectory($data)
            foreach ($directory in @($inventory.directories | Sort-Object { $_.Split('/').Count })) { [void][IO.Directory]::CreateDirectory((Join-Path $data $directory)) }
            foreach ($file in $inventory.files) {
                $copied=FileRecord (Join-Path $rootPath $file.path) (Join-Path $data $file.path)
                if ($copied.sha256 -cne $file.sha256 -or $copied.size_bytes -ne $file.size_bytes) { throw 'Workspace changed after inventory; preserve partial backup.' }
            }
            if (-not (SameInventory $inventory (Inventory $rootPath $true))) { throw 'Workspace changed during backup; preserve partial backup.' }
            $value=@{schema='german-business-backup'; schema_version=1; backup_id=[guid]::NewGuid().ToString(); created_at=[DateTime]::UtcNow.ToString('o'); excluded_paths=@($lockName); directories=$inventory.directories; files=$inventory.files}
            WriteNew (Join-Path $target 'manifest.json') ($utf8.GetBytes((ConvertTo-Json -InputObject $value -Depth 20)+"`n"))
            $result=VerifyBackup $target
        } finally {
            if ([IO.File]::Exists($lock)) {
                Chain $lock $true
                if ([Convert]::ToBase64String([IO.File]::ReadAllBytes($lock)) -ceq [Convert]::ToBase64String($token)) { [IO.File]::Delete($lock) }
            }
        }
    } else {
        $backupPath=Location $Backup; $target=Fresh $Root $backupPath; $verified=VerifyBackup $backupPath $true; $result=$verified.result; $value=$verified.manifest
        [void](New-Item -ItemType Directory -Path $target -ErrorAction Stop)
        $lock=Join-Path $target $lockName; $token=$utf8.GetBytes(([guid]::NewGuid().ToString()))
        WriteNew $lock $token
        try {
            foreach ($directory in @($value.directories | Sort-Object { $_.Split('/').Count })) { [void][IO.Directory]::CreateDirectory((Join-Path $target $directory)) }
            foreach ($file in $value.files) {
                $copied=FileRecord (Join-Path (Join-Path $backupPath 'files') $file.path) (Join-Path $target $file.path)
                if ($copied.sha256 -cne $file.sha256 -or $copied.size_bytes -ne $file.size_bytes) { throw 'Backup changed during restore; preserve partial destination.' }
            }
            if (-not (SameInventory $value (Inventory $target $true))) { throw 'Restored workspace verification failed; preserve destination.' }
        } finally {
            if ([IO.File]::Exists($lock)) {
                Chain $lock $true
                if ([Convert]::ToBase64String([IO.File]::ReadAllBytes($lock)) -ceq [Convert]::ToBase64String($token)) { [IO.File]::Delete($lock) }
            }
        }
        Workspace $target
        $verification=& (Join-Path $PSScriptRoot 'windows.ps1') -Action verify -Root $target | ConvertFrom-Json
        $result.root=$target; $result.original_integrity=$verification.status
        $result.next_action='Inspect restored originals and workspace diagnostics before resuming; keep the backup.'
    }
    ConvertTo-Json -InputObject $result -Depth 30
    exit 0
} catch { Write-Error ('Recovery stopped: '+$_.Exception.Message); exit 2 }
