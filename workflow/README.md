# Workflow dự án demo self-attention

Đây là hồ sơ thực hiện bài Deep Learning: tự viết self-attention bằng PyTorch, dùng **trọng số đã huấn luyện của GPT-2**, vẽ heatmap trước/sau causal mask và đo GPU/CPU.

**Cập nhật 14/11/2026:** phần tài liệu workflow đã hoàn thiện; toàn bộ bài còn các mục nghiệm thu mở. Notebook gốc đã được kiểm tra trên bản sao, không bị sửa trong lần bàn giao này. Máy được người dùng chốt lại là **RTX 5060 Laptop GPU / torch 2.9.1+cu128**.

## Đọc hồ sơ theo thứ tự

| File | Nội dung |
| --- | --- |
| [00_MINDMAP](docs/00_MINDMAP.md) | Luồng làm việc và vòng lặp kiểm chứng |
| [01_DEFINE](docs/01_DEFINE.md) | Bài toán, đối tượng, phạm vi, giới hạn |
| [02_REQUIREMENTS](docs/02_REQUIREMENTS.md) | Yêu cầu và tiêu chí nghiệm thu |
| [03_DESIGN](docs/03_DESIGN.md) | Kiến trúc, công thức, API thực tế và quyết định phần cứng |
| [04_BREAKDOWN](docs/04_BREAKDOWN.md) | Trạng thái 5 task và bằng chứng commit |
| [05_TOOLS](docs/05_TOOLS.md) | Môi trường thực tế và cách tái lập kiểm tra |
| [06_VERIFICATION](docs/06_VERIFICATION.md) | Kết quả chạy, log và các phát hiện còn mở |
| [07_WORK_LOG](docs/07_WORK_LOG.md) | Nhật ký, phạm vi cuối cùng và quyết định |
| [08_RELEASE](docs/08_RELEASE.md) | Bàn giao workflow và checklist nghiệm thu bài |
| [09_AI_USAGE](docs/09_AI_USAGE.md) | Công cụ AI, đóng góp đã biết và phần chưa xác nhận |

Define/Design/Breakdown là mô tả dự án tương đương `Project_description.md`; không tạo thêm bản sao cùng nội dung. Ghi nhận AI nằm trong `09_AI_USAGE.md`.

## 14 hướng dẫn thao tác

| Giai đoạn | Hướng dẫn |
| --- | --- |
| Xác định | [01 Define](01-define/GUIDE.md), [02 Design](02-design/GUIDE.md), [03 Plan](03-plan/GUIDE.md) |
| Triển khai | [04 Describe](04-describe/GUIDE.md), [05 Generate](05-generate/GUIDE.md), [06 Review](06-review/GUIDE.md) |
| Kiểm chứng | [07 Run](07-run/GUIDE.md), [08 Test](08-test/GUIDE.md), [09 Debug](09-debug/GUIDE.md) |
| Chốt thay đổi | [10 Refactor](10-refactor/GUIDE.md), [11 Commit](11-commit/GUIDE.md), [12 Explain Code](12-explain-code/GUIDE.md) |
| Bàn giao | [13 Documentation](13-documentation/GUIDE.md), [14 Definition of Done](14-definition-of-done/GUIDE.md) |

Các GUIDE là hướng dẫn, không phải bằng chứng từng bước lịch sử đã được làm. Debug/refactor chỉ dùng khi cần; trạng thái nghiệm thu xem 06_VERIFICATION và 08_RELEASE.

## Nguồn quyết định và cách dùng

Đặc tả gốc ở [docs/superpowers/specs](../docs/superpowers/specs/2026-11-10-self-attention-demo-design.md), kế hoạch gốc ở [docs/superpowers/plans](../docs/superpowers/plans/2026-11-10-self-attention-demo.md). Tuân theo yêu cầu người dùng mới nhất; workflow ghi rõ quyết định đổi phần cứng, đồng thời giữ nguyên nguồn ngoài phạm vi được giao. Không đánh dấu nghiệm thu RTX 4080 từ một lần chạy RTX 5060.

Khi code hoặc số đo thay đổi, cập nhật Verification → Breakdown/Work Log → Release theo kết quả mới. Không đánh dấu “đạt” chỉ vì đã có file hoặc commit.
