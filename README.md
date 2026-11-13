# Demo Self-Attention và Causal Mask với GPT-2

Dự án môn học Deep Learning: Thực nghiệm cơ chế Self-Attention và Causal Mask bằng PyTorch từ đầu, sử dụng **trọng số đã huấn luyện của GPT-2** (`gpt2`, 124M tham số).

## Mục tiêu chính
1. **Hàm Self-Attention tự viết**: Tự tính toán từng bước $Q, K, V$, ma trận điểm tương đồng, causal mask, softmax và nhân $V$ (không dùng hàm dựng sẵn).
2. **Kiểm chứng độ chính xác**: So sánh sai số ma trận attention với mô hình `GPT2Model` gốc của Hugging Face ($< 10^{-4}$).
3. **Trực quan hóa Heatmap**: So sánh 2 heatmap trước và sau causal mask trên câu chuẩn `"The animal didn't cross the street because it was too tired"`.
4. **Benchmark GPU vs CPU**: Đo thời gian (ms) và bộ nhớ (MB) trên GPU và CPU theo độ dài chuỗi ($128 \rightarrow 2048$).
5. **Đánh giá ưu nhược điểm**: Nhận xét định lượng về tính chất $O(n^2)$, attention sink, và khả năng mô hình hóa ngữ cảnh.

## Cài đặt môi trường
Xem chi tiết trong [workflow/docs/05_TOOLS.md](workflow/docs/05_TOOLS.md).

```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt venv (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Cài đặt PyTorch hỗ trợ CUDA
pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cu128

# Cài đặt các thư viện phụ trợ
pip install -r requirements.txt
```
