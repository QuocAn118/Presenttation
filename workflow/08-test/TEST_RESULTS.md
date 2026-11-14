# 08 - Kết quả kiểm thử demo mới

**Mã hồ sơ: TEST_RESULTS. Cập nhật: 14/11/2026.**

## Nguồn bằng chứng

Lượt mới dùng notebook đã sửa, với mã nguồn code SHA-256 `d8332185e0a9a3d5769e5c0f8ba54615035429375374455ef1229f26382f3522`. [Log offline](../evidence/2026-11-14-demo-offline.log) ghi cả stdout và Markdown nhận xét; [log CPU](../evidence/2026-11-14-demo-cpu.log), [log all-OOM](../evidence/2026-11-14-demo-oom.log), [test trước sửa](../evidence/2026-11-14-demo-red.log) và [test sau sửa](../evidence/2026-11-14-demo-tests.log) tách riêng. Log không có tiền tố demo là lịch sử bản trước.

## Ma trận kiểm thử

| Mã / AC | Hành vi | Kết quả | Giới hạn |
| --- | --- | --- | --- |
| VERIFY-001 / AC-001 | Môi trường đúng máy đã duyệt | RTX 5060 Laptop GPU, torch 2.9.1+cu128, CUDA 12.8 | Không phải phép đo RTX 4080 |
| VERIFY-002 / AC-002 | So GPT-2 gốc từng lớp | Cả 12 lớp đạt; sai số tối đa **1.76e-06** <1e-4 | Đối chiếu attention, không nhận đầu ra toàn model |
| VERIFY-003–004 | Tổng hàng và causal mask | Assert trong vòng lặp cả 12 lớp đều đạt | Không chỉ lớp cuối như bản cũ |
| VERIFY-005 / AC-003 | Quét đầu minh bạch | Lớp 4, đầu 3; `it→animal` **84.61%** | Một đầu được chọn, không đại diện toàn mô hình |
| VERIFY-006 / AC-005 | Đo 5 độ dài / bộ nhớ | Dữ liệu thật, CPU/GPU đều 20 lần; CPU đếm attention trả về | Phạm vi bộ nhớ hai thiết bị khác nhau |
| VERIFY-007 / AC-006 | CPU giả lập không GPU | Exit 0, 0 ô lỗi, 4 PNG + JSON, **14.32s** | Không thử máy vật lý thiếu GPU |
| VERIFY-008 / AC-007–008 | Offline toàn notebook | Exit 0, 0 ô lỗi, 4 PNG + JSON, **17.51s** | Dùng HF_HUB_OFFLINE=1, không ngắt mạng hệ điều hành |
| VERIFY-009 / AC-004 | Hình/nhãn | Đã xem 4 PNG gốc, chữ rõ, cùng thang màu 0–1, title pretrained | Không nhận đó là UI Run All |
| VERIFY-010 | OOM cấp phát và attention | Test weight/bias/input, attention đều ghi None/đo tiếp; all-OOM toàn notebook exit 0, **11.32s** | OOM mô phỏng, không cố làm đầy VRAM thật |
| AC-009 | Nhận xét đúng lượt | Suy ra trực tiếp từ tensor/kết quả, ghi trong log và JSON | Không ép thời gian bằng slide cũ |
| AC-010 | Restart/Run All trong VS Code | Chưa xác nhận | Người dùng yêu cầu không dùng Computer Use |

## Bảng đo của lượt offline hiện tại

[measurements.json](../evidence/measurements.json) trích đúng các giá trị đã làm tròn trong log. [demo_results.json](../../figures/demo_results.json) giữ số đầy đủ của lượt đang lưu trong notebook; manifest khóa cả nguồn này và PNG.

| N | GPU ms | CPU ms | GPU đỉnh MiB | Một ma trận CPU MiB |
| --- | --- | --- | --- | --- |
| 128 | 0.31 | 0.99 | 496.79 | 0.75 |
| 256 | 0.29 | 2.01 | 502.71 | 3.00 |
| 512 | 0.51 | 5.31 | 526.90 | 12.00 |
| 1024 | 2.36 | 25.49 | 607.15 | 48.00 |
| 2048 | 8.46 | 88.35 | 916.15 | 192.00 |

Ở N=2048, tỷ lệ từ số đầy đủ là **10.45 lần**; phép chia số đã làm tròn trong bảng có thể chênh ở chữ số cuối. PDF trang 19 ghi 10,8× của lượt khác. Một ma trận attention tăng 0.75→3→12→48→192 MiB, đúng 4 lần khi N gấp đôi. GPU peak bao gồm mô hình/tensor nền, không nhất thiết gấp 4 lần.

## Implementation và so sánh

Notebook chính giải thích theo Bước 1–6. Implementation ở Bước 2 tách sáu phép tính nhỏ 2.1–2.6, gồm QKV/chia đầu/√64/mask/softmax/V và kích thước tensor. [Bảng Transformer/CNN/RNN](../02-design/COMPARISON.md) là lý thuyết, không phải huấn luyện hoặc benchmark ba mô hình. Mốc 2048 là tensor nhân tạo, không phải context GPT-2 2048.

Lượt thêm giải thích chỉ sửa Markdown; đã đối chiếu toàn bộ ô code, output và execution count với HEAD trước sửa, không thay đổi. [Lượt chạy offline bản sao](../evidence/2026-11-14-explain-steps.log) thực thi đủ 10 ô code, exit 0, không ô lỗi, 16.81s, xuất đủ bốn PNG và JSON. Không ghi đè số đo snapshot trong bảng trên.

## Kiểm tra tính toàn vẹn hồ sơ

[test_demo.py](test_demo.py) có 8 regression tests về phép tính tay, lỗi input, API, PNG, bộ nhớ CPU thực, OOM và token thiếu. [test_check.py](../test_check.py) có 11 tests về file/link/hash/nguồn/số liệu, gồm cả file nhị phân. [check.py](../check.py) kiểm tra danh mục thực tế và bảng đo với log. Hash không thay cho đánh giá nội dung; kết quả kiểm tra cuối được xác nhận khi bàn giao.
