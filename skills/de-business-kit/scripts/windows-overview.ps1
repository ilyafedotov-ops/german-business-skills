# Dot-sourced only by windows.ps1 while its workspace lock is held.
# Saved states and local hashes are inspected; native full filing preflight is unavailable.
function ViewProperty($value,[string]$name,$default=$null) {
    if ($null -eq $value) { return ,$default }
    if ($value -is [Collections.IDictionary]) { if ($value.Contains($name)) { return ,$value[$name] }; return ,$default }
    $property=$value.PSObject.Properties[$name]
    if ($null -eq $property) { return ,$default }
    return ,$property.Value
}
function ViewObjects($value) {
    if ($value -isnot [pscustomobject]) { throw 'Expected a record collection.' }
    return @($value.PSObject.Properties | ForEach-Object { $_.Value })
}
function ViewString([string]$value) {
    # JSON's string escapes are fixed here rather than host-version serializer defaults.
    $text=New-Object Text.StringBuilder
    [void]$text.Append('"')
    foreach ($character in $value.ToCharArray()) {
        $number=[int]$character
        if ($number -eq 34) { [void]$text.Append('\"') }
        elseif ($number -eq 92) { [void]$text.Append('\\') }
        elseif ($number -eq 8) { [void]$text.Append('\b') }
        elseif ($number -eq 9) { [void]$text.Append('\t') }
        elseif ($number -eq 10) { [void]$text.Append('\n') }
        elseif ($number -eq 12) { [void]$text.Append('\f') }
        elseif ($number -eq 13) { [void]$text.Append('\r') }
        elseif ($number -lt 32) { [void]$text.Append('\u'+$number.ToString('x4')) }
        else { [void]$text.Append($character) }
    }
    [void]$text.Append('"')
    return $text.ToString()
}
function ViewJson($value,[int]$depth=0) {
    # Match the existing Python register fingerprint: sorted, indent=2, UTF-8.
    $padding=' ' * (2*$depth); $child=' ' * (2*($depth+1))
    if ($null -eq $value) { return 'null' }
    if ($value -is [pscustomobject]) {
        $names=[string[]]@($value.PSObject.Properties | ForEach-Object { $_.Name })
        [Array]::Sort($names,[StringComparer]::Ordinal)
        if ($names.Count -eq 0) { return '{}' }
        $parts=@(foreach ($name in $names) { $child+(ViewString $name)+': '+(ViewJson $value.PSObject.Properties[$name].Value ($depth+1)) })
        return "{`n"+($parts -join ",`n")+"`n"+$padding+'}'
    }
    if ($value -is [Array]) {
        if ($value.Count -eq 0) { return '[]' }
        $parts=@(foreach ($item in $value) { $child+(ViewJson $item ($depth+1)) })
        return "[`n"+($parts -join ",`n")+"`n"+$padding+']'
    }
    if ($value -is [string]) { return (ViewString $value) }
    if ($value -is [bool]) { if ($value) { return 'true' }; return 'false' }
    if ($value -is [int] -or $value -is [long]) { return $value.ToString([Globalization.CultureInfo]::InvariantCulture) }
    throw 'Unsupported value in accounting fingerprint; preserve the register.'
}
function ViewEvidence($record) {
    $relative=ViewProperty $record 'path'; $digest=ViewProperty $record 'sha256'
    if ($relative -isnot [string] -or $relative -match '(^|/)[.]{1,2}(/|$)|[\\:]' -or $digest -cnotmatch '^[0-9a-f]{64}$') { throw 'Invalid saved evidence fingerprint.' }
    $path=Absolute (WorkspacePath $relative)
    if ((Hash (ReadBytes $path)) -cne $digest) { throw ('Evidence changed: '+$relative) }
}
function ViewRegister([string]$name,[string[]]$states) {
    $records=ReadJson (WorkspacePath ('00_admin/'+$name+'.json'))
    if ($records -isnot [Array]) { throw ('Invalid '+$name+' register.') }
    $seen=@{}
    foreach ($record in $records) {
        $id=ViewProperty $record 'id'; $status=ViewProperty $record 'status'
        if ($record -isnot [pscustomobject] -or (ViewProperty $record 'schema_version') -ne 1 -or $id -cnotmatch '^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$' -or $seen.ContainsKey($id) -or $status -cnotin $states -or [string]::IsNullOrWhiteSpace((ViewProperty $record 'title')) -or [string]::IsNullOrWhiteSpace((ViewProperty $record 'owner'))) { throw ('Invalid '+$name+' entry.') }
        $seen[$id]=$true
        $due=ViewProperty $record 'due_date'
        if ($null -ne $due) {
            $parsed=[DateTime]::MinValue
            if (-not [DateTime]::TryParseExact($due,'yyyy-MM-dd',[Globalization.CultureInfo]::InvariantCulture,[Globalization.DateTimeStyles]::None,[ref]$parsed) -or [string]::IsNullOrWhiteSpace((ViewProperty $record 'deadline_source'))) { throw 'Recorded dates require a valid date and source.' }
        }
        $evidence=ViewProperty $record 'evidence_file'
        if ($null -ne $evidence) { ViewEvidence ([pscustomobject]@{path=$evidence;sha256=(ViewProperty $record 'evidence_sha256')}) }
    }
    return ,$records
}
function ViewInPeriod([string]$recordPeriod,[string]$month) {
    if ($recordPeriod -cnotmatch '^[1-9][0-9]{3}(-(0[1-9]|1[0-2]|Q[1-4]))?$') { throw 'Invalid saved accounting period.' }
    if ($recordPeriod.Length -eq 4) { return $month.StartsWith($recordPeriod+'-') }
    if ($recordPeriod.Contains('-Q')) { return ($recordPeriod.Substring(0,4) -ceq $month.Substring(0,4) -and [int]$recordPeriod.Substring(6,1) -eq [int][Math]::Ceiling([int]$month.Substring(5,2)/3.0)) }
    return $recordPeriod -ceq $month
}
function ViewTaskEvidencePath($record) {
    $relative=ViewProperty $record 'evidence_file'
    $digest=ViewProperty $record 'evidence_sha256'
    if ($null -eq $relative) {
        if ($null -ne $digest -or $record.status -ceq 'completed') { throw 'Task state requires a preserved evidence file and hash.' }
        return $null
    }
    if ($relative -isnot [string] -or [string]::IsNullOrWhiteSpace($relative) -or $relative -match '(^|/)[.]{1,2}(/|$)|[\\:]|^/' -or $digest -isnot [string] -or $digest -cnotmatch '^[0-9a-f]{64}$') { throw 'Invalid task evidence path or hash.' }
    $path=Absolute (WorkspacePath $relative)
    Chain $path $true
    if (Test-Path -LiteralPath $path) {
        $item=Get-Item -LiteralPath $path -Force
        $link=$item.PSObject.Properties['LinkType']
        if ($null -eq $link -or -not [string]::IsNullOrEmpty([string]$link.Value)) { throw 'Use an independent preserved evidence file, not a linked file.' }
    }
    # Mutable registers cannot establish that a task's result was preserved.
    foreach ($mutable in @('01_profile/business.json','00_admin/documents.json','09_audit/events.json','00_admin/workspace.json','00_admin/runtime.json','.workspace.lock','.workspace-layout.json','00_admin/tasks.json','00_admin/questions.json','00_admin/decisions.json','00_admin/casework.json','00_admin/invoicing.json','04_accounting/register.json')) {
        if ($path.Equals((WorkspacePath $mutable),[StringComparison]::OrdinalIgnoreCase)) { throw 'Use preserved task evidence, not a mutable register.' }
    }
    return $path
}
function ViewActiveTasks {
    $records=ReadJson (WorkspacePath '00_admin/tasks.json')
    if ($records -isnot [Array]) { throw 'Invalid tasks register.' }
    $byId=New-Object 'Collections.Generic.Dictionary[string,object]' ([StringComparer]::Ordinal)
    $evidence=New-Object 'Collections.Generic.Dictionary[string,string]' ([StringComparer]::Ordinal)
    $allowed=@('schema_version','id','title','owner','status','depends_on','due_date','deadline_source','evidence_file','evidence_sha256','reviewer','supersedes','superseded_by','note')
    foreach ($record in $records) {
        $id=ViewProperty $record 'id'; $status=ViewProperty $record 'status'
        $schema=ViewProperty $record 'schema_version'
        if ($record -isnot [pscustomobject] -or @($record.PSObject.Properties.Name | Where-Object { $_ -cnotin $allowed }).Count -or ($schema -isnot [int] -and $schema -isnot [long]) -or $schema -ne 1 -or $id -isnot [string] -or $id -cnotmatch '^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$' -or $byId.ContainsKey($id) -or $status -isnot [string] -or $status -cnotin @('pending','in_progress','blocked','completed','cancelled')) { throw 'Invalid task entry.' }
        foreach ($name in @('title','owner')) { $value=ViewProperty $record $name; if ($value -isnot [string] -or [string]::IsNullOrWhiteSpace($value)) { throw 'Task title and owner must be text.' } }
        foreach ($name in @('deadline_source','reviewer','supersedes','superseded_by','note')) { $value=ViewProperty $record $name; if ($null -ne $value -and ($value -isnot [string] -or [string]::IsNullOrWhiteSpace($value))) { throw 'Invalid task metadata.' } }
        $due=ViewProperty $record 'due_date'
        if ($null -ne $due) {
            $parsed=[DateTime]::MinValue
            if ($due -isnot [string] -or -not [DateTime]::TryParseExact($due,'yyyy-MM-dd',[Globalization.CultureInfo]::InvariantCulture,[Globalization.DateTimeStyles]::None,[ref]$parsed) -or [string]::IsNullOrWhiteSpace((ViewProperty $record 'deadline_source'))) { throw 'Recorded dates require a valid date and source.' }
        }
        $dependencies=ViewProperty $record 'depends_on' @()
        if ($dependencies -isnot [Array]) { throw 'Task dependencies must be an array.' }
        $seen=New-Object 'Collections.Generic.HashSet[string]' ([StringComparer]::Ordinal)
        foreach ($dependency in $dependencies) { if ($dependency -isnot [string] -or [string]::IsNullOrWhiteSpace($dependency) -or $dependency -ceq $id -or -not $seen.Add($dependency)) { throw 'Invalid task dependency.' } }
        $path=ViewTaskEvidencePath $record
        $evidence[$id]='not_recorded'
        if ($null -ne $path) {
            try {
                $bytes=ReadBytes $path
                # Canonical evidence is arbitrary bytes, including PDF and images.
                $hasContent=$false
                foreach ($byte in $bytes) { if ($byte -notin @(9,10,11,12,13,32)) { $hasContent=$true; break } }
                if (-not $hasContent -or (Hash $bytes) -cne $record.evidence_sha256) { throw 'Task evidence needs review.' }
                $evidence[$id]='checked'
            } catch { $evidence[$id]='needs_review' }
        }
        $byId.Add($id,$record)
    }
    foreach ($record in $records) {
        $links=ViewProperty $record 'depends_on' @()
        $links=$links+@((ViewProperty $record 'supersedes'),(ViewProperty $record 'superseded_by'))
        foreach ($link in $links) { if ($null -ne $link -and (-not $byId.ContainsKey($link) -or $link -ceq $record.id)) { throw 'Task link must refer to a distinct existing entry.' } }
    }
    # Topological checks cover even hidden terminal tasks and avoid recursive stack limits.
    foreach ($relationship in @('depends_on','supersedes')) {
        $remaining=New-Object 'Collections.Generic.HashSet[string]' ([StringComparer]::Ordinal)
        foreach ($id in $byId.Keys) { [void]$remaining.Add($id) }
        while ($remaining.Count) {
            $ready=@(foreach ($id in $remaining) { $links=ViewProperty $byId[$id] $relationship @(); if (@($links | Where-Object { $null -ne $_ -and $remaining.Contains($_) }).Count -eq 0) { $id } })
            if (-not $ready.Count) { throw 'Task dependencies and supersession links cannot form cycles.' }
            foreach ($id in $ready) { [void]$remaining.Remove($id) }
        }
    }
    $active=@(foreach ($record in $records) {
        if ($record.status -cin @('completed','cancelled')) { continue }
        $pending=New-Object 'Collections.Generic.HashSet[string]' ([StringComparer]::Ordinal)
        $visited=New-Object 'Collections.Generic.HashSet[string]' ([StringComparer]::Ordinal)
        $queue=New-Object 'Collections.Generic.Queue[string]'
        $dependencies=ViewProperty $record 'depends_on' @()
        foreach ($id in $dependencies) { $queue.Enqueue($id) }
        $needsReview=$evidence[$record.id] -ceq 'needs_review'
        while ($queue.Count) {
            $id=$queue.Dequeue(); if (-not $visited.Add($id)) { continue }
            if ($byId[$id].status -cne 'completed' -or $evidence[$id] -cne 'checked') { [void]$pending.Add($id) }
            if ($evidence[$id] -ceq 'needs_review') { $needsReview=$true }
            $ancestors=ViewProperty $byId[$id] 'depends_on' @()
            foreach ($ancestor in $ancestors) { $queue.Enqueue($ancestor) }
        }
        $readiness='ready'
        if ($needsReview) { $readiness='needs_review' } elseif ($record.status -cnotin @('pending','in_progress') -or $pending.Count) { $readiness='blocked' }
        $pendingIds=[string[]]@($pending); [Array]::Sort($pendingIds,[StringComparer]::Ordinal)
        @{id=$record.id;title=$record.title;owner=$record.owner;status=$record.status;due_date=(ViewProperty $record 'due_date');deadline_source=(ViewProperty $record 'deadline_source');note=(ViewProperty $record 'note');evidence_status=$evidence[$record.id];pending_dependencies=$pendingIds;readiness=$readiness}
    })
    $compare=[Collections.Generic.Comparer[object]]::Create([Comparison[object]]{
        param($left,$right)
        $leftDate=$left.due_date; if ($null -eq $leftDate) { $leftDate='9999-12-31' }
        $rightDate=$right.due_date; if ($null -eq $rightDate) { $rightDate='9999-12-31' }
        $order=[StringComparer]::Ordinal.Compare($leftDate,$rightDate)
        if ($order) { return $order }
        $leftState=1; if ($left.status -ceq 'in_progress') { $leftState=0 }
        $rightState=1; if ($right.status -ceq 'in_progress') { $rightState=0 }
        if ($leftState -ne $rightState) { return $leftState-$rightState }
        return [StringComparer]::Ordinal.Compare($left.id,$right.id)
    })
    [Array]::Sort($active,$compare)
    return ,$active
}
function ViewAccounting($events) {
    $path=WorkspacePath '04_accounting/register.json'
    $history=@($events | Where-Object { $details=ViewProperty $_ 'details'; (ViewProperty $details 'history_id' '') -like 'accounting-*' })
    if (-not (Test-Path -LiteralPath $path)) {
        if ($history.Count) { throw 'Accounting register is missing but history exists.' }
        return @{accounting_system='undecided';method='unresolved';product=$null;entry_count=0;filings=@();readiness='not_assessed';evidence_status='no_accounting_records';preflight='not_implemented'}
    }
    $state=ReadJson $path
    $fields=@($state.PSObject.Properties.Name | Sort-Object)
    if (($fields -join ',') -cne 'checksum,configuration,entries,filings,schema_version' -or $state.schema_version -ne 1) { throw 'Unsupported accounting register.' }
    $checksum=$state.checksum
    $unsigned=ReadJson $path
    $unsigned.PSObject.Properties.Remove('checksum')
    if ($checksum -cnotmatch '^[0-9a-f]{64}$' -or (Hash $utf8.GetBytes((ViewJson $unsigned)+"`n")) -cne $checksum -or $history.Count -eq 0) { throw 'Accounting checksum/history mismatch.' }
    $historyId=(ViewProperty $history[-1].details 'history_id')
    if ($historyId -cnotmatch '^accounting-[a-zA-Z0-9_.:-]{1,160}$') { throw 'Invalid accounting history reference.' }
    $checkpoint=ReadJson (WorkspacePath ('09_audit/history/'+$historyId+'.json'))
    if ((ViewProperty $checkpoint 'after_sha256') -cne $checksum) { throw 'Accounting history checkpoint disagrees.' }
    $config=$state.configuration
    if ($null -eq $config -or (ViewProperty $config 'system') -cnotin @('local','external') -or (ViewProperty $config 'method') -cnotin @(('E' + [char]0x00dc + 'R'),'Bilanzierung','unresolved')) { throw 'Invalid saved accounting choice.' }
    ViewEvidence $config.evidence
    $entries=@(ViewObjects $state.entries)
    $periodEntries=@()
    foreach ($entry in $entries) {
        if ((ViewProperty $entry 'date') -cnotmatch '^[1-9][0-9]{3}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$') { throw 'Invalid cash entry date.' }
        if ($entry.date.StartsWith($Period)) { ViewEvidence $entry.evidence; $periodEntries+=@($entry) }
    }
    $filings=@()
    foreach ($filing in @(ViewObjects $state.filings)) {
        if ((ViewProperty $filing 'state') -cnotin @('draft','reviewed','authorized','submission_unconfirmed','submitted','cancelled')) { throw 'Invalid saved filing state.' }
        $responses=ViewProperty $filing 'responses' @()
        if ($responses -isnot [Array]) { throw 'Invalid authority response collection.' }
        $datedResponses=@($responses | Where-Object { $null -ne (ViewProperty $_ 'due_date') })
        if (-not (ViewInPeriod $filing.period $Period) -and $filing.state -cne 'submission_unconfirmed' -and $datedResponses.Count -eq 0) { continue }
        foreach ($response in $responses) {
            if ((ViewProperty $response 'response_kind') -cnotin @('acknowledgement','request_for_information','assessment','rejection','other')) { throw 'Invalid observed authority response kind.' }
            ViewEvidence $response.evidence
            if ($null -ne (ViewProperty $response 'due_date')) {
                $parsed=[DateTime]::MinValue
                if (-not [DateTime]::TryParseExact($response.due_date,'yyyy-MM-dd',[Globalization.CultureInfo]::InvariantCulture,[Globalization.DateTimeStyles]::None,[ref]$parsed)) { throw 'Invalid recorded authority response date.' }
            }
        }
        $issues=New-Object 'Collections.Generic.List[string]'
        if ($filing.state -ceq 'submission_unconfirmed') { $issues.Add('Submission outcome is unconfirmed; investigate the existing attempt before retrying.') }
        if ($filing.state -cin @('draft','reviewed','authorized')) {
            $unresolved=ViewProperty $filing 'unresolved_items' @()
            foreach ($item in $unresolved) { $issues.Add([string]$item) }
        }
        $sources=@($filing.payload)+@($filing.sources)
        foreach ($source in $sources) { ViewEvidence $source; if ($filing.state -cin @('draft','reviewed','authorized')) { ViewEvidence $source.source } }
        foreach ($event in @($filing.events)) { ViewEvidence $event.evidence }
        $filings+=@(@{filing_id=$filing.filing_id;form=$filing.form;period=$filing.period;state=$filing.state;responses=$responses;issues=@($issues.ToArray());evidence_status='checked_local_hashes';preflight='not_implemented'})
    }
    return @{accounting_system=$config.system;method=$config.method;product=$config.product;entry_count=$periodEntries.Count;filings=$filings;readiness='not_assessed';evidence_status='checked_local_hashes';preflight='not_implemented'}
}
function ViewSave([string]$relative,[byte[]]$bytes) {
    $path=WorkspacePath $relative
    if (Test-Path -LiteralPath $path) {
        Chain $path $true
        $temp=$path+'.'+[guid]::NewGuid().ToString('N')+'.tmp'
        WriteNew $temp $bytes
        try { [IO.File]::Replace($temp,$path,[NullString]::Value) } finally { if ([IO.File]::Exists($temp)) { [IO.File]::Delete($temp) } }
    } else { WriteNew $path $bytes }
}
function NativeOverview {
    if ($Period -cnotmatch '^[1-9][0-9]{3}-(0[1-9]|1[0-2])$' -or [int]$Period.Substring(0,4) -lt 1900) { throw 'Overview period must be YYYY-MM, 1900-9999.' }
    $language=$marker.language; if ($language -ceq 'de') { $language='en' }
    $words=@{title='Business workspace';boundary='Saved records and local evidence only. Full filing preflight and tax correctness are not assessed by this native view. Ask the assistant to refresh after changes.';documents='Documents';questions='Open questions';tasks='Tasks with recorded dates';accounting='Accounting and filings';system='Chosen accounting system';entries='Cash records in selected month';filings='Saved filing versions';repair='Inspect the workspace issue before changing records.';review_questions='Resolve the open question with the assistant.';resolve_submission='Investigate the unconfirmed submission outcome before retrying.';review_filings='Review the saved filing and its unresolved items.';choose_accounting='Choose local cash accounting or your existing accounting software.';review_documents='Review documents and reconcile the month in the selected accounting system.';unknown='Not assessed';snapshot='Snapshot date';source='Recorded date / source';empty='No supplied records in this section.';errors='Workspace issues';next='Next useful action';undecided='Not chosen';local='Local cash journal';external='Existing software';draft='Draft';reviewed='Reviewed';authorized='Authorized';submission_unconfirmed='Submission outcome unconfirmed';submitted='Submission evidenced';cancelled='Cancelled';evidence='Evidence status';readiness='Full filing readiness';not_assessed='Not assessed';checked_local_hashes='Local file hashes checked';no_accounting_records='No accounting records';method='Method';product='Product'}
    if ($language -ceq 'ru') {
        # Unicode escapes keep this source compatible with Windows PowerShell 5.1 without BOM.
        $ru=ReadJson (Join-Path $kitRoot 'assets/casework-messages.json')
        $words.title=$ru.ru.title; $words.documents=$ru.ru.documents; $words.questions=''; $words.questions=[Text.RegularExpressions.Regex]::Unescape('\u041e\u0442\u043a\u0440\u044b\u0442\u044b\u0435 \u0432\u043e\u043f\u0440\u043e\u0441\u044b')
        $translations=@{
            boundary='\u0421\u043e\u0445\u0440\u0430\u043d\u0451\u043d\u043d\u044b\u0435 \u0437\u0430\u043f\u0438\u0441\u0438 \u0438 \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u044b\u0435 \u0444\u0430\u0439\u043b\u044b. \u041f\u043e\u043b\u043d\u0430\u044f \u043f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u043f\u043e\u0434\u0430\u0447\u0438 \u0438 \u043d\u0430\u043b\u043e\u0433\u043e\u0432\u0430\u044f \u043a\u043e\u0440\u0440\u0435\u043a\u0442\u043d\u043e\u0441\u0442\u044c \u043d\u0435 \u043e\u0446\u0435\u043d\u0435\u043d\u044b. \u041f\u043e\u043f\u0440\u043e\u0441\u0438\u0442\u0435 \u0430\u0441\u0441\u0438\u0441\u0442\u0435\u043d\u0442\u0430 \u043e\u0431\u043d\u043e\u0432\u0438\u0442\u044c \u043e\u0431\u0437\u043e\u0440 \u043f\u043e\u0441\u043b\u0435 \u0438\u0437\u043c\u0435\u043d\u0435\u043d\u0438\u0439.'
            accounting='\u0423\u0447\u0451\u0442 \u0438 \u043f\u043e\u0434\u0430\u0447\u0438'; system='\u0412\u044b\u0431\u0440\u0430\u043d\u043d\u0430\u044f \u0441\u0438\u0441\u0442\u0435\u043c\u0430'; entries='\u0414\u0435\u043d\u0435\u0436\u043d\u044b\u0435 \u0437\u0430\u043f\u0438\u0441\u0438 \u0437\u0430 \u043c\u0435\u0441\u044f\u0446'; filings='\u0421\u043e\u0445\u0440\u0430\u043d\u0451\u043d\u043d\u044b\u0435 \u0432\u0435\u0440\u0441\u0438\u0438 \u043f\u043e\u0434\u0430\u0447'; resolve_submission='\u0423\u0442\u043e\u0447\u043d\u0438\u0442\u0435 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u043f\u0440\u0435\u0434\u044b\u0434\u0443\u0449\u0435\u0439 \u043f\u043e\u043f\u044b\u0442\u043a\u0438 \u0434\u043e \u043f\u043e\u0432\u0442\u043e\u0440\u0430.'; review_filings='\u041f\u0440\u043e\u0432\u0435\u0440\u044c\u0442\u0435 \u0432\u0435\u0440\u0441\u0438\u044e \u043f\u043e\u0434\u0430\u0447\u0438 \u0438 \u0435\u0451 \u043e\u0442\u043a\u0440\u044b\u0442\u044b\u0435 \u0432\u043e\u043f\u0440\u043e\u0441\u044b.'; review_questions='\u0420\u0430\u0437\u0431\u0435\u0440\u0438\u0442\u0435 \u043e\u0442\u043a\u0440\u044b\u0442\u044b\u0439 \u0432\u043e\u043f\u0440\u043e\u0441 \u0441 \u0430\u0441\u0441\u0438\u0441\u0442\u0435\u043d\u0442\u043e\u043c.'; choose_accounting='\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043b\u043e\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u0434\u0435\u043d\u0435\u0436\u043d\u044b\u0439 \u0436\u0443\u0440\u043d\u0430\u043b \u0438\u043b\u0438 \u0443\u0447\u0451\u0442\u043d\u0443\u044e \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0443.'; evidence='\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 \u0444\u0430\u0439\u043b\u043e\u0432'; readiness='\u041f\u043e\u043b\u043d\u0430\u044f \u0433\u043e\u0442\u043e\u0432\u043d\u043e\u0441\u0442\u044c \u043f\u043e\u0434\u0430\u0447\u0438'; checked_local_hashes='\u041b\u043e\u043a\u0430\u043b\u044c\u043d\u044b\u0435 \u0445\u0435\u0448\u0438 \u043f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u044b'; no_accounting_records='\u0417\u0430\u043f\u0438\u0441\u0435\u0439 \u0443\u0447\u0451\u0442\u0430 \u043d\u0435\u0442'; method='\u041c\u0435\u0442\u043e\u0434'; product='\u041f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430'; undecided='\u041d\u0435 \u0432\u044b\u0431\u0440\u0430\u043d\u0430'; local='\u041b\u043e\u043a\u0430\u043b\u044c\u043d\u044b\u0439 \u0434\u0435\u043d\u0435\u0436\u043d\u044b\u0439 \u0436\u0443\u0440\u043d\u0430\u043b'; external='\u0423\u0447\u0451\u0442\u043d\u0430\u044f \u043f\u0440\u043e\u0433\u0440\u0430\u043c\u043c\u0430'; draft='\u0427\u0435\u0440\u043d\u043e\u0432\u0438\u043a'; reviewed='\u041f\u0440\u043e\u0432\u0435\u0440\u0435\u043d\u043e'; authorized='\u041e\u0434\u043e\u0431\u0440\u0435\u043d\u043e'; submission_unconfirmed='\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u043e\u0442\u043f\u0440\u0430\u0432\u043a\u0438 \u043d\u0435 \u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0451\u043d'; submitted='\u041e\u0442\u043f\u0440\u0430\u0432\u043a\u0430 \u0437\u0430\u0444\u0438\u043a\u0441\u0438\u0440\u043e\u0432\u0430\u043d\u0430'; cancelled='\u041e\u0442\u043c\u0435\u043d\u0435\u043d\u043e'
        }
        foreach ($key in $translations.Keys) { $words[$key]=[Text.RegularExpressions.Regex]::Unescape($translations[$key]) }
        foreach ($key in @('tasks','source','snapshot','empty','errors','next','repair','unknown','not_assessed','review_documents')) {
            $map=@{tasks='tasks';source='task_date';snapshot='as_of';empty='empty_section';errors='error';next='next';repair='repair';unknown='not_assessed';not_assessed='not_assessed';review_documents='next_accounting'}
            $words[$key]=$ru.ru.PSObject.Properties[$map[$key]].Value
        }
    }
    $messages=ReadJson (Join-Path $kitRoot 'assets/casework-messages.json')
    $words.urgent=$messages.PSObject.Properties[$language].Value.urgent
    $words.authority_response=$messages.PSObject.Properties[$language].Value.authority_response
    $words.response_kinds=$messages.PSObject.Properties[$language].Value.response_kinds
    foreach ($key in @('choose_task','continue_task','review_tasks','active_tasks','tasks_scope','no_active_tasks','task_no_date','task_ready','task_blocked','task_needs_review','task_owner','task_dependencies','task_states')) {
        $words[$key]=$messages.PSObject.Properties[$language].Value.PSObject.Properties[$key].Value
    }
    $errors=New-Object 'Collections.Generic.List[string]'
    $docs=@(); $allDocumentCount=0; $questions=@(); $tasks=@(); $activeTasks=@(); $accounting=$null; $nextTaskId=$null
    try {
        $integrity=Verify
        if ($integrity.status -ne 'ok') { throw 'Original integrity needs review; inspect verify output.' }
        $events=ReadJson (WorkspacePath '09_audit/events.json')
        if ($events -isnot [Array] -or @($events | Where-Object { $_ -isnot [pscustomobject] }).Count) { throw 'Invalid audit log.' }
        $allDocuments=(Index).documents
        $allDocumentCount=$allDocuments.Count
        $docs=@($allDocuments | Where-Object { $_.period -ceq $Period })
        $questions=@((ViewRegister 'questions' @('open','deferred','resolved')) | Where-Object { $_.status -cin @('open','deferred') })
        $activeTasks=ViewActiveTasks
        $taskRecords=ReadJson (WorkspacePath '00_admin/tasks.json')
        $tasks=@($taskRecords | Where-Object { $_.status -cnotin @('completed','cancelled') -and $null -ne (ViewProperty $_ 'due_date') } | Sort-Object due_date,id)
        $accounting=ViewAccounting $events
    } catch { $errors.Add($_.Exception.Message); $activeTasks=@(); $tasks=@() }
    if (-not $errors.Count) { $readyTasks=@($activeTasks | Where-Object { $_.readiness -ceq 'ready' }); if ($readyTasks.Count) { $nextTaskId=$readyTasks[0].id } }
    $soon=(Get-Date).Date.AddDays(7).ToString('yyyy-MM-dd')
    $urgentTasks=@($tasks | Where-Object { $_.due_date -cle $soon })
    $urgentResponses=@()
    if ($null -ne $accounting) { $urgentResponses=@($accounting.filings | ForEach-Object { $_.responses } | Where-Object { $null -ne (ViewProperty $_ 'due_date') -and $_.due_date -cle $soon }) }
    $next='review_documents'
    if ($errors.Count) { $next='repair' }
    elseif (@($accounting.filings | Where-Object { $_.state -ceq 'submission_unconfirmed' }).Count) { $next='resolve_submission' }
    elseif ($urgentTasks.Count -gt 0 -or $urgentResponses.Count -gt 0) { $next='urgent' }
    elseif (@($accounting.filings | Where-Object { $_.issues.Count -gt 0 -or $_.state -cin @('draft','reviewed','authorized') }).Count) { $next='review_filings' }
    elseif ($questions.Count) { $next='review_questions' }
    elseif ($activeTasks.Count) { if ($null -ne $nextTaskId) { $next='continue_task' } else { $next='review_tasks' } }
    elseif ($accounting.accounting_system -ceq 'undecided' -and $allDocumentCount -eq 0 -and $accounting.entry_count -eq 0 -and $accounting.filings.Count -eq 0) { $next='choose_task' }
    elseif ($accounting.accounting_system -ceq 'undecided') { $next='choose_accounting' }
    $health='ok'; $docCount=$docs.Count; $entryCount=$null
    if ($null -ne $accounting) { $entryCount=$accounting.entry_count }
    if ($errors.Count) { $health='needs_review';$docCount=$null;$entryCount=$null }
    $result=@{schema_version=1;generated_by='de-business-kit-native-overview-v1';health=$health;errors=@($errors.ToArray());language=$language;period=$Period;as_of=(Get-Date).ToString('yyyy-MM-dd');questions=$questions;tasks=$tasks;active_tasks=$activeTasks;next_task_id=$nextTaskId;documents=$docs;accounting=$accounting;counts=@{documents=$docCount;entries=$entryCount};next_action=$next;scope='Saved state and local hashes only; full filing preflight, tax correctness and period completeness are not assessed.'}
    $e={param($value) [Net.WebUtility]::HtmlEncode([string]$value)}
    $section={param($title,$items) '<section><h2>'+(& $e $title)+'</h2>'+$(if (@($items).Count) { '<ul>'+(@($items | ForEach-Object { '<li>'+(& $e $_)+'</li>' }) -join '')+'</ul>' } else { '<p>'+(& $e $words.empty)+'</p>' })+'</section>'}
    $body='<section><h2>'+(& $e $words.next)+'</h2><p>'+(& $e $words[$next])+'</p></section>'
    if ($errors.Count) { $body+=& $section $words.errors @($errors.ToArray()) }
    $taskRows=@(foreach ($task in $activeTasks) {
        $state=$words.task_states.PSObject.Properties[$task.status].Value
        $date=$words.task_no_date; if ($null -ne $task.due_date) { $date=$task.due_date+' / '+$task.deadline_source }
        $row=$task.title+' / '+$words.task_owner+': '+$task.owner+' / '+$state+' / '+$words[('task_'+$task.readiness)]+' / '+$date
        if ($null -ne $task.note) { $row+=' / '+$task.note }
        if ($task.pending_dependencies.Count) { $row+=' / '+$words.task_dependencies+': '+($task.pending_dependencies -join ', ') }
        $row
    })
    $noTasks=$words.no_active_tasks; if ($errors.Count) { $noTasks=$words.repair }
    $body+=& $section $words.active_tasks (@($words.tasks_scope)+$(if ($taskRows.Count) { $taskRows } else { @($noTasks) }))
    $body+=& $section ($words.documents+' ('+$(if ($null -eq $docCount) { $words.unknown } else { $docCount })+')') @($docs | ForEach-Object { $_.original_name })
    $body+=& $section $words.questions @($questions | ForEach-Object { $_.title })
    $accountRows=@($words.readiness+': '+$words.not_assessed)
    if ($null -ne $accounting) {
        $accountRows+=@(($words.system+': '+$words[$accounting.accounting_system]),($words.method+': '+$(if ($accounting.method -ceq 'unresolved') { $words.not_assessed } else { $accounting.method })),($words.entries+': '+$(if ($null -eq $entryCount) { $words.unknown } else { $entryCount })),($words.evidence+': '+$words[$accounting.evidence_status]))
        if ($null -ne $accounting.product) { $accountRows+=@($words.product+': '+$accounting.product) }
        foreach ($filing in $accounting.filings) { $accountRows+=@($filing.filing_id+' / '+$filing.form+' / '+$filing.period+' / '+$words[$filing.state]); $accountRows+=@($filing.issues)
            foreach ($response in $filing.responses) {
                $kind=$words.response_kinds.PSObject.Properties[$response.response_kind].Value
                $accountRows+=@($words.authority_response+': '+$kind+' / '+(ViewProperty $response 'due_date' '')+' / '+$response.evidence.path)
            }
        }
    }
    $body+=& $section $words.accounting $accountRows
    $mark="<!-- German Business Kit native overview v1 -->`n"
    $html=$mark+'<!doctype html><html lang="'+$language+'"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src ''none''; style-src ''unsafe-inline''; base-uri ''none''; form-action ''none''"><title>'+(& $e $words.title)+'</title><style>body{margin:0;background:#f5f6f3;color:#182d29;font:16px/1.55 system-ui,sans-serif}main{max-width:1000px;margin:auto;padding:24px}section{background:white;border:1px solid #d7dfd9;border-radius:12px;padding:20px;margin:18px 0}h1{line-height:1.15}li,p{overflow-wrap:anywhere}li{margin-bottom:12px}small{color:#52635f}</style></head><body><main><h1>'+(& $e $words.title)+'</h1><p>'+(& $e $Period)+' / '+(& $e $result.as_of)+'</p><p>'+(& $e $words.boundary)+'</p>'+$body+'</main></body></html>'
    # Preflight every output before replacing any; only these generated projections are replaceable.
    foreach ($name in @('native-overview.html','native-overview.md','native-overview.json')) {
        $target=WorkspacePath ('00_admin/'+$name)
        if (Test-Path -LiteralPath $target) {
            if ($name.EndsWith('.json')) { if ((ViewProperty (ReadJson $target) 'generated_by') -cne $result.generated_by) { throw 'Existing native view is not tool-generated; preserve it.' } }
            elseif (-not $utf8.GetString((ReadBytes $target)).StartsWith($mark,[StringComparison]::Ordinal)) { throw 'Existing native view is not tool-generated; preserve it.' }
        }
    }
    $markdownRows=@($errors.ToArray())+@($words.active_tasks,$words.tasks_scope)+$(if ($taskRows.Count) { $taskRows } else { @($noTasks) })+@($docs | ForEach-Object { $_.original_name })+@($questions | ForEach-Object { $_.title })+$accountRows
    $markdownRows=@($markdownRows | ForEach-Object { ([Net.WebUtility]::HtmlEncode([string]$_)) -replace '([\\`*_{}\[\]()#+.!|>~-])','\$1' })
    $markdown=$mark+'# '+$words.title+"`n`n"+$Period+' / '+$result.as_of+"`n`n"+$words.boundary+"`n`n"+$words.next+': '+$words[$next]+"`n`n"+($markdownRows -join "`n`n")+"`n"
    ViewSave '00_admin/native-overview.html' ($utf8.GetBytes($html))
    ViewSave '00_admin/native-overview.md' ($utf8.GetBytes($markdown))
    ViewSave '00_admin/native-overview.json' (BytesJson $result)
    $prefix=(WorkspacePath '00_admin').Substring($rootPath.TrimEnd([char[]]'\/').Length+1).Replace('\','/')
    return @{health=$health;errors=@($errors.ToArray());html_path=$prefix+'/native-overview.html';markdown_path=$prefix+'/native-overview.md';json_path=$prefix+'/native-overview.json';next_action=$next;next_task_id=$nextTaskId;scope=$result.scope}
}
