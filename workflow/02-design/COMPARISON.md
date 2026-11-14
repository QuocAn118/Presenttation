# So sánh Transformer, CNN và RNN

**Mã hồ sơ: COMPARISON. Cập nhật: 14/11/2026.**

## Bảng dùng khi trình bày

| Tiêu chí | Transformer | CNN trên chuỗi | RNN |
| --- | --- | --- | --- |
| Phép xử lý chính | Attention giữa các vị trí | Bộ lọc trên cửa sổ cục bộ | Truyền trạng thái theo thời gian |
| Song song trên chuỗi đã có | Tốt qua nhân ma trận | Tốt giữa các vị trí | Phụ thuộc trạng thái bước trước |
| Quan hệ xa | Kết nối trực tiếp qua attention | Mở rộng vùng nhìn bằng lớp/dilation | Truyền qua nhiều trạng thái; LSTM/GRU hỗ trợ ghi nhớ |
| Điểm hạn chế | Attention dày đặc có ma trận N×N | Một lớp chỉ có vùng nhìn hữu hạn | Khó song song theo chiều thời gian |

## Liên hệ demo

Hàm tự viết minh họa cơ chế attention của Transformer và causal mask. Nó không đo chất lượng hoặc tốc độ CNN/RNN; bảng này là so sánh kiến trúc theo lý thuyết. Việc sinh văn bản tự hồi quy vẫn tuần tự theo token, kể cả GPT-2. Không kết luận Transformer luôn tốt/nhanh hơn hai loại còn lại với mọi tác vụ.

## Nguồn

PDF của nhóm trang 3–4 giới thiệu RNN và động cơ self-attention. Phần CNN được bổ sung theo yêu cầu người dùng: [Vaswani et al., mục 4](https://arxiv.org/html/1706.03762v7#S4), [Gehring et al.](https://arxiv.org/abs/1705.03122). Không phục hồi bài huấn luyện IMDB đã bỏ.
