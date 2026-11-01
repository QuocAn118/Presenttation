# So sánh Transformer / RNN / LSTM trên IMDB: kế hoạch triển khai

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bộ code PyTorch chia module, chạy bằng `python run.py`, so sánh mốc trung bình embedding, RNN, LSTM, Transformer trên IMDB, xuất biểu đồ, bảng, phân tích lỗi vào `results/`.

**Architecture:** Mỗi module một việc (`config`, `data`, `models`, `train`, `benchmark`, `analysis`, `report`) và `run.py` ghép lại. Mỗi module có một file test trong `tests/`, chạy trên CPU với dữ liệu tổng hợp nhỏ. IMDB chỉ được tải khi chạy `run.py`.

**Tech Stack:** Python, PyTorch (bản CUDA khi chạy chính thức), `datasets` (Hugging Face), numpy, matplotlib, pytest.

**Spec:** `docs/superpowers/specs/2026-11-01-transformer-vs-rnn-lstm-design.md`

## Global Constraints

- Tên mô hình cố định, theo thứ tự: `MODEL_NAMES = ["meanemb", "rnn", "lstm", "transformer"]`.
- Dữ liệu: Hugging Face `stanfordnlp/imdb`, cố định `revision` bằng mã commit tra lúc cài đặt. Train 25.000 / test 25.000; validation 2.500 tách từ train; từ điển 20.000; `PAD=0`, `UNK=1`; giữ 256 từ đầu.
- Mọi mô hình: embedding 128; dropout 0.1 ở embedding và trước lớp phân loại; Adam lr 1e-3; batch 64; 5 epoch; cắt gradient 1.0.
- RNN/LSTM: một chiều, ẩn 128, `pack_padded_sequence`, trạng thái ẩn cuối. Transformer: 2 lớp, 4 đầu, feed-forward 256, `norm_first=True`, vị trí học được tối đa 2048, mean pooling bỏ padding.
- Seed mặc định 42, 1 seed (`--seeds 1`). Bật `cudnn.deterministic=True`, `cudnn.benchmark=False`. Accuracy lấy ở epoch có validation tốt nhất.
- Phép đo độ dài: (a) train lại ở 128/256/512; (b) một bước train + bộ nhớ đỉnh ở 128/256/512/1024/2048, batch 8, Transformer đo hai chế độ `"standard"` (ép `SDPBackend.MATH`) và `"optimized"` (mặc định), OOM ghi `None`; (c) nhóm độ dài review gốc `bins=(0,100,250,500,10**6)`.
- Độ trễ: trung vị batch 1, thông lượng batch 128, trên `"cuda"` (nếu có) và `"cpu"`, có warm-up, `torch.inference_mode`, đồng bộ CUDA.
- Đầu ra `results/`: `curves.png`, `tradeoff.png`, `scaling.png`, `length_sweep.png`, `length_bucket.png`, `confusion.png`, `summary.md`, `errors.md`, `results.json` (chỉ số tổng hợp, không lưu xác suất từng mẫu).
- `run.py` thoát với thông báo rõ ràng nếu không có CUDA, trừ khi dùng `--quick`. Không viết kết luận tự động.
- Tên hàm và biến bằng tiếng Anh. Thông báo in ra, nhãn biểu đồ và README bằng tiếng Việt.
- Người thực hiện kế hoạch là **thành viên thực hiện** (máy RTX 4080), không phải chồng. Thành viên thực hiện commit sau mỗi task và push thẳng lên `main` của repo GitHub chồng tạo.
- torch ghim `2.9.1`, bản CUDA 12.6 (`--index-url https://download.pytorch.org/whl/cu126`). Kiểm tra driver bằng `nvidia-smi` trước khi cài (lựa chọn của em).
- `--quick` ghi mặc định vào `results_quick/` (đã thêm vào `.gitignore`), và mọi file của nó có dòng "CHẠY THỬ – không dùng số liệu này". Chỉ `results/` của lần chạy đầy đủ trên GPU được commit (lựa chọn của em).
- Nếu chạy đầy đủ quá 40 phút, cắt theo thứ tự: giảm số mẫu đo thông lượng CPU, rồi bỏ độ dài 512 trong phép train lại. Ghi vào README phần đã cắt (lựa chọn của em).
- Khi `--seeds > 1`: accuracy lấy trung bình ± độ lệch chuẩn; phân tích lỗi, độ trễ, đường cong và `reuse` của phép train lại lấy từ seed đầu tiên (lựa chọn của em).

