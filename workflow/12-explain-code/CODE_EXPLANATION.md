# 12 - Giải thích code bằng câu demo

**Mã hồ sơ: CODE_EXPLANATION. Cập nhật: 14/11/2026.**

## Từ câu chữ tới tensor

Đầu vào là `The animal didn't cross the street because it was too tired`. Tokenizer GPT-2 trả 12 token: `The`, `animal`, `didn`, `'t`, `cross`, `the`, `street`, `because`, `it`, `was`, `too`, `tired`. Nhãn hình bỏ `Ġ` để đọc, không thay token ID. Token không đồng nghĩa một từ: `didn't` thành hai token.

Theo PDF trang 6, mô hình cần embedding và thông tin vị trí. GPT-2 gốc làm phần đó và các khối trước. `get_layer_input` lấy hidden state của lớp đang xét rồi áp `ln_1`; tensor đưa vào hàm tự viết có shape `(12,768)` với câu này.

## Q, K và V làm gì trong code

Q biểu diễn truy vấn của vị trí đang xét; K dùng để đối sánh với truy vấn; V mang thông tin được tổng hợp. Cả ba là phép chiếu học được của cùng hidden state trong self-attention, không phải ba câu khác nhau. `c_attn` gộp ba ma trận chiếu trong một weight/bias, nên code nhân một lần rồi `chunk(3)`.

Chia thành 12 đầu tạo Q/K/V shape `(12,12,64)`: chiều đầu là attention head, chiều thứ hai là vị trí token, chiều cuối là đặc trưng của một đầu. Nhân QKᵀ tạo scores `(12,12,12)`, chia √64 để chuẩn hóa theo kích thước đầu. Công thức tương ứng PDF trang 7/9/17.

## Causal mask và softmax

Với hàng của `it` ở index 8, có mask thì cột 0–8 được phép; cột `was`, `too`, `tired` ở 9–11 bị gán `-inf` trước softmax. Trọng số ba cột này trở thành 0; các cột được phép được chuẩn hóa lại thành tổng hàng 1.

Không mask giữ cùng Q/K và cho phép nhìn mọi cột. Đây là phép minh họa so sánh, không phải cách checkpoint GPT-2 được huấn luyện. Khi đọc heatmap: hàng là Query đang xét, cột là Key được chú ý, màu là trọng số sau softmax; “trước mask” không có nghĩa vẽ scores thô trước softmax.

## Nhân V và ghép đầu

Mỗi hàng attention là bộ hệ số để lấy tổng có trọng số của V. Kết quả theo đầu `(12,T,64)` được transpose/ghép về `(T,768)`. Hàm trả ở đây, **chưa nhân `c_proj`/Wᴼ** trên hình multi-head PDF trang 9. Vì thế phép so chính là attention, không tuyên bố toàn output một block đã giống GPT-2 khi thiếu các bước còn lại.

## Vì sao chọn lớp 4, đầu 3

`pick_head` quét mọi lớp/đầu, tối đa hóa attention từ `it` đến `animal` sau mask. Giá trị được in là 0.8461 (~84.61%), nên dùng đầu đó để minh họa như trang 18. Việc chọn theo mục tiêu này phải công khai; nó không cho thấy mọi đầu đều giải quyết đại từ theo cùng cách.

## Benchmark nói lên điều gì

`benchmark` dùng tensor ngẫu nhiên, không token hóa câu dài hay chạy toàn GPT-2. Ma trận mỗi đầu có N×N phần tử nên 12 đầu float32 cần `12*N*N*4` byte cho một ma trận. N gấp đôi thì kích thước này gấp bốn; GPU có thể xử lý nhân ma trận song song nhưng số nhanh hơn bao nhiêu phải đọc đúng lượt đo trong TEST_RESULTS.

PDF có FFN, residual, chuẩn hóa và các dạng Transformer để giải thích kiến trúc; các phần đó không đều nằm trong hàm attention tự viết. GPT-2 còn sinh token tuần tự khi dùng cho generation, nhưng notebook này không benchmark generation hoặc KV cache. Các giới hạn diễn giải đã được ghi riêng, không gán mọi ưu điểm lý thuyết thành kết quả đã thử.
