# 08 - Kết quả kiểm thử và thực nghiệm

**Mã hồ sơ: TEST_RESULTS. Cập nhật: 14/11/2026.**

## Nguồn bằng chứng

Các kết quả dưới đây đến từ notebook gốc chạy trong các kernel thử nghiệm riêng ngày 14/11/2026, không phải số chép từ slide. [Log offline](../evidence/2026-11-14-offline.log), [log CPU](../evidence/2026-11-14-cpu.log) và [log nhánh lỗi](../evidence/2026-11-14-branches.log) được giữ nguyên nội dung kết quả. Thời gian/row hiển thị đã được log làm tròn; tỷ lệ tính từ chúng là xấp xỉ.

## Ma trận kiểm thử

| Mã | Hành vi / kỳ vọng | Kết quả thực tế | Giới hạn |
| --- | --- | --- | --- |
| VERIFY-001 / AC-001 | Tự nhận GPU đúng môi trường | RTX 5060 Laptop, torch 2.9.1+cu128, CUDA 12.8 | Không phải phép chạy trên RTX 4080 |
| VERIFY-002 / AC-002 | Mỗi lớp sai số attention <`1e-4` | Cả 12 lớp đạt; lớn nhất **1.76e-06** | Kiểm tra attention, không đối chiếu toàn đầu ra model |
| VERIFY-003 | Tổng hàng xấp xỉ 1 | Assertion `allclose(...,atol=1e-5)` đạt | Ô đối chiếu assert tổng hàng sau vòng lặp, tức lớp cuối |
| VERIFY-004 | Sau mask không nhìn tương lai | Tam giác trên bằng 0 ở lớp cuối và lớp vẽ | Không tuyên bố đã assert riêng mọi lớp cho thuộc tính này |
| VERIFY-005 / AC-003 | Token chuẩn, quét 144 đầu | `animal` index 1, `it` index 8; lớp 4/đầu 3, **84.61%** | Chỉ số 0; mẫu được chọn theo tiêu chí liên kết này |
| VERIFY-006 / AC-005 | Đo 5 độ dài; ma trận tăng bậc hai | Có đủ row GPU/CPU; bộ nhớ CPU tăng 4 lần khi N gấp đôi | Phạm vi bộ nhớ hai thiết bị khác nhau |
| VERIFY-007 / AC-006 | Nhánh không GPU chạy hết | Giả lập cho Device=cpu, thông báo chỉ đo CPU, 0 ô lỗi | Chưa thử máy vật lý thiếu GPU |
| VERIFY-008 / AC-007–008 | Offline và toàn notebook | Exit 0; GPU/CPU **13.41s**, bản CPU riêng **12.33s** | Cả hai là bản sao; source gốc không đổi |
| VERIFY-009 / AC-004 | Xuất 4 PNG không rỗng | Đạt trong cả hai thư mục chạy thử | Chưa xác nhận mọi hình hiển thị trong VS Code |
| VERIFY-010 | OOM trong attention và thiếu token | Ghi `None`, tiếp tục hai độ dài; token thiếu báo `ValueError` | OOM mô phỏng, không bao phủ cấp phát ngoài `try` |

## Bảng đo của lượt offline

Dữ liệu máy đọc được ở [measurements.json](../evidence/measurements.json); checker đối chiếu lại từng row với log. Đây là lượt kiểm tra riêng, không thay output lưu sẵn trong notebook gốc.

| N | GPU ms | CPU ms | GPU đỉnh MiB | Một ma trận CPU MiB |
| --- | --- | --- | --- | --- |
| 128 | 0.29 | 1.10 | 497.95 | 0.75 |
| 256 | 0.29 | 1.89 | 506.49 | 3.00 |
| 512 | 0.52 | 5.41 | 540.93 | 12.00 |
| 1024 | 2.32 | 20.03 | 658.18 | 48.00 |
| 2048 | 8.04 | 92.88 | 1114.18 | 192.00 |

Ở N=2048, 92.88/8.04 ≈ **11.55 lần**. PDF trang 19 ghi **10,8 lần** cho lượt trình bày của slide; không đồng nhất hai con số. Bộ nhớ một ma trận scores tăng 0.75→3→12→48→192 MiB, đúng 4 lần mỗi khi N gấp đôi. GPU peak còn chứa tensor nền nên không đòi hỏi tăng đúng 4 lần.

## Phép đo này chứng minh được gì

Có bằng chứng code tự viết khớp attention GPT-2 trên câu đã chọn, causal mask chặn tương lai và kernel chạy song song có lợi về thời gian trong các kích thước thử. Kích thước scores thể hiện chi phí O(N²). Không có thử nghiệm chất lượng RNN/LSTM, tốc độ sinh văn bản, tải doanh nghiệp, huấn luyện hay toàn context GPT-2 ở N=2048.

## Kiểm tra tính toàn vẹn hồ sơ

[test_check.py](../test_check.py) kiểm tra các ca lỗi có ý nghĩa của bộ kiểm soát: thiếu file, sửa nội dung chưa cập nhật duyệt, liên kết hỏng dù hash đã cập nhật, nguồn thay đổi, ID trùng, file lạ/GUIDE và số đo bị đổi so với log. [check.py](../check.py) chạy trên danh mục thực tế, gồm cả bảng ở file này.

Kết quả test/check cuối cùng được báo khi chạy thật và kèm commit bàn giao; không suy ra pass chỉ từ việc có test. Các điều kiện sản phẩm chưa được kiểm tra hoặc chưa đạt vẫn nằm ở [ACCEPTANCE](../14-definition-of-done/ACCEPTANCE.md) và [REVIEW](../06-review/REVIEW.md).
