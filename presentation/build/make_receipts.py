"""Generates the Beleg-world carousels (EN, DE) and the YouTube scenes (EN) from one content model.

Example slides summarize the real answers in post/real-examples.md (EN) and post/real-examples.de.md (DE);
every source line names a page that session actually fetched (qa-transcripts/*.jsonl).
"""
import html, os

BUILD = os.path.dirname(os.path.abspath(__file__))
REPO = 'https://github.com/ilyafedotov-ops/german-business-skills'
TOTAL = 12

# ── line helpers: each returns (kind, payload, options) ─────────────────────────
def hdr(title, *sub): return ('hdr', (title, sub), {})
def dh(text, **o): return ('dh', text, o)
def dw(text, **o): return ('dw', text, o)
def t(text, cls='', **o): return ('t', (text, cls), o)
def lbl(text, **o): return ('lbl', text, o)
def rule(): return ('rule', None, {})
def dbl(): return ('dbl', None, {})
def row(k, v, kcls='', vcls='', **o): return ('row', (k, v, kcls, vcls), o)
def roww(k, v, vcls='red', **o): return ('roww', (k, v, vcls), o)
def box(text, **o): return ('box', text, o)
def letter(text, stamp, **o): return ('letter', (text, stamp), o)
def barcode(code): return ('barcode', code, {})
def qr(url, text, **o): return ('qr', (url, text), o)
def foot(text): return ('foot', text, {})
def gap(): return ('gap', None, {})
def group(lines, spotlight=False): return ('group', lines, {'spotlight': spotlight})


def render_lines(lines, landscape=False, counter=None, n_total=None):
    out = []
    for kind, p, o in lines:
        if kind == 'group':
            inner = render_lines(p, landscape, counter, n_total)
            out.append(f'<div{" data-spotlight" if o.get("spotlight") else ""}>{inner}</div>')
            continue
        if landscape and o.get('portrait_only'):
            continue
        i = counter[0]; counter[0] += 1
        if o.get('cue'):
            anim = f' data-cue="{html.escape(o["cue"])}" data-fx="print"'
        else:
            anim = f' data-at="{0.03 + 0.82 * i / max(1, n_total - 1):.3f}" data-fx="print"'
        if kind == 'hdr':
            title, sub = p
            out.append(f'<div class="hdr"{anim}><b>{title}</b>{"<br>".join(sub)}</div>')
        elif kind == 'dh':
            out.append(f'<div class="dh"{anim}>{p}</div>')
        elif kind == 'dw':
            out.append(f'<div class="dw"{anim}>{p}</div>')
        elif kind == 't':
            text, cls = p
            out.append(f'<div class="t {cls}"{anim}>{text}</div>')
        elif kind == 'lbl':
            out.append(f'<div class="lbl"{anim}>{p}</div>')
        elif kind == 'rule':
            out.append(f'<div class="rule"{anim}></div>')
        elif kind == 'dbl':
            out.append(f'<div class="rule dbl"{anim}></div>')
        elif kind == 'row':
            k, v, kc, vc = p
            out.append(f'<div class="row t {kc}"{anim}><span class="k">{k}</span><span class="dots"></span><span class="v {vc}">{v}</span></div>')
        elif kind == 'roww':
            k, v, vc = p
            out.append(f'<div class="row dw"{anim}><span class="k">{k}</span><span class="dots"></span><span class="v {vc}">{v}</span></div>')
        elif kind == 'box':
            out.append(f'<div class="box"{anim}>{p}</div>')
        elif kind == 'letter':
            text, stamp = p
            out.append(f'<div class="letter"{anim}><span class="stamp">{stamp}</span>{text}</div>')
        elif kind == 'barcode':
            out.append(f'<svg class="barcode" data-code="{p}"{anim}></svg>')
        elif kind == 'qr':
            url, text = p
            out.append(f'<div class="qrrow"{anim}><div class="qr" data-qr="{url}"></div><div class="t bold">{text}</div></div>')
        elif kind == 'foot':
            out.append(f'<div class="foot"{anim}>{p}</div>')
        elif kind == 'gap':
            out.append(f'<div class="gap"{anim}></div>')
    return ''.join(out)


def count(lines, landscape=False):
    n = 0
    for kind, p, o in lines:
        if kind == 'group':
            n += count(p, landscape)
        elif not (landscape and o.get('portrait_only')):
            n += 1
    return n


def receipt(lines, paper, landscape=False):
    n = count(lines, landscape)
    return f'<div class="receipt {paper}">{render_lines(lines, landscape, [0], n)}</div>'


# ── content ────────────────────────────────────────────────────────────────────
FOOT_EN = 'Real reply · Claude Code + German Business Kit 0.13 · 25.11.2026 · fictional person · summary · not tax advice'
FOOT_DE = 'Echte Antwort · Claude Code + German Business Kit 0.13 · 25.11.2026 · fiktive Person · Zusammenfassung · keine Steuerberatung'


