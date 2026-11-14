# Cơ sở lý thuyết và đối chiếu với bài demo

**Mã hồ sơ: THEORY. Cập nhật: 14/11/2026.**

## Nguồn đã đọc

Đầu vào là `G4_Presentation_TRANSFORMER (1).pdf`, 20 trang, SHA-256 `a9cfc2e1d75a0c71828758ff3aa958416b1096ae52d4e17c8f8449248a898d25`. Số trang dưới đây là thứ tự trang vật lý của PDF, không phải số slide in ở góc. Đã đọc văn bản và xem các trang chứa sơ đồ; phần lớn trang 3–12 là ảnh nên trích xuất text riêng lẻ không đủ.

PDF là tài liệu lý thuyết đầu vào, không phải log của lần kiểm tra mới. Giữ bản PDF người dùng cung cấp ở thư mục gốc khi chạy kiểm tra nguồn; bản này không được tự đưa vào commit workflow.

## Lý thuyết áp dụng vào bài

| Trang PDF | Nội dung | Áp dụng cụ thể |
| --- | --- | --- |
| 3–4 | RNN/LSTM xử lý tuần tự; self-attention nối trực tiếp các vị trí | Giải thích động cơ và phụ thuộc xa; không khôi phục thí nghiệm IMDB đã bỏ |
| 5 | Kiến trúc encoder–decoder tổng quát | Làm nền phân biệt các dạng Transformer; không xem GPT-2 là encoder–decoder |
| 6 | Tokenization, embedding và thông tin vị trí | Tokenizer GPT-2 tách câu chuẩn thành 12 token; mô hình gốc cung cấp hidden state đã mang thông tin vị trí |
| 7–8 | Chiếu Q/K/V, attention, softmax và đọc heatmap | Tự viết phép tính; hàng là Query, cột là Key, màu biểu diễn trọng số sau softmax |
| 9 | Nhiều đầu, ghép đầu và chiếu đầu ra | Dùng 12 đầu, mỗi đầu 64 chiều; hàm demo dừng sau ghép đầu, trước `c_proj` |
| 10 | FFN theo từng token | Giải thích ranh giới attention/FFN; không tự viết lại FFN trong bài demo |
| 11–12 | Masked self-attention, cross-attention, residual và chuẩn hóa | Cài causal mask; đối chiếu điểm khác với khối GPT-2 thực tế |
| 13–16 | Encoder-only, decoder-only, encoder–decoder; BERT/GPT/T5 | GPT-2 thuộc decoder-only, dùng causal self-attention, không có cross-attention trong checkpoint đang nạp |
| 17 | Demo attention tự viết và so GPT-2 | QKV → chia đầu → QKᵀ/√64 → mask → softmax → nhân V; sai số tối đa <`1e-4` |
| 18 | Heatmap trước/sau mask; `it` → `animal` 84,61% | Quét 144 đầu theo tiêu chí công khai, chọn lớp 4/đầu 3 theo chỉ số 0; không đại diện toàn mô hình |
| 19 | Benchmark GPU/CPU, O(N²), phân biệt ma trận và VRAM đỉnh | Dùng log riêng cho mỗi lượt đo; không chép tỷ lệ 10,8× của slide thành kết quả của lượt kiểm tra mới |

Trang 1 là bìa, trang 2 là danh sách nhóm, trang 20 là kết thúc; không dùng tỷ lệ hoàn thành ghi trên slide thành bằng chứng nghiệm thu code hay quy trình.

## Công thức và quy ước chính xác

Với một đầu attention:

$$S=QK^T/\sqrt{d_k},\quad A=\operatorname{softmax}(S+M),\quad O=AV.$$

Trong bài này `d_model=768`, `n_head=12`, `d_k=64`. Vì tính theo từng đầu nên chia **√64=8**, không chia √768. Hình trang 7 dùng ký hiệu √d_model; ở trường hợp một đầu hai kích thước có thể trùng nhau, nhưng áp dụng vào multi-head phải dùng kích thước đầu như trang 17.

Mask cộng `M[i,j]=0` khi `j≤i`, và `-∞` khi `j>i`. Hình mask 0/1 ở trang 11 biểu diễn vị trí được phép/chặn; không cộng nguyên ma trận 0/1 đó vào scores. Sau softmax, tổng hàng xấp xỉ 1 và vùng tương lai bằng 0.

Không mask là phép thử trên **cùng Q và K** của đầu được chọn. Nó không biến GPT-2 thành BERT hoặc chứng minh checkpoint đã được huấn luyện hai chiều.

## Phân biệt lý thuyết tổng quát với GPT-2

| Điểm | PDF | Mô hình/code của bài |
| --- | --- | --- |
| Kiến trúc | Có cả ba dạng Transformer | Chỉ nạp GPT-2 decoder-only |
| Cross-attention | Có trong decoder của encoder–decoder | `add_cross_attention=False`; không tự thêm vào bài |
| FFN | Trang 10 minh họa Linear–ReLU–Linear | Config GPT-2 cục bộ dùng `gelu_new`; FFN không thuộc hàm attention tự viết |
| Vị trí LayerNorm | Trang 12 vẽ Add & Norm phía sau khối con | `GPT2Block.forward` thực tế có `ln_1` trước attention; lấy đúng hidden state sau `ln_1` |
| Đầu ra multi-head | Trang 9 có phép chiếu Wᴼ | Hàm demo trả đầu ra trước `c_proj`; phép đối chiếu chính là ma trận attention |
| Câu minh họa | Trang 18 có dấu câu hiển thị theo slide | Code giữ nguyên câu ASCII trong đặc tả, không tự thêm dấu chấm/BOS vì sẽ đổi token |

Các điểm về GPT-2 được đối chiếu với config cache và code `transformers.models.gpt2.modeling_gpt2` đang cài, không suy ra chỉ từ sơ đồ slide.

## Giới hạn kết luận

Attention cao giữa `it` và `animal` là quan sát của một đầu đã được chọn theo tiêu chí này. Nó không chứng minh toàn bộ cơ chế suy luận, khả năng tổng quát trên nhiều câu hoặc chất lượng vượt RNN/LSTM. Benchmark là hàm attention trên dữ liệu ngẫu nhiên, không phải độ trễ sinh văn bản hay tổng chi phí GPT-2. Các khác biệt số liệu và hạn chế code được ghi trong [review](06-review/REVIEW.md).

## Bổ sung so sánh CNN/RNN và trình bày Implementation

Yêu cầu mới thêm bảng [Transformer/CNN/RNN](02-design/COMPARISON.md) dựa trên nguồn gốc được dẫn ở đó; không coi PDF đã có thí nghiệm CNN. Notebook trình bày Implementation và giải thích ngắn ở mục 1–4, phần chi phí ở phụ lục. Nhận xét được sinh từ output; API/máy/method đã đồng bộ. PDF trang 19 và ảnh slide cũ vẫn mang số lịch sử, không chỉnh để bằng lượt mới.
