# Bàn giao workflow và nghiệm thu bài

Cập nhật **14/11/2026**. Phân biệt phạm vi tài liệu được giao với trạng thái toàn bộ bài để không báo hoàn thành vượt bằng chứng.

## Bàn giao phần workflow

- [x] Có mục lục [workflow/README](../README.md) và 14 hướng dẫn từng bước.
- [x] Có hồ sơ Define, Requirements, Design và Breakdown tương ứng dự án hiện tại.
- [x] Tiến độ 5 task khớp code và commit thực tế; chỉ rõ phần đạt và phần còn mở.
- [x] Môi trường RTX 5060 Laptop/cu128 được người dùng duyệt lại và ghi vào thiết kế workflow.
- [x] Có log chạy offline, CPU giả lập không GPU và kiểm tra nhánh lỗi trong `workflow/evidence/`.
- [x] Có nhận xét dựa trên số đo mới, phân biệt với output gốc và giới hạn phương pháp đo.
- [x] Có nhật ký và [ghi nhận dùng AI](09_AI_USAGE.md).
- [x] Chỉ thay đổi `workflow/`; giữ nguyên notebook, PNG gốc, README, requirements, AGENTS và đặc tả/kế hoạch gốc.

**Kết quả phần việc:** hồ sơ workflow đã được hoàn thiện theo phạm vi này. Việc phát hành toàn bộ bài vẫn còn các mục phía dưới.

## Checklist nghiệm thu toàn bộ bài

- [x] Có hàm self-attention tự viết và output so GPT-2 ở 12 lớp, sai số <`1e-4`.
- [x] Có dòng “trọng số đã huấn luyện của GPT-2” ở đầu notebook và tiêu đề hình so sánh.
- [x] Có đủ 3 heatmap và biểu đồ chi phí trong `figures/`.
- [x] Bản sao nguyên trạng notebook gốc chạy hết từ kernel mới trong chế độ offline (log ngày 14/11).
- [x] Nhánh không GPU chạy hết khi giả lập trong kernel riêng.
- [ ] Nhận xét notebook khớp số liệu cùng lượt chạy, mức kết luận phù hợp với heatmap một đầu (REVIEW-001–002).
- [ ] Phương pháp bộ nhớ và số lần lặp được ghi nhất quán trong notebook/README ngoài workflow (REVIEW-003).
- [ ] Đặc tả/AGENTS/kế hoạch ngoài workflow được đồng bộ với phần cứng mới hoặc có ghi chú quyết định tương ứng (REVIEW-005).
- [ ] Đã Restart, Run All trong VS Code và nhìn đủ mọi hình; người dùng dừng Computer Use trước khi xác nhận mục này.
- [ ] Bản chạy cuối sau khi sửa các mục còn mở đã được lưu output và push; không dùng log kiểm tra hiện tại để thay cho một lần chạy sau thay đổi tương lai.

## Phạm vi tài liệu và nguồn hình

- Notebook/ảnh gốc là sản phẩm đã có từ các commit ngày 13/11; lần này không sửa chúng.
- Ba heatmap và `cost_gpu_cpu.png` được code Matplotlib trong notebook tạo. Các bản `_dark`, sơ đồ luồng và ảnh slide được thêm riêng; không tự cập nhật theo Run All và chưa được đối chiếu số liệu mới.
- Các PNG trong `scratch/wf-offline/` và `scratch/wf-cpu/` chỉ là output kiểm tra, không thay thế ảnh nộp bài. Log văn bản đã được lưu trong workflow để đọc lại kết quả.

## Repo và trạng thái Git

Repo: [QuocAn118/Presenttation](https://github.com/QuocAn118/Presenttation). Lần rà soát bắt đầu ở nhánh `hoangdang`, commit nền `47246be`; `origin/main` có merge commit `3e594be`. Trạng thái này là mốc trước bàn giao, không khẳng định hai nhánh đang đồng bộ.

Commit/push chỉ chọn thay đổi workflow, giữ nguyên thay đổi xóa PDF ngoài phạm vi. Hash và kết quả push cuối cùng được báo trong phần bàn giao của trợ lý; không đánh dấu checklist sản phẩm hoàn tất chỉ vì đã đẩy tài liệu.
