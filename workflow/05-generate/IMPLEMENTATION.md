# 05 - Triển khai thực tế của demo

**Mã hồ sơ: IMPLEMENTATION. Cập nhật: 14/11/2026.**

## Sản phẩm đã có

Code nằm trong [notebook](../../self_attention_demo.ipynb). Phần chính có 6 bước: chuẩn bị → Implementation → kiểm chứng → chọn đầu → vẽ/đọc heatmap → so sánh Transformer/CNN/RNN. Mỗi bước có lời giải thích trước ô code; riêng Implementation có sáu bước nhỏ 2.1–2.6, khớp sáu phép tính trong bảng dưới. Benchmark và assert bổ sung nằm trong phụ lục thu gọn. Không có module web, API nghiệp vụ hoặc vòng huấn luyện riêng.

Đây là mô tả code hiện có, không nhận rằng mọi dòng được viết mới trong phiên hoàn thiện workflow. Lịch sử được ghi ở [COMMITS](../11-commit/COMMITS.md).

## Các phép tính đã hiện thực

| Bước | Phép tính trong hàm | Liên hệ lý thuyết |
| --- | --- | --- |
| 2.1 | `(x @ w_qkv + b_qkv).chunk(3, dim=-1)` | Chiếu Q/K/V, PDF trang 7/17 |
| 2.2 | View `(T,12,64)`, transpose thành `(12,T,64)` | Multi-head, trang 9/17 |
| 2.3 | `q @ k.transpose(-1,-2) / sqrt(64)` | Scaled dot-product |
| 2.4 | Mask `triu(...,diagonal=1)`, gán `-inf` nếu causal | Trang 11/17; không chặn chính token |
| 2.5 | Softmax theo chiều cuối | Tạo phân phối trên các Key, trang 8 |
| 2.6 | `attn @ v`, transpose/ghép đầu | Context theo trọng số, trước Wᴼ/`c_proj` |

Hàm tự viết không gọi API attention dựng sẵn. Trọng số lấy từ GPT-2 đã huấn luyện; hidden state đầu vào lấy sau `ln_1`. Việc nạp trọng số không đồng nghĩa tự huấn luyện GPT-2 từ đầu.

Công thức được dẫn tới LT-01, checkpoint/mã đối chứng tới MH-01/MH-02 trong [danh mục nguồn THEORY](../THEORY.md). Trang PDF trong bảng là đối chiếu lịch sử của bản đã xóa.

## Triển khai hình và benchmark

`find_token` kiểm tra token và báo lỗi tiếng Việt. `pick_head` quét 144 đầu, sắp giảm theo attention `it` → `animal`, trả tuple đầu tốt nhất, in top 3. Hàm `plot_attention` được định nghĩa đúng API kế hoạch; ô vẽ gọi hàm attention hai lần trên cùng lớp, một lần có mask, một lần không mask; dùng Matplotlib ghi ba PNG.

`benchmark` tạo dữ liệu ngẫu nhiên theo thiết bị, warm-up và đo trung vị trong inference mode. GPU có synchronize, reset peak và max memory allocated; CPU đếm ma trận attention thực trả về (cùng shape/dtype với scores), không dùng dummy. CPU/GPU đều đo trung vị 20 lần. Ô đo chạy CPU và GPU nếu có, in bảng bằng f-string và vẽ hai panel log-scale.

Bốn PNG gốc do code notebook tạo và được giữ cùng JSON kết quả để kiểm chứng. Các bản nền tối, sơ đồ và ảnh tổng quan slide thêm ở lượt trước đã được bỏ theo yêu cầu mới.

## Kiểm chứng và giới hạn hiện có

Log xác minh ma trận ở cả 12 lớp trong ngưỡng, lựa chọn đầu minh bạch, chạy offline và nhánh CPU giả lập thành công. Cấp phát weight/bias/input và các lần gọi attention đều nằm trong `try`; đã thử từng điểm OOM mô phỏng và luồng toàn bộ mốc OOM. Chưa cố gây OOM thật trên máy.

Nhận xét heatmap/chi phí được tính trực tiếp từ tensor và số đo của lượt chạy, xuất Markdown sau hình; không còn nhận xét số tĩnh. Một đầu được chọn chỉ được mô tả như ví dụ, không chứng minh chất lượng chung. Danh sách đầy đủ ở [REVIEW](../06-review/REVIEW.md).

## Thay đổi của nhiệm vụ này

Đã làm lại demo theo yêu cầu mới, sửa API/đường lỗi/nhận xét và tái tạo PNG cùng `figures/demo_results.json` từ lượt thật. Giữ GPT-2, câu mẫu và chức năng đo GPU/CPU; so sánh CNN/RNN chỉ ở mức lý thuyết. Tệp trình chiếu đã được bỏ, chỉ giữ code, hồ sơ kỹ thuật và output notebook.