def slides_en():
    S = []
    S.append(dict(id='r01', k=1.12, paper='white', copies=True, lines=[
        hdr('GERMAN BUSINESS KIT', 'Claude Code · Claude app · Codex', '25.11.2026  21:47'),
        rule(), dh('Every answer comes with its receipt.'), rule(),
        t('7 open-source AI skills for freelancers and sole traders in Germany.', 'mid'), rule(),
        row('Registration', 'OK'), row('Invoices &amp; receipts', 'OK'), row('Tax &amp; Finanzamt letters', 'OK'), row('Official sources shown', 'OK'),
        dbl(), roww('SENT BY', 'YOU'), barcode('GBK-0.14'), foot('Preview · AI assistance, not tax advice · swipe →')]))
    S.append(dict(id='r02', paper='white', lines=[
        dh('Before your first invoice:', cue='Running'), rule(),
        row('Fragebogen steuerl. Erfassung', '1×', cue='registration'), t('tax registration questionnaire', 'faded'),
        row('Gewerbeanmeldung', 'if Gewerbe', cue='forms'), t('trade registration', 'faded'),
        row('Rechnungen', 'every job', cue='invoices'), t('invoices with mandatory details', 'faded'),
        row('Belege · Kontoauszüge', 'monthly', cue='receipts'), t('receipts and bank statements', 'faded'),
        row('Steuererklärungen', 'yearly', cue='tax returns'), row('Post vom Finanzamt', 'any day', cue='Finanzamt'),
        dbl(), t('Often in a language that isn’t your first.', 'red bold', cue='second language')]))
    S.append(dict(id='r03', k=1.12, paper='white', lines=[
        dh('Not another app.', cue='So I built'), t('Skills for the assistant you already use:', 'mid', cue='seven'), rule(),
        row('Claude Code', 'OK', cue='Claude'), row('Claude app', 'OK', cue='Claude'), row('Codex', 'OK', cue='Codex'), rule(),
        t('A skill is a package of instructions, references and templates your assistant loads when a request needs it.', 'mid', cue='assistant'),
        rule(), row('Ask in', 'EN · DE · RU', cue='You just ask'), row('Guides &amp; reports', 'all three', cue='German or Russian'),
        dbl(), roww('NEW APP', 'NONE', cue='No new app')]))
    S.append(dict(id='r04', k=1.2, paper='white', lines=[
        dh('How every task runs'), rule(),
        t('<span class="num">1</span>You ask in your own words.', '', cue='asks'),
        t('<span class="num">2</span>It asks only what’s missing.', '', cue='missing'),
        t('<span class="num">3</span>It drafts and names the next step.', '', cue='prepares'),
        t('<span class="num">4</span>It saves facts in your private folder.', '', cue='saves'),
        t('<span class="num">5</span>Next month it continues there.', 'mid', cue='next month'),
        dbl(), roww('SENT BY', 'YOU', cue='stopped')]))
    S.append(dict(id='r05', paper='white', lines=[
        dh('Freiberufler or Gewerbe?', cue='asks'), t('Berlin · translator · €800/month', 'faded', cue='asks'), rule(),
        lbl('Checked: official pages it opened', cue='names the law'),
        row('§18 EStG „Übersetzer“', 'OK', 'faded', cue='names the law'), row('§138 AO one-month rule', 'OK', 'faded', cue='deadline'),
        row('elster.de founding', 'OK', 'faded', cue='registration'), row('berlin.de FAQ start-ups', 'OK', 'faded', cue='registration'),
        row('+ 6 more official pages', 'OK', 'faded', cue='official sources'),
        dbl(), dw('FREIBERUFLER<span class="stamp inl">GEPRÜFT 25.11.</span>', cue='names the law'),
        row('Register with', 'Finanzamt · ELSTER', cue='one registration'), row('Deadline', '1 month after start', cue='deadline'),
        row('Gewerbeanmeldung', 'not needed', cue='one registration'), rule(),
        t('Asks 2 follow-up questions that would change the details.', 'mid', cue='its deadline'),
        dbl(), roww('SENT BY', 'YOU', cue='opened'), foot(FOOT_EN)]))
    S.append(dict(id='r06', paper='blue', lines=[
        dh('Do I have to charge VAT?'), t('Hamburg · web designer · €22k, year 1', 'faded'), rule(),
        lbl('Checked: official pages it opened'),
        row('§19 UStG Kleinunternehmer', 'OK', 'faded'), row('finanzamt.hessen.de', 'OK', 'faded'),
        row('BMF letter 18.03.2025', 'NOT REACHABLE', 'faded', 'red'),
        dbl(), dw('KLEINUNTERNEHMER'),
        row('First-year limit', '€25,000'), row('What counts', 'money received'),
        row('Payment crossing it', 'taxed normally'), row('Over €25k in 2027', 'VAT from 1.1.2028'), rule(),
        t('Couldn’t load the BMF letter, and said so instead of guessing.', 'red bold'),
        dbl(), roww('SENT BY', 'YOU'), foot(FOOT_EN)]))
    S.append(dict(id='r07', k=0.95, paper='yellow', lines=[
        dh('Can I pay less in advance?'), t('Munich · photographer · €38k → ~€21k', 'faded'), rule(),
        lbl('Checked: official pages it opened'),
        row('§37 EStG prepayments', 'OK', 'faded'), row('§32a EStG 2026 tariff', 'OK', 'faded'), row('ELSTER adjustment form', 'OK', 'faded'),
        dbl(), dw('REDUCTION: YES'),
        row('Rough tax estimate', '~€1,819'), t('single, no deductions · checked 2 ways', 'faded'),
        row('Next payment due', 'in 15 days', '', 'red'), rule(),
        letter('„Ich beantrage daher gemäß § 37 Abs. 3 EStG, … die Vorauszahlung zum 10. Dezember 2026 auf 0 € herabzusetzen.“', 'ENTWURF · NICHT VERSANDT'),
        dbl(), roww('SENT BY', 'YOU'), foot(FOOT_EN)]))
    S.append(dict(id='r08', k=1.16, paper='white', lines=[
        dh('Seven skills, one business life', cue='covers'), t('de-business-…', 'faded', cue='covers'), rule(),
        group([row('kit', 'the front door', cue='journey'), row('start', 'registration', cue='starting'),
               row('operations', 'invoices, letters', cue='invoices'), row('accounting', 'receipts, bank', cue='receipts'),
               row('tax', 'tax, Finanzamt', cue='tax preparation'), row('services', 'bank, insurance, software', cue='services'),
               row('changes', 'hire, pause, close', cue='changes')], spotlight=True),
        dbl(), t('Mixed question? The kit routes it.', 'bold', cue='closing')]))
    S.append(dict(id='r09', k=1.08, paper='white', lines=[
        dh('One private folder'), rule(),
        t('My business/', 'bold'), row('01 Inbox', 'unsorted'), row('02 Documents', 'originals, numbered'),
        row('03 Accounts', 'bank, reports'), row('04 Taxes', 'by year'), row('05 Business', 'registration, letters'),
        dbl(), row('One profile', 'all activities, years'), row('Originals', 'kept, hashed'),
        row('Full backup', 'verified'), row('Folder names', 'EN · RU · DE')]))
    S.append(dict(id='r10', k=1.1, paper='white', lines=[
        dh('It prepares. You decide and send.', cue='One rule'), rule(),
        row('Source document', 'kept', cue='prepares'), row('Proposal', 'assistant', cue='prepares'), row('Review', 'YOU', '', 'red', cue='decide'),
        row('Booking', 'recorded', cue='decide'), row('Return draft', 'assistant', cue='send'), row('Authorization', 'YOU', '', 'red', cue='send'),
        row('Submission', 'YOU', '', 'red', cue='sign in'), row('Authority’s answer', 'evidence', cue='ELSTER'), rule(),
        t('You sign in to ELSTER and your bank yourself. No passwords or TANs in the chat.', 'mid', cue='bank yourself'),
        dbl(), roww('FINAL CLICK', 'YOU', cue='final click')]))
    S.append(dict(id='r11', paper='white', lines=[
        dh('Honest status: preview 0.14'), rule(), lbl('Works today'),
        row('7 skills in Claude &amp; Codex', 'OK'), row('Guides, reports in EN · DE · RU', 'OK'), row('Invoices, receipts, cash records', 'OK'),
        row('Lexware Office browser route', 'tested'), row('Backup &amp; restore', 'verified'), rule(), lbl('Not included'),
        row('Tax advice', 'NO', '', 'red'), row('ELSTER transmission', 'NO', '', 'red'), row('Complete tax engine', 'NO', '', 'red'),
        row('Local-only AI', 'NO', '', 'red'), dbl(),
        row('Commits since 25.10.', '190+'), row('Automated tests', '500+'), row('License', 'MIT')]))
    S.append(dict(id='r12', k=1.05, paper='pink', copies=True, lines=[
        dh('Try it with a made-up example.', cue='preview'), rule(),
        row('<span class="num">1</span>Open', 'Claude Code · app · Codex', cue='Try'),
        row('<span class="num">2</span>Paste', 'install request (README)', cue='Try'),
        t('<span class="num">3</span>Type:', '', cue='made-up'), box('Use de-business-kit. Start the welcome setup.', cue='made-up'), rule(),
        qr(REPO, 'github.com/<br>ilyafedotov-ops/<br>german-business-skills', cue='GitHub'),
        dbl(), roww('NEXT STEP', 'YOURS', cue='missing'),
        foot('Free · MIT · AI assistance, not tax advice · feedback very welcome')]))
    return S


