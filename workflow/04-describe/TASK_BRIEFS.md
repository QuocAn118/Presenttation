# 04 - Mô tả các nhiệm vụ của bài

**Mã hồ sơ: TASK_BRIEFS. Cập nhật: 14/11/2026.**

## Bối cảnh chung

Các brief dưới đây cụ thể hóa [PLAN](../03-plan/PLAN.md), không phải prompt để điền tiếp. Input và hợp đồng thống nhất với [DESIGN](../02-design/DESIGN.md); mỗi task có kết quả kiểm tra riêng. PDF trang 17–19 nối trực tiếp tới Task 2–4; nền lý thuyết nằm ở [THEORY](../THEORY.md).

## TASK-001 - Môi trường và mô hình

- **Input:** Windows, Python, GPU hiện tại, checkpoint `gpt2` và tokenizer từ Hugging Face.
- **File:** requirements, gitignore, README và các ô mở đầu notebook.
- **Output:** `DEVICE`, `model`, `tokenizer`; tên GPU/CPU và phiên bản thực tế.
- **Ràng buộc:** PyTorch 2.9.1+cu128 theo máy được duyệt; không cài thư viện trong notebook; model float32/eval/eager.
- **Chấp nhận:** AC-001 và notebook khởi tạo được từ kernel mới. Môi trường đã xác minh ở ENVIRONMENT; không giả định wheel CPU dùng được CUDA.

## TASK-002 - Tự viết attention và đối chiếu

- **Input:** câu chuẩn không BOS; hidden state sau `ln_1`; weight/bias `c_attn`.
- **File:** ô định nghĩa `get_layer_input`, `get_qkv_weights`, `self_attention` và ô assert.
- **Output:** `(out,attn)`; sai số so GPT-2 ở cả 12 lớp.
- **Hành vi:** QKV → 12 đầu → QKᵀ/√64 → mask `-inf` nếu causal → softmax → nhân V → ghép đầu.
- **Chấp nhận:** AC-002, tổng hàng ~1, vùng tương lai bằng 0. Không nới ngưỡng, không dùng attention dựng sẵn.
- **Quy trình được yêu cầu:** assert trước, chạy thấy lỗi, rồi viết hàm và chạy lại. Hồ sơ hiện tại không có bằng chứng để xác nhận mọi bước lịch sử này đã diễn ra.

## TASK-003 - Heatmap và chọn đầu

- **Input:** tokens, model và hàm Task 2.
- **File:** ô `find_token`, `pick_head`, ô vẽ và ba PNG heatmap.
- **Output:** top 3 đầu, lớp/đầu chính, hình trước/sau cùng thang 0–1.
- **Lỗi cần xử lý:** thiếu `it`/`animal` phải báo rõ bằng tiếng Việt, không chọn nhầm chỉ số.
- **Chấp nhận:** AC-003–004; cùng Q/K của một đầu; trước mask là phép thử minh họa. Cách nhận tham số thực tế của `pick_head` và việc vẽ inline khác kế hoạch đã được ghi, chưa refactor.

## TASK-004 - Hiệu năng và bộ nhớ

- **Input:** tensor/weight ngẫu nhiên seed 42, 12 đầu ×64; N=128/256/512/1024/2048.
- **File:** `benchmark`, ô đo/vẽ và `cost_gpu_cpu.png`.
- **Output:** median ms, bộ nhớ đúng phạm vi mỗi thiết bị, bảng/hình có tên máy và nhãn dữ liệu ngẫu nhiên.
- **Chấp nhận:** AC-005–006; warm-up 3, CPU 10/GPU 20 lần; đồng bộ CUDA; OOM được ghi nhận trong vùng đã bắt lỗi.
- **Giới hạn:** CPU là một tensor tương đương scores; GPU là đỉnh tensor tổng còn sống. Không so hai giá trị như cùng phép đo RAM/VRAM.

## TASK-005 - Nhận xét và bàn giao

- **Input:** hình và số của cùng lượt Task 3–4, cấu hình thật, cache mô hình.
- **File:** markdown nhận xét notebook, README, output cuối và hồ sơ nghiệm thu.
- **Output:** ưu/nhược điểm có dẫn chứng; cách chọn kernel, Restart/Run All và offline; GitHub có output sẵn.
- **Chấp nhận:** AC-007–010. Không chép tỷ lệ 10,8× của PDF sang một lượt benchmark khác.
- **Hiện trạng:** offline/CLI đạt; nhận xét và kiểm tra hiển thị còn mở. Nguồn trạng thái là REVIEW và TEST_RESULTS.

## Nhiệm vụ tài liệu đang được giao

Viết lại các hồ sơ workflow theo PDF, loại bỏ GUIDE và quản lý chặt từng file. Không thực thi các brief sửa code chỉ vì chúng xuất hiện trong tài liệu. Phạm vi thay đổi lần này là workflow, danh mục file và bộ kiểm tra; notebook, hình và nguồn PDF giữ nguyên.
