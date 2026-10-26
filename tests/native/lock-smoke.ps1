# Synthetic native lock recovery checks; no Python or external dependency.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2
$kit = Join-Path $PSScriptRoot '../../skills/de-business-kit/scripts/windows.ps1'
$base = Join-Path ([IO.Path]::GetTempPath()) ('gbk-lock-' + [guid]::NewGuid().ToString('N'))
function Assert($condition, $message) { if (-not $condition) { throw $message } }
function Reject([scriptblock]$operation) {
    $rejected=$false
    try { & $operation | Out-Null } catch { $rejected=$true }
    Assert $rejected 'Unsafe lock recovery unexpectedly succeeded'
}
try {
    & $kit -Action start -Root $base -Year 2026 | Out-Null
    $lockPath = Join-Path $base '.workspace.lock'
    $encoding = New-Object Text.UTF8Encoding($false)
    $raw = $encoding.GetBytes('legacy-recovery-token')
    [IO.File]::WriteAllBytes($lockPath, $raw)
    $status = & $kit -Action lock-status -Root $base | ConvertFrom-Json
    Assert ($status.lock.assessment -eq 'unverifiable') 'Legacy lock was automatically treated as stale'
    Reject { & $kit -Action unlock -Root $base -ExpectedSha256 $status.lock.sha256 }
    Reject { & $kit -Action unlock -Root $base -ExpectedSha256 ('0' * 64) -ConfirmedNoWriter }
    $recovered = & $kit -Action unlock -Root $base -ExpectedSha256 $status.lock.sha256 -ConfirmedNoWriter | ConvertFrom-Json
    Assert ($recovered.status -eq 'removed' -and -not (Test-Path -LiteralPath $lockPath)) 'Recovery failed'
    $folders = & $kit -Action folders -Root $base | ConvertFrom-Json
    $audit = Join-Path $base $folders.paths.'09_audit'
    Assert ([IO.File]::ReadAllText((Join-Path $audit ('history/' + $recovered.history_id + '.lock'))) -ceq 'legacy-recovery-token') 'Original lock bytes were lost'
    $events = Get-Content -LiteralPath (Join-Path $audit 'events.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    Assert ($events[-1].action -eq 'stale_lock_removed') 'Recovery audit event missing'
    $active = @{pid=$PID; host=[System.Net.Dns]::GetHostName(); created_at=[DateTime]::UtcNow.ToString('o')} | ConvertTo-Json -Compress
    [IO.File]::WriteAllText($lockPath, $active, $encoding)
    $status = & $kit -Action lock-status -Root $base | ConvertFrom-Json
    Assert ($status.lock.assessment -eq 'active') 'Live native process was not recognized'
    Reject { & $kit -Action unlock -Root $base -ExpectedSha256 $status.lock.sha256 -ConfirmedNoWriter }
    Assert ([IO.File]::ReadAllText($lockPath) -ceq $active) 'Active lock was modified'
    [IO.File]::Delete($lockPath)
    # Use the same helper as backup/restore; confirm exclusive handle and ownership metadata.
    function Chain([string]$path, [bool]$file=$false) { }
    . (Join-Path $PSScriptRoot '../../skills/de-business-kit/scripts/windows-locks.ps1')
    $owned = OpenNativeLock $lockPath
    try {
        $record = $encoding.GetString($owned.bytes) | ConvertFrom-Json
        Assert ($record.pid -eq $PID -and $record.host -ceq [System.Net.Dns]::GetHostName() -and $record.token.Length -eq 32) 'Writer diagnostics or unique ownership token missing'
        if ($env:OS -eq 'Windows_NT') {
            $status = & $kit -Action lock-status -Root $base | ConvertFrom-Json
            Assert ($status.lock.assessment -eq 'active' -and $null -eq $status.lock.sha256) 'Exclusive Windows lock was not diagnosed as active'
            Reject { & $kit -Action unlock -Root $base -ExpectedSha256 ('0' * 64) -ConfirmedNoWriter }
        }
    } finally { CloseNativeLock $owned }
    Assert (-not (Test-Path -LiteralPath $lockPath)) 'Owned lock was not released'
    $owned = OpenNativeLock $lockPath
    $owned.stream.Dispose()
    [IO.File]::Delete($lockPath)
    [IO.File]::WriteAllText($lockPath, 'replacement-owner', $encoding)
    CloseNativeLock $owned
    Assert ([IO.File]::ReadAllText($lockPath) -ceq 'replacement-owner') 'Replacement ownership was ignored'
    'Native lock smoke passed: diagnostics, confirmation, hash identity, evidence, audit, active refusal and ownership.'
} finally {
    if (Test-Path -LiteralPath $base) { Remove-Item -LiteralPath $base -Recurse -Force }
}
