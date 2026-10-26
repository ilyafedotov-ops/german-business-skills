$ErrorActionPreference='Stop'
$repo=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
$recovery=Join-Path $repo 'skills/de-business-kit/scripts/recovery.ps1'
$windows=Join-Path $repo 'skills/de-business-kit/scripts/windows.ps1'
$base=Join-Path ([IO.Path]::GetTempPath()) ('gbk-recovery-'+[guid]::NewGuid().ToString('N'))
[void][IO.Directory]::CreateDirectory($base)
function Check($condition,$message) { if (-not $condition) { throw $message } }
function Reject([scriptblock]$operation,[string]$message) {
    $failed=$false
    try { & $operation 2>$null | Out-Null; $failed=($LASTEXITCODE -ne 0) } catch { $failed=$true }
    Check $failed $message
}
try {
    $workspace=Join-Path $base 'workspace'; $backup=Join-Path $base 'backup'; $restored=Join-Path $base 'restored'
    $started=& $windows -Action start -Root $workspace -Year 2026 -Language ru | ConvertFrom-Json
    Check ($started.status -eq 'initialized') 'Native workspace setup failed.'
    [IO.File]::WriteAllText((Join-Path $workspace 'synthetic-note.txt'),'Synthetic note')
    [void][IO.Directory]::CreateDirectory((Join-Path $workspace 'empty'))
    $created=& $recovery -Action backup -Root $workspace -Destination $backup | ConvertFrom-Json
    Check ($LASTEXITCODE -eq 0 -and $created.status -eq 'verified') 'Native backup failed.'
    Reject { & $recovery -Action backup -Root $workspace -Destination $backup } 'Existing backup was overwritten.'
    Reject { & $recovery -Action backup -Root $workspace -Destination (Join-Path $workspace 'nested') } 'Nested backup accepted.'
    [IO.File]::WriteAllText((Join-Path $workspace '.workspace.lock'),'Synthetic active lock')
    try { Reject { & $recovery -Action backup -Root $workspace -Destination (Join-Path $base 'locked-backup') } 'Active workspace lock ignored.' }
    finally { [IO.File]::Delete((Join-Path $workspace '.workspace.lock')) }
    Check (-not (Test-Path -LiteralPath (Join-Path $base 'locked-backup'))) 'Locked operation created a backup.'
    $checked=& $recovery -Action verify -Backup $backup | ConvertFrom-Json
    Check ($LASTEXITCODE -eq 0 -and $checked.status -eq 'verified') 'Native backup verification failed.'
    $result=& $recovery -Action restore -Backup $backup -Root $restored | ConvertFrom-Json
    Check ($LASTEXITCODE -eq 0 -and $result.original_integrity -eq 'ok') 'Native restore failed.'
    Reject { & $recovery -Action restore -Backup $backup -Root $restored } 'Existing restored workspace was overwritten.'
    Check ([IO.File]::ReadAllText((Join-Path $restored 'synthetic-note.txt')) -ceq 'Synthetic note') 'Restored note changed.'
    Check ([IO.Directory]::Exists((Join-Path $restored 'empty'))) 'Empty directory lost.'
    Check (-not (Test-Path -LiteralPath (Join-Path $restored '.workspace.lock'))) 'Active lock was restored.'
    [IO.File]::WriteAllText((Join-Path $backup 'files/synthetic-note.txt'),'Changed')
    $failure=$false
    try { & $recovery -Action restore -Backup $backup -Root (Join-Path $base 'must-not-exist') 2>$null | Out-Null; $failure=($LASTEXITCODE -ne 0) } catch { $failure=$true }
    Check $failure 'Corrupt backup unexpectedly restored.'
    Check (-not (Test-Path -LiteralPath (Join-Path $base 'must-not-exist'))) 'Corrupt backup created restoration destination.'
    'Native recovery roundtrip and corruption rejection: PASS'
} finally { if ([IO.Directory]::Exists($base)) { [IO.Directory]::Delete($base,$true) } }
