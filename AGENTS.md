# AGENTS.md

Hướng dẫn cho trợ lý AI làm việc trong repo này, trên máy của thành viên thực hiện (GPU RTX 4080).

## Dự án

Bài môn Deep Learning: so sánh **mốc trung bình embedding, RNN, LSTM, Transformer** trên phân loại cảm xúc IMDB bằng PyTorch. Kết quả gồm số liệu, biểu đồ và phân tích lỗi trong `results/`. Chồng (trưởng nhóm) dùng các biểu đồ này để làm slide thuyết trình. Giảng viên làm ở doanh nghiệp, quan tâm hiệu năng, chi phí và độ trễ.

## Đọc trước khi làm bất cứ việc gì

1. `docs/superpowers/specs/2026-11-01-transformer-vs-rnn-lstm-design.md`: thiết kế (làm gì, vì sao, giới hạn). **Đây là nguồn quyết định cao nhất.**
2. `docs/superpowers/plans/2026-11-01-transformer-vs-rnn-lstm.md`: kế hoạch 7 task. Làm **đúng thứ tự**, đúng tên hàm và tham số đã ghi. Phần "Global Constraints" áp dụng cho mọi task.

Nếu kế hoạch mâu thuẫn với thiết kế thì làm theo thiết kế. Trong tài liệu, chữ "em" là người viết tài liệu. Các bước giao cho "em" hoặc "người thực hiện" là việc của bạn, trừ việc làm slide (của chồng).

Nếu có skill `superpowers:executing-plans` thì dùng nó. Nếu không có, tự làm theo kế hoạch từng task một.

## Cách làm mỗi task

- **Test trước (TDD):** viết test, chạy và thấy nó fail, rồi viết code tối thiểu cho test pass.
- Chạy toàn bộ test (`python -m pytest tests -v`) trước khi commit. Không commit khi còn test đỏ.
- Commit sau mỗi task, đúng message trong kế hoạch (ví dụ `feat: models`), rồi push thẳng lên `main`.

## Lệnh

```bash
nvidia-smi                                   # kiểm tra driver hỗ trợ CUDA 12.6
python -m venv .venv                         # Windows: .venv\Scripts\activate
pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cu126
pip install -r requirements.txt
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"  # phải in True và tên card

python -m pytest tests -v                    # test, chạy trên CPU, không cần mạng
python run.py --quick                        # chạy thử, ghi vào results_quick/
python run.py                                # bản chính thức trên GPU, ghi vào results/
```

Lưu ý: `pip install torch` mặc định trên Windows là bản CPU. Luôn cài bằng `--index-url` như trên.

## Quy tắc bắt buộc

- **Không bịa hay chỉnh số liệu.** Mọi con số trong `results/` và README phải từ lần chạy `python run.py` trên máy RTX 4080 này.
- **Không chỉnh thí nghiệm cho khớp giả thuyết.** Nếu kết quả lệch (ví dụ Transformer không nhanh hơn LSTM, RNN gần như không học), báo đúng thực tế và giải thích.
- **Không đổi siêu tham số.** Embedding 128, dropout 0.1, Adam lr 1e-3, batch 64, 5 epoch, cắt gradient 1.0, seed 42, 1 seed là cố định và dùng chung cho mọi mô hình. Không tinh chỉnh riêng cho mô hình nào.
- **Ngoài phạm vi:** bài toán tổng hợp, bộ dữ liệu khác, mô hình tiền huấn luyện, RNN hai chiều, notebook, slide.
- **Không commit `results_quick/`** và số liệu chạy thử. Chỉ commit `results/` của bản chạy đầy đủ.
- **Test không được tải mạng hay dùng GPU.** Dùng dữ liệu tổng hợp nhỏ, và `monkeypatch` như kế hoạch mô tả.
- Tên hàm và biến bằng tiếng Anh. Thông báo in ra, nhãn biểu đồ và README bằng tiếng Việt.
- Mỗi module một việc, theo cấu trúc trong thiết kế: `config`, `data`, `models`, `train`, `benchmark`, `analysis`, `report`, `run`, cùng `tests/`.

## Khi gặp vấn đề

- **Hết bộ nhớ GPU:** phép đo theo độ dài phải ghi `OOM`, không dừng chương trình. Nếu lỗi hết bộ nhớ xảy ra lúc train chính, dừng lại và báo chồng, không tự giảm batch.
- **Chạy đầy đủ quá 40 phút:** cắt theo thứ tự trong kế hoạch. Trước tiên giảm số mẫu đo thông lượng CPU; sau đó bỏ độ dài 512 trong phép train lại. Ghi rõ phần đã cắt vào README.
- **Kế hoạch có chỗ không làm được, hoặc mâu thuẫn:** chọn cách nhỏ nhất vẫn đúng với thiết kế. Ghi quyết định vào commit message (dòng `Quyết định: ...`), rồi báo chồng.
- **Phải đổi một điều trong mục "Quyết định của chồng" của thiết kế:** không tự đổi. Hỏi chồng trước.

## Bàn giao

Sau khi xong 7 task và chạy bản chính thức:

1. Điền mục "Cấu hình máy" trong README từ `results/results.json`.
2. Viết mục "Kết quả và kết luận" trong README, gồm:
   - bảng "khi nào chọn mô hình nào";
   - nhận xét về hai chế độ attention (chuẩn và tối ưu);
   - hai giới hạn: IMDB chủ yếu dựa vào từ khoá nên không chứng minh chắc chắn phụ thuộc xa; mỗi cấu hình chạy 1 lần nên chênh lệch dưới khoảng 1–2% chưa chắc có ý nghĩa.
3. Commit `results/` và README, push lên `main`, rồi báo chồng.
