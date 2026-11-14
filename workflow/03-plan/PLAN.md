# 03 - Kế hoạch và tiến độ bài demo

**Mã hồ sơ: PLAN. Cập nhật: 14/11/2026.**

## Thứ tự và phụ thuộc

Giữ 5 task của [kế hoạch gốc](../../docs/superpowers/plans/2026-11-10-self-attention-demo.md): môi trường → attention/đối chứng → heatmap → benchmark → nhận xét/hướng dẫn/bản chạy cuối. Các task đã có code; không lập lại dự án hoặc hồi tố lịch sử TDD chưa có bằng chứng.

```mermaid
flowchart LR
    T1["TASK-001 Môi trường"] --> T2["TASK-002 Attention + đối chứng"]
    T2 --> T3["TASK-003 Heatmap"]
    T3 --> T4["TASK-004 Benchmark"]
    T4 --> T5["TASK-005 Nhận xét + bàn giao"]
```

## Mốc công việc và trạng thái thực tế

| Task | Phạm vi | Cơ sở PDF | Bằng chứng | Trạng thái |
| --- | --- | --- | --- | --- |
| TASK-001 | Venv, requirements, model/tokenizer, thông tin máy | Trang 17 | Commit `55a1ad7`, log GPU | Đã triển khai; máy mới đã được duyệt |
| TASK-002 | QKV, chia đầu, scores/mask/softmax/V và đối chiếu 12 lớp | Trang 7/9/11/17 | Commit `43d7c10`, AC-002 | Đạt kiểm tra số học |
| TASK-003 | Quét đầu, 3 PNG, nhận xét heatmap | Trang 8/18 | Commit `89a2b15`, AC-003–004 | Code/hình có kiểm tra; mức diễn giải còn mở |
| TASK-004 | Đo CPU/GPU, bảng và biểu đồ | Trang 19 | Commit `7961be7`, log GPU/CPU | Đạt runtime; phương pháp/nhận xét còn điểm review |
| TASK-005 | Ưu/nhược điểm, README, offline và VS Code | Trang 3–16/19 | Commit `19f3203`, AC-007–008 | Có nội dung và offline đạt; chưa nghiệm thu toàn bộ |

Các commit chứng minh file đã được lưu, không chứng minh đã chạy assert thất bại trước khi viết code hoặc Run All trước từng commit. Trạng thái chi tiết ở [TEST_RESULTS](../08-test/TEST_RESULTS.md).

## Bản hoàn thiện workflow theo yêu cầu mới

1. Đọc đủ 20 trang PDF và đối chiếu công thức/kiến trúc với GPT-2 cục bộ.
2. Viết nội dung thật cho từng bước 01–14; giữ các mục chưa thực hiện ở trạng thái chưa thực hiện.
3. Chuyển hồ sơ cũ về đúng thư mục chịu trách nhiệm, cập nhật toàn bộ liên kết, loại GUIDE và bản trùng.
4. Giữ log gốc, lập dữ liệu số đối chiếu log; bổ sung manifest và kiểm tra tính toàn vẹn.
5. Kiểm tra nội dung, nguồn, số liệu, danh mục và diff; commit riêng workflow và push main theo quyền đã có của repo.

## Công việc còn lại của sản phẩm

Ưu tiên khi được giao sửa notebook: đồng bộ nhận xét với output cùng lượt (REVIEW-001); thu hẹp kết luận heatmap (REVIEW-002); ghi đúng phương pháp/số lần lặp (REVIEW-003). Sau đó xử lý giới hạn OOM và sai khác API theo yêu cầu thiết kế, đồng bộ tài liệu ngoài workflow, chạy lại từ kernel mới rồi kiểm tra VS Code.

Không cắt ba phần trọng tâm để khớp mốc thuyết trình. Việc viết lại workflow không được tính là đã sửa các lỗi notebook. Phạm vi nhiệm vụ cụ thể ở [TASK_BRIEFS](../04-describe/TASK_BRIEFS.md), điều kiện bàn giao ở [ACCEPTANCE](../14-definition-of-done/ACCEPTANCE.md).
