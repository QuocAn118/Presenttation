# So sánh Transformer với RNN và LSTM trên IMDB: thiết kế

## Mục đích và lý do

Đây là bài cá nhân môn Deep Learning, nộp bằng **link GitHub**. Bài được chấm qua code Python và buổi thuyết trình trên lớp. Giảng viên làm việc ở doanh nghiệp nên quan tâm chính đến hiệu năng, chi phí và độ trễ. Bộ code xuất ra số liệu và biểu đồ; chồng tự dựng slide từ đó.

Sau phần so sánh, khán giả cần nhớ ba ý. Cả ba là **giả thuyết cần kiểm chứng bằng số liệu**, không phải kết luận định sẵn:

1. Transformer xử lý song song nên train nhanh hơn và bắt phụ thuộc xa tốt hơn RNN, LSTM.
2. LSTM tốt hơn RNN thuần nhờ các cổng, nhưng vẫn yếu dần khi chuỗi dài.
3. Transformer không miễn phí: bộ nhớ tăng O(n²) theo độ dài chuỗi, nên chọn mô hình là bài toán đánh đổi giữa độ chính xác và chi phí.

**Giới hạn đã biết, phải ghi trong README và slide:** cảm xúc trong IMDB chủ yếu nằm ở các từ khoá rải rác, nên thí nghiệm không chứng minh chắc chắn được năng lực phụ thuộc xa. Ý về độ dài chuỗi được kiểm chứng gián tiếp bằng cách train lại ở các độ dài tối đa khác nhau.

## Mục tiêu

- Bộ code PyTorch chạy từ đầu đến cuối bằng **một lệnh duy nhất** (`python run.py`). Kết quả tái lập được.
- So sánh bốn mô hình trên phân loại cảm xúc IMDB: **mốc trung bình embedding**, **RNN**, **LSTM**, **Transformer**. Các tiêu chí:
  - độ chính xác và loss;
  - tốc độ train và bộ nhớ;
  - ảnh hưởng của độ dài chuỗi lên độ chính xác, thời gian và bộ nhớ;
  - độ trễ và thông lượng khi suy luận, trên **cả GPU và CPU của cùng một máy**;
  - bảng đánh đổi giữa accuracy và chi phí. Lời khuyên "khi nào chọn mô hình nào" được viết tay sau khi có số liệu thật;
  - phân tích lỗi ngắn: confusion matrix, review bị đoán sai, accuracy theo độ dài review, các review mà Transformer và LSTM bất đồng.
- Biểu đồ đủ chất lượng để dùng ngay trong slide.

## Không làm

- Không làm bài toán tổng hợp hay bộ dữ liệu nào ngoài IMDB.
- Không làm slide hay kịch bản thuyết trình.
- Không dùng notebook.
- Không dùng mô hình tiền huấn luyện, không tinh chỉnh siêu tham số, không dùng RNN hai chiều.

## Điều tuyệt đối tránh

- Không chỉnh thí nghiệm hay chọn số liệu cho khớp ba giả thuyết. Nếu kết quả lệch, báo đúng thực tế và giải thích.
- Không dùng số liệu bịa hoặc chạy trên máy khác với máy ghi trong kết quả.

## Ràng buộc

- Python, PyTorch, nộp dạng các file `.py` chia module. Có cờ `--quick` để chạy thử nhanh trên CPU trước khi chạy bản đầy đủ trên GPU.
- Dữ liệu: Hugging Face `stanfordnlp/imdb`, cố định phiên bản bộ dữ liệu.
- **Người thực hiện:** một thành viên khác trong nhóm (gọi là "thành viên thực hiện"). Thành viên này viết code, chạy thử, chạy bản chính thức và viết phần kết luận trên máy của mình.
- Máy chạy chính thức: máy của thành viên thực hiện, GPU RTX 4080 (dung lượng VRAM chưa chắc chắn, thiết kế theo mức an toàn 8GB). Thời gian chạy đầy đủ tối đa khoảng 40 phút. Mọi số liệu trong `results/` phải từ máy này.
- Repo tự đủ: README, `requirements.txt`, thư mục `results/` chứa kết quả đã chạy, và thư mục `docs/superpowers/` (đưa lên GitHub).
- Git: chồng tạo repo GitHub. Thành viên thực hiện commit sau mỗi task và push thẳng lên `main`.

## Quyết định của chồng

- Chỉ dùng IMDB. Không làm bài toán tổng hợp. Ghi rõ giới hạn về phụ thuộc xa.
- PyTorch, máy riêng có GPU, nộp file `.py`, không dùng notebook.
- Chạy **1 seed cố định (42)**. Ghi chú trong báo cáo rằng mỗi cấu hình chỉ chạy một lần, nên chênh lệch nhỏ (dưới khoảng 1–2%) chưa chắc có ý nghĩa. `--seeds` vẫn là tham số tuỳ chọn, mặc định 1.
- Đo độ trễ trên cả GPU và CPU.
- Thêm mô hình mốc trung bình embedding.
- Đo thật hai chế độ attention (chuẩn và tối ưu), không suy luận từ tài liệu.
- Đưa `docs/superpowers/` lên GitHub.
- Tự làm slide.
- Thành viên thực hiện code và chạy trên máy RTX 4080 của họ, push thẳng `main`, và viết mục "Kết quả và kết luận" trong README.