## Review Focus

1. Review rỗng hoặc toàn khoảng trắng: độ dài là 1, cả bốn mô hình cho đầu ra hữu hạn (Task 1, 2).
2. Độ dài lớn hơn 2048: Transformer báo `ValueError` nêu rõ giới hạn 2048 (Task 2).
3. Hết bộ nhớ trong phép đo độ dài: điểm đó là `None`, các điểm khác vẫn đo (Task 4).
4. Nhóm độ dài không có mẫu: `nan`, biểu đồ và bảng không lỗi (Task 5, 6).
5. Chạy đầy đủ trên máy không có CUDA: thoát ngay với thông báo hướng dẫn cài bản CUDA, không âm thầm chạy CPU (Task 7).

---

### Task 1: Khung repo, cấu hình, dữ liệu

**Files:**
- Create: `config.py`, `data.py`, `requirements.txt`, `.gitignore`, `tests/test_data.py`

**Interfaces:**
- Produces: `config.Config` (dataclass, đủ giá trị trong Global Constraints, gồm `seed=42`, `seeds=1`, `max_len=256`, `vocab_size=20000`, `emb=128`, `hidden=128`, `dropout=0.1`, `lr=1e-3`, `batch=64`, `epochs=5`, `clip=1.0`, `val_size=2500`, `sweep_lens=(128,256,512)`, `scaling_lens=(128,256,512,1024,2048)`, `scaling_batch=8`, `max_pos=2048`); `config.MODEL_NAMES`.
- `data.tok(text: str) -> list[str]`; `data.build_vocab(texts: list[str], size: int) -> dict[str, int]`; `data.encode(texts, vocab, max_len) -> (x: LongTensor[N,max_len], lens: LongTensor[N], raw_lens: np.ndarray)`; `data.load_imdb() -> {"train": (texts, labels), "test": (texts, labels)}`; `data.split(train, val_size, seed) -> (train, val)` (mỗi phần là `(texts, labels)`).

- [ ] **Step 1: Viết test lỗi** trong `tests/test_data.py`:
  - `test_tok_strips_br_and_keeps_punct`: `tok("Good<br />Movie!") == ["good", "movie", "!"]`.
  - `test_build_vocab_orders_by_frequency_and_starts_at_2`.
  - `test_encode_pads_truncates_and_marks_unk`: từ lạ là 1, padding là 0, `lens` cắt về `max_len`, `raw_lens` giữ độ dài gốc.
  - `test_encode_empty_review_has_length_1`: `""` và `"   "` đều cho `lens == 1`.
  - `test_split_is_deterministic_and_disjoint`.
- [ ] **Step 2: Chạy** `python -m pytest tests/test_data.py -v`. Mong đợi: FAIL vì chưa có module.
- [ ] **Step 3: Cài đặt.**
  - `load_imdb` dùng `datasets.load_dataset("stanfordnlp/imdb", revision=...)`. Khi tải lỗi, in thông báo tiếng Việt rằng cần mạng tới Hugging Face.
  - `requirements.txt` ghim phiên bản `datasets`, `numpy`, `matplotlib`, `pytest` (bản đã cài và test được trên máy thực hiện). Riêng `torch==2.9.1`, ghi chú trỏ sang README để cài bản CUDA cu126.
  - `.gitignore`: `data/`, `__pycache__/`, `.pytest_cache/`, `results_quick/`, `.venv/`.
- [ ] **Step 4: Chạy lại.** Mong đợi: PASS.
- [ ] **Step 5: Commit** `feat: config and data pipeline`.

### Task 2: Mô hình

**Files:** Create `models.py`, `tests/test_models.py`

