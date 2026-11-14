# Bằng chứng kiểm tra ngày 14/11/2026

Các log dùng code notebook gốc của commit nền `47246be`; notebook này giống bản tại `origin/main` (`3e594be`) khi bắt đầu bàn giao workflow. Ngày được ghi theo Asia/Bangkok.

| Log | Phạm vi | Kết quả |
| --- | --- | --- |
| [offline](2026-11-14-offline.log) | Bản sao nguyên trạng, GPU và CPU, `HF_HUB_OFFLINE=1` | Exit code 0; 0 ô lỗi; 4 PNG; 13.41 giây |
| [cpu](2026-11-14-cpu.log) | Thêm ô giả lập không GPU trước các ô gốc, chạy trong kernel mới | Exit code 0; 0 ô lỗi; 4 PNG; 12.33 giây |
| [branches](2026-11-14-branches.log) | Chạy các hàm gốc với OOM giả lập và token bị thiếu | Bắt lỗi và trả kết quả đúng trong phạm vi thử |

Lệnh CLI, stdout notebook, môi trường offline và warning được giữ trong hai log thực thi. Các output thử nghiệm đầy đủ nằm trong `scratch/wf-offline/` và `scratch/wf-cpu/` trên máy chạy, không được commit. Cách chạy lại xem [05_TOOLS](../docs/05_TOOLS.md).

## Tái lập nhánh lỗi

Trong kernel thử nghiệm riêng đã định nghĩa các hàm gốc, chạy:

```python
original_attention = self_attention
def simulated_oom(*args, **kwargs):
    raise torch.OutOfMemoryError("simulated")

try:
    self_attention = simulated_oom
    assert benchmark([16, 32], "cpu", n_rep=1) == [
        {"len": 16, "ms": None, "mem_mb": None},
        {"len": 32, "ms": None, "mem_mb": None},
    ]
finally:
    self_attention = original_attention

try:
    find_token(["The", "animal"], "it")
except ValueError as error:
    assert "Không tìm thấy token 'it'" in str(error)
else:
    raise AssertionError("Thiếu token phải báo ValueError")
```

Không gây OOM thật. Phép mô phỏng không bao phủ cấp phát nằm ngoài `try` trong benchmark. Các kiểm tra CLI không thay thế kiểm tra hiển thị trong VS Code.