def slides_de():
    S = []
    S.append(dict(id='r01', k=1.12, paper='white', copies=True, lines=[
        hdr('GERMAN BUSINESS KIT', 'Claude Code · Claude-App · Codex', '25.11.2026  21:47'),
        rule(), dh('Zu jeder Antwort gibt es den Beleg.'), rule(),
        t('7 Open-Source-KI-Skills für Selbstständige in Deutschland.', 'mid'), rule(),
        row('Anmeldung', 'OK'), row('Rechnungen &amp; Belege', 'OK'), row('Steuern &amp; Finanzamt-Post', 'OK'), row('Offizielle Quellen sichtbar', 'OK'),
        dbl(), roww('SENDEN', 'SIE'), barcode('GBK-0.14'), foot('Vorschau · KI-Unterstützung, keine Steuerberatung · wischen →')]))
    S.append(dict(id='r02', paper='white', lines=[
        dh('Vor der ersten Rechnung:'), rule(),
        row('Fragebogen steuerl. Erfassung', '1×'), row('Gewerbeanmeldung', 'falls Gewerbe'),
        row('Rechnungen', 'jeder Auftrag'), row('Belege · Kontoauszüge', 'monatlich'),
        row('Steuererklärungen', 'jährlich'), row('Post vom Finanzamt', 'jederzeit'),
        dbl(), t('Und alles mit Fristen.', 'red bold')]))
    S.append(dict(id='r03', k=1.12, paper='white', lines=[
        dh('Keine neue App.'), t('Skills für den Assistenten, den Sie schon nutzen:', 'mid'), rule(),
        row('Claude Code', 'OK'), row('Claude-App', 'OK'), row('Codex', 'OK'), rule(),
        t('Ein Skill ist ein Paket aus Anweisungen, Referenzen und Vorlagen, das der Assistent lädt, wenn eine Anfrage es braucht.', 'mid'),
        rule(), row('Sprachen', 'DE · EN · RU'), row('Anleitungen, Berichte', 'alle drei'), row('Briefe ans Amt', 'auf Deutsch'),
        dbl(), roww('NEUE APP', 'KEINE')]))
    S.append(dict(id='r04', k=1.2, paper='white', lines=[
        dh('So läuft jede Aufgabe'), rule(),
        t('<span class="num">1</span>Sie fragen in Ihren Worten.'), t('<span class="num">2</span>Es fragt nur, was fehlt.'),
        t('<span class="num">3</span>Es entwirft und nennt den nächsten Schritt.'), t('<span class="num">4</span>Es speichert alles im privaten Ordner.'),
        t('<span class="num">5</span>Nächsten Monat geht es dort weiter.', 'mid'),
        dbl(), roww('SENDEN', 'SIE')]))
    S.append(dict(id='r05', k=0.95, paper='white', lines=[
        dh('Freiberuflich oder Gewerbe?'), t('Berlin · Übersetzer · 800 €/Monat', 'faded'), rule(),
        lbl('Geprüft: geöffnete Amtsseiten'),
        row('§ 18 EStG „Übersetzer“', 'OK', 'faded'), row('§ 138 AO Monatsfrist', 'OK', 'faded'),
        row('service.berlin.de Gewerbe', 'OK', 'faded'), row('elster.de Gründung', 'OK', 'faded'),
        row('+ 3 weitere Seiten', 'OK', 'faded'),
        dbl(), dw('FREIBERUFLICH<span class="stamp inl">GEPRÜFT 25.11.</span>'),
        row('Anmeldung', 'Finanzamt · ELSTER'), row('Frist', '1 Monat nach Start'), row('Gewerbeanmeldung', 'nicht nötig'), rule(),
        t('Stellt 3 Rückfragen, bevor es das ELSTER-Arbeitsblatt vorbereitet.', 'mid'),
        dbl(), roww('SENDEN', 'SIE'), foot(FOOT_DE)]))
    S.append(dict(id='r06', paper='blue', lines=[
        dh('Muss ich Umsatzsteuer berechnen?'), t('Hamburg · Webdesign · 22.000 €, Jahr 1', 'faded'), rule(),
        lbl('Geprüft: geöffnete Amtsseiten'),
        row('§ 19 UStG Kleinunternehmer', 'OK', 'faded'), row('finanzamt.hessen.de', 'OK', 'faded'),
        row('BMF-Schreiben 2025', 'NICHT ABRUFBAR', 'faded', 'red'),
        dbl(), dw('KLEINUNTERNEHMER'),
        row('Grenze im Gründungsjahr', '25.000 €'), row('Es zählt', 'der Geldeingang'),
        row('Zahlung über Grenze', 'steuerpflichtig'), row('2027 über 25.000 €', 'USt ab 1.1.2028'), rule(),
        t('BMF-Schreiben nicht abrufbar (503). Steht offen in der Antwort.', 'red bold'),
        dbl(), roww('SENDEN', 'SIE'), foot(FOOT_DE)]))
    S.append(dict(id='r07', k=0.95, paper='yellow', lines=[
        dh('Kann ich weniger vorauszahlen?'), t('München · Fotograf · 38 T€ → ~21 T€', 'faded'), rule(),
        lbl('Geprüft: geöffnete Amtsseiten'),
        row('§ 37 EStG Vorauszahlungen', 'OK', 'faded'), row('§ 240 AO Säumniszuschlag', 'OK', 'faded'), row('ELSTER-Hilfe Vorauszahlung', 'OK', 'faded'),
        dbl(), dw('HERABSETZUNG: JA'),
        row('Bis zur Entscheidung', 'alter Bescheid'), row('Ohne Zahlung', '14,50 €/Monat', '', 'red'),
        row('Neue Steuer', 'nicht geschätzt'), t('fragt erst nach Familienstand und Einkünften', 'faded'), rule(),
        letter('„Ich beantrage daher nach § 37 Abs. 3 EStG, die Einkommensteuer-Vorauszahlungen … anzupassen und herabzusetzen.“', 'ENTWURF · NICHT VERSANDT'),
        dbl(), roww('SENDEN', 'SIE'), foot(FOOT_DE)]))
    S.append(dict(id='r08', k=1.16, paper='white', lines=[
        dh('Sieben Skills für den ganzen Weg'), t('de-business-…', 'faded'), rule(),
        group([row('kit', 'der Einstieg'), row('start', 'Anmeldung'), row('operations', 'Rechnungen, Briefe'),
               row('accounting', 'Belege, Bank'), row('tax', 'Steuern, Finanzamt'), row('services', 'Bank, Versicherung, Apps'),
               row('changes', 'Personal, Pause, Aufgabe')], spotlight=True),
        dbl(), t('Gemischte Frage? Das Kit leitet sie weiter.', 'bold')]))
    S.append(dict(id='r09', k=1.08, paper='white', lines=[
        dh('Ein privater Ordner'), rule(),
        t('Mein Unternehmen/', 'bold'), row('01 Eingang', 'unsortiert'), row('02 Dokumente', 'Originale'),
        row('03 Buchhaltung', 'Bank, Berichte'), row('04 Steuern', 'nach Jahr'), row('05 Unternehmen', 'Anmeldung, Briefe'),
        dbl(), row('Ein Profil', 'für alle Jahre'), row('Originale', 'mit Prüfsumme'),
        row('Vollsicherung', 'geprüft'), row('Ordnernamen', 'DE · EN · RU')]))
    S.append(dict(id='r10', k=1.1, paper='white', lines=[
        dh('Es bereitet vor. Sie entscheiden und senden.'), rule(),
        row('Quelldokument', 'bleibt'), row('Vorschlag', 'Assistent'), row('Prüfung', 'SIE', '', 'red'),
        row('Buchung', 'erfasst'), row('Erklärungsentwurf', 'Assistent'), row('Freigabe', 'SIE', '', 'red'),
        row('Übermittlung', 'SIE', '', 'red'), row('Antwort des Amts', 'Nachweis'), rule(),
        t('Bei ELSTER und der Bank melden Sie sich selbst an. Keine Passwörter oder TANs im Chat.', 'mid'),
        dbl(), roww('LETZTER KLICK', 'SIE')]))
    S.append(dict(id='r11', paper='white', lines=[
        dh('Ehrlicher Stand: Vorschau 0.14'), rule(), lbl('Funktioniert heute'),
        row('7 Skills in Claude &amp; Codex', 'OK'), row('Anleitungen, Berichte DE · EN · RU', 'OK'), row('Rechnungen, Belege, Kassenbuch', 'OK'),
        row('Lexware-Office-Browserweg', 'getestet'), row('Sicherung &amp; Wiederherstellung', 'geprüft'), rule(), lbl('Nicht enthalten'),
        row('Steuerberatung', 'NEIN', '', 'red'), row('ELSTER-Übermittlung', 'NEIN', '', 'red'), row('Vollständige Steuerberechnung', 'NEIN', '', 'red'),
        row('Nur-lokale KI', 'NEIN', '', 'red'), dbl(),
        row('Commits seit 25.10.', '190+'), row('Automatische Tests', '500+'), row('Lizenz', 'MIT')]))
    S.append(dict(id='r12', k=1.05, paper='pink', copies=True, lines=[
        dh('Probieren Sie es mit einem erfundenen Beispiel.'), rule(),
        row('<span class="num">1</span>Öffnen', 'Claude Code · App · Codex'),
        row('<span class="num">2</span>Einfügen', 'Anfrage aus dem README'),
        t('<span class="num">3</span>Schreiben:'), box('Use de-business-kit. Starte die Einrichtung.'), rule(),
        qr(REPO, 'github.com/<br>ilyafedotov-ops/<br>german-business-skills'),
        dbl(), roww('ALS NÄCHSTES', 'SIE'),
        foot('Kostenlos · MIT · KI-Unterstützung, keine Steuerberatung · Feedback willkommen')]))
    return S


