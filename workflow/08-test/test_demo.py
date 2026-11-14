import ast
import inspect
import json
from pathlib import Path
import statistics
import tempfile
import time
import unittest
from unittest.mock import patch

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import torch

scope = dict(torch=torch, plt=plt, np=np, Path=Path, statistics=statistics, time=time)
notebook = json.loads((Path(__file__).resolve().parents[2] / 'self_attention_demo.ipynb').read_text(encoding='utf-8'))
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        for node in ast.parse(''.join(cell['source'])).body:
            if isinstance(node, ast.FunctionDef):
                exec(compile(ast.Module(body=[node], type_ignores=[]), '<notebook>', 'exec'), scope)


class DemoContracts(unittest.TestCase):
    def test_attention_analytical_example(self):
        x = torch.eye(2)
        w = torch.cat([torch.eye(2)] * 3, dim=1)
        out, attn = scope['self_attention'](x, w, torch.zeros(6), n_head=1)
        p = torch.exp(torch.tensor(1 / 2**0.5))
        expected = torch.tensor([[1., 0.], [1 / (1 + p), p / (1 + p)]])
        assert torch.allclose(attn[0], expected, atol=1e-6)
        assert torch.allclose(out, expected, atol=1e-6)

    def test_invalid_head_count_is_clear(self):
        with self.assertRaises(ValueError):
            scope['self_attention'](torch.eye(2), torch.zeros(2, 6), torch.zeros(6), n_head=0)

    def test_pick_head_contract(self):
        assert list(inspect.signature(scope['pick_head']).parameters) == ['src', 'tgt']

    def test_plot_attention_exports(self):
        assert 'plot_attention' in scope, 'Missing plot_attention API required by the plan'
        with tempfile.TemporaryDirectory() as folder:
            prefix = str(Path(folder) / 'heatmap')
            scope['plot_attention'](torch.full((2, 2), .5), torch.tensor([[1., 0.], [.5, .5]]), ['a', 'b'], 'Trọng số đã huấn luyện của GPT-2', prefix)
            assert all(Path(prefix + suffix).stat().st_size > 0 for suffix in ['_compare.png', '_no_mask.png', '_causal_mask.png'])
        plt.close('all')

    def test_cpu_measures_actual_returned_matrix(self):
        def returned_matrix(x, *args, **kwargs):
            return x, torch.zeros((12, len(x), len(x)), dtype=torch.float64)
        with patch.dict(scope, self_attention=returned_matrix):
            result = scope['benchmark']([2], 'cpu', n_rep=1)
        assert result[0]['mem_mb'] == 12 * 2 * 2 * 8 / 2**20

    def test_oom_during_each_allocation_continues(self):
        original = torch.randn
        for fail_at in [1, 2, 3]:
            calls = 0
            def fail_once(*args, **kwargs):
                nonlocal calls
                calls += 1
                if calls == fail_at:
                    raise torch.OutOfMemoryError('simulated allocation OOM')
                return original(*args, **kwargs)
            with self.subTest(allocation=fail_at), patch('torch.randn', side_effect=fail_once):
                rows = scope['benchmark']([2, 3], 'cpu', n_rep=1)
                assert rows[0] == {'len': 2, 'ms': None, 'mem_mb': None}
                assert rows[1]['len'] == 3 and rows[1]['ms'] > 0

    def test_attention_oom_records_all_rows(self):
        def oom(*args, **kwargs):
            raise torch.OutOfMemoryError('simulated attention OOM')
        with patch.dict(scope, self_attention=oom):
            assert scope['benchmark']([2, 3], 'cpu', n_rep=1) == [
                {'len': 2, 'ms': None, 'mem_mb': None},
                {'len': 3, 'ms': None, 'mem_mb': None},
            ]

    def test_missing_token_error(self):
        with self.assertRaisesRegex(ValueError, "Không tìm thấy token 'it'"):
            scope['find_token'](['The', 'animal'], 'it')


if __name__ == '__main__':
    unittest.main()
