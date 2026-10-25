# No Pester, Python, package manager or external process required.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2
$kit = Join-Path $PSScriptRoot '../../skills/de-business-kit/scripts/windows.ps1'
if (-not (Test-Path -LiteralPath $kit)) { throw 'Native Windows entry point is missing' }
$base = Join-Path ([IO.Path]::GetTempPath()) ('gbk-native-' + [guid]::NewGuid().ToString('N'))
[void][IO.Directory]::CreateDirectory($base)
function Assert($condition, $message) { if (-not $condition) { throw $message } }
function Reject([scriptblock]$operation) {
    $rejected = $false
    try { & $operation | Out-Null } catch { $rejected = $true }
    Assert $rejected 'Unsafe operation unexpectedly succeeded'
}
try {
    $root = Join-Path $base 'Private [business]'
    $source = Join-Path $base 'Mixed files'
    [void][IO.Directory]::CreateDirectory($source)
    $invoice = Join-Path $source ('invoice [1] ' + [char]0x00fc + '.csv')
    [IO.File]::WriteAllText($invoice, "amount,currency`n12.34,EUR`n", (New-Object Text.UTF8Encoding($false)))
    [IO.File]::WriteAllText((Join-Path $source 'certificate.pfx'), 'synthetic-not-a-key')
    [IO.File]::WriteAllText((Join-Path $source '.hidden.csv'), 'hidden')
    [IO.File]::WriteAllText((Join-Path $source 'export.zip'), 'not-a-zip')
    $original = (Get-FileHash -LiteralPath $invoice -Algorithm SHA256).Hash
    $start = & $kit -Action start -Root $root -Year 2026 -Language ru | ConvertFrom-Json
    Assert ($start.status -eq 'initialized') 'Start failed'
    Assert (@(Get-ChildItem -LiteralPath (Join-Path $root '06_bookkeeping')).Count -eq 0) 'Empty months should not be created before intake'
    $profile = Join-Path $root '01_profile/business.json'
    $before = (Get-FileHash -LiteralPath $profile).Hash
    $resume = & $kit -Action start -Root $root -Language en | ConvertFrom-Json
    Assert ($resume.status -eq 'resumed' -and $resume.language -eq 'ru') 'Resume changed preferences'
    Assert ((Get-FileHash -LiteralPath $profile).Hash -eq $before) 'Resume changed facts'
    $preview = & $kit -Action scan -Root $root -Source $source | ConvertFrom-Json
    Assert ($preview.candidates -eq 1 -and $preview.entries.Count -eq 4) 'Preview did not exclude secrets/hidden/unsupported files'
    $bounded = & $kit -Action scan -Root $root -Source $source -MaxEntries 1 | ConvertFrom-Json
    Assert (-not $bounded.traversal_complete -and $bounded.entries.Count -eq 1) 'Scan limit incorrectly claimed complete'
    if ($env:OS -eq 'Windows_NT') {
        $junction = Join-Path $base 'linked-source'
        New-Item -ItemType Junction -Path $junction -Value $source | Out-Null
        try { Reject { & $kit -Action scan -Root $root -Source $junction } }
        finally { [IO.Directory]::Delete($junction) }
        $hiddenFile = Join-Path $source 'native-hidden.csv'
        [IO.File]::WriteAllText($hiddenFile, 'hidden')
        [IO.File]::SetAttributes($hiddenFile, [IO.FileAttributes]::Hidden)
        $hiddenPreview = & $kit -Action scan -Root $root -Source $source | ConvertFrom-Json
        Assert ($hiddenPreview.candidates -eq 1) 'Windows hidden attribute not excluded'
    }
    $import = & $kit -Action ingest -Root $root -Source $invoice -Period '2026-10' | ConvertFrom-Json
    Assert ($import.status -eq 'imported') 'Import failed'
    $duplicate = & $kit -Action ingest -Root $root -Source $invoice -Period '2026-11' | ConvertFrom-Json
    Assert ($duplicate.status -eq 'existing_content') 'Duplicate content copied again'
    $events = Get-Content -LiteralPath (Join-Path $root '09_audit/events.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    Assert ($events.Count -eq 3 -and $events[0].action -eq 'workspace_initialized' -and $events[2].action -eq 'document_content_seen_again') 'Audit events are not flat or were lost'
    $verify = & $kit -Action verify -Root $root | ConvertFrom-Json
    Assert ($verify.status -eq 'ok' -and $verify.indexed_documents -eq 1) 'Integrity check failed'
    Assert ((Get-FileHash -LiteralPath $invoice).Hash -eq $original) 'Source changed'
    Reject { & $kit -Action start -Root $source }
    Reject { & $kit -Action scan -Root $root -Source $base }
    Reject { & $kit -Action ingest -Root $root -Source (Join-Path $source 'certificate.pfx') -Period '2026-10' }
    [IO.File]::WriteAllText((Join-Path $root '.workspace.lock'), 'other writer')
    Reject { & $kit -Action ingest -Root $root -Source $invoice -Period '2026-10' }
    Assert ([IO.File]::ReadAllText((Join-Path $root '.workspace.lock')) -eq 'other writer') 'Another writer lock removed'
    [IO.File]::Delete((Join-Path $root '.workspace.lock'))
    $index = Get-Content -LiteralPath (Join-Path $root '00_admin/documents.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    $stored = Join-Path $root $index.documents[0].path
    [IO.File]::WriteAllText($stored, 'tampered')
    $bad = & $kit -Action verify -Root $root | ConvertFrom-Json
    Assert ($bad.status -eq 'needs_review') 'Changed original was accepted'
    Reject { & $kit -Action ingest -Root $root -Source $invoice -Period '2026-10' }
    Assert ([IO.File]::ReadAllText($stored) -eq 'tampered') 'Damaged original silently replaced'
    $homeDir = Join-Path $base 'Test user'
    [void][IO.Directory]::CreateDirectory($homeDir)
    & $kit -Action install -Root $homeDir -Target both -DryRun | Out-Null
    Assert (-not (Test-Path -LiteralPath (Join-Path $homeDir '.agents'))) 'Dry-run wrote files'
    & $kit -Action install -Root $homeDir -Target both | Out-Null
    Assert (Test-Path -LiteralPath (Join-Path $homeDir '.claude/skills/de-business-kit/SKILL.md')) 'Claude install missing'
    Assert (Test-Path -LiteralPath (Join-Path $homeDir '.agents/skills/de-business-kit/scripts/windows.ps1')) 'Detached native utility missing'
    Reject { & $kit -Action install -Root $homeDir -Target both }
    $corruptRoot = Join-Path $base 'Corrupt audit'
    & $kit -Action start -Root $corruptRoot | Out-Null
    $auditPath = Join-Path $corruptRoot '09_audit/events.json'
    foreach ($malformed in @('[null]', '[],"extra":true', '[],"value":[]')) {
        [IO.File]::WriteAllText($auditPath, $malformed)
        Reject { & $kit -Action ingest -Root $corruptRoot -Source $invoice -Period '2026-10' }
        Assert ([IO.File]::ReadAllText($auditPath) -eq $malformed) 'Malformed audit was silently normalized'
    }
    $secondHome = Join-Path $base 'Preflight user'
    [void][IO.Directory]::CreateDirectory($secondHome)
    & $kit -Action install -Root $secondHome -Target claude | Out-Null
    Reject { & $kit -Action install -Root $secondHome -Target both }
    Assert (-not (Test-Path -LiteralPath (Join-Path $secondHome '.agents'))) 'Second-target conflict wrote first target'
    $detached = Join-Path $homeDir '.agents/skills/de-business-kit/scripts/windows.ps1'
    & $detached -Action start -Root (Join-Path $base 'detached') -Year 2026 | Out-Null
    'Native smoke passed: start/resume, preview, preservation, duplicates, tamper, locks, install and detached resources.'
} finally {
    # Only this test's randomly named synthetic directory is removed.
    Remove-Item -LiteralPath $base -Recurse -Force
}