FIT = '''
<script>
  // Scale each landscape receipt to its box and centre it; the engine calls this before setup.
  window.__fit = () => document.querySelectorAll('.fitbox').forEach(box => {
    const inner = box.querySelector('.fitinner'), lift = box.querySelector('.lift');
    lift.style.transform = ''; inner.style.width = inner.style.height = '';
    const w = lift.offsetWidth, h = lift.offsetHeight;
    const sc = Math.min(box.clientWidth / w, box.clientHeight / h, 1.05);
    lift.style.transform = `scale(${sc})`; lift.style.transformOrigin = '0 0';
    inner.style.width = (w * sc) + 'px'; inner.style.height = (h * sc) + 'px';
  });
  document.fonts.ready.then(() => window.__fit());
</script>'''

SCRIPTS = '''
<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jsbarcode/3.11.6/JsBarcode.all.min.js"></script>
<script>
  document.querySelectorAll('.qr').forEach(el => new QRCode(el, { text: el.dataset.qr, width: 352, height: 352, colorDark: '#141414', colorLight: '#ffffff', correctLevel: QRCode.CorrectLevel.M }));
  document.querySelectorAll('svg.barcode').forEach(el => JsBarcode(el, el.dataset.code, { format: 'CODE128', displayValue: false, height: 64, margin: 0, width: 3, background: 'transparent', lineColor: '#141414' }));
</script>'''

