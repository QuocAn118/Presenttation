# 11 - Quản lý phiên bản và phạm vi commit

**Mã hồ sơ: COMMITS. Cập nhật: 14/11/2026.**

## Lịch sử được xác nhận

| Commit | Nội dung | Điều chứng minh được |
| --- | --- | --- |
| `091ca78` | Đặc tả/kế hoạch self-attention và AGENTS | Quyết định dự án đã được lưu |
| `55a1ad7` | Môi trường và notebook khung | Sản phẩm Task 1 có trong Git |
| `43d7c10` | Self-attention và đối chiếu GPT-2 | Sản phẩm Task 2 có trong Git |
| `89a2b15` | Heatmap trước/sau mask | Sản phẩm Task 3 có trong Git |
| `7961be7` | Benchmark GPU/CPU | Sản phẩm Task 4 có trong Git |
| `19f3203` | Nhận xét, README, output | Bản Task 5 đã được lưu, không tự chứng minh nghiệm thu đầy đủ |
| `2d15b4c`, `47246be` | Hình nền tối và ảnh tổng quan slide | Ảnh bổ sung được tạo riêng với notebook |
| `6ec834b` trên main | Hồ sơ workflow và log kiểm tra | Lần bàn giao tài liệu trước lần viết lại theo PDF |
| `66089ea` trên main | Hồ sơ từng bước theo PDF và bộ kiểm soát file | Mốc tài liệu trước khi người dùng mở phạm vi sửa demo |
| `23d41e7` trên main | Demo Implementation và so sánh Transformer/CNN/RNN | Mốc sửa code/nhận xét/benchmark và hồ sơ kiểm chứng |
| `b4b1759` trên main | Bỏ tài sản trình chiếu, giữ code/tài liệu/output | Mốc dọn repo theo yêu cầu người dùng |
| `5a74198` trên main | Giải thích Bước 1–6 và sáu phép tính attention | Mốc sửa Markdown, giữ snapshot code/output; có log chạy offline bản sao |

Không dùng tên tác giả commit để suy ra ai tự viết từng dòng hoặc mô hình AI đã dùng. Không dùng lịch sử có commit làm chứng cứ đã TDD/Run All trước từng commit.

## Quyền và kiểm soát phạm vi

AGENTS của repo đã giao commit/push main; chỉ stage phạm vi nhiệm vụ. Lượt đầu chỉ sửa workflow và không stage thay đổi PDF có sẵn của người dùng. Các yêu cầu tiếp theo mở phạm vi sửa demo/nguồn hướng dẫn và sau đó xóa tài sản trình chiếu; những thay đổi đó đã có các commit main riêng ở bảng trên. Không áp trạng thái working tree của lượt cũ cho bản hiện tại.

Trước commit: xem `git status`, xác nhận source không đổi, chạy bộ kiểm soát workflow và kiểm tra whitespace/staged diff. Theo AGENTS, chạy lại toàn notebook trước commit; có thể dùng checkout/worktree riêng để không ghi đè sản phẩm ở workspace người dùng, nhưng phải dùng đúng source.

## Commit và push khi nhánh khác main

Không dùng `git add .` hoặc force push để vượt khác biệt nhánh. Kiểm tra remote và quan hệ commit trước khi push. Nếu workspace đang ở nhánh khác và main đã có merge riêng, đưa **chỉ commit workflow** lên checkout riêng từ `origin/main`, giữ thay đổi ngoài phạm vi tại workspace.

Thông điệp commit mô tả hồ sơ thực tế; nếu lệch kế hoạch do yêu cầu mới, ghi `Quyết định:` với phạm vi đã được người dùng chốt. Chỉ báo đã push sau khi Git trả thành công và kiểm tra ref remote. Hash cuối không tự chèn vào nội dung commit của chính nó; được báo ở bàn giao.

## Trạng thái đối với lượt viết lại hiện tại

Lịch sử trên ghi các mốc đã tồn tại, gồm cả sửa demo, dọn tệp trình chiếu và giải thích từng bước. Commit mới chỉ được báo đã lên main sau khi kiểm tra ref remote; không tự ghi hash của một commit chưa tồn tại vào hồ sơ.
