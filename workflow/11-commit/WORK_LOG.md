# Nhật ký và quyết định của dự án

**Mã hồ sơ: WORK_LOG. Cập nhật: 14/11/2026.**

## Các mốc có bằng chứng

- **10/11/2026:** Git ghi việc bỏ bài IMDB cũ, lưu AGENTS/đặc tả/kế hoạch cho self-attention.
- **13/11/2026:** có 5 commit triển khai từ môi trường đến nhận xét/README; ảnh nền tối và tổng quan slide được thêm riêng. Chi tiết tại COMMITS.
- **14/11/2026, lần rà soát trước:** người dùng duyệt RTX 5060 Laptop/cu128; chạy bản sao notebook gốc offline GPU/CPU, bản CPU giả lập và nhánh lỗi; lưu 3 log. Các chỉnh thử notebook/ảnh được hoàn tác khi người dùng thu hẹp phạm vi chỉ workflow.
- **14/11/2026:** người dùng dừng Computer Use bằng Escape; chưa có xác nhận Restart/Run All và toàn bộ hình trong VS Code. Không tiếp tục tự động UI để điền mục còn thiếu.
- **14/11/2026, yêu cầu hiện tại:** đọc PDF lý thuyết, hoàn thiện từng file theo bài, bỏ GUIDE và kiểm soát chặt hồ sơ.

## Công việc của lượt viết lại theo PDF

Đọc nguồn 20 trang, trích text và xem các sơ đồ ảnh. Lập THEORY đối chiếu trang với phép tính/code; xác nhận config GPT-2 cục bộ dùng 12 lớp/12 đầu/768 chiều, `gelu_new`, không cross-attention, context 1024. Phân biệt cú pháp mask nhị phân trên hình với mask cộng và √d_k theo từng đầu.

Viết lại hồ sơ cho từng bước 01–14, chuyển nội dung từ bộ docs cũ, gỡ GUIDE, giữ bằng chứng gốc và danh sách lỗi chưa sửa. Viết test cho bộ kiểm soát trước; lần đầu thất bại vì chưa có `check.py`, rồi mới triển khai checker. Kết quả kiểm tra cuối phải lấy từ lệnh thực thi thật, không suy ra từ việc file đã được tạo.

## Quyết định phạm vi

- Hoàn thiện **tài liệu bài** và công cụ kiểm soát trong workflow, không dừng ở khung hướng dẫn/prompt mẫu.
- Không tự sửa notebook, hình, requirements, AGENTS, đặc tả hoặc PDF. Lưu hash nguồn để bắt thay đổi về sau.
- Không nâng trạng thái sản phẩm trong ACCEPTANCE khi REVIEW-001–006 và kiểm tra UI còn mở.
- Không đưa danh sách/MSSV/tỷ lệ hoàn thành của trang thành viên vào hồ sơ bằng chứng đóng góp; thông tin đóng góp chưa xác nhận phải giữ nguyên trạng thái đó.

## Việc tiếp theo của sản phẩm

Khi được giao sửa notebook, bắt đầu từ lệch số nhận xét và mức kết luận heatmap, sau đó phương pháp đo/OOM/tài liệu môi trường. Chạy lại notebook, kiểm tra hình và cập nhật log/manifest tương ứng trước khi đóng nghiệm thu. Các việc này chưa được làm chỉ bằng lần viết lại workflow.