HEAD = '''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Martian+Mono:wdth,wght@75..112.5,300..800&display=block" rel="stylesheet">
<link rel="stylesheet" href="receipt.css">
<style>@page {{ size: 1080px 1350px; margin: 0; }} @media print {{ .vonly {{ display: none !important; }} }}</style>
</head>
<body>
'''


def portrait_slide(s, n, meta_left, lang):
    copies = ''
    if s.get('copies'):
        copies = ('<div class="copy" style="--c:var(--paper-yellow);transform:translate(34px,18px) rotate(3deg)"></div>'
                  '<div class="copy" style="--c:var(--paper-pink);transform:translate(-22px,26px) rotate(-2.4deg)"></div>')
    stamp = ''
    if s.get('stamp'):
        text, style = s['stamp']
        stamp = f'<div class="stamp" style="{style}">{text}</div>'
    k = s.get('k', 1)
    return (f'<section class="slide R" id="{s["id"]}">'
            f'<div class="meta"><span><b>GERMAN BUSINESS KIT</b>{meta_left}</span><span>BELEG {n:02d}/{TOTAL}</span></div>'
            f'<div class="area"><div class="lift" style="--k:{k}">{copies}{receipt(s["lines"], s["paper"])}{stamp}</div></div>'
            f'</section>\n')


