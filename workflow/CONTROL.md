# Kiểm soát hồ sơ workflow

**Mã hồ sơ: CONTROL. Cập nhật: 14/11/2026.**

## Phạm vi và thứ tự quyết định

Lượt trước đã hoàn thiện hồ sơ và thay GUIDE. Yêu cầu mới mở phạm vi sửa demo: Implementation ngắn, hai heatmap, nhận xét theo output, bảng lý thuyết Transformer/CNN/RNN; benchmark và kiểm tra ở phụ lục. Notebook, PNG, README và nguồn hướng dẫn được đồng bộ; PDF/ảnh dựng riêng cho slide được bỏ theo yêu cầu mới, giữ bản đối chiếu lý thuyết trong tài liệu. Không đổi trạng thái sản phẩm thành “đã nghiệm thu” chỉ vì đã viết xong tài liệu.

Thứ tự áp dụng: yêu cầu người dùng mới nhất → đặc tả gốc → kế hoạch gốc → PDF lý thuyết → triển khai và bằng chứng để xác định trạng thái thực tế. PDF giải thích lý thuyết, không tự mở rộng phạm vi thành huấn luyện mô hình/encoder–decoder/IMDB. Quyết định người dùng ngày 14/11/2026 đã thay máy mục tiêu thành RTX 5060 Laptop/cu128; nguồn gốc còn ghi RTX 4080 được đánh dấu khác biệt, không âm thầm sửa.

## Một nơi chính cho mỗi loại thông tin

| Thông tin | File chịu trách nhiệm |
| --- | --- |
| Nguồn PDF lịch sử, bài báo gốc, checkpoint, nguồn hình và diễn giải lý thuyết | [THEORY](THEORY.md) |
| Phạm vi bài và yêu cầu | [DEFINE](01-define/DEFINE.md), [REQUIREMENTS](01-define/REQUIREMENTS.md) |
| Kiến trúc và API thực tế | [DESIGN](02-design/DESIGN.md) |
| Kế hoạch và tiến độ | [PLAN](03-plan/PLAN.md) |
| Phạm vi từng nhiệm vụ | [TASK_BRIEFS](04-describe/TASK_BRIEFS.md) |
| Code đã có | [IMPLEMENTATION](05-generate/IMPLEMENTATION.md) |
| Phát hiện còn mở | [REVIEW](06-review/REVIEW.md) |
| Môi trường và lần chạy | [ENVIRONMENT](07-run/ENVIRONMENT.md), [RUN](07-run/RUN.md) |
| Kết quả kiểm thử | [TEST_RESULTS](08-test/TEST_RESULTS.md) |
| Dữ liệu số của lượt offline | [measurements](evidence/measurements.json), đối chiếu với log gốc |
| Kế hoạch xử lý lỗi và refactor | [DEBUG](09-debug/DEBUG.md), [REFACTOR](10-refactor/REFACTOR.md) |
| Commit và nhật ký | [COMMITS](11-commit/COMMITS.md), [WORK_LOG](11-commit/WORK_LOG.md) |
| Giải thích code | [CODE_EXPLANATION](12-explain-code/CODE_EXPLANATION.md) |
| Hồ sơ bàn giao và dùng AI | [DOCUMENTATION](13-documentation/DOCUMENTATION.md), [AI_USAGE](13-documentation/AI_USAGE.md) |
| Kết luận nghiệm thu | [ACCEPTANCE](14-definition-of-done/ACCEPTANCE.md) |

Các file liên kết về nơi chính thay vì duy trì hai bản bảng số liệu độc lập. Không có `GUIDE.md` hoặc bộ hồ sơ song song trong `workflow/docs/` sau khi chuyển cấu trúc.

## Danh mục và kiểm tra tự động

