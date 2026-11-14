# Yêu cầu và tiêu chí nghiệm thu

## Danh sách yêu cầu chức năng (FR)

### FR-001: Hàm tính Self-Attention tự viết bằng PyTorch
- **Người sử dụng**: Giảng viên, người thuyết trình.
- **Mục đích**: Hiện thực hóa từng bước cơ chế Attention mà không gọi API có sẵn.
- **Dữ liệu đầu vào**: Hidden state $X \in \mathbb{R}^{T \times 768}$ sau LayerNorm 1 (`ln_1`), trọng số ma trận $W_{qkv}$, bias $b_{qkv}$.
- **Luồng tính toán**:
  1. Chiếu tuyến tính ra $Q, K, V$ và chia thành $n_{head}=12$ đầu, mỗi đầu $d=64$.
  2. Tính điểm tương đồng: $Scores = \frac{Q K^T}{\sqrt{d}}$.
  3. Áp dụng Causal Mask nếu `causal=True`: gán $-\infty$ vào nửa trên đường chéo (vị trí tương lai).
  4. Tính trọng số chú ý: $Attn = \text{softmax}(Scores, \text{dim}=-1)$.
  5. Nhân giá trị: $Out = Attn \cdot V$ và ghép các đầu lại thành tensor $(T, 768)$.
- **Trường hợp biên**: Đầu vào hỗ trợ tensor 2D `(T, 768)` theo thiết kế; không yêu cầu hỗ trợ batch 3D. Mask đúng vị trí tương lai.

### FR-002: Kiểm chứng độ chính xác so với GPT-2 gốc
- **Mục đích**: Đảm bảo code tự viết không lệch so với cài đặt chuẩn của Hugging Face `GPT2Model`.
- **Thao tác**: Chạy forward mô hình gốc với `output_attentions=True`, so sánh ma trận attention ở cả 12 layer.
- **Tiêu chí**: Sai số tuyệt đối lớn nhất $|Attn_{ours} - Attn_{gpt2}| < 10^{-4}$ ở mọi layer.
- **Kiểm tra tính chất toán học**: Tổng mỗi hàng ma trận attention phải bằng $1.0 \pm 10^{-5}$; sau causal mask nửa trên đường chéo tuyệt đối bằng 0.

### FR-003: Trực quan hóa Heatmap trước và sau Causal Mask
- **Dữ liệu**: Câu ví dụ `"The animal didn't cross the street because it was too tired"`.
- **Thao tác**: Quét tìm layer và head có trọng số attention từ `"it"` tới `"animal"` cao nhất khi có mask; vẽ 2 panel heatmap trước và sau mask cạnh nhau, chung colormap.
- **Tiêu đề hình**: Ghi rõ *"Trọng số đã huấn luyện của GPT-2 - Layer L, Head H"*.
- **Xuất file**: Lưu vào `figures/heatmap_compare.png`, `figures/heatmap_no_mask.png`, `figures/heatmap_causal_mask.png` (dpi 200).

### FR-004: Benchmark thời gian và bộ nhớ trên GPU và CPU
- **Dữ liệu**: Đầu vào ngẫu nhiên, độ dài chuỗi $N \in [128, 256, 512, 1024, 2048]$.
- **Môi trường**: Đo trên GPU NVIDIA RTX 5060 Laptop GPU và CPU (`torch.inference_mode()`).
- **Độ trễ**: Đo thời gian trung vị qua 10 lần trên CPU, 20 lần trên GPU (sau warm-up 3 lần), đồng bộ CUDA bằng `torch.cuda.synchronize()`.
- **Bộ nhớ**: 
  - GPU: Đo `torch.cuda.max_memory_allocated()`.
  - CPU: Code hiện tại cấp phát tensor `dummy_scores` cùng kích thước ma trận điểm rồi tính dung lượng $12 \times N \times N \times 4$ bytes; không đo bộ nhớ đỉnh tiến trình.
- **Khả năng chịu lỗi**: Bắt lỗi `torch.OutOfMemoryError` nếu có, đánh dấu "OOM" và tiếp tục chạy các độ dài khác, không làm dừng chương trình.
- **Xuất file**: Lưu biểu đồ 2 panel vào `figures/cost_gpu_cpu.png`.