DEMO_PORTRAIT = '''<section class="slide R vonly" id="rdemo">
  <div class="meta"><span><b>GERMAN BUSINESS KIT</b> · real apps</span><span>SCREENSHOTS</span></div>
  <div class="dh demo-title" style="position:absolute;left:82px;right:82px;top:120px;color:#fff;font-size:76px">Ask in your own words.</div>
  <div class="browser" style="position:absolute;left:82px;top:312px;width:916px"><div class="chrome"><i></i><i></i><i></i><span>Claude app</span></div><div class="vp" style="width:916px;height:740px"><img class="demo-img" alt="" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"></div></div>
  <div class="lift" style="left:82px;top:1128px;width:916px"><div class="receipt white" style="padding:30px 40px 34px"><div class="t mid" style="font-size:26px">Real Claude and Codex screenshots · fictional example · nothing is submitted</div></div></div>
</section>
'''


def write_carousel(lang, slides):
    meta = {'en': '', 'de': ''}[lang]
    body = ''.join(portrait_slide(s, i, meta, lang) for i, s in enumerate(slides, 1))
    if lang == 'en':
        body += DEMO_PORTRAIT
    path = os.path.join(BUILD, f'receipt-{lang}.html')
    open(path, 'w').write(HEAD.format(lang=lang, title=f'German Business Kit carousel {lang.upper()}') + body + SCRIPTS + '\n</body>\n</html>\n')
    return path


# ── YouTube scenes (EN, 16:9): receipt on the left, headline and notes on the carbon ──
def side(headline, sub=None, notes=(), small=None, top=170):
    n = ''.join(f'<div data-cue="{html.escape(c)}">{txt}</div>' for txt, c in notes)
    return (f'<div class="side">'
            f'<div class="dh">{headline}</div>'
            + (f'<div class="t" style="margin-top:26px">{sub}</div>' if sub else '')
            + (f'<div class="notes">{n}</div>' if notes else '')
            + (f'<div class="small" style="margin-top:34px">{small}</div>' if small else '')
            + '</div>')


def scene(sid, label, body_lines, paper, side_html, scale=0.78, left=96, top=104, width=880, extra=''):
    return (f'<section class="scene R" id="{sid}">'
            f'<div class="meta"><span><b>GERMAN BUSINESS KIT</b> · {label}</span><span></span></div>'
            f'<div class="fitbox"><div class="fitinner"><div class="lift">{receipt(body_lines, paper, landscape=True)}</div></div></div>'
            f'{side_html}{extra}</section>\n')


def strip_dh(lines):
    return [l for l in lines if l[0] != 'dh']


