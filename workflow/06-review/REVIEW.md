# 06 - Kết quả rà soát theo lý thuyết và code

**Mã hồ sơ: REVIEW. Cập nhật: 14/11/2026.**

## Phạm vi và cách đối chiếu

Đọc PDF, notebook/outputs, config/code GPT-2 đang cài và log kiểm tra. Đối chiếu công thức, shape tensor, mask, lựa chọn đầu và cách diễn giải. Đây là hồ sơ phát hiện, không phải tuyên bố đã sửa lỗi ngoài phạm vi tài liệu.

Các điểm lý thuyết dễ nhầm được chốt ở [THEORY](../THEORY.md): √d_k cho từng đầu, mask cộng khác mask nhị phân, GPT-2 pre-LN/không cross-attention, hàm trả đầu ra trước `c_proj`.

## Phần đã có bằng chứng phù hợp

- QKV và sáu phép tính attention hiện rõ trong hàm tự viết; chia √64 đúng kích thước đầu.
- Đối chứng eager GPT-2 dùng cùng hidden state/trọng số; sai số mỗi lớp được assert dưới `1e-4`.
- Quét toàn bộ lớp/đầu theo tiêu chí công khai; lớp 4, đầu 3 được chọn theo index 0, không gán là đại diện toàn model.
- Hai panel dùng cùng Q/K, một có causal mask; kiểm tra số xác nhận vùng tương lai bị triệt tiêu.
- Cache offline và nhánh CPU có log runtime. Không dùng các kiểm tra CLI này để xác nhận mọi chi tiết hiển thị trong VS Code.

## Phát hiện còn mở

| ID | Bằng chứng cụ thể | Ảnh hưởng | Trạng thái |
| --- | --- | --- | --- |
| REVIEW-001 | Nhận xét notebook ghi GPU đỉnh 19.77–636.88 MB; bảng lưu sẵn ghi 497.95–1114.18 MB. Thời gian markdown 0.23/1.00 và 8.05/86.61 ms khác bảng 0.27/0.97 và 8.09/88.17 ms | Người trình bày có thể đọc số của lượt khác | Chưa sửa notebook; cần dùng cùng lượt đo hoặc suy ra nhận xét trực tiếp từ kết quả |
| REVIEW-002 | Văn bản dùng một đầu để khẳng định “chứng minh” tham chiếu/so RNN; con số attention sink chưa có output xác minh riêng | Kết luận vượt mẫu đo | Chưa sửa; thu hẹp về quan sát một lớp/đầu như lưu ý PDF trang 18 |
| REVIEW-003 | GPU đo tổng peak tensor còn sống, CPU chỉ tính `dummy_scores`; phần phương pháp ghi 20 lần nhưng CPU thực tế 10 | Hai đường bộ nhớ không cùng phạm vi; lời mô tả chưa khớp code | Workflow ghi đúng; notebook ngoài phạm vi còn cần đồng bộ |
| REVIEW-004 | Chưa có `plot_attention`; `pick_head` nhận từ, trả `(best,top3)` khác kế hoạch | Không thể gọi API theo chữ ký trong kế hoạch | Ghi rõ API thật; chưa refactor/thay kế hoạch gốc |
| REVIEW-005 | AGENTS và spec/plan gốc còn RTX 4080/cu126; README chỉ ghi GPU laptop chung | Khó xác định máy nghiệm thu | Người dùng đã duyệt RTX 5060/cu128; workflow ghi quyết định, nguồn ngoài phạm vi còn lệch |
| REVIEW-006 | `x`, `w_qkv`, `b_qkv` được cấp phát ngoài `try` | OOM tại đây chưa được bắt | Chưa sửa; phép thử OOM hiện tại chỉ bao phủ lời gọi attention bên trong `try` |
| REVIEW-007 | PDF trang 19 dùng 10,8×; lượt offline kiểm tra mới có số ms khác | Dễ trộn số liệu slide và runtime mới | Workflow tách hai lượt, không chỉnh PDF hoặc ảnh slide |

## Mức độ và hướng giải quyết

REVIEW-001–003 ảnh hưởng trực tiếp phần nhận xét chấm bài, cần xử lý trước khi xác nhận sản phẩm hoàn thành. REVIEW-005 ảnh hưởng hướng dẫn chạy/bàn giao. REVIEW-006 là giới hạn xử lý lỗi cần công khai. REVIEW-004 có thể xử lý bằng sửa API hoặc ghi nhận quyết định phù hợp thiết kế, không cần refactor toàn notebook. REVIEW-007 đã được phân biệt trong hồ sơ nhưng slide chưa được sửa.

Chỉ đóng phát hiện sau khi có thay đổi và kiểm tra liên quan. Mẫu tái hiện/cách kiểm tra ở [DEBUG](../09-debug/DEBUG.md); kết luận sản phẩm ở [ACCEPTANCE](../14-definition-of-done/ACCEPTANCE.md).
