# Hồ sơ bài demo self-attention theo lý thuyết Transformer

**Mã hồ sơ: INDEX. Cập nhật: 14/11/2026.**

Nội dung được viết theo PDF lý thuyết người dùng cung cấp và bài tự viết attention/GPT-2. Các thư mục bước chứa kết quả cụ thể của bài, không còn khung GUIDE hay prompt chờ điền.

## Cách đọc

Đọc [THEORY](THEORY.md) để thấy từng trang PDF nối với phép tính/code và các điểm phải phân biệt. [CONTROL](CONTROL.md) quy định nơi chính của từng loại thông tin, danh mục file, nguồn/hash và quy trình thay đổi. [PROCESS](PROCESS.md) thể hiện luồng làm bài.

| Bước | Hồ sơ đã viết |
| --- | --- |
| 01 - Define | [Bài toán/phạm vi](01-define/DEFINE.md), [yêu cầu/nghiệm thu](01-define/REQUIREMENTS.md) |
| 02 - Design | [Kiến trúc, tensor, công thức và API](02-design/DESIGN.md) |
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

Log runtime ở [evidence](evidence/README.md). [manifest.json](manifest.json) quản lý từng file và khóa fingerprint nguồn PDF/notebook/spec/plan/requirements. [check.py](check.py) phát hiện file thiếu/lạ, ID trùng, hash/nguồn đổi, mục bắt buộc thiếu, liên kết hỏng, dấu giữ chỗ và số đo lệch log. Bộ kiểm tra dùng thư viện chuẩn Python.

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python.exe workflow/test_check.py
.\.venv\Scripts\python.exe workflow/check.py
```

Giữ PDF đúng tên ở gốc theo manifest để đối chiếu nguồn; thiếu PDF sẽ báo lỗi nguồn chưa đủ. Công cụ không tự sửa hash/file hoặc tuyên bố nội dung đúng chỉ nhờ checksum. Khi sửa nguồn hoặc hồ sơ, làm theo CONTROL.

## Trạng thái và ranh giới

Máy được duyệt lại là **RTX 5060 Laptop GPU, torch 2.9.1+cu128**. Đã có log notebook gốc chạy offline/CPU giả lập; sản phẩm vẫn còn các mục review và kiểm tra UI chưa xác nhận, xem ACCEPTANCE. Không lấy tỷ lệ benchmark trên PDF làm số của lần chạy khác.

Lượt này chỉ viết lại workflow và kiểm soát tài liệu. Notebook, ảnh, PDF, requirements, AGENTS và đặc tả/kế hoạch gốc giữ nguyên; khác biệt phần cứng ở nguồn cũ được ghi công khai. Các hồ sơ cũ trong workflow/docs đã chuyển về các file ở bảng trên, không giữ hai bản song song.