def write_youtube(en):
    by = {s['id']: s for s in en}
    yq = {  # narration cues from post/scripts.md (Yq1..Yq3)
        'r05': ('Berlin · translator · side job', [('Quotes the law that names translators', 'quotes the law'), ('One registration, one-month deadline', 'one registration'), ('Links the official pages it opened', 'official pages')]),
        'r06': ('Hamburg · web designer · first year', [('First-year limit: €25,000', 'first-year limit'), ('What happens when a payment crosses it', 'crosses it'), ('Says what it couldn’t check', 'said so')]),
        'r07': ('Munich · photographer · profit dropped', [('Estimate with this year’s tariff', 'estimates'), ('Arithmetic checked two ways', 'two ways'), ('Deadline flagged: 15 days', 'fifteen days'), ('German letter, marked as a draft', 'drafts')]),
    }
    out = []
    # Y0 title
    out.append(scene('y0', 'a walkthrough', strip_dh(by['r01']['lines']), 'white',
                     side('Every answer comes with its receipt.', '7 open-source AI skills for freelancers and sole traders in Germany, for <b>Claude</b> and <b>Codex</b>.', small='A walkthrough: what it is, how it works, and what it won’t do.'), scale=0.74))
    # Y1 problem + reveal
    reveal = ('<div class="reveal" data-cue="So I built" style="position:absolute;inset:0;background:var(--carbon-deep);display:flex;align-items:center;justify-content:center">'
              '<div class="lift" style="position:relative;width:1100px"><div class="receipt white" style="padding:70px 80px 80px">'
              '<div class="hdr"><b>GERMAN BUSINESS KIT</b>Claude Code · Claude app · Codex</div><div class="rule"></div>'
              '<div class="dh" style="font-size:92px">An assistant for all of it, one line at a time.</div><div class="rule dbl"></div>'
              '<div class="row dw"><span class="k">SENT BY</span><span class="dots"></span><span class="v red">YOU</span></div></div></div></div>')
    y1_lines = [l for l in by['r02']['lines'] if l[0] != 'dh']
    y1_lines = [(k, p, {kk: vv for kk, vv in o.items() if kk != 'cue'}) for k, p, o in y1_lines]
    y1_cues = ['questionnaire', None, 'invoices with', None, 'invoices with', None, 'receipts', None, 'bank statements', 'Finanzamt', None, 'language']
    y1_lines = [(k, p, ({**o, 'cue': c} if c else o)) for (k, p, o), c in zip(y1_lines, y1_cues + [None] * 20)]
    out.append(scene('y1', 'the problem', y1_lines, 'white', side('Before your first invoice, the paperwork starts.'), scale=0.8, extra=reveal))
    # Y2 idea
    y2 = [rule(), row('Claude Code', 'OK', cue='seven skills'), row('Claude app', 'OK', cue='for Claude'), row('Codex', 'OK', cue='Codex.'), rule(),
          t('A skill is a package of instructions, references and templates the assistant loads when your request needs it.', 'mid', cue='A skill'),
          rule(), row('Ask in', 'EN · DE · RU', cue='plain English'), row('Guides, reports', 'all three', cue='all three'), dbl(), roww('NEW APP', 'NONE', cue='no new app')]
    out.append(scene('y2', 'what it is', y2, 'white', side('Seven skills for Claude and Codex.'), scale=0.82))
    # Y3 how
    y3 = [rule(), t('<span class="num">1</span>You ask in your own words.', '', cue='One:'), t('“Turn these agreed terms into a German proposal.”', 'faded', cue='For example'),
          t('<span class="num">2</span>It reuses confirmed facts.', '', cue='Two:'), t('<span class="num">3</span>It asks only what’s missing.', '', cue='asks only'),
          t('<span class="num">4</span>It drafts and names the next step.', '', cue='readable draft'), t('<span class="num">5</span>It saves results and open questions.', '', cue='Three:'),
          t('<span class="num">6</span>Next month it continues there.', 'mid', cue='Next month'), dbl(), roww('SENT BY', 'YOU', cue='starting over')]
    out.append(scene('y3', 'how it works', y3, 'white', side('Ask. Clarify. Continue.'), scale=0.84))
    # Y4 skills (spotlight follows the narration)
    y4 = [t('de-business-…', 'faded'), rule(),
          group([row('start', 'registration', cue='Start helps'), row('operations', 'invoices, letters', cue='Operations'), row('accounting', 'receipts, bank, month', cue='Accounting'),
                 row('tax', 'rules, estimates, returns', cue='Tax researches'), row('services', 'bank, insurance, software', cue='Services'),
                 row('changes', 'activity, hire, pause, close', cue='Changes'), row('kit', 'the front door', cue='front door')], spotlight=True)]
    out.append(scene('y4', 'the seven skills', y4, 'white', side('Seven skills, one business life.', 'Each one follows a stage in the life of a sole trader.'), scale=0.88, top=170))
    # Y5 folder
    y5 = [t('My business/', 'bold'), row('01 Inbox', 'unsorted', cue='inbox'), row('02 Documents', 'originals, numbered', cue='documents,'),
          row('03 Accounts', 'bank, reports', cue='accounts'), row('04 Taxes', 'by year', cue='taxes'), row('05 Business', 'registration, letters', cue='and business'), dbl(),
          row('Originals', 'kept, numbered', cue='Originals'), row('One profile', 'all activities, all years', cue='One profile'), row('Overview page', 'where you stand', cue='overview page'),
          row('Full backup', 'verified', cue='verified backup')]
    out.append(scene('y5', 'your business folder', y5, 'white', side('One private folder. Everything in its place.'), scale=0.84))
    # Y6 demo: step receipt + browser
    steps = ''.join(f'<div class="row t dstep" data-step="{i}"><span class="k"><span class="num">{i}</span>{txt}</span><span class="dots"></span>'
                    f'<span class="v"><span class="pend">·</span><span class="now red">NOW</span><span class="ok">OK</span></span></div>'
                    for i, txt in enumerate(['Seven skills, ready', 'Ask in your own words', 'One small next step', 'In German, too'], 1))
    out.append('<section class="scene R" id="y6"><div class="meta"><span><b>GERMAN BUSINESS KIT</b> · real apps</span><span>SCREENSHOTS</span></div>'
               '<div class="lift" style="left:80px;top:150px;width:600px;transform:scale(.86);transform-origin:0 0"><div class="receipt white">'
               '<div class="hdr"><b>REAL APPS</b>fictional example · nothing submitted</div><div class="rule"></div>'
               f'{steps}<div class="rule dbl"></div><div class="t mid" style="font-size:24px">Unedited screenshots from Claude and Codex with the kit installed.</div></div></div>'
               '<div class="browser" style="position:absolute;left:640px;top:118px;width:1190px"><div class="chrome"><i></i><i></i><i></i><span>Codex</span></div>'
               '<div class="vp" style="width:1190px;height:744px"><img class="demo-img" alt="" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"></div></div></section>\n')
    # Yq examples
    for n, rid in enumerate(['r05', 'r06', 'r07'], 1):
        s = by[rid]
        sub, notes = yq[rid]
        lines = [(k, p, {kk: vv for kk, vv in o.items() if kk != 'cue'}) for k, p, o in strip_dh(s['lines'])]
        lines = [l for l in lines if not (l[0] == 't' and 'faded' in l[1][1] and '·' in l[1][0] and l is lines[0])]
        q = [l for l in s['lines'] if l[0] == 'dh'][0][1]
        stamp = ''
        out.append(scene(f'yq{n}', f'real question {n}/3', lines, s['paper'],
                         side(q, sub, notes, small='Real reply · Claude Code + German Business Kit 0.13 · 25.11.2026 · fictional person · summary · not tax advice', top=150),
                         scale=0.72, top=110, extra=stamp))
    # Y7 principle
    y7 = [(k, p, {kk: vv for kk, vv in o.items() if kk != 'cue'}) for k, p, o in strip_dh(by['r10']['lines'])]
    y7_cues = [None, 'Extraction', 'proposal,', 'review,', 'booking', 'booking', 'authorization', 'submission', 'answer', None, 'You sign in', None, 'final click']
    y7 = [(k, p, ({**o, 'cue': c} if c else o)) for (k, p, o), c in zip(y7, y7_cues + [None] * 20)]
    out.append(scene('y7', 'the principle', y7, 'white', side('It prepares. You decide and send.', 'A polished draft is never treated as a filed return.'), scale=0.84))
    # Y8 install
    y8 = [lbl('Claude app', cue='Claude app'), t('Customize → Plugins → Add marketplace →', '', cue='Customize'), t('ilyafedotov-ops/german-business-skills', 'bold', cue='marketplace'),
          t('→ Install German Business Kit', '', cue='install German'), rule(), lbl('Claude Code', cue='Claude Code,'),
          t('claude plugin marketplace add ilyafedotov-ops/german-business-skills', 'mid', cue='two commands'), t('claude plugin install de-business-kit@german-business-kit', 'mid', cue='two commands'),
          rule(), lbl('Codex', cue='In Codex'), t('Copy the released skills into your project.', '', cue='released skills'), rule(),
          t('Or paste the install request from the README.', 'bold', cue='paste the install'), dbl(), box('Use de-business-kit. Start the welcome setup.', cue='fresh chat')]
    out.append(scene('y8', 'install', y8, 'white', side('Install in a few minutes.'), scale=0.78, top=96))
    # Y9 limits + CTA
    y9 = [lbl('Not included', cue='honest limits'), row('Tax advice', 'NO', '', 'red', cue='not professional'), row('ELSTER transmission', 'NO', '', 'red', cue='ELSTER'),
          row('Complete tax engine', 'NO', '', 'red', cue='tax engine'), row('Local-only AI', 'NO', '', 'red', cue='AI provider'), rule(),
          t('Start with a made-up example.', 'bold', cue='made-up'), dbl(), qr(REPO, 'github.com/<br>ilyafedotov-ops/<br>german-business-skills', cue='open source'),
          dbl(), roww('NEXT STEP', 'YOURS', cue='what\'s missing')]
    out.append(scene('y9', 'honest limits', y9, 'pink', side('A few honest limits.', 'Early preview. AI can get calculations and deadlines wrong.',
                     notes=[('Tell me what’s missing', 'what\'s missing'), ('Danke, bis bald.', 'Danke')]), scale=0.86, top=110))
    # Y10 end card
    out.append('<section class="scene R" id="y10"><div class="lift" style="left:560px;top:120px;width:800px"><div class="receipt pink" style="text-align:left">'
               '<div class="hdr"><b>GERMAN BUSINESS KIT</b>7 open-source skills · Claude &amp; Codex · preview</div><div class="rule"></div>'
               f'<div class="qrrow"><div class="qr" data-qr="{REPO}"></div><div class="t bold">github.com/<br>ilyafedotov-ops/<br>german-business-skills</div></div>'
               '<div class="rule dbl"></div><div class="row dw"><span class="k">NEXT STEP</span><span class="dots"></span><span class="v red">YOURS</span></div></div></div></section>\n')
    path = os.path.join(BUILD, 'scenes-receipt-yt.html')
    head = HEAD.format(lang='en', title='German Business Kit walkthrough scenes').replace('@page {{ size: 1080px 1350px; margin: 0; }}', '')
    open(path, 'w').write(head.replace('<body>', '<body style="width:1920px;height:1080px;overflow:hidden">') + ''.join(out)
                          + '<style>.dstep .now,.dstep .ok{display:none}.dstep.on .pend,.dstep.done .pend{display:none}.dstep.on .now{display:inline}.dstep.done .ok{display:inline}.dstep.on .k{font-weight:800}.dstep:not(.on):not(.done) .k{color:var(--ink-faded)}</style>'
                          + SCRIPTS + FIT + '\n</body>\n</html>\n')
    return path


if __name__ == '__main__':
    en, de = slides_en(), slides_de()
    print(write_carousel('en', en))
    print(write_carousel('de', de))
    print(write_youtube(en))
