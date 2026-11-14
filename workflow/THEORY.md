# Cơ sở lý thuyết và đối chiếu với bài demo

**Mã hồ sơ: THEORY. Cập nhật: 14/11/2026.**

## Nguồn đã đọc

Đầu vào là `G4_Presentation_TRANSFORMER (1).pdf`, 20 trang, SHA-256 `a9cfc2e1d75a0c71828758ff3aa958416b1096ae52d4e17c8f8449248a898d25`. Số trang dưới đây là thứ tự trang vật lý của PDF, không phải số slide in ở góc. Đã đọc văn bản và xem các trang chứa sơ đồ; phần lớn trang 3–12 là ảnh nên trích xuất text riêng lẻ không đủ.

PDF là nguồn đã đọc ở lượt trước, không phải log của lần kiểm tra mới. Người dùng yêu cầu bỏ tài sản thuyết trình ngày 14/11/2026 nên tệp PDF đã được xóa; tài liệu kỹ thuật này giữ lại các ý đã đối chiếu, tên/hash/trang nguồn để truy vết. Checker không yêu cầu PDF hiện diện nữa.

Chưa xác minh độc lập tác giả hoặc nguồn xuất bản của PDF nhóm; tên file và hash chỉ nhận diện bản từng được cung cấp. Các nguồn công khai bên dưới hỗ trợ kiểm tra lại nội dung cốt lõi khi PDF không còn trong repo.

## Tài liệu gốc và phạm vi sử dụng

Các nguồn công khai được mở và đối chiếu ngày **14/11/2026**. Bảng này là danh mục nguồn chính; các hồ sơ khác dẫn về đây.

| Mã | Nguồn | Nội dung được dùng |
| --- | --- | --- |
| LT-01 | Vaswani et al. (2017), [Attention Is All You Need](https://arxiv.org/html/1706.03762v7) | Mục 3.2.1, công thức (1): QKᵀ/√d_k, softmax, nhân V; mục 3.2.2: multi-head và Wᴼ; mục 3.2.3: mask; mục 3.5: vị trí; mục 4/bảng 1: so sánh attention, CNN, RNN. |
| LT-02 | Radford et al. (2019), [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) | Mục 2.2–2.3: byte-level BPE, kiến trúc GPT-2, LayerNorm trước khối con và context 1024. Báo cáo cũ ghi bản nhỏ là 117M; [repo OpenAI](https://github.com/openai/gpt-2) đã đính chính lỗi đếm tham số. Demo dùng tên bản phát hành 124M. |
| LT-03 | Gehring et al. (2017), [Convolutional Sequence to Sequence Learning](https://arxiv.org/abs/1705.03122) | Bổ sung CNN trên chuỗi và khả năng tính song song khi huấn luyện; không dùng kết quả của bài báo như benchmark của repo. |
| MH-01 | [Model card GPT-2 trên Hugging Face](https://huggingface.co/openai-community/gpt2), [config](https://huggingface.co/openai-community/gpt2/raw/main/config.json) | Nguồn checkpoint/tokenizer của lệnh `from_pretrained("gpt2")`; model card ghi giấy phép MIT. Cấu hình 12 lớp/12 đầu/768 chiều, `gelu_new`, context 1024 được đối chiếu thêm với cache cục bộ. |
| MH-02 | Hugging Face, [mã GPT-2 trong Transformers v5.22.2](https://github.com/huggingface/transformers/blob/v5.22.2/src/transformers/models/gpt2/modeling_gpt2.py) | Đối chiếu `GPT2Block.forward`, `ln_1`, phép chiếu `c_attn`, attention eager và `c_proj` với bản thư viện đang cài. Hàm trong notebook tự viết các phép tensor theo công thức, không gọi attention này. |
| DO-01 | PyTorch 2.9, [CUDA synchronize](https://docs.pytorch.org/docs/2.9/generated/torch.cuda.synchronize.html), [max memory allocated](https://docs.pytorch.org/docs/2.9/generated/torch.cuda.memory.max_memory_allocated.html) | Đồng bộ GPU trước/sau đo thời gian; đỉnh bộ nhớ tensor PyTorch kể từ lần reset. Không coi đây là toàn VRAM hệ thống hoặc peak RAM CPU. |

Nguồn trọng số đã kiểm tra trên máy: cache `models--gpt2`, ref `main` trỏ snapshot `607a30d783dfa663caf39e06633721c8d4cfcd7e`. SHA-256 của `model.safetensors`: `248dfc3911869ec493c76e65bf2fcf7f615828b0254c12b473182f0f81d3a707`; `config.json`: `0daed7749b4f02b8f76240d5444551d7b08712dab4d0adb8239c56ba823bb7b4`. Đây là định danh cache quan sát được, không phải tuyên bố notebook đã ghim `revision`: code hiện dùng tên `gpt2`; lần tải mới có thể trỏ bản khác. Chạy offline trên cache này giữ đúng bản đã kiểm tra.

## Nguồn hình, số liệu và code

- Bốn PNG trong `figures/` được **Matplotlib vẽ từ code notebook**, không lấy hình minh họa trên Internet hay dùng ảnh AI. Heatmap lấy attention từ trọng số GPT-2 đã huấn luyện; biểu đồ chi phí lấy phép đo tensor ngẫu nhiên trên máy. Các output này được khóa hash trong manifest.
- Số đo, sai số và tiêu chí chọn đầu của bản đang lưu nằm trong [JSON kết quả](../figures/demo_results.json) và [TEST_RESULTS](08-test/TEST_RESULTS.md), đối chiếu [log offline](evidence/2026-11-14-demo-offline.log). Chúng là kết quả repo, không trích số hiệu năng từ các bài báo trên.
- Công thức thuật toán dẫn LT-01; checkpoint và code đối chứng dẫn MH-01/MH-02. Phần hỗ trợ của AI và giới hạn xác nhận quyền tác giả từng dòng được ghi trong [AI_USAGE](13-documentation/AI_USAGE.md); không nhận toàn bộ code là do sinh viên tự viết độc lập.

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

Yêu cầu mới thêm bảng [Transformer/CNN/RNN](02-design/COMPARISON.md) dựa trên nguồn gốc được dẫn ở đó; không coi PDF đã có thí nghiệm CNN. Notebook trình bày giải thích theo Bước 1–6; Implementation có sáu bước nhỏ 2.1–2.6, phần chi phí ở phụ lục. Nhận xét được sinh từ output; API/máy/method đã đồng bộ. Số ghi theo PDF trang 19 là dữ liệu lịch sử đã đối chiếu; tệp trình chiếu và các ảnh dựng riêng đã được bỏ. Không dùng số lịch sử thay số đo mới.
