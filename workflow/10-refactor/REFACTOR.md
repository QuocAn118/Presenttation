# 10 - Quyết định về refactor

**Mã hồ sơ: REFACTOR. Cập nhật: 14/11/2026.**

## Vấn đề cấu trúc đã xác định

Kế hoạch gốc có `plot_attention`, nhưng code vẽ đang viết trực tiếp và lặp cấu hình trục cho ba PNG. Điểm này đã được xử lý bằng `plot_attention` trong lượt sửa demo được giao. Hàm attention vẫn ngắn và hiện rõ phép tính, phù hợp mục đích PDF trang 17; không cần tách module hay thêm lớp chỉ để đủ kiến trúc.

Trong tài liệu cũ, GUIDE là hướng dẫn thao tác chung còn hồ sơ dự án nằm song song ở `workflow/docs/`. Việc người dùng yêu cầu là chuyển thành nội dung bài theo từng bước và kiểm soát từng file, nên refactor **tài liệu** là phần thực hiện của phiên này.

## Thay đổi tài liệu đã chọn

- Thay GUIDE bằng file kết quả cụ thể trong thư mục bước tương ứng.
- Chuyển nội dung hồ sơ cũ vào file chịu trách nhiệm; bỏ bản trùng sau khi cập nhật liên kết.
- Giữ log và tách dữ liệu đo máy đọc được; THEORY là nơi đối chiếu PDF, TEST_RESULTS là nơi chính cho bảng đo.
- Dùng manifest/hash, kiểm tra liên kết và đối chiếu số với log để phát hiện chỉnh sửa chưa được rà soát.

Bảng chuyển vị trí và quy trình đổi file ở [CONTROL](../CONTROL.md). Lượt hồ sơ ban đầu giữ nguyên code; lượt yêu cầu mới đã sửa notebook/PNG và nguồn hướng dẫn, PDF/slide giữ nguyên lịch sử.

## Các refactor code đã chọn

| Đề xuất | Lợi ích | Quyết định |
| --- | --- | --- |
| Tách `plot_attention` | Gom cấu hình hình và khớp tên trong kế hoạch | Đã làm đúng tên/chữ ký của kế hoạch |
| Tính nhận xét chi phí từ kết quả | Tránh số tĩnh lệch lượt chạy | Đã triển khai Markdown tính từ dữ liệu lúc chạy |
| Tách attention thành package/classes | Không giúp giảng viên xem từng bước rõ hơn | Không đề xuất cho bài hiện tại |

## Bất biến phải giữ khi sửa code sau này

Câu chuẩn không BOS; trọng số pretrained; tự viết QKV/mask/softmax; chia √64; đầu ra trước `c_proj`; sai số <`1e-4`; tiêu chí quét đầu và thang màu 0–1; lỗi có thông báo rõ; nhánh CPU/offline. Mọi refactor phải chạy lại kiểm tra chịu ảnh hưởng và notebook từ kernel mới. Các thay đổi code có regression tests và log thực thi riêng, không chỉ mô tả trên giấy.
