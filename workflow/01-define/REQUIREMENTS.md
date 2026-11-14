# Yêu cầu và tiêu chí nghiệm thu

**Mã hồ sơ: REQUIREMENTS. Cập nhật: 14/11/2026.**

## Yêu cầu chức năng

| ID | Yêu cầu của bài | Liên hệ PDF | Đầu ra |
| --- | --- | --- | --- |
| FR-001 | Tự tính Q/K/V, chia đầu, QKᵀ/√d_k, mask, softmax, nhân V | Trang 7, 9, 11, 17 | Hàm `self_attention`, đầu ra trước `c_proj`, ma trận attention |
| FR-002 | Dùng trọng số đã huấn luyện GPT-2 và so attention với mô hình gốc | Trang 17 | Sai số mỗi lớp <`1e-4`, không nới ngưỡng |
| FR-003 | Hai heatmap cùng Q/K, cùng lớp/đầu, trước và sau causal mask | Trang 8, 11, 18 | Hai panel thang 0–1, cùng nhãn token và thanh màu |
| FR-004 | Đo attention trên GPU và CPU với dữ liệu ngẫu nhiên | Trang 19 | Bảng ms/bộ nhớ, hình hai panel theo độ dài 128–2048 |
| FR-005 | Giải thích ưu/nhược điểm, ranh giới lý thuyết/thực nghiệm và cách chạy | Trang 3–16, 19 | Nhận xét khớp output, README, hướng dẫn offline |

## Ràng buộc bắt buộc

`self_attention` không gọi `scaled_dot_product_attention`, `nn.MultiheadAttention` hoặc attention GPT-2. Mô hình gốc chỉ cung cấp trọng số/hidden state và ma trận đối chứng. Input hàm là tensor 2D `(T, 768)` sau `ln_1`; không yêu cầu hỗ trợ batch 3D. Output là `(T, 768)` trước `c_proj` và attention `(12, T, T)`.

Câu chuẩn, không BOS, chỉ số lớp/đầu bắt đầu từ 0. Tiêu chí chọn đầu là attention `it` → `animal` lớn nhất sau mask qua toàn bộ 144 đầu; in top 3. Không tự chọn đầu đẹp bằng mắt rồi trình bày như ngẫu nhiên.

Phần giải thích và nhãn hình dùng tiếng Việt. Đầu notebook và heatmap ghi rõ “trọng số đã huấn luyện của GPT-2”. Không có `pip install` trong notebook. File nộp lưu output của máy chạy thật; không sửa số liệu hoặc nhận xét trước khi có kết quả.

## Tiêu chí có thể kiểm tra

| ID | Điều kiện đạt | Phép kiểm tra | Trạng thái được phép kết luận |
| --- | --- | --- | --- |
| AC-001 | GPU/cu128 khớp máy đã duyệt | In tên GPU, torch, CUDA runtime | Đạt runtime trên RTX 5060 Laptop |
| AC-002 | Ma trận attention khớp ở 12 lớp | `abs(attn-ref).max() < 1e-4` trong vòng lặp | Đạt; giá trị thật ở TEST_RESULTS |
| AC-003 | Định vị đúng token; chọn đầu minh bạch | Kiểm tra `find_token(tokens, word)`, in top 3 | Đạt; có cả phép thử thiếu token |
| AC-004 | Hình đúng cấu trúc và xuất đủ | Sau mask tam giác trên =0; trước mask có phần >0; 3 PNG | Đạt kiểm tra số/file; chưa thay kiểm tra hiển thị bằng CLI |
| AC-005 | Benchmark có đủ năm độ dài và nhãn phương pháp đúng | Bảng GPU/CPU, thời gian trung vị, log-scale | Số đo đạt; diễn giải trong notebook còn mục review |
| AC-006 | Không có GPU vẫn chạy hết | Kernel riêng ép CUDA không khả dụng | Đạt giả lập; chưa thử máy vật lý không GPU |
| AC-007 | Cache đủ cho offline | Kernel mới với `HF_HUB_OFFLINE=1` | Đạt theo log |
| AC-008 | Toàn notebook không có ô lỗi | `nbconvert --to notebook --execute` | Đạt CLI trên bản sao gốc |
| AC-009 | Nhận xét dùng đúng số của cùng lượt và không suy rộng quá mức | Đối chiếu bảng, heatmap, văn bản | Chưa đạt đầy đủ; xem REVIEW |
| AC-010 | Restart/Run All và mọi hình đúng trong VS Code | Kiểm tra UI thực tế | Chưa xác nhận; người dùng đã dừng Computer Use |

## Truy vết từ yêu cầu đến hồ sơ

| Yêu cầu | Thiết kế | Nhiệm vụ | Nghiệm thu |
| --- | --- | --- | --- |
| FR-001–002 | DESIGN: tensor, công thức và đối chứng | TASK-002 | AC-001–002, AC-008 |
| FR-003 | DESIGN: chọn đầu và heatmap | TASK-003 | AC-003–004, AC-009 |
| FR-004 | DESIGN: benchmark và phạm vi phép đo | TASK-004 | AC-005–006 |
| FR-005 | THEORY; CODE_EXPLANATION; DOCUMENTATION | TASK-005 | AC-007–010 |

Nguồn trạng thái là [TEST_RESULTS](../08-test/TEST_RESULTS.md), [REVIEW](../06-review/REVIEW.md) và [ACCEPTANCE](../14-definition-of-done/ACCEPTANCE.md). Bảng này không tự đóng phát hiện chưa sửa.
