# Khảo sát và thiết kế

## Khảo sát dự án hiện có
- **Mô hình mục tiêu**: GPT-2 (`gpt2`, 124M tham số, 12 layers, 12 heads, $d_{model}=768$, $d_{head}=64$).
- **Điểm trích xuất trọng số**:
  - Trọng số chiếu $Q, K, V$: `model.h[layer].attn.c_attn.weight` shape $(768, 2304)$, `bias` shape $(2304,)$.
  - Trọng số và cơ chế chuẩn hóa LayerNorm: `model.h[layer].ln_1`.
- **Cấu hình mô hình chuẩn làm đối chứng**:
  - `GPT2Model.from_pretrained("gpt2", attn_implementation="eager")`.
  - Chạy `model(input_ids, output_attentions=True, output_hidden_states=True)`.
  - Không thêm token BOS đặc biệt để danh sách token khớp nguyên bản câu ví dụ.

## Thiết kế chi tiết hàm Self-Attention tự viết

### Công thức toán học
$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{Q K^T}{\sqrt{d_k}} + M\right) V$$

Trong đó:
- $M_{i,j} = 0$ nếu $j \le i$
- $M_{i,j} = -\infty$ nếu $j > i$ (khi `causal=True`)

### Sơ đồ luồng tính toán
```mermaid
flowchart TD
    X["Hidden State (T, 768)"] --> LN["LayerNorm (ln_1)"]
    LN --> QKV_Proj["Linear Projection (c_attn): X @ W_qkv + b_qkv"]
    QKV_Proj --> Split["Tách thành Q, K, V (mỗi ma trận T, 768)"]
    Split --> Reshape["Chia 12 heads: (12, T, 64)"]
    Reshape --> Matmul["Nhân Q @ K^T / sqrt(64) -> Scores (12, T, T)"]
    Matmul --> MaskCheck{"causal=True?"}
    MaskCheck -->|Có| ApplyMask["masked_fill(triu(1) == 1, -inf)"]
    MaskCheck -->|Không| Softmax["Softmax theo dim=-1 -> Attn (12, T, T)"]
    ApplyMask --> Softmax
    Softmax --> OutVal["Attn @ V -> (12, T, 64)"]
    OutVal --> Concat["Nối 12 heads -> Out (T, 768)"]
```

## Quyết định thiết kế (Design Decisions)

| Mã | Quyết định | Vì sao | Đánh đổi / Lựa chọn thay thế | Trạng thái |
| --- | --- | --- | --- | --- |
| **DEC-001** | Nạp trọng số đã huấn luyện của GPT-2 | Nhóm chọn trọng số đã huấn luyện để minh họa cấu trúc attention; giảng viên yêu cầu nêu rõ nguồn trọng số, không bắt buộc GPT-2. | Tốn ~500MB tải mô hình từ HF (khắc phục bằng offline cache). | Đã chốt |
| **DEC-002** | Toàn bộ code nằm trong 1 file notebook `self_attention_demo.ipynb` | Người thuyết trình dễ dàng trình diễn từng bước trong VS Code; người chấm xem được liền mạch. | Khó viết pytest truyền thống (khắc phục bằng các ô `assert` và `nbconvert`). | Đã chốt |
| **DEC-003** | Tự code từng phép toán, cấm dùng `scaled_dot_product_attention` | Mục tiêu cốt lõi của môn học là hiểu sâu cơ chế toán học bên dưới. | Chưa benchmark với kernel tối ưu; demo tập trung vào từng phép tính. | Đã chốt |
| **DEC-004** | Tự động quét chọn layer/head có liên kết "it" $\rightarrow$ "animal" mạnh nhất | Công khai tiêu chí chọn và top 3; kết quả là đầu được chọn theo liên kết mục tiêu, không đại diện cho mọi đầu. | Thêm ô code quét 144 heads; chưa đo riêng thời gian của ô này. | Đã chốt |
| **DEC-005** | Bắt lỗi OOM trong benchmark và tiếp tục chạy | Giữ notebook không bị crash giữa chừng khi đo chuỗi độ dài lớn. | Cần xử lý hiển thị giá trị `None` trên đồ thị và bảng biểu. | Đã chốt |

## Điểm cần kiểm tra trước khi hoàn thiện
- [x] Thiết kế bao gồm ba phần trọng tâm: code attention, hai heatmap, ưu điểm và hạn chế.
- [ ] Bao phủ OOM ở mọi điểm cấp phát; hiện còn REVIEW-006.
- [x] Sai số tuyệt đối với mô hình gốc được khống chế dưới $10^{-4}$.
- [x] Các hình ảnh được xuất ra file PNG độ phân giải cao phục vụ thuyết trình.

## Thiết kế và triển khai thực tế

| Interface | Thực tế trong notebook |
| --- | --- |
| `get_layer_input(model, input_ids, layer)` | Hidden state sau `ln_1`, dạng `(T, 768)` |
| `get_qkv_weights(model, layer)` | Lấy trọng số và bias `c_attn` của GPT-2 đã huấn luyện |
| `self_attention(x, w_qkv, b_qkv, n_head=12, causal=True)` | Trả đầu ra ghép các đầu trước `c_proj`, và ma trận `(12, T, T)` |
| `find_token(token_list, word)` | Trả chỉ số hoặc báo `ValueError` bằng tiếng Việt |
| `pick_head(src_word="it", tgt_word="animal")` | Nhận từ thay vì chỉ số; trả `(best, top3)`, mỗi phần tử `(layer, head, value)` |
| Ô vẽ heatmap | Code trực tiếp; chưa có hàm `plot_attention` như kế hoạch ban đầu |
| `benchmark(lengths, device, n_rep=20)` | CPU được gọi với 10 lần lặp, GPU 20 lần; trả danh sách `len`, `ms`, `mem_mb` |

**DEC-006 — Môi trường được duyệt lại:** ngày 14/11/2026, người dùng chọn “Dùng RTX 5060 Laptop hiện tại và cập nhật thiết kế”. Hồ sơ workflow ghi nhận RTX 5060 Laptop GPU và CUDA runtime 12.8. Đặc tả/AGENTS ngoài `workflow/` chưa được sửa theo yêu cầu giới hạn phạm vi mới nhất.

**DEC-007 — Phạm vi lần hoàn thiện:** chỉ đồng bộ tài liệu workflow và lưu bằng chứng kiểm tra. Giữ nguyên API/code/ảnh hiện có, ghi rõ khác biệt với kế hoạch thay vì tự refactor để khớp tên hàm. Sai lệch về đo bộ nhớ và nhận xét được giữ trong danh sách cần xử lý ở [06_VERIFICATION](06_VERIFICATION.md).
