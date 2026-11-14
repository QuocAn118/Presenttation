# Nhật ký công việc và quyết định

Nhật ký dùng ngày commit có trong Git và kết quả quan sát được; không gán lại người viết hoặc quy trình chưa có bằng chứng.

## 10/11/2026 — Chốt phạm vi mới

- `6fb733c`: bỏ tài liệu bài Transformer/RNN/LSTM trên IMDB cũ.
- `091ca78`: cập nhật AGENTS, thiết kế và kế hoạch demo self-attention/GPT-2.

## 13/11/2026 — Triển khai đã có trong repo

| Commit | Kết quả |
| --- | --- |
| `55a1ad7` | Môi trường và notebook khung |
| `43d7c10` | Self-attention tự viết và đối chiếu GPT-2 |
| `89a2b15` | Heatmap trước/sau causal mask |
| `7961be7` | Benchmark GPU/CPU |
| `19f3203` | Nhận xét, README và output |
| `2d15b4c` | Bổ sung các ảnh nền tối |
| `47246be` | Bổ sung ảnh tổng quan slide 18 |

Những commit này chứng minh sản phẩm đã được lưu, không chứng minh mọi bước TDD/Run All/offline lịch sử đã được làm. Không khôi phục trạng thái “Chưa bắt đầu” cho các phần đã có code.

## 14/11/2026 — Hoàn thiện riêng hồ sơ workflow

- Người dùng yêu cầu kiểm tra rồi hoàn thiện docs/workflow; sau đó thu hẹp rõ: **“hoàn thiện cái wf cho tui thôi”**.
- Người dùng chốt **RTX 5060 Laptop hiện tại** thay RTX 4080. Ghi DEC-006 trong 03_DESIGN; tài liệu ngoài workflow được giữ nguyên theo phạm vi cuối cùng.
- Các chỉnh sửa thử ở notebook/hình trong phiên đã được hoàn tác; hồ sơ xác minh cuối dùng **notebook gốc**, không dùng bản chỉnh thử để nhận là sản phẩm gốc đã đạt.
- Chạy bản sao gốc với `HF_HUB_OFFLINE=1`: GPU/CPU cùng chạy, exit code 0, 0 ô lỗi, 4 PNG; thời gian 13.41 giây.
- Chạy bản sao riêng, thêm ô ép `torch.cuda.is_available()` trả `False`: toàn notebook chạy CPU, exit code 0, 0 ô lỗi, 4 PNG; thời gian 12.33 giây.
- Kiểm tra riêng lỗi thiếu token và mô phỏng OOM trong attention: đạt. Không chủ động gây OOM thật.
- Đồng bộ Define, Requirements, Design, Breakdown, Tools, Verification, Work Log, Release; bổ sung mục lục và ghi nhận sử dụng AI.
- Người dùng dừng Computer Use bằng Escape; kiểm tra Restart/Run All và toàn bộ hình trong VS Code chưa được xác nhận.
- Giữ nguyên việc xóa PDF đã có sẵn trong working tree; không đưa thay đổi đó vào phạm vi workflow.

## Việc cần làm tiếp cho toàn bộ bài

Xử lý REVIEW-001–006 theo [06_VERIFICATION](06_VERIFICATION.md), chạy lại notebook từ kernel mới sau sửa, kiểm tra trực quan trong VS Code rồi mới đóng checklist nghiệm thu bài. Bản thân hồ sơ workflow đã ghi đầy đủ trạng thái và bằng chứng hiện có.
