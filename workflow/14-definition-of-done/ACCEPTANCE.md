# 14 - Nghiệm thu demo và hồ sơ

**Mã hồ sơ: ACCEPTANCE. Cập nhật: 14/11/2026.**

## Phạm vi đã được giao

Lượt đầu hoàn thiện workflow theo PDF. Lượt mới mở phạm vi sửa demo cho khớp, thêm Implementation và so sánh Transformer/CNN/RNN, code/giải thích ngắn. Giữ GPT-2, câu mẫu và phép đo GPU/CPU đã chốt; chuyển phần đo/kiểm tra ra phụ lục. Không huấn luyện lại hay sửa PDF/slide.

## Tiêu chí đã kiểm chứng

| Tiêu chí | Kết quả |
| --- | --- |
| Implementation từng phép tính, giải thích đơn giản | Có trong mục 1; không gọi attention dựng sẵn |
| So sánh lý thuyết Transformer/CNN/RNN | Có bảng ngắn ở mục 4 và COMPARISON có nguồn gốc |
| Ma trận khớp GPT-2, tổng hàng/mask đúng cả 12 lớp | Đạt, sai số không nới ngưỡng 1e-4 |
| Nhận xét đúng output | Sinh trực tiếp từ kết quả, không giữ số tĩnh |
| API chọn đầu/vẽ, phương pháp và máy khớp tài liệu | Đã đồng bộ; REVIEW-001–005 được xử lý |
| OOM tại cấp phát/attention và toàn bộ row | Đạt mô phỏng; tiếp tục, có bảng/hình/giải thích hợp lệ; REVIEW-006 được xử lý |
| Toàn notebook offline và nhánh CPU | Đạt CLI, exit 0, không ô lỗi; có log cùng mã nguồn |
| PNG và JSON | 4 hình gốc đã xem, JSON giữ số/phương pháp thật |
| Manifest/file/link/nguồn/bảng số | Được kiểm bằng checker và regression tests trước bàn giao |

## Các điều chưa nhận là hoàn thành

- Chưa xác nhận Restart/Run All trong VS Code: người dùng đã yêu cầu không dùng Computer Use. Không thay chứng cứ UI bằng CLI.
- Không benchmark chất lượng hoặc huấn luyện CNN/RNN; bảng so sánh là lý thuyết theo yêu cầu được hiểu và thông báo.
- Không cố gây OOM thật; chỉ mô phỏng các điểm cấp phát/attention và luồng báo OOM.
- PDF và ảnh slide/nền tối cũ giữ số của lượt lịch sử, không tự cập nhật. Để trình bày số mới, dùng PNG gốc và JSON của notebook.

**Kết luận:** bản demo ngắn và các kiểm tra dòng lệnh đã đạt; còn bước người trình bày tự xác nhận thao tác/hiển thị trong VS Code. Không gán bước này đã đạt.

## Bàn giao và kiểm soát thay đổi

TEST_RESULTS chứa nguồn/log của lượt mới; CONTROL quy định một nơi chính cho từng thông tin. Manifest khóa snapshot gồm notebook, JSON, hình và nguồn hướng dẫn. Run All sau này có thể đổi timing/output nên cần review/cập nhật log/hash tương ứng, không đặt số bằng lượt cũ. Chỉ stage thay đổi được giao; giữ nguyên PDF mới và việc xóa PDF cũ của người dùng. Chỉ báo push main sau khi xác nhận ref remote.