**Interfaces:**
- Consumes: `Config`.
- Produces:
  - `MeanEmbClf(V, cfg)`, `RecClf(kind: str, V, cfg)` với `kind` thuộc `{"rnn", "lstm"}`, `TransClf(V, cfg)`. Mọi lớp có `forward(x: LongTensor[B,L], lens: LongTensor[B]) -> Tensor[B,2]`.
  - `build(name: str, V: int, cfg, dev) -> nn.Module`.
  - `count_params(m) -> (total: int, non_embedding: int)`. `non_embedding` bỏ cả embedding từ và embedding vị trí.

- [ ] **Step 1: Viết test lỗi:**
  - `test_output_shape_all_models`: batch 4, độ dài 16, đầu ra `(4, 2)` cho cả 4 tên trong `MODEL_NAMES`.
  - `test_padding_invariance`: ở chế độ eval, thêm cột padding vào cuối không đổi logits, `atol=1e-5`, cho cả 4 mô hình.
  - `test_empty_review_finite_output`: hàng toàn padding với `lens=1` cho đầu ra hữu hạn.
  - `test_transformer_rejects_len_above_max_pos`: độ dài 2049 gây `ValueError` có chữ "2048".
  - `test_count_params_excludes_embeddings`: `non_embedding < total`, và với `meanemb` thì `non_embedding == 128*2 + 2`.
- [ ] **Step 2: Chạy** `python -m pytest tests/test_models.py -v`. Mong đợi: FAIL.
- [ ] **Step 3: Cài đặt** theo Global Constraints.
  - `RecClf`: dùng `pack_padded_sequence(..., enforce_sorted=False)` với `lens.cpu()`. Lấy `h[-1]`; với LSTM lấy `h` trong bộ `(h, c)`.
  - `TransClf`: dùng `nn.TransformerEncoder(..., enable_nested_tensor=False)` với `src_key_padding_mask`. Đặt vị trí padding về 0 trước khi lấy trung bình; mẫu số tối thiểu 1.
- [ ] **Step 4: Chạy lại.** Mong đợi: PASS.
- [ ] **Step 5: Commit** `feat: models`.

### Task 3: Huấn luyện và dự đoán

**Files:** Create `train.py`, `tests/test_train.py`

**Interfaces:**
- Consumes: `build`, `Config`.
- Produces:
  - `set_seed(seed: int) -> None`: seed cho `random`, `numpy`, `torch`; đặt `cudnn.deterministic=True`, `cudnn.benchmark=False`.
  - `predict(m, x, lens, dev, bs=256) -> Tensor[N,2]`: xác suất, trên CPU.
  - `train(m, tr, va, cfg, dev, on_epoch=None) -> dict`. `tr` và `va` là `(x, lens, y)`. Dict trả về có:
    - `train_loss`, `val_acc`, `epoch_time`: list theo epoch;
    - `best_epoch`: đếm từ 1;
    - `peak_mem_mb`: `None` nếu không có CUDA.
  - `train` khôi phục trọng số epoch tốt nhất vào `m`. `on_epoch(epoch, hist)` được gọi sau mỗi epoch (`run.py` dùng nó để in thời gian dự kiến).

- [ ] **Step 1: Viết test lỗi:**
  - `test_train_reduces_loss_on_separable_data`: dữ liệu tổng hợp, nhãn 1 khi chứa token 5; LSTM, 3 epoch; loss cuối nhỏ hơn loss đầu.
  - `test_train_restores_best_epoch`: sau `train`, accuracy của `predict` trên `va` bằng `max(hist["val_acc"])`.
  - `test_predict_rows_sum_to_one`.
  - `test_set_seed_reproducible`: hai lần train với cùng seed cho `train_loss` giống hệt.
  - `test_rnn_learns_short_sequences`: dữ liệu tổng hợp độ dài 32, nhãn 1 khi chứa token 5; RNN thuần, 3 epoch; loss cuối nhỏ hơn loss đầu.
- [ ] **Step 2: Chạy.** Mong đợi: FAIL.
- [ ] **Step 3: Cài đặt.** Dùng `CrossEntropyLoss`; hoán vị mẫu mỗi epoch. Chỉ đo thời gian vòng lặp train, đồng bộ CUDA trước và sau. Khi validation tốt hơn thì lưu bản sao `state_dict`.
- [ ] **Step 4: Chạy lại.** Mong đợi: PASS.
- [ ] **Step 5: Commit** `feat: training loop`.

