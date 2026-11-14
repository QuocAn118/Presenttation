# 14 - Nghiệm thu hồ sơ và sản phẩm

**Mã hồ sơ: ACCEPTANCE. Cập nhật: 14/11/2026.**

## Phạm vi hồ sơ được giao

Đọc PDF lý thuyết, viết nội dung bài vào từng thư mục bước 01–14, bỏ GUIDE và kiểm soát từng file. Đây là nhiệm vụ tài liệu; không mặc nhiên mở phạm vi sửa notebook/slide. Hồ sơ phải phản ánh cả kết quả đạt và điểm còn mở của sản phẩm.

## Tiêu chí hoàn tất bộ workflow

| Tiêu chí | Kết quả nội dung / cách xác nhận |
| --- | --- |
| Đọc PDF và nêu nguồn | THEORY ghi hash/20 trang, đối chiếu sơ đồ ảnh và các trang 17–19 |
| Nội dung cụ thể cho từng bước | Mỗi thư mục có artifact của bài, không còn prompt mẫu/GUIDE |
| Không tồn tại hai bộ hồ sơ mâu thuẫn | Nội dung `workflow/docs/` chuyển về vị trí chịu trách nhiệm; liên kết cũ được cập nhật |
| Lý thuyết khớp phạm vi GPT-2 | Phân biệt √64, mask cộng, decoder-only/pre-LN/không cross-attention và đầu ra trước `c_proj` |
| Số liệu có nguồn | Bảng TEST_RESULTS và measurements đối chiếu log cùng lượt; số 10,8× trên PDF là lượt khác |
| Kiểm soát thay đổi | Manifest định danh/hash/mục bắt buộc/nguồn; checker và regression tests |
| Không bịa trạng thái sản phẩm | Review, UI và OOM chưa bao phủ giữ trạng thái mở |
| Giữ đúng phạm vi Git | Chỉ thay workflow, không stage việc xóa PDF cũ hoặc PDF mới của người dùng |

File đầy đủ chưa đủ để nhận kiểm tra tự động đạt. Lệnh test/check phải chạy thành công sau nội dung cuối; hash được cập nhật cho đúng những file đã rà soát và diff chỉ gồm phạm vi đã giao. Kết quả lệnh và hash commit được báo ở bàn giao sau khi có thực tế.

## Trạng thái toàn bộ bài

| Tiêu chí sản phẩm | Trạng thái |
| --- | --- |
| Hàm attention tự viết và đối chiếu GPT-2 12 lớp | Đạt trên source đã kiểm tra |
| Causal mask đúng thuộc tính số; xuất đủ hình | Đạt kiểm tra số/file |
| Offline từ kernel mới và CPU giả lập không GPU | Đạt theo log |
| Mọi nhận xét khớp số của cùng lượt | Còn REVIEW-001 |
| Kết luận heatmap ở mức bằng chứng hỗ trợ | Còn REVIEW-002 |
| Mô tả phương pháp/số lần lặp và API khớp triển khai | Còn REVIEW-003–004 |
| Tài liệu ngoài workflow thống nhất máy mới | Còn REVIEW-005 |
| OOM được bao phủ ở mọi cấp phát | Còn REVIEW-006 |
| PDF/slide đã cập nhật theo lượt benchmark mới | Chưa thực hiện; REVIEW-007 phân biệt hai lượt |
| Restart/Run All và nhìn mọi hình trong VS Code | Chưa xác nhận; người dùng dừng Computer Use |

**Kết luận sản phẩm:** đã triển khai và có bằng chứng CLI, chưa nghiệm thu đầy đủ. Hoàn tất workflow không đổi kết luận này.

## Bàn giao và điều kiện đóng các mục mở

Mục lục có ở [README](../README.md); nguồn chính từng loại thông tin ở [CONTROL](../CONTROL.md). Khi code hoặc nguồn thay đổi, phải xem lại hash nguồn, chạy kiểm tra liên quan, lưu log mới và review các kết luận chịu ảnh hưởng trước khi cập nhật trạng thái. Không chỉ sửa manifest để làm checker xanh khi bằng chứng chưa được cập nhật.

Repo được giao push main; chỉ báo đã push khi ref remote được xác nhận. Hash cuối nằm ở thông báo bàn giao, không điền hash dự kiến vào chính tài liệu đang commit. Giữ nguyên thay đổi ngoài phạm vi đang có của người dùng.
