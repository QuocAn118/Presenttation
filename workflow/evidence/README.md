# Bằng chứng chạy và kiểm tra

## Lượt demo ngắn hiện tại

| File | Nội dung |
| --- | --- |
| [demo-offline](2026-11-14-demo-offline.log) | Chạy notebook đang lưu trên GPU/CPU, offline, có stdout + nhận xét Markdown |
| [demo-cpu](2026-11-14-demo-cpu.log) | Bản sao ép nhánh không GPU |
| [demo-oom](2026-11-14-demo-oom.log) | Bản sao có toàn bộ row OOM, vẫn xuất hình/JSON và chạy hết |
| [demo-red](2026-11-14-demo-red.log) | Regression trước sửa: thất bại như dự kiến, bằng chứng TDD |
| [demo-tests](2026-11-14-demo-tests.log) | Regression sau sửa, mã nguồn mới |
| [explain-steps](2026-11-14-explain-steps.log) | Chạy lại offline sau khi giải thích Bước 1–6, giữ snapshot số đo gốc |
| [source-audit](2026-11-14-source-audit.log) | Rà soát lý thuyết/nguồn, đối chiếu snapshot và chạy lại offline sau khi bổ sung trích dẫn |
| [measurements](measurements.json) | Bảng số đã làm tròn, đối chiếu demo-offline và TEST_RESULTS |

[figures/demo_results.json](../../figures/demo_results.json) giữ số chưa làm tròn, phương pháp, cấu hình và sai số của lượt chính. Log ghi mã nguồn code SHA-256 để phân biệt các bản; mã nguồn của bản sao CPU/OOM được sửa tạm như RUN mô tả.

## Lịch sử trước khi sửa demo

[offline cũ](2026-11-14-offline.log), [CPU cũ](2026-11-14-cpu.log), [nhánh lỗi cũ](2026-11-14-branches.log) thuộc bản trước (nền code 47246be). Giữ nguyên kết quả lịch sử; không dùng bảng cũ để giải thích output mới. Thời gian cũ 13.41/12.33 giây không phải thời gian của demo ngắn mới.

## Tái lập kiểm tra

Từ gốc repo: `python workflow/08-test/test_demo.py` kiểm tra hàm gốc được trích trực tiếp từ notebook bằng AST, không tạo module sản phẩm riêng. Notebook cũng có assert ở phụ lục. Cách chạy đầy đủ và các bước mô phỏng tại [RUN](../07-run/RUN.md). Manifest kiểm soát file/link/nguồn và dữ liệu số; không làm mới hash để che số liệu chưa được kiểm chứng.