### Task 4: Đo tốc độ và bộ nhớ

**Files:** Create `benchmark.py`, `tests/test_benchmark.py`

**Interfaces:**
- Consumes: `build`, `Config`.
- Produces:
  - `inference_speed(m, x, lens, dev, n_latency=200, n_throughput=2560) -> {"latency_ms": float, "throughput": float}`: thông lượng đo trên `min(n_throughput, len(x))` mẫu đầu.
  - `scaling(V, cfg, dev) -> list[dict]`, mỗi dict có khóa `model`, `attn` (`"standard"`, `"optimized"`, hoặc `None` với mô hình không phải Transformer), `len`, `ms` (`float | None`), `mem_mb` (`float | None`).

- [ ] **Step 1: Viết test lỗi:**
  - `test_inference_speed_keys_positive`: CPU, mô hình nhỏ; hai khóa có giá trị dương.
  - `test_scaling_covers_models_and_attn_modes`: dùng `cfg.scaling_lens=(16,32)`. Có đủ 4 mô hình; Transformer có cả `"standard"` và `"optimized"`.
  - `test_scaling_records_none_on_oom`: `monkeypatch` hàm `build` để mô hình ném `torch.OutOfMemoryError` ở độ dài lớn nhất. Điểm đó có `ms is None`, các điểm khác vẫn có số.
- [ ] **Step 2: Chạy.** Mong đợi: FAIL.
- [ ] **Step 3: Cài đặt.**
  - `inference_speed`: warm-up một lần. Batch 1 lặp 200 mẫu, lấy trung vị (ms). Batch 128 lấy tổng số mẫu chia tổng thời gian. Dùng `torch.inference_mode()`.
  - `scaling`: mỗi điểm chạy fwd+bwd 4 lần, bỏ lần đầu, lấy trung vị. Chế độ `"standard"` bọc trong `torch.nn.attention.sdpa_kernel(SDPBackend.MATH)`.
  - Bắt `torch.OutOfMemoryError`; nếu có CUDA thì gọi `torch.cuda.empty_cache()`.
  - Bộ nhớ lấy từ `torch.cuda.max_memory_allocated` (đặt lại trước mỗi điểm); `None` trên CPU.
- [ ] **Step 4: Chạy lại.** Mong đợi: PASS.
- [ ] **Step 5: Commit** `feat: benchmarks`.

### Task 5: Phân tích lỗi

**Files:** Create `analysis.py`, `tests/test_analysis.py`

**Interfaces:**
- Produces:
  - `bucket_accuracy(pred, y, raw_lens, bins) -> list[float]`: nhóm rỗng là `nan`.
  - `confusion(pred, y) -> [[int, int], [int, int]]`: hàng là nhãn thật.
  - `top_wrong(probs: Tensor[N,2], y, k=3) -> list[int]`: review tự tin nhất đứng trước.
  - `disagreements(pred_a, pred_b, y, k=3) -> {"a_right_b_wrong": list[int], "b_right_a_wrong": list[int]}`.

- [ ] **Step 1: Viết test lỗi:**
  - `test_bucket_accuracy_values`.
  - `test_bucket_accuracy_empty_bucket_is_nan`.
  - `test_confusion_sums_to_n_and_rows_are_truth`.
  - `test_top_wrong_picks_most_confident_errors`.
  - `test_disagreements_both_directions`.
- [ ] **Step 2: Chạy.** Mong đợi: FAIL.
- [ ] **Step 3: Cài đặt** bằng numpy. Mỗi hàm chỉ vài dòng.
- [ ] **Step 4: Chạy lại.** Mong đợi: PASS.
- [ ] **Step 5: Commit** `feat: error analysis`.

### Task 6: Báo cáo (biểu đồ, bảng, JSON)

**Files:** Create `report.py`, `tests/test_report.py`

