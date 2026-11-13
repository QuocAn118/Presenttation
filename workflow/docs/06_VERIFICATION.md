# Kiểm chứng và debug

Tài liệu này ghi nhận quy trình kiểm chứng chất lượng mã nguồn và kết quả thực nghiệm trong dự án.

---

## Danh mục các phép kiểm chứng (Verification Records)

| Mã | Hạng mục kiểm tra | Thao tác thực hiện | Kỳ vọng chuẩn | Kết quả thực tế | Trạng thái |
| --- | --- | --- | --- | --- | --- |
| **VERIFY-001** | Khả năng nhận diện GPU | Chạy script kiểm tra `torch.cuda` | Nhận diện đúng NVIDIA GeForce RTX 4080 | [Chờ chạy Task 1] | Chưa xác minh |
| **VERIFY-002** | Độ khớp số học hàm Self-Attention | So sánh ma trận attention tự tính với `GPT2Model` gốc ở 12 layer | Sai số tuyệt đối lớn nhất $< 10^{-4}$ | [Chờ chạy Task 2] | Chưa xác minh |
| **VERIFY-003** | Tính chất xác suất của Softmax | Tính tổng theo hàng của ma trận attention `attn.sum(-1)` | Mọi hàng đều xấp xỉ bằng $1.0 \pm 10^{-5}$ | [Chờ chạy Task 2] | Chưa xác minh |
| **VERIFY-004** | Tính chất chặn tương lai của Causal Mask | Kiểm tra tam giác trên `attn.triu(1)` khi `causal=True` | Giá trị lớn nhất bằng chính xác 0.0 | [Chờ chạy Task 2] | Chưa xác minh |
| **VERIFY-005** | Nhận diện token chuẩn | Tìm kiếm vị trí token `"it"` và `"animal"` | Vị trí `"animal"` phải xuất hiện trước `"it"` | [Chờ chạy Task 3] | Chưa xác minh |
| **VERIFY-006** | Tính logic của ma trận Benchmark | Kiểm tra bộ nhớ lý thuyết khi tăng độ dài chuỗi gấp đôi | Dung lượng ma trận $N \times N$ tăng xấp xỉ 4 lần | [Chờ chạy Task 4] | Chưa xác minh |
| **VERIFY-007** | Khả năng chịu lỗi thiếu GPU | Chạy thử nghiệm với cờ giả lập môi trường CPU | Báo "Không có GPU, chỉ đo CPU", không crash | [Chờ chạy Task 4] | Chưa xác minh |
| **VERIFY-008** | Khả năng thực thi không cần Internet | Đặt `$env:HF_HUB_OFFLINE="1"` và chạy lại `nbconvert` | Tải thành công từ cache, exit code 0 | [Chờ chạy Task 5] | Chưa xác minh |

---

## Tiêu chí đánh giá chất lượng mã nguồn

1. **Tính độc lập & minh bạch**:
   - Hàm `self_attention` tuyệt đối không gọi `scaled_dot_product_attention`, `nn.MultiheadAttention` hay class attention có sẵn của GPT-2.
   - Đầu vào hàm lấy trực tiếp từ hidden state sau `ln_1` của layer tương ứng.
2. **Quy chuẩn trình bày**:
   - Mọi ô code tự viết đều có chú thích từng bước bằng tiếng Việt.
   - Tiêu đề trên biểu đồ và đầu notebook ghi rõ: *"Trọng số đã huấn luyện của GPT-2"*.
   - Nhận xét kết quả bám sát số liệu thực tế đo được trên máy, tuyệt đối không bịa số liệu.

---

## Quy trình xử lý lỗi (Troubleshooting Protocol)

- **Nếu sai số giữa hàm tự viết và GPT-2 gốc $\ge 10^{-4}$**:
  - Kiểm tra thứ tự các chiều tensor khi `view` và `transpose` giữa các head.
  - Kiểm tra xem đã chia đúng hệ số $\sqrt{d_k} = \sqrt{64} = 8$ chưa.
  - Kiểm tra giá trị mask: phải là $-\infty$ (hoặc $-10^4$) trước khi đưa vào hàm `softmax`.
  - Không được nới lỏng ngưỡng sai số `1e-4`.
- **Nếu gặp lỗi Out of Memory (OOM) khi đo độ dài lớn**:
  - Gán giá trị đo tại mốc đó là `None` (hiển thị "OOM" trên bảng).
  - Gọi `torch.cuda.empty_cache()` và tiếp tục vòng lặp đo độ dài tiếp theo.
