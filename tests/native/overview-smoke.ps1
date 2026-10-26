# Native synthetic overview contract; no Python/Pester/runtime installation.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2
$kit = Join-Path $PSScriptRoot '../../skills/de-business-kit/scripts/windows.ps1'
$base = Join-Path ([IO.Path]::GetTempPath()) ('gbk-overview-' + [guid]::NewGuid().ToString('N'))
[void][IO.Directory]::CreateDirectory($base)
function Assert($condition, $message) { if (-not $condition) { throw $message } }
function Reject([scriptblock]$operation) {
    $failed=$false; try { & $operation | Out-Null } catch { $failed=$true }
    Assert $failed 'Expected protected operation to stop'
}
$utf8 = New-Object Text.UTF8Encoding($false)
try {
    foreach ($language in @('en','ru','de')) {
        $root=Join-Path $base $language
        & $kit -Action start -Root $root -Year 2026 -Language $language | Out-Null
        $folders=& $kit -Action folders -Root $root | ConvertFrom-Json
        $admin=Join-Path $root $folders.paths.'00_admin'
        $empty=& $kit -Action overview -Root $root -Period '2026-10' | ConvertFrom-Json
        Assert ($empty.next_action -eq 'choose_task' -and $null -eq $empty.next_task_id) 'Empty workspace forced an accounting choice'
        $questions=Join-Path $admin 'questions.json'
        [IO.File]::WriteAllText($questions,'[{"schema_version":1,"id":"vat-question","title":"VAT <script>unsafe</script>","owner":"owner","status":"open"}]',$utf8)
        $tasks=Join-Path $admin 'tasks.json'
        [IO.File]::WriteAllText($tasks,'[{"schema_version":1,"id":"task-1","title":"Inspect actual letter","owner":"owner","status":"pending","due_date":"2099-10-27","deadline_source":"Synthetic letter page 1"}]',$utf8)
        $before=(Get-FileHash -LiteralPath $questions).Hash
        $view=& $kit -Action overview -Root $root -Period '2026-10' | ConvertFrom-Json
        Assert ($view.health -eq 'ok') 'Valid native view failed'
        $json=Get-Content -LiteralPath (Join-Path $root $view.json_path) -Raw -Encoding UTF8 | ConvertFrom-Json
        Assert ($json.questions.Count -eq 1 -and $json.tasks.Count -eq 1) 'Questions/tasks absent'
        Assert ($json.accounting.accounting_system -eq 'undecided') 'Accounting choice invented'
        Assert ($json.accounting.readiness -eq 'not_assessed') 'Native view claimed full preflight'
        Assert ($json.next_action -eq 'review_questions') 'Question did not appear as next action'
        $html=[IO.File]::ReadAllText((Join-Path $root $view.html_path),$utf8)
        Assert ($html.Contains('VAT &lt;script&gt;unsafe&lt;/script&gt;') -and -not $html.Contains('<script>')) 'Evidence markup executed'
        Assert ($html.Contains('Synthetic letter page 1') -and $html.Contains('Content-Security-Policy')) 'Deadline source/CSP missing'
        Assert ((Get-FileHash -LiteralPath $questions).Hash -eq $before) 'Overview changed canonical questions'
        [IO.File]::WriteAllText($questions,'[]',$utf8)
        [IO.File]::WriteAllText($tasks,'[{"schema_version":1,"id":"undated","title":"Prepare <script>customer</script> letter","owner":"owner","status":"pending","depends_on":[],"note":"Synthetic recipient details"},{"schema_version":1,"id":"cancelled","title":"Cancelled prerequisite","owner":"owner","status":"cancelled"},{"schema_version":1,"id":"blocked","title":"Wait for prerequisite","owner":"owner","status":"pending","depends_on":["cancelled"]}]',$utf8)
        $beforeTasks=(Get-FileHash -LiteralPath $tasks).Hash
        $taskView=& $kit -Action overview -Root $root -Period '2026-10' | ConvertFrom-Json
        $taskProjection=Get-Content -LiteralPath (Join-Path $root $taskView.json_path) -Raw -Encoding UTF8 | ConvertFrom-Json
        Assert ($taskView.next_action -eq 'continue_task' -and $taskView.next_task_id -eq 'undated') 'Undated task could not continue'
        Assert ($taskProjection.active_tasks.Count -eq 2 -and $taskProjection.tasks.Count -eq 0) 'Active tasks were filtered by dates or included terminal work'
        $blocked=@($taskProjection.active_tasks | Where-Object { $_.id -eq 'blocked' })[0]
        Assert ($blocked.readiness -eq 'blocked' -and $blocked.pending_dependencies[0] -eq 'cancelled') 'Cancelled dependency was treated as satisfied'
        $html=[IO.File]::ReadAllText((Join-Path $root $taskView.html_path),$utf8)
        Assert ($html.Contains('Prepare &lt;script&gt;customer&lt;/script&gt; letter') -and $html.Contains('Synthetic recipient details')) 'Active task text or escaping missing'
        Assert ((Get-FileHash -LiteralPath $tasks).Hash -eq $beforeTasks) 'Overview changed canonical tasks'
        & $kit -Action overview -Root $root -Period '2026-10' | Out-Null
        [IO.File]::WriteAllText((Join-Path $root '.workspace.lock'),'other writer',$utf8)
        Reject { & $kit -Action overview -Root $root -Period '2026-10' }
        Assert ([IO.File]::ReadAllText((Join-Path $root '.workspace.lock')) -eq 'other writer') 'Other lock removed'
        [IO.File]::Delete((Join-Path $root '.workspace.lock'))
        $register=Join-Path $root ($folders.paths.'04_accounting'+'/register.json')
        [IO.File]::WriteAllText($register,'{"schema_version":99}',$utf8)
        $broken=& $kit -Action overview -Root $root -Period '2026-10' | ConvertFrom-Json
        Assert ($broken.health -eq 'needs_review') 'Broken accounting hidden'
        $bad=Get-Content -LiteralPath (Join-Path $root $broken.json_path) -Raw -Encoding UTF8 | ConvertFrom-Json
        Assert ($null -eq $bad.counts.documents -and $bad.errors.Count -gt 0) 'Unreadable records became zero counts'
        [IO.File]::WriteAllText((Join-Path $root $view.html_path),'USER OWNED FILE',$utf8)
        Reject { & $kit -Action overview -Root $root -Period '2026-10' }
        Assert ([IO.File]::ReadAllText((Join-Path $root $view.html_path)) -eq 'USER OWNED FILE') 'Non-generated view overwritten'
    }
    # Static, Python-fingerprinted synthetic fixtures: serializer independence matters.
    $root=Join-Path $base 'Accounting response fixture'
    & $kit -Action start -Root $root -Year 2026 -Language en -Layout legacy | Out-Null
    $proof=Join-Path $root '08_correspondence/proof.txt'
    [IO.File]::WriteAllText($proof,'synthetic proof',$utf8)
    $register=Join-Path $root '04_accounting/register.json'
    $history=Join-Path $root '09_audit/history/accounting-smoke.json'
    $audit=Join-Path $root '09_audit/events.json'
    $originalAudit=Get-Content -LiteralPath $audit -Raw -Encoding UTF8 | ConvertFrom-Json
    foreach ($fixture in @(
        '{"schema_version": 1, "configuration": {"system": "external", "method": "E\u00dcR", "product": "O''Brien <\u0440\u0443\u0441\u0441\u043a\u0438\u0439> \ud83d\ude00", "account_reference": "business-one", "reviewer": "O''Brien", "evidence_file": "08_correspondence/proof.txt", "evidence": {"path": "08_correspondence/proof.txt", "sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826"}}, "entries": {"one": {"entry_id": "one", "date": "2026-09-10", "evidence": {"path": "08_correspondence/proof.txt", "sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826"}, "note": "2026-10-26T12:00:00.123400+00:00"}}, "filings": {}, "checksum": "1e474c4cae48c11dd4f60f470df286cd389f78e9b32b2b90ab8a9de831133518"}',
        '{"schema_version": 1, "configuration": {"system": "external", "method": "E\u00dcR", "product": "O''Brien <\u0440\u0443\u0441\u0441\u043a\u0438\u0439> \ud83d\ude00", "account_reference": "business-one", "reviewer": "O''Brien", "evidence_file": "08_correspondence/proof.txt", "evidence": {"path": "08_correspondence/proof.txt", "sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826"}}, "entries": {"one": {"entry_id": "one", "date": "2026-09-10", "evidence": {"path": "08_correspondence/proof.txt", "sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826"}, "note": "2026-10-26T12:00:00.123400+00:00"}}, "filings": {"old-return": {"filing_id": "old-return", "period": "2026-09", "form": "ustva", "state": "submitted", "responses": [{"action": "response", "actor": "owner", "note": "Synthetic observed response", "recorded_at": "2026-10-26T12:00:00.000000+00:00", "evidence": {"path": "08_correspondence/proof.txt", "sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826", "source": {"path": "08_correspondence/proof.txt", "sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826"}}, "payload_sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826", "external_id": null, "response_kind": "request_for_information", "due_date": "2000-01-01"}], "events": [{"action": "response", "actor": "owner", "note": "Synthetic observed response", "recorded_at": "2026-10-26T12:00:00.000000+00:00", "evidence": {"path": "08_correspondence/proof.txt", "sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826", "source": {"path": "08_correspondence/proof.txt", "sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826"}}, "payload_sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826", "external_id": null, "response_kind": "request_for_information", "due_date": "2000-01-01"}], "payload": {"path": "08_correspondence/proof.txt", "sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826", "source": {"path": "08_correspondence/proof.txt", "sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826"}}, "sources": [{"path": "08_correspondence/proof.txt", "sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826", "source": {"path": "08_correspondence/proof.txt", "sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826"}}], "unresolved_items": []}}, "checksum": "9e69d8b018be52fed22b51966597e2ed0c61522981bcba183caa27f2fba9ff7a"}',
        '{"schema_version": 1, "configuration": {"system": "external", "method": "E\u00dcR", "product": "O''Brien <\u0440\u0443\u0441\u0441\u043a\u0438\u0439> \ud83d\ude00", "account_reference": "business-one", "reviewer": "O''Brien", "evidence_file": "08_correspondence/proof.txt", "evidence": {"path": "08_correspondence/proof.txt", "sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826"}}, "entries": {"one": {"entry_id": "one", "date": "2026-09-10", "evidence": {"path": "08_correspondence/proof.txt", "sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826"}, "note": "2026-10-26T12:00:00.123400+00:00"}}, "filings": {"old-return": {"filing_id": "old-return", "period": "2026-10", "form": "ustva", "state": "draft", "responses": [], "events": [], "payload": {"path": "08_correspondence/proof.txt", "sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826", "source": {"path": "08_correspondence/proof.txt", "sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826"}}, "sources": [{"path": "08_correspondence/proof.txt", "sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826", "source": {"path": "08_correspondence/proof.txt", "sha256": "1e11b98fdf50fd2d1a606752ae13e0dc4538ca861fbc87c658c558bea39a8826"}}], "unresolved_items": ["Synthetic unresolved VAT question"]}}, "checksum": "9a5316a423e7e6f4d83ef46aa629abc4b637e43e17a9683c25c1ecb0522e7b7c"}'
    )) {
        [IO.File]::WriteAllText($register,$fixture,$utf8)
        $record=$fixture | ConvertFrom-Json
        [IO.File]::WriteAllText($history,('{"after_sha256":"'+$record.checksum+'"}'),$utf8)
        $events=@($originalAudit)+@(@{event_id='synthetic-audit';recorded_at='2026-10-26T12:00:00.000000+00:00';action='accounting_fixture';details=@{history_id='accounting-smoke'}})
        [IO.File]::WriteAllText($audit,(ConvertTo-Json -InputObject $events -Depth 40),$utf8)
        $view=& $kit -Action overview -Root $root -Period '2026-10' | ConvertFrom-Json
        Assert ($view.health -eq 'ok') ('Valid fixture fingerprint failed: '+($view.errors -join '; '))
        $projection=Get-Content -LiteralPath (Join-Path $root $view.json_path) -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($null -eq $record.filings.PSObject.Properties['old-return']) {
            Assert ($projection.accounting.filings.Count -eq 0 -and $projection.accounting.entry_count -eq 0) 'Empty filing set or other-period entry failed'
        } elseif ($record.filings.'old-return'.state -eq 'draft') {
            Assert ($projection.accounting.filings.Count -eq 1 -and $projection.next_action -eq 'review_filings') 'A draft with an empty response list failed'
            Assert ($projection.accounting.filings[0].issues[0] -eq 'Synthetic unresolved VAT question') 'Draft blocker was hidden'
        } else {
            Assert ($projection.accounting.filings.Count -eq 1 -and $projection.next_action -eq 'urgent') ('Prior-period authority response was hidden: '+(ConvertTo-Json -InputObject $projection -Depth 20 -Compress))
            Assert ($projection.accounting.filings[0].responses[0].due_date -eq '2000-01-01') 'Recorded response date was changed'
            $html=[IO.File]::ReadAllText((Join-Path $root $view.html_path),$utf8)
            Assert ($html.Contains('2000-01-01') -and $html.Contains('08_correspondence/proof.txt') -and $html.Contains('Request for information')) 'Response kind/date/evidence not visible'
        }
    }
    [IO.File]::WriteAllText($proof,'changed authority evidence',$utf8)
    $tampered=& $kit -Action overview -Root $root -Period '2026-10' | ConvertFrom-Json
    Assert ($tampered.health -eq 'needs_review') 'Changed filing evidence was hidden'
    'Native overview smoke passed: EN/RU/DE paths, questions, sourced tasks, escaped evidence, corruption, locks and protected output.'
} finally { Remove-Item -LiteralPath $base -Recurse -Force }