### FR-005: Báo cáo nhận xét và hướng dẫn chạy
- **Nội dung**: Phân tích chi tiết ưu điểm (tính toán song song, mô hình hóa liên kết xa) và hạn chế (chi phí $O(n^2)$, không có thứ tự từ nội tại, attention sink).
- **Hướng dẫn chạy**: Hướng dẫn cài đặt cụ thể trong VS Code, cài PyTorch CUDA 12.8, cấu hình chạy offline `HF_HUB_OFFLINE=1`.

---

## Tiêu chí nghiệm thu (Acceptance Criteria)

| Mã | Điều kiện ban đầu | Thao tác | Kết quả mong đợi |
| --- | --- | --- | --- |
| **AC-001** | Cài đặt PyTorch cu128 trên máy RTX 5060 Laptop GPU | Chạy `python -c "import torch; print(torch.cuda.is_available())"` | Trả về `True` và nhận diện đúng RTX 5060 Laptop GPU |
| **AC-002** | Mô hình GPT-2 được tải về | Chạy forward và so sánh ma trận attention | `assert max_diff < 1e-4` pass ở cả 12 layer |
| **AC-003** | Token hóa câu chuẩn | Chạy hàm tìm token | `find_token(tokens, "it")` và `find_token(tokens, "animal")` xác định đúng vị trí |
| **AC-004** | Sinh heatmap | Chạy ô vẽ heatmap (hiện code viết trực tiếp, chưa tách `plot_attention`) | Xuất đủ 3 file PNG vào `figures/`, nửa trên đường chéo sau mask bằng 0 |
| **AC-005** | Chạy benchmark độ dài | Chạy hàm `benchmark` | Xuất bảng f-string và đồ thị `figures/cost_gpu_cpu.png`, log y scale |
| **AC-006** | Môi trường không có GPU | Chạy thử nghiệm trên CPU | In thông báo "Không có GPU, chỉ đo CPU", không phát sinh ngoại lệ |
| **AC-007** | Môi trường mất mạng | Bật `HF_HUB_OFFLINE=1` và chạy lại | Notebook load GPT-2 từ local cache trơn tru |
| **AC-008** | Chạy toàn bộ notebook | `python -m jupyter nbconvert --to notebook --execute --inplace self_attention_demo.ipynb` | Toàn bộ các ô chạy thành công với exit code 0 |

---

## Theo dõi liên kết (Traceability Matrix)

| Yêu cầu | Thiết kế liên quan | Đầu việc | Tiêu chí kiểm chứng |
| --- | --- | --- | --- |
| FR-001 | 03_DESIGN: Cấu trúc Self-Attention | TASK-002 | AC-002 |
| FR-002 | 03_DESIGN: Kiểm chứng khớp GPT-2 | TASK-002 | AC-002, AC-008 |
| FR-003 | 03_DESIGN: Thiết kế Heatmap | TASK-003 | AC-003, AC-004 |
| FR-004 | 03_DESIGN: Phương pháp Benchmark | TASK-004 | AC-005, AC-006 |
| FR-005 | 03_DESIGN: Đánh giá & Hướng dẫn | TASK-005 | AC-007, AC-008 |

## Đối chiếu yêu cầu và bằng chứng

Trạng thái từng AC được ghi ở [06_VERIFICATION](06_VERIFICATION.md); không đánh đồng có file hay commit với đã nghiệm thu.

- **AC-001:** môi trường mới được người dùng duyệt; GPU thật là RTX 5060 Laptop GPU, không phải RTX 4080.
- **AC-002–005:** đạt kiểm tra runtime trên bản sao nguyên trạng notebook. Hai phép kiểm tra tổng hàng và tam giác trên trong ô đối chiếu GPT-2 áp dụng lên lớp cuối; ô heatmap kiểm tra thêm lớp đã chọn.
- **AC-006:** đạt khi ép `torch.cuda.is_available()` trả `False` trong kernel thử nghiệm riêng; chưa thử trên máy vật lý không có GPU.
- **AC-007–008:** bản sao notebook gốc chạy offline từ kernel mới, exit code 0. Bản gốc trong repo và hình gốc không bị ghi đè trong lần hoàn thiện workflow.
- Yêu cầu về nội dung nhận xét còn lỗi đồng bộ số liệu; vì vậy FR-005 chỉ đạt một phần. Chi tiết ở REVIEW-001–003, không đánh dấu toàn bộ sản phẩm hoàn thành.
