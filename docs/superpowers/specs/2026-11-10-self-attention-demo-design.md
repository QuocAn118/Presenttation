# Demo self-attention và causal mask: thiết kế

## Mục đích và lý do

Bài môn Deep Learning, nộp bằng **link GitHub**, chấm qua code và buổi thuyết trình trên lớp. Giảng viên làm ở doanh nghiệp nên quan tâm hiệu năng, chi phí, độ trễ. Giảng viên đã đổi yêu cầu, bài **chỉ** gồm:

| Hạng mục | Yêu cầu của giảng viên |
|---|---|
| Demo và nhận xét | Thực hiện self-attention bằng Python/PyTorch; nêu ưu điểm và hạn chế |
| Hình | Attention heatmap **trước và sau** causal mask |
| Tiêu chí | Demo chạy được; nêu rõ dùng trọng số ngẫu nhiên hay mô hình đã huấn luyện |
| Nộp | Notebook demo kèm hướng dẫn chạy |

Trên lớp, chồng mở notebook và chạy lần lượt từng ô. Giảng viên được xem toàn bộ, nhưng **trọng tâm là ba phần trên**: code self-attention, hai heatmap, phần nhận xét. Các phần khác chỉ làm nền và phải ngắn.

## Cách làm đã chốt

**Tự viết self-attention bằng PyTorch, nạp trọng số đã huấn luyện của GPT-2 (bản nhỏ, `gpt2`, 124M tham số) vào.**

- Code attention là của mình: chiếu Q, K, V, nhân Q·Kᵀ, chia √d, (tuỳ chọn) causal mask, softmax, nhân V. Giảng viên phải nhìn thấy từng bước này trong notebook, không gọi hàm attention dựng sẵn.
- Trọng số Q, K, V lấy từ một lớp của GPT-2 đã huấn luyện, nên heatmap có cấu trúc thật chứ không phải nhiễu.
- **Notebook ghi rõ ngay đầu và ở chú thích hình: "trọng số đã huấn luyện của GPT-2", không phải trọng số ngẫu nhiên.**
- **Chứng minh code đúng:** so ma trận attention của hàm mình viết với ma trận attention mà GPT-2 gốc trả về cho cùng lớp, cùng đầu; in ra sai số lớn nhất (phải rất nhỏ, cỡ 1e-5) và `assert`.
- GPT-2 vốn được huấn luyện **có** causal mask. Heatmap "trước mask" là cùng Q, K nhưng bỏ mask, để minh hoạ token nhìn được cả tương lai; phải ghi rõ đây là phép thử minh hoạ, mô hình chưa từng chạy như vậy khi huấn luyện.

## Câu ví dụ

`The animal didn't cross the street because it was too tired`

Giữ câu tiếng Anh đã chốt để token và phép đối chiếu không thay đổi. Ý muốn khán giả thấy: từ "it" chú ý mạnh vào "animal". Nhãn trục heatmap là các token GPT-2 tách ra (ví dụ "didn", "'t"), hiển thị dễ đọc (bỏ ký tự khoảng trắng đặc biệt `Ġ`).

## Nội dung notebook (theo thứ tự)

