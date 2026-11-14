# Công cụ và môi trường

Tài liệu này ghi nhận môi trường đã kiểm tra và các lệnh hướng dẫn trong dự án trên hệ điều hành Windows với card đồ họa NVIDIA GeForce RTX 5060 Laptop GPU.

---

## Bảng công cụ sử dụng

| Nhu cầu | Công cụ thực tế | Khi nào dùng | Cách kiểm tra |
| --- | --- | --- | --- |
| **Môi trường tính toán** | Python 3.10+ & venv | Quản lý dependencies độc lập | `.venv\Scripts\activate` |
| **Deep Learning Framework** | PyTorch 2.9.1 (CUDA 12.8) | Tính toán tensor, chạy GPU & CPU | `torch.cuda.is_available() == True` |
| **Mô hình tiền huấn luyện** | Hugging Face `transformers` | Tải trọng số chuẩn của GPT-2 | `GPT2Model.from_pretrained("gpt2")` |
| **Trực quan hóa dữ liệu** | `matplotlib` | Vẽ heatmap và đồ thị benchmark | Xuất file PNG kiểm tra độ phân giải |
| **Môi trường chạy Notebook** | VS Code (Jupyter Extension) | Soạn thảo, chạy tương tác demo | Mở và chọn kernel `.venv` |
| **Kiểm thử tự động** | `nbconvert` CLI | Chạy toàn bộ notebook từ đầu | `python -m jupyter nbconvert --to notebook --execute --inplace self_attention_demo.ipynb` |
| **Quản lý phiên bản** | Git | Commit sau mỗi task, push lên GitHub | `git status`, `git log` |

---

## Lệnh chuẩn bị và chạy (Windows PowerShell)

| Mục đích | Lệnh thực thi | Thư mục chạy | Điều kiện tiên quyết |
| --- | --- | --- | --- |
| **Kiểm tra Driver & GPU** | `nvidia-smi` | Bất kỳ | Driver NVIDIA hỗ trợ CUDA 12.8+ |
| **Tạo môi trường ảo** | `python -m venv .venv` | Thư mục gốc repo | Đã cài Python 3.10+ |
| **Kích hoạt venv (PowerShell)** | `.\.venv\Scripts\Activate.ps1` | Thư mục gốc repo | Quyền thực thi PowerShell mở |
| **Cài đặt PyTorch CUDA** | `pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cu128` | Trong venv | Kết nối internet |
| **Cài đặt thư viện phụ trợ** | `pip install -r requirements.txt` | Trong venv | Sau khi cài xong PyTorch |
| **Kiểm tra PyTorch CUDA** | `python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"` | Trong venv | Phải in ra `True` và `GeForce RTX 5060 Laptop GPU` |
| **Chạy toàn bộ Notebook** | `jupyter nbconvert --to notebook --execute --inplace self_attention_demo.ipynb` | Thư mục gốc repo | Kernel Jupyter sẵn sàng |
| **Chạy kiểm thử Offline** | `$env:HF_HUB_OFFLINE="1"; jupyter nbconvert --to notebook --execute --inplace self_attention_demo.ipynb` | Thư mục gốc repo | GPT-2 đã nằm trong local cache |
| **Lưu phiên bản Git** | `git add workflow/` rồi review staged diff, commit và push đúng nhánh bàn giao | Thư mục gốc repo | Sau khi kiểm tra notebook sạch lỗi |

---

## Lưu ý kỹ thuật quan trọng
1. **Lỗi thường gặp trên Windows**: Lệnh `pip install torch` mặc định sẽ cài bản CPU. Bắt buộc phải dùng tham số `--index-url https://download.pytorch.org/whl/cu128`.
2. **Đồng bộ GPU khi đo đạc**: Vì CUDA thực thi bất đồng bộ, trong các phép đo thời gian bắt buộc phải gọi `torch.cuda.synchronize()` trước và sau khi bấm giờ.
3. **Quản lý bộ nhớ GPU**: Gọi `torch.cuda.reset_peak_memory_stats()` trước mỗi vòng lặp benchmark và bắt lỗi `torch.OutOfMemoryError` nếu chuỗi quá dài.

## Môi trường quan sát ngày 14/11/2026

| Thành phần | Giá trị thực tế |
| --- | --- |
| Python | 3.12.10 trong `.venv` |
| GPU | NVIDIA GeForce RTX 5060 Laptop GPU |
| NVIDIA driver | 582.05 (`nvidia-smi` báo khả năng CUDA tối đa 13.0) |
| PyTorch / CUDA runtime | 2.9.1+cu128 / 12.8 |
| CPU | AMD64 Family 25 Model 97 Stepping 2, AuthenticAMD |
| transformers | 5.22.2 |
| matplotlib | 3.11.2 |
| ipykernel | 7.4.0 |
| nbconvert | 7.17.2 |

Không đồng nhất số CUDA tối đa của driver với CUDA runtime của wheel PyTorch. Lần này dùng môi trường có sẵn, không cài lại thư viện.

## Chạy kiểm chứng mà không ghi đè sản phẩm

Thực hiện từ thư mục gốc repo. Lệnh dưới đây khớp cách chạy đã dùng cho hồ sơ offline; output và PNG mới nằm trong `scratch/wf-offline/`.

```powershell
$env:PYTHONUTF8 = "1"
$env:HF_HUB_OFFLINE = "1"
New-Item -ItemType Directory -Force scratch/wf-offline | Out-Null
Copy-Item -LiteralPath self_attention_demo.ipynb -Destination scratch/wf-offline/self_attention_demo.ipynb
.\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace scratch/wf-offline/self_attention_demo.ipynb
```

`PYTHONUTF8=1` giúp CLI in đường dẫn và chữ tiếng Việt trong PowerShell. Kernel notebook phải trỏ đến `.venv`; kiểm tra bằng `python -m jupyter kernelspec list`.

Kiểm tra CPU dùng bản sao riêng `scratch/wf-cpu/self_attention_demo.ipynb`, thêm ô đầu `import torch; torch.cuda.is_available = lambda: False` rồi chạy cùng lệnh nbconvert. Chỉ sửa bản sao thử nghiệm; không chép bản CPU trở lại notebook nộp bài. Xem [log CPU](../evidence/2026-11-14-cpu.log).

Các lệnh cài đặt trong bảng là hướng dẫn, không phải bằng chứng chúng được thực thi trong phiên này. Log thực tế ở [06_VERIFICATION](06_VERIFICATION.md).
