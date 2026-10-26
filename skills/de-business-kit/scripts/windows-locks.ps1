# Shared native writer ownership. Callers supply their validated Chain function.
function OpenNativeLock([string]$path) {
    Chain $path $true
    $encoding = New-Object Text.UTF8Encoding($false, $true)
    $record = @{pid=$PID; host=[System.Net.Dns]::GetHostName(); created_at=[DateTime]::UtcNow.ToString('o'); token=[guid]::NewGuid().ToString('N')}
    $bytes = $encoding.GetBytes((ConvertTo-Json -InputObject $record -Compress) + "`n")
    $stream = [IO.File]::Open($path, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write, [IO.FileShare]::None)
    try { $stream.Write($bytes,0,$bytes.Length); $stream.Flush($true) }
    catch { $stream.Dispose(); throw } # Preserve an incomplete lock for inspection.
    return @{path=$path; stream=$stream; bytes=$bytes}
}
function CloseNativeLock($owned) {
    if ($null -eq $owned) { return }
    $owned.stream.Dispose()
    if ([IO.File]::Exists($owned.path)) {
        Chain $owned.path $true
        # Never remove a replacement lock, including after a failed operation.
        if ([Convert]::ToBase64String([IO.File]::ReadAllBytes($owned.path)) -ceq [Convert]::ToBase64String($owned.bytes)) {
            [IO.File]::Delete($owned.path)
        }
    }
}