[manifest.json](manifest.json) ghi ID duy nhất, đường dẫn, vai trò, trạng thái tài liệu, mục bắt buộc, trang lý thuyết liên quan và SHA-256 của từng file. File manifest không tự băm chính nó. Mỗi thư mục bước 01–14 phải có hồ sơ trong danh mục; file phát sinh ngoài danh mục là lỗi.

[check.py](check.py) chỉ đọc và kiểm tra: đủ file, không file lạ/ID trùng/khung GUIDE, hash khớp, mục bắt buộc đủ, liên kết cục bộ hợp lệ, dấu giữ chỗ chưa điền, nguồn đầu vào/PNG/JSON kết quả khớp lượt đã lưu, bảng đo khớp log. Hash text chuẩn hóa CRLF/LF để không báo sai do Git trên Windows; PDF và PNG được băm theo byte gốc. Hash giúp phát hiện thay đổi sau lần rà soát, **không thay thế đánh giá nội dung**.

Chạy từ gốc repo:

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python.exe workflow/test_check.py
.\.venv\Scripts\python.exe workflow/check.py
```

PDF đã xóa theo yêu cầu nên không còn là phụ thuộc phải có trong manifest. Tên, hash và trang đã đọc được giữ tại THEORY như nguồn gốc lịch sử, không nhận là đã kiểm tra lại tệp không còn tồn tại. Chương trình không tải nguồn, cài dependency, sửa file hoặc tự cập nhật hash.

## Quy trình kiểm soát thay đổi

1. Chọn đúng file chịu trách nhiệm ở bảng trên; ghi thay đổi yêu cầu/nguồn vào nhật ký trước khi đổi kết luận.
2. Đối chiếu nguồn công khai được dẫn trong THEORY, code và log liên quan; bảng trang PDF là ghi nhận lịch sử vì tệp đã xóa. Nếu code/đầu vào đổi, kết quả cũ chỉ còn là lịch sử.
3. Sửa file và các liên kết/bên tham chiếu bị ảnh hưởng; chỉ ghi “đạt” khi có bằng chứng tương ứng.
4. Chạy test cho checker nếu sửa logic kiểm soát; kiểm tra lại nội dung và cập nhật hash **chỉ các file đã rà soát** trong manifest. Không làm mới toàn bộ hash để che lỗi.
5. Chạy `workflow/check.py`; review diff cả tài liệu lẫn manifest. Ghi giới hạn còn lại trong ACCEPTANCE.
6. Chỉ stage file thuộc phạm vi, kiểm tra staged diff, tuân thủ yêu cầu chạy notebook trước commit của repo và push không dùng force.

Người thực hiện rà soát nội dung/kết quả, trưởng nhóm duyệt phần dùng khi trình bày. Chưa có xác nhận trưởng nhóm duyệt thì không gán trạng thái đó cho hồ sơ.

## Chuyển vị trí hồ sơ cũ

| Vị trí cũ | Vị trí chính mới |
| --- | --- |
| `docs/00_MINDMAP.md` trong workflow | `PROCESS.md` |
| `docs/01_DEFINE.md`, `docs/02_REQUIREMENTS.md` | `01-define/DEFINE.md`, `01-define/REQUIREMENTS.md` |
| `docs/03_DESIGN.md`, `docs/04_BREAKDOWN.md` | `02-design/DESIGN.md`, `03-plan/PLAN.md` |
| `docs/05_TOOLS.md`, `docs/06_VERIFICATION.md` | `07-run/ENVIRONMENT.md`, `08-test/TEST_RESULTS.md`; phát hiện lỗi tách sang REVIEW |
| `docs/07_WORK_LOG.md`, `docs/08_RELEASE.md`, `docs/09_AI_USAGE.md` | `11-commit/WORK_LOG.md`, `14-definition-of-done/ACCEPTANCE.md`, `13-documentation/AI_USAGE.md` |

Đây là chuyển nội dung có đối chiếu, không xóa log lịch sử. Có thể tra bản cũ qua Git; các liên kết đang dùng được cập nhật về vị trí mới.
