# 05 - Triển khai thực tế của demo

**Mã hồ sơ: IMPLEMENTATION. Cập nhật: 14/11/2026.**

## Sản phẩm đã có

Code nằm trong [notebook](../../self_attention_demo.ipynb). Trình tự ô gồm giới thiệu/môi trường, tải GPT-2, câu chuẩn và hàm attention, đối chiếu, quét đầu, vẽ heatmap, benchmark, nhận xét/ưu nhược điểm. Không có module web, API nghiệp vụ hoặc vòng huấn luyện riêng.

Đây là mô tả code hiện có, không nhận rằng mọi dòng được viết mới trong phiên hoàn thiện workflow. Lịch sử được ghi ở [COMMITS](../11-commit/COMMITS.md).

## Các phép tính đã hiện thực

| Bước | Phép tính trong hàm | Liên hệ lý thuyết |
| --- | --- | --- |
| 1 | `qkv = x @ w_qkv + b_qkv`, tách 3 phần | Chiếu Q/K/V, PDF trang 7/17 |
| 2 | View `(T,12,64)`, transpose thành `(12,T,64)` | Multi-head, trang 9/17 |
| 3 | `q @ k.transpose(-1,-2) / sqrt(64)` | Scaled dot-product |
| 4 | Mask `triu(...,diagonal=1)`, gán `-inf` nếu causal | Trang 11/17; không chặn chính token |
| 5 | Softmax theo chiều cuối | Tạo phân phối trên các Key, trang 8 |
| 6 | `attn @ v`, transpose/ghép đầu | Context theo trọng số, trước Wᴼ/`c_proj` |

Hàm tự viết không gọi API attention dựng sẵn. Trọng số lấy từ GPT-2 đã huấn luyện; hidden state đầu vào lấy sau `ln_1`. Việc nạp trọng số không đồng nghĩa tự huấn luyện GPT-2 từ đầu.

## Triển khai hình và benchmark

`find_token` kiểm tra token và báo lỗi tiếng Việt. `pick_head` quét 144 đầu, sắp giảm theo attention `it` → `animal`, trả đầu tốt nhất và top 3. Ô vẽ gọi hàm attention hai lần trên cùng lớp, một lần có mask, một lần không mask; dùng Matplotlib ghi ba PNG.

`benchmark` tạo dữ liệu ngẫu nhiên theo thiết bị, warm-up và đo trung vị trong inference mode. GPU có synchronize, reset peak và max memory allocated; CPU dùng `dummy_scores`. Ô đo chạy CPU và GPU nếu có, in bảng bằng f-string và vẽ hai panel log-scale.

Nguồn PNG gốc là code trong notebook; bản `_dark`, sơ đồ và ảnh tổng quan slide được thêm ở commit riêng. Không coi các ảnh bổ sung là output tự tái tạo của Run All.

## Kiểm chứng và giới hạn hiện có

Log xác minh ma trận ở cả 12 lớp trong ngưỡng, lựa chọn đầu minh bạch, chạy offline và nhánh CPU giả lập thành công. Code có bắt OOM trong `try`, nhưng các cấp phát trước `try` còn có thể làm notebook dừng; không ghi “chịu mọi OOM”.

Nhận xét tĩnh đang có số khác bảng output; một số khẳng định heatmap mạnh hơn bằng chứng. Hai vấn đề này không được che bằng việc mô tả code đúng công thức. Danh sách đầy đủ ở [REVIEW](../06-review/REVIEW.md).

## Thay đổi của nhiệm vụ này

Chỉ triển khai lại hồ sơ workflow và bộ kiểm tra toàn vẹn tài liệu. Không thay các hàm/model/câu mẫu hoặc tạo thêm kết quả thực nghiệm để lấp phần chưa đạt. Những bước Generate/Debug/Refactor code sản phẩm cần được giao riêng trước khi thay đổi notebook.
