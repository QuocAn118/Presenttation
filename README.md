# Demo Self-Attention và Causal Mask với GPT-2

Dự án bài tập môn Deep Learning: Hiện thực hóa cơ chế Self-Attention và Causal Mask từ đầu bằng PyTorch, nạp **trọng số đã huấn luyện của GPT-2** (`gpt2`, 124M tham số), trực quan hóa attention heatmap và đo lường chi phí tính toán thực tế trên GPU và CPU.

> **Tiêu chí cốt lõi**: Toàn bộ notebook sử dụng **trọng số đã huấn luyện của GPT-2**, không phải trọng số ngẫu nhiên. Hàm `self_attention` được tự code từng bước ma trận ($Q, K, V$, scaling, masking, softmax), không sử dụng hàm thư viện dựng sẵn như `scaled_dot_product_attention` hay `nn.MultiheadAttention`.

---

## 1. Cấu trúc Dự án

```text
├── self_attention_demo.ipynb    # Notebook duy nhất chứa toàn bộ code demo và output
├── requirements.txt            # Phiên bản các thư viện phụ trợ
├── README.md                   # Hướng dẫn cài đặt, chạy và cấu hình
├── figures/                    # Các hình ảnh độ phân giải cao xuất ra phục vụ slide
│   ├── heatmap_compare.png     # So sánh 2 heatmap trước và sau Causal Mask cạnh nhau
│   ├── heatmap_no_mask.png     # Heatmap trước Causal Mask (thử nghiệm minh họa)
│   ├── heatmap_causal_mask.png # Heatmap sau Causal Mask (chặn tương lai)
│   └── cost_gpu_cpu.png        # Biểu đồ đo thời gian (ms) và bộ nhớ (MB) GPU vs CPU
├── workflow/                   # Bộ tài liệu quy trình Vibe Coding chuẩn mực
│   ├── docs/                   # 00_MINDMAP đến 08_RELEASE (5W1H, Spec, Verification)
│   └── 01-define/ ...          # Hướng dẫn chi tiết từng bước phát triển sản phẩm với AI
└── docs/superpowers/           # Đặc tả thiết kế và kế hoạch 5 task ban đầu
```

---

## 2. Hướng dẫn Cài đặt Môi trường trong VS Code

### Điều kiện tiên quyết:
- Đã cài đặt **VS Code** và hai extension: **Python** và **Jupyter**.
- Đã cài đặt Python 3.10+ (khuyên dùng Python 3.12).
- Máy có card đồ họa NVIDIA (khuyên dùng RTX 4080 / RTX Series có hỗ trợ CUDA 12.6+).

### Các bước cài đặt chi tiết (Windows PowerShell):

1. **Mở thư mục dự án trong VS Code**:
   ```powershell
   cd "c:\Users\Legion\Desktop\TÀI LIỆU HỌC\Presenttation"
   ```

2. **Tạo môi trường ảo (.venv)**:
   ```powershell
   python -m venv .venv
   ```

3. **Kích hoạt môi trường ảo**:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

4. **Cài đặt PyTorch bản CUDA**:
   > **LƯU Ý QUAN TRỌNG**: Nếu chỉ gõ `pip install torch`, pip trên Windows sẽ mặc định tải bản CPU. Bắt buộc phải cài bằng lệnh có `--index-url` dưới đây:
   ```powershell
   pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cu128
   ```
   *(Hoặc `--index-url https://download.pytorch.org/whl/cu126` tùy phiên bản driver)*.

5. **Cài đặt các thư viện còn lại**:
   ```powershell
   pip install -r requirements.txt
   ```

6. **Đăng ký kernel cho Jupyter Notebook**:
   ```powershell
   python -m ipykernel install --user --name self-attention-env --display-name "Python (.venv)"
   ```

---

## 3. Hướng dẫn Chạy Notebook

1. Trong VS Code, mở file `self_attention_demo.ipynb`.
2. Ở góc trên cùng bên phải của notebook, bấm vào **Select Kernel** $\rightarrow$ chọn **Python (.venv)** (hoặc `self-attention-env`).
3. Bấm **Clear All Outputs** rồi bấm **Run All** (hoặc **Restart & Run All**) để chạy toàn bộ notebook từ đầu.
4. **Chuẩn bị trước buổi thuyết trình (Chạy Offline)**:
   - Lần đầu chạy cần có mạng để tải mô hình GPT-2 (~500MB) từ Hugging Face về cache máy.
   - **Chạy notebook một lần trước ngày 14/11** để toàn bộ mô hình và tokenizer được lưu sẵn trong local cache.
   - Khi lên lớp thuyết trình (phòng học không có internet), mở PowerShell và đặt biến môi trường offline trước khi khởi động VS Code:
     ```powershell
     $env:HF_HUB_OFFLINE="1"
     code .
     ```
     Notebook sẽ tự động đọc trực tiếp từ cache mà không cần kết nối mạng.

---

## 4. Danh mục Hình ảnh trong `figures/` dùng làm Slide

| Tên File | Nội dung chi tiết | Dùng cho Slide |
|---|---|---|
| `heatmap_compare.png` | Hình so sánh 2 panel cạnh nhau trước và sau Causal Mask (Lớp 4, Đầu 3), chung thang màu 0-1 | **Slide Demo**: Trực quan hóa vai trò của Causal Mask và chứng minh liên kết `"it"` $\rightarrow$ `"animal"` |
| `heatmap_causal_mask.png` | Panel riêng biệt sau Causal Mask (nửa trên bằng 0, attention sink `"The"`, liên kết `"it"` $\rightarrow$ `"animal"` = 84.61%) | **Slide Cơ chế Causal Mask** |
| `heatmap_no_mask.png` | Panel trước Causal Mask (thử nghiệm minh họa token nhìn cả tương lai) | **Slide So sánh Encoder vs Decoder** |
| `cost_gpu_cpu.png` | Biểu đồ 2 panel đo độ trễ (ms) và bộ nhớ (MB) log-scale theo độ dài chuỗi $128 \rightarrow 2048$ trên GPU và CPU | **Slide Hiệu năng & Chi phí**: Chứng minh độ phức tạp $O(n^2)$ và ưu thế của GPU |

---

## 5. Cấu hình Phần cứng Đã Chạy và Lưu Output Sẵn

File `self_attention_demo.ipynb` được cam kết kèm toàn bộ output và hình ảnh thực tế từ lượt chạy trên cấu hình:
- **Hệ điều hành**: Windows 11 (64-bit)
- **GPU**: NVIDIA GeForce RTX Laptop GPU (CUDA 12.8 / Driver 582.05)
- **CPU**: AMD64 Family 25 Model 97 Stepping 2, AuthenticAMD
- **Phiên bản PyTorch**: `2.9.1+cu128` (CUDA khả dụng: `True`)
- **Phiên bản Transformers**: `5.22.2`
- **Mô hình tiền huấn luyện**: `gpt2` (124M tham số, 12 layers, 12 heads, $d=64$)
