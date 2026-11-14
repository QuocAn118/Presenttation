# Ghi nhận công cụ AI và đóng góp

**Mã hồ sơ: AI_USAGE. Cập nhật: 14/11/2026.**

## Phần đóng góp quan sát được

| Công cụ / bên tham gia | Mục đích | Phần đã xác định |
| --- | --- | --- |
| ChatGPT/Codex | Rà soát code, PDF và hoàn thiện workflow | Đọc tài liệu/ảnh trang PDF, kiểm tra config/code GPT-2, viết các hồ sơ, chạy kiểm tra và lưu giới hạn |
| Skill `vibe-coding` | Tổ chức 14 bước | Dùng Define/Design/Plan và các bước Review/Run/Test/Documentation/Done để ghi nội dung cụ thể của bài |
| Skill `ponytail` | Giữ phạm vi và giảm trùng lặp | Tái sử dụng log, một file chính cho mỗi loại thông tin; không mở rộng notebook |
| Skill `pdf` | Đọc tài liệu lý thuyết | Trích text và render trang để đọc sơ đồ nằm trong ảnh |
| Python/PyTorch/Jupyter | Kiểm chứng | Chạy bản sao notebook gốc offline, CPU giả lập, lỗi mô phỏng ở lượt kiểm tra đã lưu log |
| Người dùng | Quyết định và nguồn đầu vào | Chọn RTX 5060 Laptop; cung cấp PDF; yêu cầu viết nội dung từng file, bỏ GUIDE và kiểm soát chặt workflow |

Các hình trang PDF được render bằng thư viện có sẵn để đọc, không phải AI tự tạo ảnh lý thuyết mới. Checker dùng thư viện chuẩn Python, không thêm dependency vào requirements sản phẩm.

## Điều chưa được xác nhận

Code/notebook và các commit ngày 13/11 đã có trước lượt viết lại này; chưa đủ bằng chứng phân chia dòng code do người thực hiện hay AI viết. Git author không tự chứng minh quyền tác giả từng dòng. Không gán tên công cụ/mô hình cho các phiên trước nếu chưa được xác nhận.

Trang thành viên PDF có tỷ lệ hoàn thành, nhưng không dùng tỷ lệ trên slide để xác nhận đóng góp code/AI hay kiểm thử. Không sao chép MSSV/dữ liệu thành viên vào hồ sơ công cụ.

## Ranh giới của phiên này

Lượt hồ sơ ban đầu chỉ sửa workflow; lượt mới được người dùng giao sửa demo và thêm Implementation/so sánh lý thuyết ngắn. AI sửa notebook/hình/nguồn hướng dẫn, thêm test và chạy CLI. Giữ PDF/slide, GPT-2 và câu mẫu. Người dùng dừng Computer Use và yêu cầu không dùng nó; không nhận có kiểm tra UI hoàn chỉnh.
