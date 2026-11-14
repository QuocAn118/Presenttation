# Hồ sơ kiểm chứng và các điểm còn mở

Cập nhật **14/11/2026 (Asia/Bangkok)**. Kiểm tra trên bản sao nguyên trạng của notebook tại commit nền `47246be`, chạy từ kernel mới. Không chỉnh notebook và ảnh gốc trong phạm vi hoàn thiện workflow.

## Kết quả thực thi

| Mã | Hành vi | Kết quả thực tế | Bằng chứng / giới hạn |
| --- | --- | --- | --- |
| VERIFY-001 | Môi trường GPU | Đạt: RTX 5060 Laptop GPU, torch 2.9.1+cu128, CUDA runtime 12.8 | [Log GPU](../evidence/2026-11-14-offline.log); thay phần cứng theo DEC-006 |
| VERIFY-002 | So attention với GPT-2 ở 12 lớp | Đạt: sai số lớn nhất **1.76e-06**, nhỏ hơn `1e-4` | Assertion mỗi lớp trong notebook; log GPU |
| VERIFY-003 | Tổng mỗi hàng attention | Đạt assertion `allclose(..., atol=1e-5)` | Ô đối chiếu áp dụng assertion tổng hàng lên lớp cuối; không ghi thành đã assert riêng cả 12 lớp |
| VERIFY-004 | Tam giác trên sau causal mask | Đạt: bằng 0 tuyệt đối | Kiểm tra lớp cuối và lớp được chọn vẽ heatmap |
| VERIFY-005 | Token và tiêu chí chọn đầu | Đạt: `animal` ở vị trí 1, `it` ở vị trí 8; lớp 4, đầu 3, **84.61%** | Quét 12×12 đầu, chỉ số bắt đầu từ 0; log GPU |
| VERIFY-006 | Benchmark và kích thước ma trận | Đạt: 5 độ dài, GPU/CPU đều có số; ma trận CPU 0.75→3→12→48→192 MiB | Kiểm tra gấp 4 khi gấp đôi chiều dài; log GPU |
| VERIFY-007 | Nhánh không GPU | Đạt kiểm tra giả lập: Device=cpu; in “Không có GPU, chỉ đo CPU”; không ô lỗi | [Log CPU](../evidence/2026-11-14-cpu.log); không phải thử trên máy vật lý thiếu GPU |
| VERIFY-008 | Offline và toàn notebook | Đạt: `HF_HUB_OFFLINE=1`, exit code 0, **13.41 giây**, 0 ô lỗi | Bản sao notebook gốc; [log offline](../evidence/2026-11-14-offline.log). Bản CPU: **12.33 giây**, exit code 0 |
| VERIFY-009 | Xuất hình | Đạt: mỗi lần chạy tạo đủ 4 PNG không rỗng | Trong thư mục thử nghiệm; không thay PNG được commit trước đó. Chưa kiểm tra trực quan từng hình trong VS Code |
| VERIFY-010 | Nhánh lỗi | Đạt: giả lập attention ném OOM tại hai độ dài → ghi `None` và tiếp tục; thiếu token → `ValueError` tiếng Việt | [Log nhánh lỗi](../evidence/2026-11-14-branches.log); không gây OOM thật |

Lệnh thực tế, đường dẫn bản sao và stdout của các ô notebook đều được lưu trong log. Cách tái lập ở [05_TOOLS](05_TOOLS.md). Warning Jupyter/tqdm được giữ nguyên trong log; các lần chạy kết thúc exit code 0.

## Số liệu của lần kiểm tra offline mới

Đây là **lần kiểm tra riêng**, không phải thay thế bảng output lưu trong notebook gốc. Tỷ lệ dưới đây lấy từ các giá trị ms đã làm tròn trong log.

| N | GPU ms | CPU ms | GPU đỉnh MiB | Một ma trận CPU MiB | CPU/GPU xấp xỉ |
| --- | --- | --- | --- | --- | --- |
| 128 | 0.29 | 1.10 | 497.95 | 0.75 | 3.79× |
| 256 | 0.29 | 1.89 | 506.49 | 3.00 | 6.52× |
| 512 | 0.52 | 5.41 | 540.93 | 12.00 | 10.40× |
| 1024 | 2.32 | 20.03 | 658.18 | 48.00 | 8.63× |
| 2048 | 8.04 | 92.88 | 1114.18 | 192.00 | 11.55× |

