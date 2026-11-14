# Tiến độ thực tế của 5 task

Cập nhật ngày **14/11/2026**, dựa trên lịch sử Git, notebook lưu sẵn và kiểm tra mới trong [06_VERIFICATION](06_VERIFICATION.md). Không hồi tố quy trình TDD hay lần Run All trước mỗi commit nếu không có log.

| Task | Sản phẩm | Trạng thái thực tế | Bằng chứng |
| --- | --- | --- | --- |
| TASK-001 | Môi trường, requirements, notebook khung | Đã triển khai; xác minh lại trên RTX 5060 Laptop GPU/cu128 được người dùng duyệt | `55a1ad7`; VERIFY-001 |
| TASK-002 | Self-attention tự viết và đối chiếu GPT-2 | Đã triển khai; sai số đạt ở 12 lớp | `43d7c10`; VERIFY-002–004 |
| TASK-003 | Chọn đầu, vẽ 3 heatmap và nhận xét | Code và ảnh đạt kiểm tra; nhận xét còn cần chỉnh mức khẳng định; chưa có `plot_attention` | `89a2b15`; VERIFY-005, 009; REVIEW-002, 004 |
| TASK-004 | Benchmark GPU/CPU và biểu đồ | Đã chạy thành công; còn giới hạn phép đo và số nhận xét cũ | `7961be7`; VERIFY-006, 007, 010; REVIEW-001, 003 |
| TASK-005 | Ưu/nhược điểm, README, offline, bản chạy cuối | Đã có nội dung và offline đạt; chưa nghiệm thu Run All trong VS Code và tính nhất quán toàn bộ tài liệu | `19f3203`; VERIFY-008; REVIEW-001–005 |

## Phụ thuộc và tiêu chí

TASK-001 → TASK-002 → TASK-003/TASK-004 → TASK-005. Thiết kế và kế hoạch gốc nằm ngoài workflow tại [đặc tả](../../docs/superpowers/specs/2026-11-10-self-attention-demo-design.md) và [kế hoạch](../../docs/superpowers/plans/2026-11-10-self-attention-demo.md).

- Task 1: dùng GPU thật, phiên bản thư viện được ghi đúng. Lựa chọn phần cứng mới xem DEC-006 trong [thiết kế](03_DESIGN.md).
- Task 2: không gọi attention dựng sẵn trong hàm tự viết; sai số không được nới quá `1e-4`.
- Task 3: giữ câu chuẩn, quét 144 đầu; hai panel cùng thang 0–1, có cả hai PNG riêng. Không suy rộng một đầu được chọn thành kết luận tổng quát.
- Task 4: warm-up 3; trung vị CPU 10 lần/GPU 20 lần; đồng bộ CUDA; phân biệt hai cách đo bộ nhớ. Không coi phép đo kernel này là độ trễ toàn bộ GPT-2.
- Task 5: hướng dẫn chạy, offline, kiểm tra hiển thị trong VS Code và dữ liệu nhận xét phải thống nhất trước nghiệm thu toàn bộ bài.

## Công việc hoàn tất trong phạm vi workflow

- [x] Đối chiếu tiến độ với commit thật.
- [x] Bổ sung log GPU/offline, CPU giả lập không GPU và các nhánh lỗi.
- [x] Ghi nhận phần cứng đã được người dùng chốt lại.
- [x] Bổ sung ghi nhận sử dụng AI và hướng dẫn tìm tài liệu.
- [x] Phân biệt kết quả kiểm chứng đạt với lỗi/điều kiện chưa giải quyết.
- [x] Giữ nguyên notebook, README gốc, đặc tả, requirements và ảnh theo yêu cầu “chỉ workflow”.

Các việc ngoài phạm vi còn lại được liệt kê tại [08_RELEASE](08_RELEASE.md), không ẩn bằng cách đánh dấu tất cả task hoàn thành.
