# Ghi nhận sử dụng AI

Cập nhật 14/11/2026. Tài liệu chỉ ghi phần đóng góp quan sát được trong phiên; không mặc định sinh viên tự viết toàn bộ code hoặc gán công cụ cho lịch sử chưa xác nhận.

| Công cụ | Mục đích thực tế | AI hỗ trợ | Đóng góp người dùng được xác nhận |
| --- | --- | --- | --- |
| ChatGPT / Codex | Rà soát và hoàn thiện workflow | Đọc repo/spec/plan/notebook, đối chiếu Git, cập nhật hồ sơ workflow, chạy kiểm tra và ghi hạn chế | Giao phạm vi, chọn RTX 5060 Laptop, thu hẹp yêu cầu chỉ workflow |
| Skill `vibe-coding` | Dùng quy trình tài liệu và Definition of Done | Đối chiếu hướng dẫn bước 13–14; ghi rõ bằng chứng và phần chưa xác minh | Người dùng có bộ hướng dẫn workflow trong repo |
| Skill `ponytail` | Giữ thay đổi trong phạm vi nhỏ | Tái sử dụng cấu trúc tài liệu hiện có, không thêm tính năng notebook | Chưa xác nhận đóng góp khác |
| Python/PyTorch/Jupyter qua công cụ lệnh | Kiểm tra notebook gốc trong bản sao | Chạy offline GPU, CPU giả lập không GPU, OOM mô phỏng và thiếu token; lưu log | Chưa xác nhận người dùng tự chạy lại các lệnh này trong phiên |
| Computer Use | Xem VS Code để chuẩn bị kiểm tra hiển thị | Chỉ quan sát/chọn cửa sổ; chưa hoàn tất Restart/Run All | Người dùng dừng thao tác bằng Escape |

## Giới hạn ghi nhận

- Code, notebook và bộ tài liệu ban đầu đã có trước lần rà soát này. Lịch sử Git có tên tác giả commit nhưng không chứng minh ai tự viết từng dòng hay đã dùng mô hình AI nào.
- Không có đủ thông tin để xác nhận tỷ lệ code do sinh viên/AI viết trong các phiên trước; ghi là **chưa xác nhận**.
- Các sửa thử notebook/ảnh của phiên này đã hoàn tác theo yêu cầu chỉ workflow. Sản phẩm cuối của phiên là các file trong `workflow/`.
- Không đưa file hướng dẫn skill hoặc dữ liệu tài khoản riêng vào repo. Đường dẫn cục bộ trong log chỉ phục vụ tái lập môi trường chạy.
