# Môi trường đã xác minh

**Mã hồ sơ: ENVIRONMENT. Cập nhật: 14/11/2026.**

## Cấu hình thực tế

| Thành phần | Giá trị quan sát |
| --- | --- |
| Hệ điều hành | Windows |
| Python | 3.12.10, môi trường `.venv` |
| GPU | NVIDIA GeForce RTX 5060 Laptop GPU |
| NVIDIA driver | 582.05; `nvidia-smi` báo hỗ trợ CUDA tối đa 13.0 |
| PyTorch | 2.9.1+cu128; `torch.version.cuda=12.8` |
| CPU | AMD64 Family 25 Model 97 Stepping 2, AuthenticAMD |
| transformers | 5.22.2 |
| matplotlib | 3.11.2 |
| ipykernel | 7.4.0 |
| nbconvert | 7.17.2 |
| GPT-2 | 12 lớp, 12 đầu, embedding 768, `gelu_new`, không cross-attention, `n_positions=1024` |

Tên CPU ở đây là chuỗi `platform.processor()`, không tự suy ra tên thương mại chưa xác nhận. Phân biệt mức CUDA tối đa của driver với runtime 12.8 trong wheel PyTorch. Cấu hình và code GPT-2 được đọc cục bộ; phiên này không cài lại mô hình/thư viện.

## Lệnh chuẩn bị khi cần tạo lại môi trường

Chạy từ gốc repo, PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cu128
python -m pip install -r requirements.txt
python -m ipykernel install --user --name self-attention-env --display-name "Python (.venv)"
```

Đây là hướng dẫn tái tạo, không phải báo cáo đã chạy lại cài đặt trong phiên. Dùng index CUDA cụ thể theo cấu hình đã duyệt; không đặt lệnh cài đặt vào notebook. Lần tải `gpt2` đầu tiên cần mạng; các lần kiểm tra offline dùng cache hiện có.

## Kiểm tra đúng môi trường trước demo

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python.exe -c "import torch; print(torch.__version__, torch.version.cuda, torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
.\.venv\Scripts\python.exe -m jupyter kernelspec list
```

Chọn kernel trỏ về Python `.venv` trong VS Code. Nếu CUDA không khả dụng, notebook có nhánh CPU; không gọi `get_device_name(0)` vô điều kiện trong kiểm tra thiếu GPU.

## Quyết định phần cứng và nguồn số liệu

Người dùng đã chọn RTX 5060 Laptop/cu128 ngày 14/11/2026. Spec/AGENTS bên ngoài workflow còn RTX 4080/cu126; không lấy các dòng cũ đó làm mô tả lần chạy hiện tại. Quyết định và khác biệt nằm tại DEC-006 trong [DESIGN](../02-design/DESIGN.md) và REVIEW-005 trong [REVIEW](../06-review/REVIEW.md).

Kết quả phép đo được giữ trong log, không dự đoán từ thông số GPU. PDF trang 19 chỉ trình bày lượt thử nghiệm của slide; thời gian chạy mới không bắt buộc trùng slide.
