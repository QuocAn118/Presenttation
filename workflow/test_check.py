"""Regression checks for document integrity, links, sources and measured data."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('workflow_check', Path(__file__).with_name('check.py'))
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class DocumentControlTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'workflow'
        self.root.mkdir()
        (self.root / 'DOC.md').write_text('# Bài demo\n\n## Kết quả\nĐã kiểm tra.\n', encoding='utf-8')
        (self.root.parent / 'source.txt').write_text('nguồn gốc', encoding='utf-8')
        self.manifest = {
            'schema_version': 1,
            'files': [{'id': 'DOC', 'path': 'DOC.md', 'sha256': checker.fingerprint(self.root / 'DOC.md'), 'sections': ['## Kết quả']}],
            'sources': [{'id': 'SRC', 'path': '../source.txt', 'sha256': checker.fingerprint(self.root.parent / 'source.txt')}],
        }
        (self.root / 'manifest.json').write_text('{}', encoding='utf-8')

    def test_valid_inventory(self):
        self.assertEqual(checker.validate(self.root, self.manifest), [])

    def test_missing_file(self):
        (self.root / 'DOC.md').unlink()
        self.assertTrue(any('Thiếu file' in e for e in checker.validate(self.root, self.manifest)))

    def test_unreviewed_edit(self):
        (self.root / 'DOC.md').write_text('đổi nội dung', encoding='utf-8')
        self.assertTrue(any('Hash lệch' in e for e in checker.validate(self.root, self.manifest)))

    def test_broken_link_even_with_updated_hash(self):
        (self.root / 'DOC.md').write_text('# Bài demo\n\n## Kết quả\n[x](missing.md)\n', encoding='utf-8')
        self.manifest['files'][0]['sha256'] = checker.fingerprint(self.root / 'DOC.md')
        self.assertTrue(any('Liên kết hỏng' in e for e in checker.validate(self.root, self.manifest)))

    def test_source_drift(self):
        (self.root.parent / 'source.txt').write_text('nguồn đã đổi', encoding='utf-8')
        self.assertTrue(any('Nguồn đổi' in e for e in checker.validate(self.root, self.manifest)))

    def test_unregistered_file_and_guide(self):
        (self.root / 'GUIDE.md').write_text('khung hướng dẫn', encoding='utf-8')
        errors = checker.validate(self.root, self.manifest)
        self.assertTrue(any('Ngoài danh mục' in e for e in errors))
        self.assertTrue(any('GUIDE.md' in e for e in errors))

    def test_duplicate_id(self):
        self.manifest['files'].append(copy.deepcopy(self.manifest['files'][0]))
        self.assertTrue(any('ID trùng' in e for e in checker.validate(self.root, self.manifest)))

    def test_benchmark_does_not_accept_changed_measurement(self):
        (self.root / 'run.log').write_text('128 | 0.29 | 1.10 | 497.95 | 0.75\n', encoding='utf-8')
        (self.root / 'measurements.json').write_text(json.dumps([{'length': 128, 'gpu_ms': 0.29, 'cpu_ms': 999, 'gpu_mib': 497.95, 'cpu_matrix_mib': 0.75}]), encoding='utf-8')
        for name in ['run.log', 'measurements.json']:
            self.manifest['files'].append({'id': name, 'path': name, 'sha256': checker.fingerprint(self.root / name)})
        self.manifest['benchmark'] = {'log': 'run.log', 'data': 'measurements.json'}
        self.assertTrue(any('Số liệu lệch log' in e for e in checker.validate(self.root, self.manifest)))

    def test_benchmark_paths_must_be_registered(self):
        self.manifest['benchmark'] = {'log': '../source.txt', 'data': '../source.txt'}
        self.assertTrue(any('Số liệu ngoài danh mục' in e for e in checker.validate(self.root, self.manifest)))

    def test_text_hash_is_stable_across_windows_line_endings(self):
        path = self.root / 'DOC.md'
        before = checker.fingerprint(path)
        path.write_bytes(path.read_text(encoding='utf-8').replace('\n', '\r\n').encode('utf-8'))
        self.assertEqual(checker.fingerprint(path), before)

    def test_binary_figures_can_be_fingerprinted(self):
        path = self.root.parent / 'figure.png'
        path.write_bytes(b'\x89PNG\r\n\x1a\n\xff\x00')
        self.assertEqual(len(checker.fingerprint(path)), 64)


if __name__ == '__main__':
    unittest.main()
