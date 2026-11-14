# Demo self-attention bằng PyTorch

Dùng **trọng số đã huấn luyện của GPT-2**, tự viết phép attention và kiểm chứng với mô hình gốc. Câu mẫu: `The animal didn't cross the street because it was too tired`.

## Trình bày ngắn trên lớp

Mở [self_attention_demo.ipynb](self_attention_demo.ipynb), chạy lần lượt **Bước 1–6**. Mỗi bước có giải thích ngay trước ô code:

1. **Chuẩn bị:** tải GPT-2 đã huấn luyện, tách câu mẫu thành token.
2. **Implementation:** giải thích từng phép Q/K/V → chia đầu → QKᵀ/√64 → mask → softmax → nhân V và ghép đầu, kèm kích thước tensor.
3. **Kiểm chứng:** đối chiếu cả 12 lớp với GPT-2, sai số phải <`1e-4`.
4. **Chọn đầu attention:** quét 144 đầu, in top 3 theo trọng số `it` → `animal`.
5. **Vẽ và đọc heatmap:** so cùng Q/K trước/sau mask; đọc hàng `it`, cột `animal` và vùng tương lai bằng 0.
6. **So sánh Transformer/CNN/RNN:** bảng lý thuyết ngắn, ưu điểm và hạn chế.

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

Repo giữ code, tài liệu kỹ thuật và output của notebook. PDF thuyết trình, ảnh nền tối và ảnh tổng quan slide đã được bỏ theo yêu cầu; bốn PNG gốc và JSON kết quả vẫn được giữ để kiểm chứng code.

## Hồ sơ và kiểm tra

[workflow/README.md](workflow/README.md) là mục lục 14 bước; [Implementation](workflow/05-generate/IMPLEMENTATION.md), [bảng so sánh](workflow/02-design/COMPARISON.md), [kết quả kiểm chứng](workflow/08-test/TEST_RESULTS.md).

Phần [lý thuyết và danh mục nguồn](workflow/THEORY.md) có công thức attention, mask, multi-head và đối chiếu GPT-2. Nguồn chính là [Vaswani et al. (2017)](https://arxiv.org/html/1706.03762v7), [báo cáo GPT-2 của Radford et al. (2019)](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) và [checkpoint GPT-2](https://huggingface.co/openai-community/gpt2). Hình do notebook vẽ, số đo lấy từ lượt chạy thật; [AI_USAGE](workflow/13-documentation/AI_USAGE.md) ghi phần hỗ trợ AI. PDF nhóm đã xóa theo yêu cầu, chỉ còn tên/hash và đối chiếu lịch sử.

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python.exe workflow/test_check.py
.\.venv\Scripts\python.exe workflow/check.py
```

Manifest là ảnh chụp của lượt đã nghiệm thu. Chạy lại notebook sẽ đổi timing/output; cần đối chiếu và cập nhật hồ sơ/hash theo CONTROL trước khi nhận checker đạt cho lượt mới. Không tự đặt số bằng kết quả cũ.
