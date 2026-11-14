# 07 - Hồ sơ chạy notebook

**Mã hồ sơ: RUN. Cập nhật: 14/11/2026.**

## Đầu vào và cách thực thi

Nguồn là notebook gốc tại commit nền `47246be`, giống bản notebook trên `main` ở `3e594be` trước lần bàn giao workflow. Những lần chạy đã ghi log dùng bản sao để không ghi đè notebook/ảnh nộp bài. Source hash hiện tại được khóa trong manifest; nếu nguồn đổi, không tái sử dụng kết luận runtime cũ như bằng chứng cho code mới.

```powershell
$env:PYTHONUTF8 = "1"
$env:HF_HUB_OFFLINE = "1"
New-Item -ItemType Directory -Force scratch/wf-offline | Out-Null
Copy-Item -LiteralPath self_attention_demo.ipynb -Destination scratch/wf-offline/self_attention_demo.ipynb
.\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace scratch/wf-offline/self_attention_demo.ipynb
```

Đường dẫn làm việc là gốc repo. `PYTHONUTF8=1` tránh lỗi xuất chữ Việt/đường dẫn trong CLI. Kernel notebook phải là môi trường nêu ở [ENVIRONMENT](ENVIRONMENT.md).

## Lần chạy đã quan sát

| Lượt | Input/thao tác | Kết quả | Log |
| --- | --- | --- | --- |
| Offline GPU/CPU | Bản sao nguyên trạng, kernel mới, `HF_HUB_OFFLINE=1` | Exit 0, 0 ô lỗi, 4 PNG; 13.41 giây | [offline](../evidence/2026-11-14-offline.log) |
| CPU giả lập không GPU | Bản sao riêng, thêm ô đầu ép CUDA không khả dụng | Exit 0, 0 ô lỗi, 4 PNG; 12.33 giây | [cpu](../evidence/2026-11-14-cpu.log) |

Nhánh CPU dùng `import torch; torch.cuda.is_available = lambda: False` chỉ trong bản sao/kernel thử nghiệm. Không ghi bản đó vào notebook nộp bài. Đây là giả lập, không phải kết quả đo trên máy vật lý không có GPU.

## Output được xác nhận

Lượt offline nạp được GPT-2 từ cache, token hóa đúng câu, so attention ở cả 12 lớp và in top 3 đầu. Các file `heatmap_compare.png`, `heatmap_no_mask.png`, `heatmap_causal_mask.png`, `cost_gpu_cpu.png` được tạo không rỗng trong thư mục thử nghiệm.

Số liệu đầy đủ được dẫn ở [TEST_RESULTS](../08-test/TEST_RESULTS.md). Warning về tqdm/Jupyter được giữ trong log; không biến warning thành ô lỗi khi exit code và notebook xác nhận chạy thành công.

## Kiểm tra hiển thị và giới hạn

VS Code là môi trường trình bày đã chốt. Chưa hoàn thành xác nhận Restart → Run All rồi quan sát mọi hình: người dùng đã dừng Computer Use bằng Escape. Không thay kết quả UI bằng kết quả CLI và không tự đánh dấu phần này đạt.

Không ngắt mạng hệ điều hành để thử; offline được kiểm tra theo `HF_HUB_OFFLINE=1`. Các bản PNG nền tối/slide không tự tái tạo theo Run All. Việc chạy CLI thành công cũng không chứng minh các nhận xét tĩnh đã đúng số.