## Các lựa chọn kỹ thuật (của em)

**Cấu trúc repo**

| File | Nội dung |
|---|---|
| `config.py` | Siêu tham số chung |
| `data.py` | Dữ liệu |
| `models.py` | Bốn mô hình |
| `train.py` | Huấn luyện và dự đoán |
| `benchmark.py` | Đo tốc độ và bộ nhớ |
| `analysis.py` | Phân tích lỗi |
| `report.py` | Biểu đồ, bảng, JSON |
| `run.py` | Điểm chạy duy nhất |
| `tests/` | Mỗi module một file test |

**Dữ liệu**
- Train 25.000, test 25.000. Tách 2.500 mẫu từ train làm validation.
- Từ điển 20.000 từ phổ biến nhất của phần train (id 0 là padding, 1 là từ lạ). Tách từ bằng regex.
- Giữ 256 từ đầu mỗi review.

**Mô hình**
- Cả bốn mô hình dùng embedding 128 và dropout 0.1 ở embedding và trước lớp phân loại.
- Mốc: trung bình embedding (bỏ padding) rồi qua một lớp tuyến tính.
- RNN, LSTM: một chiều, ẩn 128, dùng `pack_padded_sequence`, lấy trạng thái ẩn cuối.
- Transformer: encoder 2 lớp, 4 đầu, feed-forward 256, kiểu Pre-LN (`norm_first=True`), embedding vị trí học được tối đa 2048, mean pooling bỏ padding.

**Huấn luyện**
- Chung cho mọi mô hình: Adam lr 1e-3, batch 64, 5 epoch, cắt gradient 1.0.
- Accuracy lấy ở epoch có validation tốt nhất (khôi phục trọng số của epoch đó).

**Tái lập**
- Seed 42 cho `random`, `numpy`, `torch`. Bật `cudnn.deterministic`, tắt `cudnn.benchmark`.
- Ghi phiên bản Python, torch, CUDA và tên card vào kết quả. Cố định phiên bản thư viện trong `requirements.txt`.

**Số tham số:** báo hai cột, tổng tham số và tham số không tính embedding.

**Tốc độ train:** giây mỗi epoch, chỉ tính vòng lặp train, kèm epoch đạt validation tốt nhất. Script in thời gian dự kiến sau epoch đầu.

**Độ dài chuỗi, ba phép đo**
- (a) Train lại cả bốn mô hình ở độ dài tối đa 128, 256, 512 (1 seed) và so sánh accuracy.
- (b) Đo thời gian một bước train và bộ nhớ GPU đỉnh ở độ dài 128, 256, 512, 1024, 2048, dữ liệu ngẫu nhiên, batch 8. Transformer đo **hai chế độ attention**:
  - **chuẩn:** ép kernel `MATH` của `scaled_dot_product_attention`, tạo ma trận n×n đầy đủ;
  - **tối ưu:** để PyTorch tự chọn kernel.
  
  Điểm hết bộ nhớ ghi là OOM, không dừng chương trình.
- (c) Accuracy theo nhóm độ dài review gốc: dưới 100, 100–250, 250–500, trên 500 từ. Trên biểu đồ ghi rõ "đã cắt về 256 từ", vì nhóm dài bị mất phần cuối.

**Độ trễ suy luận**
- Đo trên GPU và CPU, với review thật của tập test, độ dài tối đa 256.
- Độ trễ là trung vị với batch 1; thông lượng đo với batch 128.
- Có warm-up, đồng bộ GPU khi đo, dùng `torch.inference_mode`.

**Phân tích lỗi**
- Confusion matrix.
- 3 review sai mà mô hình tự tin nhất, cho mỗi mô hình.
- 3 review Transformer đúng mà LSTM sai, và 3 review ngược lại.

**Đầu ra trong `results/`**
- Hình: `curves.png`, `tradeoff.png`, `scaling.png`, `length_sweep.png`, `length_bucket.png`, `confusion.png`.
- Tài liệu: `summary.md`, `errors.md`.
- `results.json`: chỉ chứa số tổng hợp và cấu hình máy, không lưu xác suất từng mẫu.

**An toàn khi chạy**
- `run.py` dừng với thông báo rõ ràng nếu không thấy GPU, trừ khi dùng `--quick`.
- README hướng dẫn cài PyTorch bản CUDA, vì cài mặc định trên Windows là bản CPU.

## Để người xây quyết

- Tên tham số dòng lệnh phụ, cách trình bày README (đủ các mục: cài đặt, cách chạy, kết quả, cấu hình máy, giới hạn).
- Kiểm thử chạy trên CPU với dữ liệu tổng hợp nhỏ, không tải IMDB.
