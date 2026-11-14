# 12 - Giải thích code từng bước

**Mã hồ sơ: CODE_EXPLANATION. Cập nhật: 14/11/2026.**

Các bước dưới khớp tiêu đề trong [notebook](../../self_attention_demo.ipynb). Đọc lời giải thích rồi chạy ô code ngay bên dưới.

## Bước 1 - Chuẩn bị mô hình và câu đầu vào

Nạp **trọng số đã huấn luyện của GPT-2**, chọn GPU nếu có và đặt mô hình ở chế độ đánh giá. Tokenizer đổi câu `The animal didn't cross the street because it was too tired` thành 12 token: `The`, `animal`, `didn`, `'t`, `cross`, `the`, `street`, `because`, `it`, `was`, `too`, `tired`. Vì vậy một token không nhất thiết là một từ. Bỏ ký tự `Ġ` chỉ làm nhãn hình dễ đọc, không đổi token ID.

Kết quả: `input_ids` có shape `(1,12)`. Khi xét một lớp, `get_layer_input` lấy hidden state GPT-2 rồi áp `ln_1`, cho `x` shape `(T,768)`; câu này có `T=12`. Embedding và thông tin vị trí do GPT-2 gốc thực hiện (PDF trang 6).

## Bước 2 - Tự tính self-attention

Đầu vào là `x` cùng weight/bias QKV đã học của lớp đang xét. Công thức: `A = softmax(QKᵀ/√64 + M)`, `O = AV`.

| Bước nhỏ | Làm gì trong code? | Kết quả và ý nghĩa |
| --- | --- | --- |
| 2.1 - Tạo Q, K, V | `(x @ w_qkv + b_qkv).chunk(3, dim=-1)` | Ba tensor `(T,768)`: Q là truy vấn, K để đối sánh, V mang thông tin cần tổng hợp. Cả ba xuất phát từ cùng `x`. |
| 2.2 - Chia đầu | `view(T,12,64).transpose(0,1)` | Mỗi tensor thành `(12,T,64)`, để 12 đầu tính attention riêng. |
| 2.3 - Tính điểm | `q @ k.transpose(-1,-2) / 64**0.5` | Scores `(12,T,T)`: mỗi Query đối sánh mọi Key; chia √64=8 để giữ độ lớn điểm ổn định. |
| 2.4 - Chặn tương lai | `triu(1)` rồi `masked_fill(..., -inf)` nếu `causal=True` | Hàng i chỉ giữ cột j≤i. Với `it` ở index 8, chặn `was`, `too`, `tired` ở cột 9–11. |
| 2.5 - Đổi điểm thành trọng số | `torch.softmax(scores, dim=-1)` | Attention `(12,T,T)`, mỗi hàng tổng bằng 1; cột bị mask có trọng số 0. |
| 2.6 - Tổng hợp và ghép đầu | `attn @ v`, transpose rồi view | Lấy tổng V theo trọng số; `(12,T,64)` ghép thành `out (T,768)`. Hàm trả `(out, attn)`, **chưa qua `c_proj`/Wᴼ**. |

Sáu bước này tương ứng scaled dot-product và multi-head trong PDF trang 7–9/17. FFN, residual và các bước còn lại của Transformer không nằm trong hàm tự viết.

## Bước 3 - Kiểm chứng với GPT-2 gốc

Cho hai cách tính cùng câu, cùng trọng số và đầu vào sau `ln_1`. Vòng lặp đối chiếu ma trận attention của cả 12 lớp với GPT-2 ở chế độ eager. Ba điều phải đạt: sai số lớn nhất <`1e-4`, tổng mỗi hàng bằng 1 và vùng tương lai bằng 0. Dòng in sau ô code cho biết sai số thực; không nới ngưỡng khi có lỗi.

## Bước 4 - Chọn đầu để minh họa

`find_token` tìm vị trí `it` và `animal`; `pick_head` quét 12 lớp ×12 đầu, xếp giảm dần trọng số `it` → `animal` sau mask và in top 3. Lấy đầu cao nhất theo tiêu chí công khai này, dùng chỉ số lớp/đầu bắt đầu từ 0. Đầu được chọn minh họa một quan hệ trong câu, không đại diện mọi đầu của GPT-2.

## Bước 5 - Vẽ và đọc hai heatmap

Tính lại attention trên cùng lớp và `x`/weight với `causal=False` rồi `causal=True`, lấy cùng đầu đã chọn và vẽ cùng thang màu 0–1. Hàng là Query đang xét, cột là Key được chú ý. Đọc hàng `it`, cột `animal`; sau mask, nửa trên đường chéo phải bằng 0.

“Trước mask” là attention **sau softmax khi bỏ mask**, không phải scores thô. Đây là phép thử minh họa; GPT-2 được huấn luyện có causal mask. Nhận xét dưới hình tính trực tiếp từ output, bao gồm mức chú ý tới token đầu nếu có; heatmap không giải thích đầy đủ quyết định mô hình.

## Bước 6 - So sánh và rút ra ưu điểm, hạn chế

Đọc bảng [Transformer/CNN/RNN](../02-design/COMPARISON.md): attention nối trực tiếp các vị trí và tính song song bằng ma trận; CNN dùng cửa sổ cục bộ; RNN truyền trạng thái từng bước. Attention dày đặc cần ma trận N×N, cần thông tin vị trí; GPT-2 sinh văn bản vẫn tuần tự theo token. Đây là so sánh lý thuyết, không phải kết quả huấn luyện ba mô hình.

## Phụ lục - Đo chi phí theo bốn bước

1. Tạo tensor/weight ngẫu nhiên seed 42 cho N=128–2048, 12 đầu ×64 chiều. Không chạy GPT-2 ở context 2048.
2. Chạy làm nóng 3 lần, đo 20 lần mỗi thiết bị và lấy trung vị; GPU đồng bộ CUDA trước/sau bấm giờ.
3. Ghi thời gian và bộ nhớ: CPU đếm một ma trận attention thật; GPU ghi đỉnh tensor gồm cả mô hình. Đơn vị MiB, phạm vi hai phép đo khác nhau. Gặp OOM thì ghi OOM rồi đo tiếp.
4. Đọc bảng/biểu đồ và nhận xét sinh từ số thật. Ma trận float32 cần `12*N*N*4` byte, nên N gấp đôi thì dung lượng một ma trận gấp bốn. Không suy ra tốc độ sinh token hoặc KV cache từ phép đo này.
