# AGENTS.md

Hướng dẫn cho trợ lý AI làm việc trong repo này, trên máy của thành viên thực hiện (GPU RTX 5060 Laptop GPU).

## Dự án

Bài môn Deep Learning: **notebook demo self-attention** tự viết bằng PyTorch, nạp **trọng số đã huấn luyện của GPT-2**, vẽ heatmap attention **trước và sau causal mask**, đo thời gian và bộ nhớ trên GPU và CPU, kèm nhận xét ưu điểm, hạn chế và hướng dẫn chạy. Chồng (trưởng nhóm) thuyết trình ngày **14/11/2026**, chạy notebook trong VS Code trên chính máy này, và dùng hình trong `figures/` để làm slide. Giảng viên làm ở doanh nghiệp, quan tâm hiệu năng, chi phí và độ trễ.

Bài so sánh Transformer với RNN, LSTM trên IMDB **đã bỏ**. Không làm lại.

## Đọc trước khi làm bất cứ việc gì

1. `docs/superpowers/specs/2026-11-10-self-attention-demo-design.md`: thiết kế. **Đây là nguồn quyết định cao nhất.**
2. `docs/superpowers/plans/2026-11-10-self-attention-demo.md`: kế hoạch 5 task. Làm **đúng thứ tự**, đúng tên hàm, tên file đã ghi. Phần "Global Constraints" áp dụng cho mọi task.

Nếu kế hoạch mâu thuẫn với thiết kế thì làm theo thiết kế. Trong tài liệu, chữ "em" là người viết tài liệu; các bước giao cho "người thực hiện" là việc của bạn, trừ việc làm slide (của chồng).

Nếu có skill `superpowers:executing-plans` thì dùng nó; không có thì tự làm từng task một theo kế hoạch.

## Cách làm mỗi task

- Viết ô kiểm tra (`assert`) trước, chạy thấy lỗi, rồi mới viết hàm cho nó chạy đúng.
- Trước khi commit, chạy lại **toàn bộ** notebook từ đầu: `jupyter nbconvert --to notebook --execute --inplace self_attention_demo.ipynb`. Không commit khi còn ô lỗi.
- Commit sau mỗi task, đúng message trong kế hoạch, rồi push thẳng lên `main`.

## Lệnh

```bash
nvidia-smi                                   # kiểm tra driver hỗ trợ CUDA 12.8
python -m venv .venv                         # Windows: .venv\Scripts\activate
pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cu128
pip install -r requirements.txt              # Task 1 tạo file này
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"  # phải in True và tên card
jupyter nbconvert --to notebook --execute --inplace self_attention_demo.ipynb
```

Lưu ý: `pip install torch` mặc định trên Windows là bản CPU. Luôn cài bằng `--index-url` như trên.

## Quy tắc bắt buộc

- **Hàm self-attention phải tự viết** từng bước (Q, K, V, QKᵀ/√d, mask, softmax, nhân V). Không gọi `scaled_dot_product_attention`, `nn.MultiheadAttention` hay attention của GPT-2 trong hàm đó.
- **Ghi rõ "trọng số đã huấn luyện của GPT-2"** ở đầu notebook và trên tiêu đề heatmap. Đây là tiêu chí chấm.
- **Không bịa hay chỉnh số liệu, không viết nhận xét trước khi có hình.** Nhận xét heatmap và chi phí phải đúng với output thật trên máy này.
- **Không chọn lớp, đầu attention lén lút cho đẹp.** Dùng tiêu chí trong kế hoạch và ghi rõ trong notebook.
- **Ngoài phạm vi:** tự huấn luyện hay tinh chỉnh mô hình, thêm bản trọng số ngẫu nhiên, slide, giao diện tương tác, bài IMDB cũ.
- Không đặt `pip install` trong notebook. Chữ giải thích và nhãn hình bằng tiếng Việt; tên hàm, biến bằng tiếng Anh.
- Notebook commit **kèm output** của lần chạy trên máy RTX 5060 Laptop GPU, để mở trên GitHub thấy sẵn hình.

## Khi gặp vấn đề

- **Hết bộ nhớ GPU khi đo:** ghi "OOM", đo tiếp, không dừng notebook.
- **Hàm tự viết lệch GPT-2 gốc quá 1e-4:** đó là lỗi code, sửa cho tới khi khớp. Không nới ngưỡng.
- **Kế hoạch có chỗ không làm được hoặc mâu thuẫn:** chọn cách nhỏ nhất vẫn đúng với thiết kế, ghi dòng `Quyết định: ...` vào commit message, rồi báo chồng.
- **Phải đổi một điều chồng đã quyết** (GPT-2, câu ví dụ, VS Code, đo GPU và CPU, ngày 14/11): không tự đổi, hỏi chồng trước.
- **Có nguy cơ trễ hạn 14/11:** báo chồng sớm, đừng cắt phần nào trong ba phần trọng tâm (code self-attention, hai heatmap, nhận xét ưu điểm và hạn chế).

## Bàn giao

Sau khi xong 5 task:

1. Kiểm tra chạy offline với `HF_HUB_OFFLINE=1` (Task 5).
2. Mở notebook trong VS Code, chạy "Restart" rồi "Run All" một lần, xem mọi hình hiện đúng.
3. Push lên `main`, báo chồng kèm link repo. Trước ngày 14/11, chạy notebook một lần nữa để GPT-2 nằm sẵn trong cache.

## Cập nhật yêu cầu ngày 14/11/2026

- Người dùng duyệt RTX 5060 Laptop GPU/cu128 thay cấu hình RTX 4080/cu126 ban đầu.
- Demo chính ngắn: Implementation self-attention, kiểm chứng, hai heatmap và giải thích đơn giản. Đo GPU/CPU cùng các kiểm tra bổ sung nằm ở phụ lục, không cắt bỏ phần đo đã chốt.
- Bổ sung bảng so sánh **lý thuyết Transformer/CNN/RNN**, không huấn luyện ba mô hình hay làm lại bài IMDB.
- `pick_head(src, tgt)` nhận chỉ số và trả `(layer, head, value)`, tự in top 3; `plot_attention` đúng tên/API trong kế hoạch.
- Nhận xét số liệu được tạo từ kết quả lúc chạy. CPU đếm ma trận attention thật (cùng kích thước/kiểu với scores); GPU ghi đỉnh tensor gồm cả mô hình. Cả hai thiết bị warm-up 3, đo trung vị 20 lần.
- OOM tại cấp phát weight/bias/input và trong attention được bắt, ghi OOM và tiếp tục. PDF/ảnh slide cũ giữ nguyên lượt đo của chúng; không ép số mới bằng số slide.
