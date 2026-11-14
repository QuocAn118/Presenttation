# 09 - Sửa lỗi và kiểm tra lại

**Mã hồ sơ: DEBUG. Cập nhật: 14/11/2026.**

## Tái hiện trước sửa

Bản cũ thất bại ở API `pick_head`, thiếu `plot_attention`, OOM lúc cấp phát không được bắt và bộ nhớ CPU đếm dummy thay vì ma trận trả về. [Log đỏ](../evidence/2026-11-14-demo-red.log) ghi test chạy trước thay code, gồm lỗi thực tế; không đánh dấu log lịch sử này là lỗi của bản cuối.

## Nguyên nhân và bản sửa

Nhận xét chứa số tĩnh nên drift sau chạy lại: thay bằng Markdown suy ra từ tensor/số đo trong kernel. Không đổi ngưỡng GPT-2 hay chỉnh số đo cho khớp nhận xét cũ. Mô tả heatmap được giới hạn về một câu/lớp/đầu.

Đưa cấp phát weight/bias/input vào vùng `try` cùng attention, dọn tham chiếu sau từng độ dài rồi tiếp tục nếu OOM. CPU lấy kích thước ma trận thật, giữ API attention hai phần tử và ghi rõ phạm vi đo. Hai thiết bị đo 20 lần sau warm-up 3. Bổ sung đúng `plot_attention` và `pick_head(src,tgt)`.

## Bằng chứng sau sửa

[test_demo.py](../08-test/test_demo.py) kiểm tra ví dụ số tính tay, input lỗi, API, PNG, ma trận CPU thực, OOM từng cấp phát/attention và token thiếu. Phụ lục notebook cũng có assert tính tay/OOM. CLI offline, CPU giả lập và tình huống mọi độ dài OOM đều exit 0, xuất hình/JSON và không ô lỗi. Log ở TEST_RESULTS.

## Trường hợp tương lai

Nếu sai số ≥`1e-4`, kiểm tra hidden state sau `ln_1`, weight cùng lớp, reshape/transpose, √64, mask `-inf`, eval/float32. Không nới ngưỡng. Khi nguồn thay đổi, chạy lại kiểm tra liên quan và đồng bộ output/log/manifest trước khi đóng lỗi.
