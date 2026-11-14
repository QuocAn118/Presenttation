# 01 - Xác định bài demo self-attention

**Mã hồ sơ: DEFINE. Cập nhật: 14/11/2026.**

## Bài toán và người sử dụng

Bài môn Deep Learning cần một demo chạy được giúp giảng viên và người thuyết trình theo dõi cơ chế self-attention, tác dụng causal mask, ưu điểm và hạn chế. Ba trọng tâm là code tự viết, hai heatmap trước/sau mask và phần nhận xét. Nộp notebook có output và hướng dẫn chạy qua GitHub.

PDF trang 3–4 đặt vấn đề về xử lý tuần tự và phụ thuộc xa; trang 7–9 giải thích attention; trang 17–19 là phần thực nghiệm của nhóm. Các luận điểm này được chuyển thành demo có phép kiểm chứng, không coi sơ đồ lý thuyết là kết quả thực nghiệm của code.

## What - Sản phẩm cụ thể

- Một [notebook](../../self_attention_demo.ipynb) tự viết từng bước attention bằng PyTorch, nạp **trọng số đã huấn luyện của GPT-2**, không tự huấn luyện.
- Kiểm tra ma trận tự tính với GPT-2 gốc ở 12 lớp, sai số lớn nhất <`1e-4`.
- Ba PNG heatmap gồm hình so sánh và hai panel riêng; một biểu đồ thời gian/bộ nhớ GPU/CPU.
- Hướng dẫn cài môi trường, chạy trong VS Code và kiểm tra offline.
- Mục Implementation ngắn và bảng so sánh lý thuyết Transformer/CNN/RNN theo yêu cầu bổ sung; benchmark ở phụ lục.

## Why - Giá trị của bài

Tự viết Q/K/V, tích vô hướng, chuẩn hóa, mask, softmax và nhân V làm lộ từng phép tính mà API dựng sẵn che đi. Trọng số GPT-2 đã huấn luyện cho ma trận có cấu trúc để quan sát. Đo GPU/CPU bổ sung góc nhìn hiệu năng và chi phí mà giảng viên quan tâm; không thay cho benchmark mô hình hoàn chỉnh.

## When, Where, Which

| Nội dung | Quyết định |
| --- | --- |
| Mốc thuyết trình | 14/11/2026 |
| Nơi chạy | VS Code/Jupyter trên Windows, kernel `.venv` |
| Máy hiện tại | RTX 5060 Laptop GPU; người dùng duyệt thay RTX 4080 ngày 14/11/2026 |
| Mô hình | `gpt2`, 124M tham số, float32, `eval()`, attention eager để lấy đối chứng |
| Câu đầu vào | `The animal didn't cross the street because it was too tired` |
| Khi không có GPU | Notebook chuyển sang CPU; benchmark chỉ báo CPU |
| Khi không có mạng | Dùng cache đã tải trước, kiểm tra bằng `HF_HUB_OFFLINE=1` |

Không tự đổi câu theo dấu nháy/dấu chấm trình bày trên PDF vì sẽ làm thay đổi token. Không thêm BOS.

## Phạm vi và giới hạn

Bài triển khai cơ chế attention bên trong GPT-2 decoder-only, không xây toàn bộ Transformer từ đầu. Embedding, thông tin vị trí, FFN và các khối trước do mô hình gốc cung cấp; cross-attention trong PDF là phần kiến thức nền của encoder–decoder, không phải tính năng còn thiếu của GPT-2.

Ngoài phạm vi: bài IMDB cũ; huấn luyện/fine-tune; bản trọng số ngẫu nhiên để so sánh; encoder–decoder tự viết; giao diện tương tác; thiết kế lại slide. Đầu vào ngẫu nhiên chỉ được dùng trong benchmark chi phí.

## Tiêu chí thành công và trạng thái

Tiêu chí chi tiết có ID ở [REQUIREMENTS](REQUIREMENTS.md). Demo mới có nhận xét sinh từ output, API khớp kế hoạch, OOM được kiểm tra ở cấp phát/attention và toàn notebook chạy đạt; chưa xác nhận Restart/Run All trong VS Code vì người dùng yêu cầu không dùng Computer Use. Đây là khác biệt giữa hoàn tất tài liệu và hoàn tất sản phẩm, được giữ trong [ACCEPTANCE](../14-definition-of-done/ACCEPTANCE.md).
