# 07 - Hồ sơ chạy demo ngắn

**Mã hồ sơ: RUN. Cập nhật: 14/11/2026.**

## Đầu vào và cách thực thi

Notebook mới chứa Implementation, kiểm chứng, heatmap và so sánh lý thuyết ở mục 1–4; benchmark và assert ở phụ lục. Mã nguồn code SHA-256 `d8332185e0a9a3d5769e5c0f8ba54615035429375374455ef1229f26382f3522` được ghi trong các log mới. Notebook/PNG/JSON gốc đang lưu là kết quả của lượt offline GPU/CPU.

```powershell
$env:PYTHONUTF8 = "1"
$env:HF_HUB_OFFLINE = "1"
.\.venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace self_attention_demo.ipynb
```

Chạy từ gốc repo; kernel trỏ về `.venv`, xem ENVIRONMENT. Tất cả nhận xét số được sinh từ kết quả trong kernel.

## Lần chạy đã quan sát

| Lượt | Kết quả | Bằng chứng |
| --- | --- | --- |
| Offline GPU/CPU, kernel mới | Exit 0, 0 ô lỗi, 17.51s | [Log offline](../evidence/2026-11-14-demo-offline.log) |
| CPU giả lập không GPU, bản sao riêng | Exit 0, 0 ô lỗi, 14.32s | [Log CPU](../evidence/2026-11-14-demo-cpu.log) |
| Mọi row benchmark OOM, bản sao riêng | Exit 0, 0 ô lỗi, 11.32s | [Log OOM](../evidence/2026-11-14-demo-oom.log) |

Hai bản sao kiểm thử nằm trong `scratch/demo-cpu/` và `scratch/demo-oom/`, không ghi đè output nộp. CPU ép `torch.cuda.is_available()` trả False. Luồng OOM thay tạm benchmark bằng row None, khôi phục hàm thật trước assert phụ lục; không gây OOM thật. Các test cấp phát riêng kiểm tra hàm benchmark thật.

## Output được xác nhận

Mỗi lượt xuất 4 PNG và `demo_results.json`. PNG gốc đã được xem trực tiếp từ file; nhãn/thang màu rõ. TEST_RESULTS ghi bảng cùng lượt; JSON giữ cả phương pháp, máy, sai số và head. Log cũ trước sửa được giữ như lịch sử, không dùng cho mã nguồn mới.

## Kiểm tra hiển thị và giới hạn

Người dùng đã dừng Computer Use và yêu cầu tiếp tục không dùng nó. Không thao tác UI nữa, không nhận đã Restart/Run All trong VS Code. Kết quả hiện tại là CLI và kiểm tra PNG; người trình bày có thể tự Run All bằng kernel `.venv`. Tệp trình chiếu đã được bỏ; bốn PNG và JSON kết quả do notebook tạo vẫn được giữ.
