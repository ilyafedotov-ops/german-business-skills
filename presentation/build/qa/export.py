"""Write the three real Q&A transcripts to a readable Markdown file."""
import json, sys
from collections import Counter

base, out = sys.argv[1], sys.argv[2]
LANG = sys.argv[3] if len(sys.argv) > 3 else 'en'
# The exact prompts passed to run.sh (stream-json does not echo the initial prompt).
PROMPTS = {
    'berlin': "Use de-business-start. I live in Berlin and have a full-time job as an employee. On the side I want to translate documents between German and Russian for private clients and small companies, maybe 800 euros a month. Is that Freiberufler or Gewerbe, what exactly do I need to register, and where? Please include links to the official sources.",
    'hamburg': "Use de-business-tax. I'm a freelance web designer in Hamburg and started in January 2026. My revenue this year will be about 22,000 euros, all from small German businesses. Can I use the Kleinunternehmerregelung, and what happens if I go over the limit next year? Please cite official sources.",
    'munich': "Use de-business-tax. I'm a self-employed photographer in Munich. My 2025 income tax assessment from the Finanzamt München sets quarterly prepayments of 1,450 euros, the next one due on 10 December 2026. My profit this year dropped from about 38,000 to roughly 21,000 euros because I lost a big client. What does this mean, and can I ask them to lower the prepayments? If yes, draft a short German letter for me.",
}
PROMPTS_DE = {
    'berlin': "Use de-business-start. Ich wohne in Berlin und bin Vollzeit angestellt. Nebenbei möchte ich Dokumente zwischen Deutsch und Russisch übersetzen, für Privatkunden und kleine Firmen, etwa 800 Euro im Monat. Ist das freiberuflich oder ein Gewerbe, was genau muss ich anmelden und wo? Bitte mit Links zu den offiziellen Quellen. Bitte antworte auf Deutsch.",
    'hamburg': "Use de-business-tax. Ich bin freiberuflicher Webdesigner in Hamburg und habe im Januar 2026 angefangen. Mein Umsatz wird dieses Jahr etwa 22.000 Euro betragen, alles von kleinen deutschen Firmen. Kann ich die Kleinunternehmerregelung nutzen, und was passiert, wenn ich nächstes Jahr über die Grenze komme? Bitte nenne offizielle Quellen. Bitte antworte auf Deutsch.",
    'munich': "Use de-business-tax. Ich bin selbstständiger Fotograf in München. Mein Einkommensteuerbescheid 2025 vom Finanzamt München setzt vierteljährliche Vorauszahlungen von 1.450 Euro fest, die nächste ist am 10. Dezember 2026 fällig. Mein Gewinn ist dieses Jahr von etwa 38.000 auf rund 21.000 Euro gesunken, weil ich einen großen Kunden verloren habe. Was bedeutet das, und kann ich eine Herabsetzung der Vorauszahlungen beantragen? Wenn ja, entwirf mir bitte einen kurzen Brief an das Finanzamt. Bitte antworte auf Deutsch.",
}
PROMPTS_RU = {
    'berlin': "Use de-business-start. Я живу в Берлине и работаю по найму на полную ставку. В свободное время хочу переводить документы с немецкого на русский и обратно для частных клиентов и небольших фирм, примерно 800 евро в месяц. Это Freiberufler или Gewerbe, что именно мне нужно зарегистрировать и где? Пожалуйста, дай ссылки на официальные источники. Пожалуйста, отвечай по-русски.",
    'hamburg': "Use de-business-tax. Я веб-дизайнер на фрилансе в Гамбурге, начал работать в январе 2026 года. Мой оборот в этом году составит около 22 000 евро, всё от небольших немецких фирм. Могу ли я применять Kleinunternehmerregelung и что будет, если в следующем году я превышу лимит? Пожалуйста, укажи официальные источники. Пожалуйста, отвечай по-русски.",
    'munich': "Use de-business-tax. Я самозанятый фотограф в Мюнхене. Мой Einkommensteuerbescheid за 2025 год от Finanzamt München устанавливает ежеквартальные авансовые платежи по 1 450 евро, следующий нужно заплатить 10 декабря 2026 года. Моя прибыль в этом году упала примерно с 38 000 до 21 000 евро, потому что я потерял крупного клиента. Что это означает и могу ли я попросить снизить авансовые платежи? Если да, составь короткое письмо в Finanzamt на немецком. Пожалуйста, отвечай по-русски.",
}
# The English and German runs used the 0.13.0-preview.2 release; the Russian runs used 0.14.0-preview.1.
VERSION = '0.14.0-preview.1' if LANG == 'ru' else '0.13.0-preview.2'
cases = [
    ('berlin', 'Berlin · Freiberufler or Gewerbe?', 'de-business-start'),
    ('hamburg', 'Hamburg · Kleinunternehmerregelung', 'de-business-tax'),
    ('munich', 'Munich · lowering tax prepayments', 'de-business-tax'),
]
lines = ['# Real questions, real answers', '',
         'Three questions from fictional people, each asked in a fresh, isolated Claude Code session with the released',
         f'German Business Kit {VERSION} (Claude Opus 5.5, high effort) on 25 November 2026. No personal settings,',
         'plugins or MCP servers were loaded; tools allowed: web search/fetch, file reading and Python for arithmetic.',
         'The answers below are unedited. AI-assisted self-help, not tax or legal advice.', '']
for key, title, skill in cases:
    prompt, tools, urls, result, meta = None, [], [], None, {}
    for line in open(f'{base}/{key}/turn1.jsonl'):
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get('type') == 'assistant':
            for b in ev.get('message', {}).get('content', []):
                if b.get('type') == 'tool_use':
                    tools.append(b['name'])
                    if b['name'] == 'WebFetch':
                        urls.append(b['input'].get('url'))
        elif ev.get('type') == 'user' and prompt is None:
            c = ev.get('message', {}).get('content')
            if isinstance(c, str):
                prompt = c
        elif ev.get('type') == 'result':
            result = ev.get('result')
            meta = ev
    prompt = {'de': PROMPTS_DE, 'ru': PROMPTS_RU}.get(LANG, PROMPTS)[key]
    uniq = list(dict.fromkeys(u.split('?')[0] for u in urls if u))
    lines += [f'## {title}', '',
              f'**Question** (skill `{skill}`):', '', '> ' + prompt.replace('\n', '\n> '), '',
              f'**Run:** {meta.get("duration_ms", 0) / 1000:.0f} s · tools: ' + ', '.join(f'{k} ×{v}' for k, v in Counter(tools).items()),
              '', '**Pages fetched:**', ''] + [f'- {u}' for u in uniq] + ['', '**Answer:**', '', result or '', '', '---', '']
open(out, 'w').write('\n'.join(lines))
print('wrote', out)
