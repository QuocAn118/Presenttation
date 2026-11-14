# 09 - Hồ sơ lỗi và phương án xác minh

**Mã hồ sơ: DEBUG. Cập nhật: 14/11/2026.**

## Hiện trạng

Notebook chạy hết bằng CLI, nhưng “không ô lỗi” chưa đồng nghĩa mọi nhận xét và xử lý biên đều đúng. Các phát hiện chính thức nằm ở [REVIEW](../06-review/REVIEW.md); file này ghi cách tái hiện và kiểm tra để đóng chúng, không nhận là đã sửa code ngoài phạm vi.

## Lệch số liệu nhận xét

**Kỳ vọng:** markdown và bảng output nói cùng một lượt đo. **Thực tế:** số peak GPU và ms trong nhận xét khác bảng đang lưu. **Vị trí:** ô nhận xét chi phí và ô bảng benchmark trong notebook. **Bằng chứng:** REVIEW-001 nêu cặp số cụ thể.

Sự không khớp đến từ văn bản tĩnh chứa bộ số khác output; chưa có đủ lịch sử để khẳng định chính xác ai/sự kiện nào tạo ra bộ số cũ. Phương án nhỏ nhất khi được giao sửa: dùng số từ một lượt duy nhất, ghi rõ cấu hình, hoặc tính nhận xét từ `res_cpu/res_gpu`. Kiểm tra lại khi kernel mới chạy và khi nhánh GPU không có kết quả; không chỉ sửa một con số rồi giữ các tỷ lệ suy ra cũ.

## Kết luận heatmap vượt bằng chứng

**Kỳ vọng:** đúng lưu ý PDF trang 18, một đầu không đại diện mô hình. **Thực tế:** nhận xét trong notebook dùng quan sát chọn lọc để khẳng định mạnh về tham chiếu/so RNN. Phương án: giới hạn mô tả ở lớp/đầu/câu đã thử; chỉ nêu attention sink định lượng nếu có phép tính tương ứng. Không tạo thêm thí nghiệm IMDB để hợp thức hóa kết luận.

## OOM chưa được bắt ở mọi cấp phát

**Kỳ vọng:** benchmark ghi OOM và đo tiếp thay vì dừng notebook. **Thực tế:** lời gọi attention nằm trong `try`, nhưng cấp phát `x`/weight/bias ở ngoài. Phép giả lập hiện tại chứng minh nhánh bên trong hoạt động, không bao phủ hết đường lỗi.

Khi được giao sửa, đưa các cấp phát liên quan vào vùng xử lý lỗi phù hợp; xem lại biến tham chiếu và khả năng tiếp tục sau lỗi. Dùng mô phỏng ở cả cấp phát và attention thay vì cố làm đầy VRAM máy demo. Không nới độ dài xuống rồi nhận là đã xử lý OOM.

## Khi sai số GPT-2 không đạt

Sai số thực tế hiện đạt ngưỡng. Nếu một thay đổi tương lai làm `diff≥1e-4`, kiểm tra theo thứ tự: cùng hidden state sau `ln_1` → đúng weight/bias cùng lớp → reshape/transpose → chia √64 → mask tương lai `-inf` trước softmax → chế độ eval/float32. Giữ nguyên ngưỡng. Không coi việc nạp lại model hoặc đổi đầu cho sai số nhỏ là sửa nguyên nhân.

## Điều kiện đóng lỗi

Phải có diff đúng phạm vi, ca tái hiện đã kiểm tra lại, log tương ứng với source mới và cập nhật REVIEW/TEST_RESULTS/ACCEPTANCE. Lần hoàn thiện workflow này ghi hồ sơ và kiểm soát nguồn; các bản sửa notebook nêu trên chưa được thực hiện.
