# 06 - Kết quả rà soát demo đã sửa

**Mã hồ sơ: REVIEW. Cập nhật: 14/11/2026.**

## Phạm vi và cách đối chiếu

Đối chiếu PDF, code và output mới. Demo chính chỉ có Implementation, kiểm chứng, heatmap và bảng Transformer/CNN/RNN; phần đo/kiểm tra đặt ở phụ lục. Không coi bảng so sánh là thí nghiệm huấn luyện ba mô hình.

## Phát hiện và trạng thái xử lý

| ID | Vấn đề ở bản trước | Bản sửa / bằng chứng |
| --- | --- | --- |
| REVIEW-001 | Nhận xét tĩnh lệch bảng benchmark | Đã sửa: Markdown tính trực tiếp từ `res_cpu/res_gpu`, không nhét số cũ vào văn bản. JSON lưu cùng lượt và log có phần Generated explanations |
| REVIEW-002 | Kết luận mạnh từ một đầu; attention sink chưa đo riêng | Đã sửa: ghi giới hạn một đầu; `it→animal` trước/sau và trung bình về token đầu được tính từ ma trận thật |
| REVIEW-003 | CPU dummy, hai phép đo khác phạm vi; số lần lặp không thống nhất | Đã sửa: CPU đếm attention thực trả về; hai thiết bị 20 lần; GPU peak gồm mô hình và MiB được ghi rõ trên hình/notebook |
| REVIEW-004 | `pick_head` sai API và chưa có `plot_attention` | Đã sửa đúng chữ ký kế hoạch; tests kiểm tra API và xuất đủ PNG |
| REVIEW-005 | AGENTS/spec/plan/README lệch máy mới | Đã đồng bộ RTX 5060 Laptop/cu128 theo lựa chọn đã duyệt; cấu hình cũ chỉ còn trong ghi chú lịch sử |
| REVIEW-006 | Cấp phát ngoài vùng bắt OOM | Đã sửa: weight/bias/input và attention trong `try`; test từng cấp phát, OOM trong hàm và toàn bộ row OOM đều đạt |
| REVIEW-007 | PDF/ảnh slide có số của lượt cũ | Giữ nguyên nguồn lịch sử; không ép số mới khớp slide. Dùng PNG gốc/JSON mới để trình bày số hiện tại |

## Phần đã có bằng chứng phù hợp

Sai số, tổng hàng và tam giác trên được assert ở từng lớp trong cả 12 lớp. Hình gốc đã được xem trực tiếp từ file PNG: chữ/nhãn/thang màu rõ, trước/sau cùng lớp/đầu. Bản offline, CPU giả lập và all-OOM chạy hết không ô lỗi; test tính tay, API, ma trận CPU thực và OOM có log mới ở TEST_RESULTS.

## Giới hạn còn lại

Không huấn luyện/benchmark CNN hay RNN; chỉ so sánh lý thuyết theo nguồn gốc. Chưa cố gây OOM thật. Người dùng dừng Computer Use và yêu cầu tiếp tục không dùng nó, nên chưa xác nhận Restart/Run All trong VS Code bằng UI; kết quả CLI không được nhận là kết quả UI. Slide/PDF và ảnh nền tối cũ không tự tái tạo theo lượt mới.
