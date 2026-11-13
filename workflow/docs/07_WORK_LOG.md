# Nhật ký công việc và tiến độ (Work Log)

Tài liệu này lưu lại nhật ký làm việc qua các buổi và các mốc chuyển giao.

---

## Nhật ký các phiên làm việc

### Phiên 1: Khởi tạo và thiết kế kỹ thuật (2026-11-10)
- **Người thực hiện**: Trưởng nhóm / Soạn thảo đặc tả.
- **Nội dung thực hiện**:
  - Hủy bỏ bài so sánh Transformer vs RNN/LSTM trên IMDB theo định hướng mới của giảng viên.
  - Thiết kế bài toán Demo Self-Attention với trọng số đã huấn luyện của GPT-2 (`docs/superpowers/specs/2026-11-10-self-attention-demo-design.md`).
  - Lập kế hoạch chi tiết 5 Task (`docs/superpowers/plans/2026-11-10-self-attention-demo.md`).
  - Viết hướng dẫn `AGENTS.md` cố định các nguyên tắc bất di bất dịch cho AI trợ lý.

### Phiên 2: Tích hợp Workflow Vibe Coding chuẩn mực (2026-11-13)
- **Người thực hiện**: Thành viên thực hiện + AI Assistant.
- **Nội dung thực hiện**:
  - Tiếp nhận phản hồi từ trưởng nhóm: bổ sung bộ tài liệu quy trình 10 bước/mục theo đề bài của cô.
  - Đồng bộ cấu trúc thư mục `workflow/` và bộ tài liệu `workflow/docs/` (`00_MINDMAP` đến `08_RELEASE`) từ khung Vibe Coding vào repo.
  - Điền đầy đủ thông tin kỹ thuật, tiêu chí nghiệm thu (AC) và kế hoạch kiểm chứng (Verification) cho từng tài liệu.
- **Bước tiếp theo**: Bắt đầu triển khai Task 1 (tạo môi trường venv CUDA 12.6, cấu trúc repo, file notebook khung).

---

## Chu kỳ kiểm tra sau mỗi Task
Trước khi chuyển trạng thái Task sang "Hoàn thành" và commit lên Git:
1. Đã chạy thử ô kiểm tra `assert` thành công chưa?
2. Toàn bộ notebook đã được chạy lại trơn tru bằng `jupyter nbconvert` chưa?
3. Output lưu trong notebook có khớp với kết quả thực tế trên GPU RTX 4080 không?
4. Commit message có tuân thủ đúng định dạng quy định không?
