"""Read-only integrity checks for this project's workflow records (stdlib only)."""
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote


def fingerprint(path):
    text_formats = {'.md', '.py', '.json', '.log', '.txt', '.ipynb'}
    data = path.read_text(encoding='utf-8').encode('utf-8') if path.suffix.lower() in text_formats else path.read_bytes()
    return hashlib.sha256(data).hexdigest()


def measurement_rows(text):
    rows = []
    keys = ['length', 'gpu_ms', 'cpu_ms', 'gpu_mib', 'cpu_matrix_mib']
    for line in text.splitlines():
        columns = [s.strip() for s in line.strip().strip('|').split('|')]
        if len(columns) == 5 and columns[0].isdigit():
            values = [int(columns[0])] + [None if s in ('OOM', 'N/A') else float(s) for s in columns[1:]]
            rows.append(dict(zip(keys, values)))
    return rows


def validate(base, manifest):
    base = base.resolve()
    errors = []
    if manifest.get('schema_version') != 1:
        errors.append('Schema manifest không hỗ trợ')
    records = manifest.get('files', [])
    ids = [entry['id'] for entry in records + manifest.get('sources', [])]
    if len(ids) != len(set(ids)):
        errors.append('ID trùng trong danh mục')
    paths = [entry['path'] for entry in records]
    if len(paths) != len(set(paths)):
        errors.append('Đường dẫn trùng trong danh mục')
    actual = {p.relative_to(base).as_posix() for p in base.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    expected = set(paths) | {'manifest.json'}
    for path in sorted(actual - expected):
        errors.append(f'Ngoài danh mục: {path}')
    for path in sorted(expected - actual):
        errors.append(f'Thiếu file: {path}')
    for path in sorted(actual):
        if Path(path).name == 'GUIDE.md':
            errors.append(f'Còn GUIDE.md: {path}')
    for entry in records:
        path = (base / entry['path']).resolve()
        if not path.is_relative_to(base):
            errors.append(f'Đường dẫn vượt workflow: {entry["path"]}')
            continue
        if not path.is_file():
            continue
        if fingerprint(path) != entry['sha256']:
            errors.append(f'Hash lệch (cần review thay đổi): {entry["path"]}')
        pages = entry.get('pdf_pages', [])
        if any(not isinstance(page, int) or not 1 <= page <= 20 for page in pages):
            errors.append(f'Trang PDF không hợp lệ: {entry["path"]}')
        if path.suffix != '.md':
            continue
        text = path.read_text(encoding='utf-8')
        for heading in entry.get('sections', []):
            if heading not in text.splitlines():
                errors.append(f'Thiếu mục {heading}: {entry["path"]}')
        if re.search(r'\b(?:TODO|TBD|FIXME)\b|<điền[^>]*>|\{\{[^}]+\}\}', text):
            errors.append(f'Còn dấu giữ chỗ: {entry["path"]}')
        for target in re.findall(r'\[[^\]]+\]\(([^)\n]+)\)', text):
            target = target.strip('<>')
            if target.startswith(('https:', 'http:', 'mailto:', '#')):
                continue
            dest = (path.parent / unquote(target.split('#')[0])).resolve()
            if not dest.is_relative_to(base.parent) or not dest.exists():
                errors.append(f'Liên kết hỏng: {entry["path"]} -> {target}')
    for source in manifest.get('sources', []):
        path = (base / source['path']).resolve()
        if not path.is_relative_to(base.parent):
            errors.append(f'Nguồn vượt repo: {source["id"]}')
        elif not path.is_file():
            errors.append(f'Thiếu nguồn: {source["path"]}')
        elif fingerprint(path) != source['sha256']:
            errors.append(f'Nguồn đổi, cần đối chiếu lại: {source["path"]}')
    if 'steps' in manifest:
        steps = manifest['steps']
        if sorted(s['number'] for s in steps) != list(range(1, 15)):
            errors.append('Danh mục phải có đủ 14 bước duy nhất')
        for step in steps:
            if step['path'] not in paths or not step['path'].startswith(f'{step["number"]:02d}-'):
                errors.append(f'Bước không có hồ sơ đúng vị trí: {step}')
    if 'benchmark' in manifest:
        benchmark = manifest['benchmark']
        if any(benchmark[key] not in paths for key in ('log', 'data', 'table') if key in benchmark):
            errors.append('Số liệu ngoài danh mục file được kiểm soát')
            return errors
        try:
            data = json.loads((base / benchmark['data']).read_text(encoding='utf-8'))
            measured = measurement_rows((base / benchmark['log']).read_text(encoding='utf-8'))
            if not data or data != measured:
                errors.append('Số liệu lệch log benchmark')
            if 'table' in benchmark and measurement_rows((base / benchmark['table']).read_text(encoding='utf-8')) != data:
                errors.append('Số liệu lệch log trong bảng tài liệu')
        except (OSError, ValueError, KeyError) as error:
            errors.append(f'Không đọc được số liệu benchmark: {error}')
    return errors


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    try:
        registry = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))
        failures = validate(root, registry)
    except (OSError, ValueError, KeyError, TypeError) as error:
        failures = [f'Không đọc/kiểm tra được danh mục: {error}']
    if failures:
        print('\n'.join(f'FAIL: {failure}' for failure in failures))
        sys.exit(1)
    print(f'PASS: {len(registry["files"])} file, 14 bước, nguồn/hash/link/mục bắt buộc và số liệu khớp log.')
