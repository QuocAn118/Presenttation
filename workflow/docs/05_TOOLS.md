# Công cụ và môi trường

Tài liệu này ghi nhận các công cụ và câu lệnh thực tế được áp dụng trong dự án trên hệ điều hành Windows với card đồ họa NVIDIA GeForce RTX 4080.

---

## Bảng công cụ sử dụng

| Nhu cầu | Công cụ thực tế | Khi nào dùng | Cách kiểm tra |
| --- | --- | --- | --- |
| **Môi trường tính toán** | Python 3.10+ & venv | Quản lý dependencies độc lập | `.venv\Scripts\activate` |
| **Deep Learning Framework** | PyTorch 2.9.1 (CUDA 12.6) | Tính toán tensor, chạy GPU & CPU | `torch.cuda.is_available() == True` |
| **Mô hình tiền huấn luyện** | Hugging Face `transformers` | Tải trọng số chuẩn của GPT-2 | `GPT2Model.from_pretrained("gpt2")` |
| **Trực quan hóa dữ liệu** | `matplotlib` | Vẽ heatmap và đồ thị benchmark | Xuất file PNG kiểm tra độ phân giải |
| **Môi trường chạy Notebook** | VS Code (Jupyter Extension) | Soạn thảo, chạy tương tác demo | Mở và chọn kernel `.venv` |
| **Kiểm thử tự động** | `nbconvert` CLI | Chạy toàn bộ notebook từ đầu | `jupyter nbconvert --execute --inplace` |
| **Quản lý phiên bản** | Git | Commit sau mỗi task, push lên GitHub | `git status`, `git log` |

---

## Bảng lệnh thực tế (Windows PowerShell)

| Mục đích | Lệnh thực thi | Thư mục chạy | Điều kiện tiên quyết |
| --- | --- | --- | --- |
| **Kiểm tra Driver & GPU** | `nvidia-smi` | Bất kỳ | Driver NVIDIA hỗ trợ CUDA 12.6+ |
| **Tạo môi trường ảo** | `python -m venv .venv` | Thư mục gốc repo | Đã cài Python 3.10+ |
| **Kích hoạt venv (PowerShell)** | `.\.venv\Scripts\Activate.ps1` | Thư mục gốc repo | Quyền thực thi PowerShell mở |
| **Cài đặt PyTorch CUDA** | `pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cu126` | Trong venv | Kết nối internet |
| **Cài đặt thư viện phụ trợ** | `pip install transformers matplotlib ipykernel nbconvert` | Trong venv | Sau khi cài xong PyTorch |
| **Kiểm tra PyTorch CUDA** | `python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"` | Trong venv | Phải in ra `True` và `GeForce RTX 4080` |
| **Chạy toàn bộ Notebook** | `jupyter nbconvert --to notebook --execute --inplace self_attention_demo.ipynb` | Thư mục gốc repo | Kernel Jupyter sẵn sàng |
| **Chạy kiểm thử Offline** | `$env:HF_HUB_OFFLINE="1"; jupyter nbconvert --to notebook --execute --inplace self_attention_demo.ipynb` | Thư mục gốc repo | GPT-2 đã nằm trong local cache |
| **Lưu phiên bản Git** | `git add . ; git commit -m "feat/chore: ..."; git push origin main` | Thư mục gốc repo | Sau khi kiểm tra notebook sạch lỗi |

---

## Lưu ý kỹ thuật quan trọng
1. **Lỗi thường gặp trên Windows**: Lệnh `pip install torch` mặc định sẽ cài bản CPU. Bắt buộc phải dùng tham số `--index-url https://download.pytorch.org/whl/cu126`.
2. **Đồng bộ GPU khi đo đạc**: Vì CUDA thực thi bất đồng bộ, trong các phép đo thời gian bắt buộc phải gọi `torch.cuda.synchronize()` trước và sau khi bấm giờ.
3. **Quản lý bộ nhớ GPU**: Gọi `torch.cuda.reset_peak_memory_stats()` trước mỗi vòng lặp benchmark và bắt lỗi `torch.OutOfMemoryError` nếu chuỗi quá dài.