**Interfaces:**
- Consumes: kết quả do `run.py` gom lại.
- Produces: `save_report(res: dict, out: Path) -> None`. Hàm ghi đủ 9 file trong Global Constraints. Cấu trúc `res`:
  - `meta`: `device`, `gpu_name`, `vram_gb`, `cpu`, `cpu_threads` (`torch.get_num_threads()`), `os`, `python`, `torch`, `cuda`, `args`, `quick` (bool). Khi `quick` là `True`, `summary.md` và `errors.md` mở đầu bằng dòng "CHẠY THỬ – không dùng số liệu này".
  - `models[name]`: `test_acc`, `test_acc_std`, `params`, `params_non_emb`, `epoch_time_median`, `best_epoch`, `train_loss`, `val_acc`, `peak_mem_mb`, `latency` (`{dev: {"latency_ms", "throughput"}}`), `bucket_acc`, `confusion`.
  - `scaling`: list từ Task 4.
  - `length_sweep`: `{name: {max_len: test_acc}}`.
  - `errors`: `{name: [{"text", "true", "pred", "conf", "len"}]}`.
  - `disagreements`: `{"transformer_right_lstm_wrong": [...], "lstm_right_transformer_wrong": [...]}`, cùng định dạng mục với `errors`.

- [ ] **Step 1: Viết test lỗi:**
  - `test_save_report_writes_all_files`: dùng `res` tổng hợp có một nhóm độ dài `nan`, một điểm scaling `None` và `peak_mem_mb=None`. Kiểm tra 9 file tồn tại và `results.json` đọc lại được.
  - `test_summary_has_all_models_and_oom_marker`: `summary.md` chứa 4 tên mô hình, có chữ "OOM", và có dòng ghi chú về chạy 1 seed.
- [ ] **Step 2: Chạy.** Mong đợi: FAIL.
- [ ] **Step 3: Cài đặt.**
  - Dùng backend `Agg`, màu cố định cho mỗi mô hình, nhãn tiếng Việt, PNG 200 dpi.
  - `tradeoff.png`: accuracy so với thông lượng GPU (trục log), cỡ điểm theo `params_non_emb`.
  - `scaling.png`: hai ô thời gian và bộ nhớ, trục log, Transformer có hai đường `standard` và `optimized`.
  - `length_bucket.png` có chú thích "đã cắt về 256 từ".
  - `summary.md` gồm:
    - bảng accuracy (± std khi có nhiều seed), hai cột tham số, giây mỗi epoch, epoch tốt nhất, độ trễ và thông lượng GPU/CPU, bộ nhớ (hoặc "n/a"/"OOM");
    - ghi chú: "mỗi cấu hình chạy một lần, chênh lệch dưới khoảng 1–2% chưa chắc có ý nghĩa";
    - ghi chú về giới hạn phụ thuộc xa của IMDB.
  - Bỏ `nan` và `None` khỏi đường vẽ.
- [ ] **Step 4: Chạy lại.** Mong đợi: PASS.
- [ ] **Step 5: Commit** `feat: report`.

### Task 7: Điểm chạy và README

**Files:** Create `run.py`, `README.md`, `tests/test_run.py`

**Interfaces:**
- Consumes: tất cả module trên.
- Produces:
  - `main(argv: list[str] | None = None) -> None`, với các tham số `--quick`, `--seeds` (mặc định 1), `--seed` (mặc định 42), `--epochs`, `--max_len`, `--out` (mặc định `results`, hoặc `results_quick` khi có `--quick`).
  - `aggregate(values: list[float]) -> (mean, std)`: std là 0.0 khi chỉ có một giá trị.
  - `length_sweep(splits, vocab, cfg, dev, reuse: dict[str, float]) -> {name: {max_len: test_acc}}`: độ dài bằng `cfg.max_len` lấy luôn accuracy của lần chạy chính từ `reuse`, không train lại.
  - `rnn_sanity_check(splits, vocab, cfg, dev) -> (first_loss, last_loss)`: train RNN thuần trên `min(2.000, số mẫu train có)` mẫu IMDB với `max_len=32`, 3 epoch; chạy cả ở `--quick`. Chạy trước các thí nghiệm chính; nếu loss không giảm thì dừng với thông báo nghi lỗi code.

