# Demo self-attention bằng PyTorch

Dùng **trọng số đã huấn luyện của GPT-2**, tự viết phép attention và kiểm chứng với mô hình gốc. Câu mẫu: `The animal didn't cross the street because it was too tired`.

## Trình bày ngắn trên lớp

Mở [self_attention_demo.ipynb](self_attention_demo.ipynb), chạy mục **1–4**:

1. **Implementation:** Q, K, V → QKᵀ/√64 → causal mask → softmax → nhân V.
2. **Kiểm chứng:** sai số attention ở cả 12 lớp phải <`1e-4`.
3. **Heatmap:** cùng Q/K trước/sau mask; sau mask không nhìn token tương lai. Đầu được chọn công khai bằng quét 144 đầu, không đại diện toàn bộ GPT-2.
4. **So sánh Transformer/CNN/RNN:** bảng lý thuyết ngắn, ưu điểm và hạn chế.

Phép đo GPU/CPU và các assert bổ sung nằm ở **phụ lục**, có thể thu gọn khi trình bày. Đây là benchmark hàm attention trên tensor ngẫu nhiên, không phải huấn luyện hay đo toàn bộ ba mô hình.

## Cài và chạy trong VS Code

Cần Python 3.12, extension Python và Jupyter. Máy đã được người dùng duyệt: **NVIDIA GeForce RTX 5060 Laptop GPU**, driver 582.05, PyTorch 2.9.1+cu128. Máy không có GPU vẫn chạy CPU.

Từ thư mục gốc, PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cu128
python -m pip install -r requirements.txt
python -m ipykernel install --user --name self-attention-env --display-name "Python (.venv)"
```

Chọn kernel `.venv` → **Restart** → **Run All**. Lần đầu cần mạng tải GPT-2; chạy trước buổi demo để model nằm trong cache. Không cài thư viện bên trong notebook.

Kiểm tra offline với kernel mới:

```powershell
$env:PYTHONUTF8 = "1"
$env:HF_HUB_OFFLINE = "1"
.\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace self_attention_demo.ipynb
```

## Output của lượt chạy

| File | Nội dung |
| --- | --- |
| `figures/heatmap_compare.png` | Hai heatmap trước/sau cùng thang màu 0–1 |
| `figures/heatmap_no_mask.png`, `figures/heatmap_causal_mask.png` | Hai panel riêng để dùng khi trình bày |
| `figures/cost_gpu_cpu.png` | Thời gian và bộ nhớ, dữ liệu ngẫu nhiên, trục log |
| `figures/demo_results.json` | Máy, phương pháp, sai số, head và số đo chính xác của lượt vừa chạy |

Nhận xét trong notebook tính trực tiếp từ kết quả, không chép các con số tĩnh. Bộ nhớ dùng MiB: CPU là một ma trận attention thật; GPU là đỉnh tensor PyTorch gồm cả mô hình. Hai đường không có cùng phạm vi đo. Mốc 2048 là độ dài tensor nhân tạo, không phải context GPT-2 2048.

PDF và các ảnh `_dark`/ảnh slide cũ thuộc lượt trước, không tự cập nhật theo Run All; dùng các PNG gốc và JSON mới nếu cần số liệu hiện tại.

## Hồ sơ và kiểm tra

[workflow/README.md](workflow/README.md) là mục lục 14 bước; [Implementation](workflow/05-generate/IMPLEMENTATION.md), [bảng so sánh](workflow/02-design/COMPARISON.md), [kết quả kiểm chứng](workflow/08-test/TEST_RESULTS.md).

```powershell
.\.venv\Scripts\python.exe workflow/test_check.py
.\.venv\Scripts\python.exe workflow/check.py
```

Manifest là ảnh chụp của lượt đã nghiệm thu. Chạy lại notebook sẽ đổi timing/output; cần đối chiếu và cập nhật hồ sơ/hash theo CONTROL trước khi nhận checker đạt cho lượt mới. Không tự đặt số bằng kết quả cũ.
