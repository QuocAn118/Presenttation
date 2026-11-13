# Breakdown và tiến độ thực hiện (5 Tasks)

Dự án được phân rã thành 5 đầu việc tuần tự. Mỗi đầu việc hoàn thành phải vượt qua bước kiểm thử (`assert` hoặc script kiểm tra) và được commit độc lập lên Git.

---

## Danh sách đầu việc tổng quan

| Mã | Đầu việc | Yêu cầu liên quan | Phụ thuộc | Trạng thái | Bằng chứng kiểm tra |
| --- | --- | --- | --- | --- | --- |
| **TASK-001** | Thiết lập môi trường, venv CUDA 12.6 và khung repo | FR-001, AC-001 | Không | Chưa bắt đầu | `torch.cuda.is_available() == True`, in RTX 4080 |
| **TASK-002** | Xây dựng hàm Self-Attention tự viết & kiểm chứng khớp GPT-2 | FR-001, FR-002, AC-002 | TASK-001 | Chưa bắt đầu | `max_diff < 1e-4` ở cả 12 layer, `triu(1) == 0` |
| **TASK-003** | Trực quan hóa Heatmap trước/sau Causal Mask | FR-003, AC-003, AC-004 | TASK-002 | Chưa bắt đầu | 3 file ảnh trong `figures/`, `it` $\rightarrow$ `animal` |
| **TASK-004** | Benchmark thời gian & bộ nhớ trên GPU và CPU | FR-004, AC-005, AC-006 | TASK-002 | Chưa bắt đầu | Bảng số liệu f-string, đồ thị `cost_gpu_cpu.png` |
| **TASK-005** | Nhận xét chuyên sâu, hoàn thiện README & bản chạy cuối | FR-005, AC-007, AC-008 | TASK-003, TASK-004 | Chưa bắt đầu | Test `HF_HUB_OFFLINE=1` pass, notebook có output |

---

## Chi tiết từng đầu việc

### TASK-001: Môi trường và khung repo
- **Mục tiêu**: Cài đặt môi trường ảo `.venv`, PyTorch 2.9.1 hỗ trợ CUDA 12.6, tạo khung notebook và cấu trúc dự án.
- **Phạm vi thay đổi**: `requirements.txt`, `.gitignore`, `README.md`, `self_attention_demo.ipynb` (ô markdown giới thiệu, ô import cấu hình), `figures/.gitkeep`.
- **Tiêu chí đạt**: `torch.cuda.get_device_name(0)` in ra "GeForce RTX 4080", `nbconvert` chạy không lỗi.
- **Commit message**: `chore: moi truong va khung notebook`

### TASK-002: Hàm self-attention tự viết & kiểm chứng khớp GPT-2
- **Mục tiêu**: Hiện thực hóa hàm `self_attention(x, w_qkv, b_qkv, n_head=12, causal=True)` và các hàm bổ trợ trích xuất trọng số.
- **Quy trình TDD**: Viết ô `assert` so sánh với output GPT-2 trước $\rightarrow$ chạy thấy fail $\rightarrow$ viết hàm $\rightarrow$ chạy lại pass.
- **Tiêu chí đạt**: Sai số tuyệt đối lớn nhất $< 10^{-4}$ ở toàn bộ 12 layer; hàng ma trận cộng lại bằng 1.0; nửa trên đường chéo bằng 0 khi bật causal.
- **Commit message**: `feat: ham self-attention tu viet va kiem tra khop GPT-2`

### TASK-003: Heatmap trước và sau causal mask
- **Mục tiêu**: Tự động tìm head tối ưu, vẽ 2 panel heatmap trước và sau mask trên câu chuẩn `"The animal didn't cross the street because it was too tired"`.
- **Đầu ra**: 
  - `figures/heatmap_compare.png`
  - `figures/heatmap_no_mask.png`
  - `figures/heatmap_causal_mask.png`
- **Tiêu chí đạt**: 3 file ảnh chất lượng cao; ô markdown phân tích đúng thực tế hiện tượng "attention sink" và liên kết "it" $\rightarrow$ "animal".
- **Commit message**: `feat: heatmap truoc va sau causal mask`

### TASK-004: Đo thời gian và bộ nhớ trên GPU và CPU
- **Mục tiêu**: Benchmark với chuỗi độ dài $[128, 256, 512, 1024, 2048]$ trên cả GPU RTX 4080 và CPU.
- **Xử lý đặc biệt**: Sử dụng `torch.inference_mode()`, đồng bộ `cuda.synchronize()`, bắt ngoại lệ OOM an toàn, tự động ngắt nếu máy chỉ có CPU.
- **Đầu ra**: File ảnh `figures/cost_gpu_cpu.png` (2 panel thời gian và bộ nhớ dạng log-scale) và nhận xét định lượng.
- **Commit message**: `feat: do thoi gian va bo nho GPU CPU`

### TASK-005: Ưu điểm, hạn chế, README và bản chạy cuối
- **Mục tiêu**: Viết bài phân tích học thuật dựa trên dữ liệu thật, hướng dẫn chạy trong VS Code và chế độ offline.
- **Kiểm chứng**: Thiết lập `HF_HUB_OFFLINE=1` chạy lại `nbconvert` toàn bộ notebook để chứng minh khả năng chạy offline.
- **Commit message**: `docs: uu han che, README va output cuoi`