Ở N=2048, phép attention tự viết chạy nhanh hơn khoảng 11.55 lần trên GPU trong lượt này. Không suy rộng thành tốc độ toàn bộ GPT-2, sinh token hay chi phí sản phẩm. Hai cột bộ nhớ đo phạm vi khác nhau, không dùng để so mức tiết kiệm bộ nhớ giữa thiết bị.

## Điểm review còn mở ngoài phạm vi workflow

| Mã | Phát hiện có bằng chứng | Ảnh hưởng / hướng xử lý |
| --- | --- | --- |
| REVIEW-001 | Markdown nhận xét notebook ghi GPU đỉnh 19.77–636.88 MB, thời gian 0.23/1.00 và 8.05/86.61 ms; bảng lưu sẵn ghi 497.95–1114.18 MB, 0.27/0.97 và 8.09/88.17 ms | Nhận xét không khớp output. Cần đồng bộ theo cùng lượt chạy hoặc tính nhận xét trực tiếp từ kết quả trước khi nộp |
| REVIEW-002 | Heatmap của một đầu được chọn được dùng để khẳng định “chứng minh” giải quyết tham chiếu và so với RNN/LSTM; con số attention sink chưa có output kiểm chứng riêng | Giữ nhận xét ở mức quan sát một lớp/đầu; không suy ra đầy đủ ngữ nghĩa hay chất lượng so sánh |
| REVIEW-003 | CPU dùng `dummy_scores`, GPU báo toàn bộ bộ nhớ tensor đỉnh gồm cả GPT-2 còn sống; metadata phương pháp ghi 20 lần nhưng CPU thực tế chạy 10 | Cần ghi rõ CPU là dung lượng tensor cùng kích thước, GPU gồm tensor nền, không đo cùng phạm vi; số lần lặp phải thống nhất |
| REVIEW-004 | Không có `plot_attention`; `pick_head` nhận từ và trả `(best, top3)` khác chữ ký trong kế hoạch | Hình vẫn tạo đúng; đã ghi API thực tế ở 03_DESIGN. Chưa đổi code/kế hoạch ngoài workflow |
| REVIEW-005 | AGENTS và đặc tả/kế hoạch ngoài workflow còn RTX 4080/cu126; README chỉ ghi GPU laptop chung | Người dùng đã duyệt RTX 5060 Laptop; hồ sơ workflow đã cập nhật, nguồn ngoài phạm vi còn cần đồng bộ nếu được giao |
| REVIEW-006 | Tạo `x`, `w_qkv`, `b_qkv` ở ngoài `try`; lỗi OOM ở các cấp phát đó không được bắt | Kiểm tra OOM mô phỏng chỉ chứng minh lỗi trong lời gọi attention; chưa bảo đảm notebook luôn tiếp tục với mọi điểm hết bộ nhớ |

## Chưa xác minh

- Người dùng đã dừng Computer Use bằng Escape. Chưa thực hiện xong Restart rồi Run All và kiểm tra trực quan mọi hình trong VS Code; không đánh dấu đạt từ kết quả CLI.
- Chưa chứng minh TDD “assert thất bại trước khi viết hàm” hay nbconvert trước **mỗi** commit lịch sử; commit hiện có không đủ làm bằng chứng.
- Chưa đối chiếu dữ liệu của ảnh `_dark`/ảnh tổng quan slide với lần chạy mới. Notebook không tự tái tạo các bản này.
- Chưa thử mất mạng bằng cách ngắt mạng hệ điều hành; thử offline dùng `HF_HUB_OFFLINE=1` đúng kế hoạch.

## Khi cần debug

Sai số ≥`1e-4`: kiểm tra hidden state sau `ln_1`, thứ tự reshape/transpose, hệ số √64 và causal mask `-inf`; giữ nguyên ngưỡng. OOM: phân biệt cấp phát ngoài `try` và lời gọi được bắt lỗi; không tuyên bố đã bao phủ toàn bộ OOM từ một phép giả lập.