1. **Giới thiệu** (markdown ngắn): bài làm gì, dùng trọng số đã huấn luyện của GPT-2.
2. **Cài đặt và tải mô hình.**
3. **Hàm self-attention tự viết** — phần trọng tâm, có chú thích tiếng Việt từng bước và công thức `softmax(QKᵀ/√d + M)·V`.
4. **Kiểm tra khớp với GPT-2 gốc** (sai số lớn nhất + `assert`).
5. **Hai heatmap trước và sau causal mask**, đặt cạnh nhau, cùng thang màu. Sau mask, nửa trên đường chéo phải bằng 0.
6. **Nhận xét heatmap**: "it" chú ý vào đâu; sau mask mỗi token chỉ nhìn được chính nó và các token trước; token đầu nhận nhiều attention (hiện tượng "attention sink" của GPT-2) — viết đúng những gì heatmap thật cho thấy, không viết trước.
7. **Đo thật tốc độ và bộ nhớ** (chồng đồng ý): chạy hàm tự viết với đầu vào ngẫu nhiên (cùng số đầu và kích thước như GPT-2: 12 đầu, mỗi đầu 64), độ dài 128, 256, 512, 1024, 2048, **trên cả GPU và CPU** (chồng muốn dùng GPU của máy RTX 5060 Laptop GPU).
   - Thời gian: trung vị nhiều lần chạy, có chạy làm nóng trước; trên GPU phải đồng bộ (`torch.cuda.synchronize`) trước khi bấm giờ.
   - Bộ nhớ GPU: bộ nhớ đỉnh thật (`torch.cuda.reset_peak_memory_stats` rồi `torch.cuda.max_memory_allocated`), MB.
   - Bộ nhớ CPU: dung lượng ma trận attention thực trả về (`nelement() * element_size()`, cùng shape/dtype với scores), MB.
   - Một biểu đồ hai panel (thời gian, bộ nhớ theo độ dài), mỗi panel hai đường GPU và CPU, ghi rõ "dữ liệu ngẫu nhiên, chỉ để đo chi phí" cùng tên GPU, CPU. Nhận xét ngắn theo số thật: ví dụ độ dài gấp đôi thì bộ nhớ gấp khoảng bốn lần (O(n²)); GPU nhanh hơn CPU bao nhiêu lần.
   - Phải chạy xong trong khoảng một phút; nếu CPU chậm thì bỏ bớt độ dài lớn nhất ở CPU và ghi chú lại. Hết bộ nhớ thì ghi "OOM", không dừng notebook.
   - Máy không có GPU thì chỉ đo CPU và in thông báo, không lỗi.
8. **Ưu điểm và hạn chế của self-attention** (markdown, ý chính ở mục dưới; phần O(n²) dẫn chứng bằng số đo ở bước 7).
9. **Hướng dẫn chạy** cũng nằm trong README.

## Ý chính cho phần ưu điểm và hạn chế (thành viên viết thành văn, có thể dẫn chứng từ heatmap)

**Ưu điểm**
- Tính toàn bộ chuỗi cùng lúc bằng phép nhân ma trận, chạy song song tốt trên GPU; RNN phải đi tuần tự từng bước.
- Hai token bất kỳ nối trực tiếp với nhau qua một bước, nên bắt được phụ thuộc xa (ví dụ "it" → "animal") dễ hơn RNN, LSTM.
- Trọng số chú ý thay đổi theo ngữ cảnh từng câu; nhiều đầu (multi-head) bắt được nhiều kiểu quan hệ khác nhau.
- Có thể vẽ heatmap để nhìn phần nào cách mô hình liên kết các từ.

**Hạn chế**
- Thời gian và bộ nhớ tăng O(n²) theo độ dài chuỗi (ma trận n×n). Với doanh nghiệp: ngữ cảnh dài làm tăng chi phí GPU và độ trễ.
- Tự thân không biết thứ tự từ, phải thêm thông tin vị trí (positional embedding).
- Với causal mask, khi sinh văn bản vẫn phải sinh tuần tự từng token, nên độ trễ sinh câu dài vẫn cao (thường dùng KV cache để giảm).
- Heatmap attention không phải lời giải thích đầy đủ cho quyết định của mô hình; chỉ là một lớp, một đầu trong nhiều lớp, nhiều đầu.

**Vì sao cần causal mask:** mô hình sinh văn bản (như GPT-2) học đoán từ tiếp theo; nếu được nhìn tương lai thì nó "chép đáp án". Mask chặn điều đó bằng cách đặt điểm của các vị trí tương lai là −∞ trước softmax. Mô hình hiểu câu hai chiều (như BERT) thì không dùng mask này.

## Không làm

- Không làm lại phần so sánh Transformer với RNN, LSTM trên IMDB (đã bỏ).
- Không tự huấn luyện mô hình, không tinh chỉnh GPT-2.
- Không thêm bản trọng số ngẫu nhiên để so sánh.
- Không làm slide (chồng tự làm từ hình xuất ra).
- Không làm giao diện tương tác hay công cụ ngoài notebook.

## Điều tuyệt đối tránh

- Không gọi hàm attention dựng sẵn (`scaled_dot_product_attention`, `nn.MultiheadAttention`) trong hàm tự viết; chỉ được dùng GPT-2 gốc ở bước kiểm tra.
- Không chọn lớp, đầu attention lén lút cho đẹp: tiêu chí chọn phải ghi rõ trong notebook (xem mục dành cho người xây).
- Không viết nhận xét heatmap trái với hình thật.

## Ràng buộc