- [ ] **Step 1: Viết test lỗi:**
  - `test_aggregate_single_value_std_zero`.
  - `test_length_sweep_reuses_main_run`: `monkeypatch` hàm `train` để đếm số lần gọi; với `sweep_lens=(16,32)`, `max_len=32` và `reuse` có đủ 4 mô hình, chỉ train 4 lần (riêng độ dài 16), và kết quả ở 32 đúng bằng `reuse`.
  - `test_rnn_sanity_check_loss_decreases`: dữ liệu tổng hợp có tín hiệu rõ, `last_loss < first_loss`.
  - `test_main_exits_without_cuda_unless_quick`: `monkeypatch` cho `torch.cuda.is_available` trả `False`; `main([])` gây `SystemExit` với thông báo nhắc cài bản CUDA.
  - `test_main_quick_end_to_end`: `monkeypatch` thay `data.load_imdb` bằng 400 mẫu tổng hợp. Dữ liệu tổng hợp phải có tín hiệu rõ (ví dụ review dương chứa "good", âm chứa "bad") để `rnn_sanity_check` qua được. Chạy `main(["--quick", "--out", str(tmp_path)])`; mong đợi đủ 9 file, `summary.md` có 4 tên mô hình và dòng "CHẠY THỬ".
- [ ] **Step 2: Chạy.** Mong đợi: FAIL.
- [ ] **Step 3: Cài đặt `main`.**
  - In thiết bị, tên card và phiên bản thư viện ở đầu, rồi chạy `rnn_sanity_check`.
  - Với mỗi seed và mỗi mô hình: train, dự đoán test, rồi đo độ trễ trên `cuda` (nếu có) và `cpu`. Khi đo CPU, chép mô hình sang CPU.
  - Sau epoch đầu của mô hình đầu tiên, in thời gian dự kiến cho toàn bộ lần chạy.
  - Tiếp theo chạy phép (a) `length_sweep`, phép (b) `scaling`, rồi phân tích lỗi; cuối cùng gọi `save_report`.
  - `--quick` dùng `min(số mẫu có, số mẫu yêu cầu)` với yêu cầu là 3.000 mẫu train, 500 validation, 2.000 test (validation cũng không vượt quá một nửa phần train có sẵn), 1 epoch, `sweep_lens=(64,128)`, `scaling_lens=(128,256,512)`, và cho phép chạy CPU.
- [ ] **Step 4: Viết `README.md`.** Gồm các mục:
  - mục đích và ba giả thuyết;
  - giới hạn (IMDB và phụ thuộc xa; chỉ chạy 1 seed);
  - cài đặt, có lệnh cài PyTorch bản CUDA bằng `--index-url` của PyTorch;
  - cách chạy (`python run.py --quick` trước, rồi `python run.py`);
  - cấu trúc thư mục;
  - mô tả các file kết quả;
  - "Cấu hình máy": card GPU, VRAM, CPU, hệ điều hành, phiên bản Python/torch/CUDA. Để trống để điền từ `results.json` sau khi chạy GPU (script tự ghi các thông tin này);
  - mục "Kết quả và kết luận" để trống, ghi "sẽ điền sau khi có số liệu chạy trên GPU".
- [ ] **Step 5: Kiểm tra toàn bộ:**
  - `python -m pytest tests -v`. Mong đợi: tất cả PASS.
  - `python run.py --quick` (tải IMDB thật từ Hugging Face). Mong đợi: kết thúc không lỗi, `results_quick/` có đủ 9 file, `results/` không bị tạo hay ghi đè.
  - Mở từng PNG xem bằng mắt.
- [ ] **Step 6: Commit** `feat: run script and README`.

### Sau khi triển khai

Thành viên thực hiện làm các bước sau trên máy RTX 4080:

1. Chạy `python run.py` (bản đầy đủ).
2. Điền mục "Cấu hình máy" trong README từ `results/results.json`.
3. Viết mục "Kết quả và kết luận" từ số thật, kể cả khi kết quả lệch với ba giả thuyết, gồm:
   - bảng "khi nào chọn mô hình nào";
   - nhận xét về hai chế độ attention;
   - nhắc lại hai giới hạn: IMDB và phụ thuộc xa; chỉ chạy 1 seed.
4. Commit `results/` và README, push lên `main`.
5. Báo chồng link repo để chồng lấy biểu đồ làm slide.
