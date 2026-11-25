"""Summarize a stream-json transcript: tools used, URLs fetched/searched, final answer."""
import json, sys

for path in sys.argv[1:]:
    tools, urls, searches, result, meta = [], [], [], None, {}
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get('type') == 'assistant':
            for block in ev.get('message', {}).get('content', []):
                if block.get('type') == 'tool_use':
                    name = block.get('name')
                    inp = block.get('input', {})
                    tools.append(name)
                    if name == 'WebFetch':
                        urls.append(inp.get('url'))
                    elif name == 'WebSearch':
                        searches.append(inp.get('query'))
                    elif name == 'Skill':
                        tools[-1] = f"Skill({inp.get('skill') or inp.get('command')})"
        if ev.get('type') == 'result':
            result = ev.get('result')
            meta = {k: ev.get(k) for k in ('session_id', 'num_turns', 'duration_ms', 'total_cost_usd', 'is_error', 'subtype')}
    print('=' * 100)
    print(path)
    print('meta:', meta)
    from collections import Counter
    print('tools:', dict(Counter(tools)))
    print('searches:', *searches, sep='\n  - ')
    print('fetched:', *urls, sep='\n  - ')
    print('--- answer ---')
    print(result)