- **Người thực hiện:** thành viên khác trong nhóm (gọi là "thành viên thực hiện") viết notebook theo tài liệu này; em chỉ soạn tài liệu. Thành viên commit và push thẳng `main` của repo GitHub chồng tạo.
- **Thuyết trình ngày 14/11/2026**, chạy trên **máy RTX 5060 Laptop GPU của thành viên thực hiện**, mở file `.ipynb` bằng **VS Code** (quyết định của chồng). Notebook phải xong, đã chạy và push trước ngày đó. Hướng dẫn chạy viết cho VS Code: cài extension Jupyter và Python, tạo venv, cài PyTorch bản CUDA (`pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cu128`, vì cài mặc định trên Windows là bản CPU), cài `requirements.txt`, chọn kernel venv.
- Notebook tự dùng GPU nếu có, không có thì chạy CPU, nên máy nào cũng chạy được. Output lưu trong notebook là của lần chạy trên máy RTX 5060 Laptop GPU.
- Cần mạng để tải GPT-2 một lần (khoảng 500MB) từ Hugging Face. README dặn chạy notebook một lần trước giờ thuyết trình để mô hình được lưu sẵn trong cache, phòng khi lớp không có mạng (lựa chọn của em).
- Cài thư viện theo README, không đặt lệnh `pip install` trong notebook (lựa chọn của em).
- "Restart & Run All" phải chạy hết không lỗi. Notebook lưu kèm output (hình hiện sẵn khi mở trên GitHub).
- Lưu hai heatmap và biểu đồ đo chi phí ra file PNG để chồng dùng làm slide.
- Chữ giải thích, chú thích hình bằng tiếng Việt; tên biến tiếng Anh.
- Cố định phiên bản thư viện trong `requirements.txt`.

## Repo và quy trình

- Làm trong **cùng repo GitHub hiện tại**, push thẳng `main`. Các file của bài IMDB cũ đã bị xoá theo quyết định của chồng; AGENTS.md sẽ được viết lại cho bài này (lựa chọn của em).
- Không cần bộ `pytest` riêng: bước kiểm tra khớp với GPT-2 gốc (`assert`) trong notebook là phép kiểm thử chính (lựa chọn của em).

## Chi tiết kỹ thuật (lựa chọn của em)

- Đầu vào của hàm tự viết là hidden state của lớp đã chọn **sau `ln_1`**, chiếu qua `c_attn` của lớp đó để ra Q, K, V.
- Để lấy ma trận attention gốc làm đối chứng, tải GPT-2 với `attn_implementation="eager"` và `output_attentions=True`.
- Không thêm token BOS, để các token khớp đúng câu ví dụ.

## Để người xây quyết

- Chọn lớp và đầu attention cho heatmap chính, miễn ghi rõ tiêu chí trong notebook. Gợi ý: quét mọi lớp, mọi đầu, lấy đầu có attention từ "it" sang "animal" lớn nhất (sau mask), và in ra con số đó.
- Tên file notebook, tên file PNG, bố cục README (đủ: cài đặt, cách chạy, mô tả ngắn).
- Phiên bản thư viện cụ thể (ghim đúng bản đã cài và chạy được).

## Cập nhật yêu cầu ngày 14/11/2026

- Người dùng duyệt RTX 5060 Laptop GPU/cu128 thay cấu hình RTX 4080/cu126 ban đầu.
- Demo chính ngắn: Implementation self-attention, kiểm chứng, hai heatmap và giải thích đơn giản. Đo GPU/CPU cùng các kiểm tra bổ sung nằm ở phụ lục, không cắt bỏ phần đo đã chốt.
- Bổ sung bảng so sánh **lý thuyết Transformer/CNN/RNN**, không huấn luyện ba mô hình hay làm lại bài IMDB.
- `pick_head(src, tgt)` nhận chỉ số và trả `(layer, head, value)`, tự in top 3; `plot_attention` đúng tên/API trong kế hoạch.
- Nhận xét số liệu được tạo từ kết quả lúc chạy. CPU đếm ma trận attention thật (cùng kích thước/kiểu với scores); GPU ghi đỉnh tensor gồm cả mô hình. Cả hai thiết bị warm-up 3, đo trung vị 20 lần.
- OOM tại cấp phát weight/bias/input và trong attention được bắt, ghi OOM và tiếp tục. Theo yêu cầu mới, tệp thuyết trình và ảnh dựng riêng đã được bỏ; giữ code, tài liệu kỹ thuật và bốn PNG/JSON output của notebook.
