# 13 - Hồ sơ tài liệu của bài

**Mã hồ sơ: DOCUMENTATION. Cập nhật: 14/11/2026.**

## Sản phẩm tài liệu

Workflow đã được chuyển từ các hướng dẫn chung sang hồ sơ cụ thể theo bài tự viết attention/GPT-2. Mỗi thư mục 01–14 chứa kết quả của bước tương ứng: định nghĩa, thiết kế, kế hoạch, brief, triển khai, review, chạy, test, debug, refactor, Git, giải thích, tài liệu và nghiệm thu.

Mục lục ở [README](../README.md), quyền sở hữu thông tin ở [CONTROL](../CONTROL.md), nội dung lý thuyết và trang nguồn ở [THEORY](../THEORY.md). Các file `Project_description.md`/`AI_Usage.md` chung chung được thay bằng hồ sơ tương đương đã điền nội dung; không tạo bản sao trùng Define/Design/Plan.

## Liên hệ với các nguồn đầu vào

| Nguồn | Cách dùng | Giới hạn |
| --- | --- | --- |
| PDF 20 trang người dùng cung cấp | Cơ sở lý thuyết và nối slide 17–19 với demo | Có biểu diễn tổng quát khác GPT-2 và số của lượt đo cũ; đọc theo THEORY |
| Spec/plan gốc | Phạm vi, tên hàm dự kiến, 5 task và điều kiện nghiệm thu | Đã đồng bộ RTX 5060/cu128, giữ ghi chú lịch sử quyết định |
| Notebook/requirements | Hành vi, API và dependency thực tế | Không giả định code khớp toàn bộ kế hoạch nếu chưa kiểm tra |
| Log kiểm tra | Bằng chứng chạy offline, CPU giả lập và lỗi mô phỏng | Chỉ có giá trị cho đúng source được khóa; không thay UI review |

Manifest khóa fingerprint các nguồn và file tài liệu. Tệp PDF trình chiếu đã được bỏ theo yêu cầu mới; THEORY giữ tên/hash và phần đối chiếu kỹ thuật lịch sử. Manifest chỉ kiểm tra các nguồn/code/output đang giữ trong repo.

## Nội dung bàn giao theo yêu cầu giảng viên

Code self-attention, hai heatmap và phần ưu/nhược điểm nằm trong notebook đã có. Tài liệu workflow giải thích rõ nguồn trọng số, công thức, cách đọc hình, benchmark và các giới hạn của kết luận. Hướng dẫn môi trường/chạy được ghi trong ENVIRONMENT/RUN; README đã đồng bộ với Implementation, bảng so sánh và cách trình bày ngắn; benchmark đặt ở phụ lục.

Giữ bốn PNG kết quả từ Matplotlib trong notebook và JSON của lượt chạy. Các bản nền tối, sơ đồ và ảnh tổng quan slide đã được bỏ; không giữ một bộ ảnh trình chiếu song song.

## Quy tắc nội dung đã áp dụng

- Tiếng Việt cho giải thích; tên biến/hàm giữ theo code.
- Tham chiếu trang PDF vật lý để tra được, không dựa số slide in sai/tổng trang hiển thị.
- Không đưa “ví dụ API tạo bản ghi”, prompt mẫu hoặc dấu giữ chỗ vào sản phẩm tài liệu.
- Không nhận code/slide do sinh viên tự viết hoàn toàn hoặc tỷ lệ đóng góp khi không có bằng chứng; xem [AI_USAGE](AI_USAGE.md).
- Không làm lại bài IMDB, tự huấn luyện hay viết thêm encoder/cross-attention chỉ vì chúng có trong PDF.
- Không đóng lỗi sản phẩm bằng việc đã viết đủ hồ sơ.

## Kiểm soát và cập nhật

Kiểm tra file/ID/hash/link/mục bắt buộc/nguồn/số đo bằng `workflow/check.py`, test logic của checker bằng `workflow/test_check.py`. Kết quả thực thi cuối được báo khi bàn giao. Các tài liệu cũ đã chuyển vị trí theo CONTROL; không giữ GUIDE hoặc `workflow/docs/` để tránh hai nơi nội dung mâu thuẫn.
