"""CLI evidence cycle with synthetic inputs; no provider execution or tax result."""
import hashlib
import json
from pathlib import Path
import sys
from synthetic_journey import command, ws

FIXTURES = Path(__file__).resolve().parent / 'fixtures/customer'


def run(root, language='en'):
    root = Path(root).resolve()
    command('workspace.py', 'start', '--root', root, '--year', 2026, '--language', language)

    def write(relative, content):
        path = ws._inside(root, relative)
        path.write_text(content, encoding='utf-8')
        return relative

    def input_file(name, value):
        return write('00_admin/inbox/' + name, json.dumps(value, ensure_ascii=False, indent=2))

    proof = write('08_correspondence/synthetic-case.md',
                  'Synthetic test only: the chosen authority is Example Books / web. '
                  'The fixture bank reference identifies INV-SYN-001; CN-SYN-001 references that invoice. '
                  'Only these document links are reviewed here; no tax, posting, settlement or refund approval.\n')
    config = command('desk.py', 'accounting-template', '--kind', 'configuration')
    config.update(system='external', product='Example Books / web (synthetic)',
                  account_reference='synthetic-account', reviewer='synthetic test routine', evidence_file=proof)
    command('desk.py', 'accounting-configure', '--root', root, '--input', input_file('accounting.json', config))
    v1 = write('08_correspondence/customer-v01.md',
               'Синтетический черновик: исходный счёт; проверка оплаты открыта.\n' if language == 'ru' else
               'Synthetic draft: original invoice; payment review remains open.\n')
    v1_hash = hashlib.sha256(ws._inside(root, v1).read_bytes()).hexdigest()
    ids = {}
    for name in ('invoice.synthetic.xml', 'payment.synthetic.csv', 'credit-note.synthetic.xml'):
        command('desk.py', 'receive', '--root', root, '--source', FIXTURES / name,
                '--period', '2026-10', '--received-on', '2026-10-26')
    for record in json.loads(ws._inside(root, ws.DOCUMENTS).read_text())['documents']:
        ids[record['original_name']] = record['document_id']
    inspections = {}
    for name in ('invoice.synthetic.xml', 'credit-note.synthetic.xml'):
        result = command('desk.py', 'inspect-xml', '--root', root, '--document-id', ids[name])
        inspections[name] = json.loads((root / result['path']).read_text())
    before = command('desk.py', 'catalog', '--root', root, '--document-id', ids['credit-note.synthetic.xml'])
    title = 'Проверить спор и дальнейший расчёт по счёту' if language == 'ru' else 'Review dispute and remaining settlement'
    task = dict(schema_version=1, id='customer-follow-up', title=title, owner='user', status='pending', evidence_file=proof)
    command('workspace.py', 'entry', '--root', root, '--collection', 'tasks', '--input', input_file('task.json', task))
    for name, kind in (('invoice.synthetic.xml', 'invoice'), ('payment.synthetic.csv', 'bank_statement'),
                       ('credit-note.synthetic.xml', 'credit_note')):
        current = command('desk.py', 'catalog', '--root', root, '--document-id', ids[name])
        record = current['record']
        record.update(type=kind, review_status='needs_review', review_note='Synthetic evidence link only; settlement and tax remain open.')
        record['links']['task_ids'] = [task['id']]
        if kind in {'invoice', 'bank_statement'}:
            record['links']['payment_refs'] = ['SYN-PAY-1']
        if kind == 'credit_note':
            record['relations'] = [{'relation': 'corrects', 'document_id': ids['invoice.synthetic.xml']}]
        command('desk.py', 'catalog-save', '--root', root, '--input', input_file('catalog.json', record),
                '--expected-sha256', current['sha256'])
    note = ('# Синтетический цикл документов — версия 2\n\n'
            'Сохранены исходный счёт INV-SYN-001, платёж SYN-PAY-1 на 50.00 EUR и CreditNote CN-SYN-001. '
            'Связи документов проверены только на синтетических данных. Спор, возврат и окончательный расчёт остаются открытыми. '
            'Внешняя система остаётся основной; проводки, отправка и налоговый расчёт не выполнялись.\n'
            if language == 'ru' else
            '# Synthetic document cycle — version 2\n\n'
            'Preserved INV-SYN-001, payment SYN-PAY-1 for EUR 50.00 and CreditNote CN-SYN-001. '
            'Document links were checked only against synthetic inputs. Dispute, refund and final settlement remain open. '
            'External software stays authoritative; no posting, sending or tax calculation occurred.\n')
    v2 = write('08_correspondence/customer-v02.md', note)
    resumed = command('workspace.py', 'start', '--root', root)
    current_task = command('workspace.py', 'entry', '--root', root, '--collection', 'tasks', '--id', task['id'])
    catalog = command('desk.py', 'catalog', '--root', root)
    verified = command('workspace.py', 'verify', '--root', root)
    return dict(root=str(root), ids=ids, inspections=inspections, before=before, catalog=catalog,
                task=current_task, resumed=resumed, verified=verified, v1=v1, v2=v2,
                v1_preserved=hashlib.sha256(ws._inside(root, v1).read_bytes()).hexdigest() == v1_hash,
                accounting=command('desk.py', 'accounting-status', '--root', root))


if __name__ == '__main__':
    print(json.dumps(run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'en'), ensure_ascii=False, indent=2))
