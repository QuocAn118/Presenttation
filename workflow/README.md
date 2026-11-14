# Hồ sơ bài demo self-attention theo lý thuyết Transformer

**Mã hồ sơ: INDEX. Cập nhật: 14/11/2026.**

Nội dung được viết theo PDF lý thuyết người dùng cung cấp và bài tự viết attention/GPT-2. Các thư mục bước chứa kết quả cụ thể của bài, không còn khung GUIDE hay prompt chờ điền.

## Cách đọc

Đọc [THEORY](THEORY.md) để thấy công thức, đối chiếu trang PDF lịch sử, danh mục bài báo gốc/model card, nguồn checkpoint và hình/số liệu. [CONTROL](CONTROL.md) quy định nơi chính của từng loại thông tin, danh mục file, nguồn/hash và quy trình thay đổi. [PROCESS](PROCESS.md) thể hiện luồng làm bài.

| Bước | Hồ sơ đã viết |
| --- | --- |
| 01 - Define | [Bài toán/phạm vi](01-define/DEFINE.md), [yêu cầu/nghiệm thu](01-define/REQUIREMENTS.md) |
| 02 - Design | [Kiến trúc, tensor, công thức và API](02-design/DESIGN.md), [Transformer/CNN/RNN](02-design/COMPARISON.md) |
| 03 - Plan | [5 task, phụ thuộc, tiến độ](03-plan/PLAN.md) |
| 04 - Describe | [Brief cụ thể từng task](04-describe/TASK_BRIEFS.md) |
| 05 - Generate | [Triển khai thực tế](05-generate/IMPLEMENTATION.md) |
| 06 - Review | [Phát hiện có bằng chứng và trạng thái](06-review/REVIEW.md) |
| 07 - Run | [Môi trường](07-run/ENVIRONMENT.md), [lần chạy và cách tái lập](07-run/RUN.md) |
| 08 - Test | [Kết quả kiểm thử và bảng đo](08-test/TEST_RESULTS.md) |
| 09 - Debug | [Tái hiện, nguyên nhân đã biết và phương án kiểm tra](09-debug/DEBUG.md) |
| 10 - Refactor | [Quyết định cấu trúc và phần chưa làm](10-refactor/REFACTOR.md) |
| 11 - Commit | [Lịch sử/quản lý Git](11-commit/COMMITS.md), [nhật ký](11-commit/WORK_LOG.md) |
| 12 - Explain code | [Giải thích câu demo từ token tới output](12-explain-code/CODE_EXPLANATION.md) |
| 13 - Documentation | [Hồ sơ tài liệu](13-documentation/DOCUMENTATION.md), [ghi nhận AI](13-documentation/AI_USAGE.md) |
| 14 - Definition of Done | [Nghiệm thu tài liệu và sản phẩm](14-definition-of-done/ACCEPTANCE.md) |

## Bằng chứng và kiểm soát

Log runtime ở [evidence](evidence/README.md). [manifest.json](manifest.json) quản lý từng file và khóa fingerprint notebook/spec/plan/requirements và output được giữ. [check.py](check.py) phát hiện file thiếu/lạ, ID trùng, hash/nguồn đổi, mục bắt buộc thiếu, liên kết hỏng, dấu giữ chỗ và số đo lệch log. Bộ kiểm tra dùng thư viện chuẩn Python.

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python.exe workflow/test_check.py
.\.venv\Scripts\python.exe workflow/check.py
```

PDF thuyết trình đã được bỏ theo yêu cầu. THEORY giữ bản đối chiếu kỹ thuật, tên/hash nguồn lịch sử; checker không còn yêu cầu có PDF cục bộ. Công cụ không tự sửa hash/file hoặc tuyên bố nội dung đúng chỉ nhờ checksum. Khi sửa nguồn hoặc hồ sơ, làm theo CONTROL.

## Trạng thái và ranh giới

Máy được duyệt lại là **RTX 5060 Laptop GPU, torch 2.9.1+cu128**. Đã có log notebook gốc chạy offline/CPU giả lập; REVIEW-001–006 đã được xử lý/kiểm chứng; còn bước UI tự chạy trong VS Code chưa xác nhận theo yêu cầu không dùng Computer Use, xem ACCEPTANCE. Không lấy tỷ lệ benchmark trên PDF làm số của lần chạy khác.

Lượt mới đã làm lại demo theo Bước 1–6, có Implementation và so sánh lý thuyết Transformer/CNN/RNN; benchmark/kiểm tra nằm ở phụ lục. Notebook, hình gốc, README, AGENTS và đặc tả/kế hoạch đã đồng bộ với máy được duyệt. PDF thuyết trình và các ảnh dựng riêng cho slide đã được bỏ; giữ tài liệu kỹ thuật và output notebook. Các hồ sơ cũ trong workflow/docs đã chuyển về các file ở bảng trên, không giữ hai bản song song.
