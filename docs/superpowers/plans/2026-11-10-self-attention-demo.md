# Demo self-attention và causal mask: kế hoạch thực hiện

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Một notebook VS Code tự viết self-attention bằng PyTorch, nạp trọng số đã huấn luyện của GPT-2, vẽ heatmap trước/sau causal mask, đo chi phí trên GPU và CPU, kèm nhận xét ưu điểm, hạn chế và hướng dẫn chạy.

**Architecture:** Mọi code nằm trong **một notebook** `self_attention_demo.ipynb` để giảng viên thấy từng bước; các hàm định nghĩa trong ô code của notebook, không tách module. Kiểm thử là các `assert` trong notebook (so với GPT-2 gốc) và chạy lại toàn bộ notebook từ đầu bằng `nbconvert`.

**Tech Stack:** Python, PyTorch 2.9.1 (cu128), Hugging Face `transformers`, matplotlib, Jupyter trong VS Code.

**Spec:** `docs/superpowers/specs/2026-11-10-self-attention-demo-design.md` (đọc trước; nếu kế hoạch mâu thuẫn với spec thì làm theo spec).

## Global Constraints

- Người thực hiện: thành viên thực hiện, trên máy RTX 5060 Laptop GPU của họ. Commit sau mỗi task, push thẳng `main`.
- Hạn chót: notebook đã chạy xong, lưu output và push **trước ngày 14/11/2026** (ngày thuyết trình).
- Mô hình: `GPT2Model.from_pretrained("gpt2", attn_implementation="eager")`, `model.eval()`, float32. Ghi rõ trong notebook: **"trọng số đã huấn luyện của GPT-2"**.
- Câu ví dụ đúng nguyên văn: `The animal didn't cross the street because it was too tired`. Không thêm token BOS.
- Hàm tự viết không được gọi `scaled_dot_product_attention`, `nn.MultiheadAttention` hay attention của GPT-2; GPT-2 gốc chỉ dùng để lấy trọng số, hidden state và để đối chiếu.
- `DEVICE = "cuda" if torch.cuda.is_available() else "cpu"`. Máy không có GPU vẫn chạy hết notebook.
- Chữ giải thích, tiêu đề, nhãn hình bằng tiếng Việt; tên biến, hàm tiếng Anh.
- Không có lệnh `pip install` trong notebook; cài theo README.
- Notebook lưu kèm output của lần chạy trên máy RTX 5060 Laptop GPU. Hình lưu vào `figures/`.
- Không tự huấn luyện, không tinh chỉnh, không thêm bản trọng số ngẫu nhiên, không slide.

## Review Focus

1. **Máy không có GPU:** notebook chạy hết, phần đo chỉ có CPU, in "Không có GPU, chỉ đo CPU". → kiểm tra ở Task 4 Step 4.
2. **Hết bộ nhớ khi đo ở độ dài lớn:** ghi `None`, hình và bảng hiện "OOM", notebook không dừng. → Task 4 Step 2.
3. **Câu ví dụ bị sửa, không còn token " it" hoặc " animal":** báo lỗi rõ ràng bằng tiếng Việt, không chọn nhầm token. → Task 3 Step 1.
4. **Lớp học không có mạng:** sau khi đã chạy một lần, đặt `HF_HUB_OFFLINE=1` thì notebook vẫn tải được GPT-2 từ cache. → Task 5 Step 3.
5. **Chạy lại từ kernel mới cho cùng kết quả:** seed cố định cho dữ liệu ngẫu nhiên phần đo; không ô nào phụ thuộc biến tạo bằng tay. → mọi task kiểm tra bằng `nbconvert --execute` từ đầu.

---

### Task 1: Môi trường và khung repo

**Files:**
- Create: `requirements.txt`, `.gitignore`, `README.md` (khung), `self_attention_demo.ipynb` (ô giới thiệu + ô import), `figures/.gitkeep`

**Interfaces:**
- Produces: biến `DEVICE`, `model`, `tokenizer` (ô "Tải mô hình"), dùng ở mọi task sau.

- [ ] **Step 1: Cài môi trường**

```bash
nvidia-smi
python -m venv .venv          # Windows: .venv\Scripts\activate
pip install torch==2.9.1 --index-url https://download.pytorch.org/whl/cu128
pip install transformers matplotlib ipykernel nbconvert
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```
Expected: in `True` và tên card RTX 5060 Laptop GPU.

- [ ] **Step 2: Viết `requirements.txt`** ghim đúng phiên bản vừa cài của `transformers`, `matplotlib`, `ipykernel`, `nbconvert` (lấy từ `pip freeze`). Dòng đầu là comment: torch 2.9.1 cài riêng bằng `--index-url .../cu128`. `.gitignore`: `.venv/`, `__pycache__/`, `.ipynb_checkpoints/`.

- [ ] **Step 3: Tạo notebook**, gồm:
  - Ô markdown giới thiệu: bài làm gì; dòng in đậm "Dùng **trọng số đã huấn luyện của GPT-2** (bản `gpt2`, 124M tham số), không phải trọng số ngẫu nhiên".
  - Ô code: import, `torch.manual_seed(42)`, `DEVICE`, in phiên bản torch, transformers, tên GPU (hoặc "CPU"), tên CPU (`platform.processor()`).
  - Ô code "Tải mô hình": `tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")`, `model` theo Global Constraints, chuyển sang `DEVICE`.

- [ ] **Step 4: Chạy thử toàn bộ notebook**

Run: `jupyter nbconvert --to notebook --execute --inplace self_attention_demo.ipynb`
Expected: chạy xong không lỗi; ô import in đúng tên GPU.

- [ ] **Step 5: Commit**

```bash
git add requirements.txt .gitignore README.md self_attention_demo.ipynb figures/.gitkeep
git commit -m "chore: moi truong va khung notebook"
git push origin main
```

---

### Task 2: Hàm self-attention tự viết và kiểm tra khớp GPT-2

**Files:**
- Modify: `self_attention_demo.ipynb` (thêm các ô sau ô "Tải mô hình")

**Interfaces:**
- Consumes: `model`, `tokenizer`, `DEVICE` (Task 1).
- Produces:
  - `SENTENCE: str`, `input_ids: Tensor (1, T)`, `tokens: list[str]` (đã bỏ ký tự `Ġ`).
  - `get_layer_input(model, input_ids, layer: int) -> Tensor (T, 768)`: `model(input_ids, output_hidden_states=True).hidden_states[layer][0]` rồi qua `model.h[layer].ln_1`.
  - `self_attention(x, w_qkv, b_qkv, n_head: int = 12, causal: bool = True) -> tuple[Tensor (T, 768), Tensor (n_head, T, T)]`: trả về (đầu ra đã nối các đầu, **trước** `c_proj`) và ma trận attention.
  - `get_qkv_weights(model, layer) -> (w_qkv (768, 2304), b_qkv (2304,))` = `model.h[layer].attn.c_attn.weight`, `.bias`.

- [ ] **Step 1: Viết ô kiểm tra (chạy sẽ lỗi vì chưa có hàm)**

```python
with torch.no_grad():
    ref = model(input_ids, output_attentions=True).attentions   # tuple 12 lớp, mỗi lớp (1, 12, T, T)
    max_diff = 0.0
    for layer in range(12):
        x = get_layer_input(model, input_ids, layer)
        _, attn = self_attention(x, *get_qkv_weights(model, layer), causal=True)
        diff = (attn - ref[layer][0]).abs().max().item()
        assert diff < 1e-4, f"Lớp {layer}: lệch {diff:.2e}"
        max_diff = max(max_diff, diff)
print(f"Hàm tự viết khớp GPT-2 gốc ở cả 12 lớp; sai số lớn nhất: {max_diff:.2e}")
```
Cùng ô: `assert torch.allclose(attn.sum(-1), torch.ones_like(attn.sum(-1)), atol=1e-5)` (mỗi hàng cộng bằng 1) và với `causal=True`, `attn.triu(1).abs().max() == 0`.

- [ ] **Step 2: Chạy, thấy lỗi** `NameError: self_attention`.

- [ ] **Step 3: Viết ô `self_attention`** (phần trọng tâm), mỗi bước một dòng comment tiếng Việt, ô markdown phía trên ghi công thức `softmax(QKᵀ/√d + M)·V`, `M` = −∞ ở các vị trí tương lai:
  1. `qkv = x @ w_qkv + b_qkv`, tách Q, K, V;
  2. chia thành `n_head` đầu, mỗi đầu `d = 64`;
  3. `scores = Q @ Kᵀ / sqrt(d)`;
  4. nếu `causal`: `scores.masked_fill(mask_tương_lai, float("-inf"))` với mask là `torch.triu(ones(T,T), 1).bool()`;
  5. `attn = softmax(scores, dim=-1)`; `out = attn @ V`, nối các đầu.
  Cùng ô: định nghĩa `SENTENCE`, `input_ids`, `tokens`, `get_layer_input`, `get_qkv_weights`; in danh sách `tokens`.

- [ ] **Step 4: Chạy lại toàn bộ**

Run: `jupyter nbconvert --to notebook --execute --inplace self_attention_demo.ipynb`
Expected: không lỗi; in "khớp GPT-2 gốc ở cả 12 lớp" với sai số cỡ 1e-6 đến 1e-5.

- [ ] **Step 5: Commit** `feat: ham self-attention tu viet va kiem tra khop GPT-2`, push `main`.

---

### Task 3: Heatmap trước và sau causal mask

**Files:**
- Modify: `self_attention_demo.ipynb`
- Create: `figures/heatmap_no_mask.png`, `figures/heatmap_causal_mask.png`, `figures/heatmap_compare.png`

**Interfaces:**
- Consumes: `self_attention`, `get_layer_input`, `get_qkv_weights`, `tokens`, `input_ids` (Task 2).
- Produces: `find_token(tokens, word: str) -> int`; `pick_head(src: int, tgt: int) -> tuple[int, int, float]` (lớp, đầu, trọng số từ src sang tgt khi có mask); `plot_attention(attn_no_mask, attn_mask, tokens, title, path_prefix) -> None`.

- [ ] **Step 1: Viết `find_token` và ô kiểm tra**

```python
assert find_token(tokens, "it") == tokens.index("it")
assert find_token(tokens, "animal") < find_token(tokens, "it")
```
`find_token` khi không thấy từ: `raise ValueError(f"Không tìm thấy token '{word}' trong câu: {tokens}")`.

- [ ] **Step 2: Viết `pick_head`**: quét 12 lớp × 12 đầu, gọi `self_attention(..., causal=True)`, lấy đầu có `attn[head, src, tgt]` lớn nhất. Ô markdown phía trên ghi rõ **tiêu chí chọn** này; ô in "Chọn lớp L, đầu H: 'it' → 'animal' = 0.xx". In thêm top 3 đầu để minh bạch.

- [ ] **Step 3: Viết `plot_attention`** và vẽ cho lớp, đầu đã chọn:
  - Hai panel cạnh nhau, **cùng thang màu 0–1**, nhãn trục là `tokens` (trục y: token đang hỏi, trục x: token được chú ý), một thanh màu chung.
  - Tiêu đề panel: "Trước causal mask (không mask)" và "Sau causal mask"; tiêu đề chung có "Trọng số đã huấn luyện của GPT-2 – lớp L, đầu H".
  - Lưu `figures/heatmap_compare.png` và hai panel riêng `heatmap_no_mask.png`, `heatmap_causal_mask.png` (dpi 200).
  - Ô kiểm tra: `assert attn_mask.triu(1).abs().max() == 0` và `attn_no_mask.triu(1).abs().max() > 0`.

- [ ] **Step 4: Ô markdown nhận xét heatmap**, viết **sau khi** nhìn hình thật:
  - "it" chú ý vào đâu, con số bao nhiêu;
  - trước mask: token nhìn cả tương lai; ghi rõ đây chỉ là phép thử minh hoạ, GPT-2 chưa từng chạy không mask khi huấn luyện;
  - sau mask: nửa trên đường chéo bằng 0;
  - token đầu "The" nhận nhiều attention ("attention sink"), nếu hình thật cho thấy vậy.

- [ ] **Step 5: Chạy lại toàn bộ** bằng lệnh `nbconvert` ở Task 2 Step 4. Expected: không lỗi, 3 file PNG có trong `figures/`.

- [ ] **Step 6: Commit** `feat: heatmap truoc va sau causal mask` (gồm notebook và 3 PNG), push `main`.

---

### Task 4: Đo thời gian và bộ nhớ trên GPU và CPU

**Files:**
- Modify: `self_attention_demo.ipynb`
- Create: `figures/cost_gpu_cpu.png`

**Interfaces:**
- Consumes: `self_attention` (Task 2).
- Produces: `benchmark(lengths: list[int], device: str, n_rep: int = 20) -> list[dict]`, mỗi dict `{"len": int, "ms": float | None, "mem_mb": float | None}`.

- [ ] **Step 1: Ô kiểm tra trước**

```python
r = benchmark([16, 32], "cpu", n_rep=2)
assert [x["len"] for x in r] == [16, 32] and all(x["ms"] > 0 for x in r)
assert abs(r[1]["mem_mb"] / r[0]["mem_mb"] - 4) < 0.01   # độ dài gấp đôi → ma trận điểm gấp 4
```

- [ ] **Step 2: Viết `benchmark`**:
  - Đầu vào ngẫu nhiên `x (len, 768)`, `w_qkv (768, 2304)`, `b_qkv (2304,)` tạo bằng `torch.Generator().manual_seed(42)`, 12 đầu, `causal=True`, trong `torch.inference_mode()`.
  - Chạy làm nóng 3 lần, rồi `n_rep` lần, lấy trung vị (ms). Trên GPU gọi `torch.cuda.synchronize()` trước và sau mỗi lần bấm giờ.
  - Bộ nhớ GPU: `torch.cuda.reset_peak_memory_stats()` trước, `torch.cuda.max_memory_allocated()/2**20` sau. Bộ nhớ CPU: lấy `attn.nelement() * attn.element_size() / 2**20` từ ma trận attention thực trả về, cùng shape/dtype với scores; không tạo dummy tensor và không coi là peak RAM.
  - Bắt `torch.OutOfMemoryError`: ghi `ms`, `mem_mb` là `None`, `torch.cuda.empty_cache()`, đo tiếp độ dài sau.

- [ ] **Step 3: Ô đo và vẽ**:
  - `LENGTHS = [128, 256, 512, 1024, 2048]`; đo CPU, và đo GPU nếu `torch.cuda.is_available()`, ngược lại in "Không có GPU, chỉ đo CPU".
  - In bảng (pandas không dùng; in bằng f-string): độ dài | GPU ms | CPU ms | GPU MB | CPU MB, ô `None` in "OOM".
  - Hình hai panel: trái thời gian (ms, trục y log), phải bộ nhớ (MB, trục y log), mỗi panel hai đường GPU và CPU; tiêu đề có tên GPU, CPU và chữ "dữ liệu ngẫu nhiên, chỉ để đo chi phí". Lưu `figures/cost_gpu_cpu.png`.
  - Nếu riêng phần CPU chạy quá ~60 giây: bỏ độ dài 2048 ở CPU, ghi chú trong ô markdown.

- [ ] **Step 4: Kiểm tra trường hợp không GPU**: chạy ô đo một lần với `DEVICE` ép `"cpu"` và nhánh GPU tắt (tạm sửa điều kiện thành `False`), thấy không lỗi và in thông báo; trả lại như cũ.

- [ ] **Step 5: Ô markdown nhận xét chi phí** theo số thật: bộ nhớ khi độ dài gấp đôi tăng bao nhiêu lần; GPU nhanh hơn CPU bao nhiêu lần ở độ dài 2048 (hoặc độ dài lớn nhất đo được); ý nghĩa với doanh nghiệp (ngữ cảnh dài → tăng chi phí GPU, độ trễ).

- [ ] **Step 6: Chạy lại toàn bộ** bằng `nbconvert`. Expected: không lỗi, có `figures/cost_gpu_cpu.png`, toàn notebook chạy dưới ~3 phút.

- [ ] **Step 7: Commit** `feat: do thoi gian va bo nho GPU CPU`, push `main`.

---

### Task 5: Ưu điểm, hạn chế, README và bản chạy cuối

**Files:**
- Modify: `self_attention_demo.ipynb`, `README.md`

**Interfaces:**
- Consumes: mọi ô và hình của Task 1–4.

- [ ] **Step 1: Ô markdown "Ưu điểm và hạn chế của self-attention"**: viết thành văn theo đúng các ý trong mục "Ý chính cho phần ưu điểm và hạn chế" của spec, kể cả đoạn "Vì sao cần causal mask". Ý O(n²) dẫn số đo của Task 4; ý phụ thuộc xa dẫn heatmap "it" → "animal" của Task 3.

- [ ] **Step 2: Viết README** (tiếng Việt) gồm:
  - Mô tả ngắn, dòng "Dùng trọng số đã huấn luyện của GPT-2".
  - **Cài đặt cho VS Code:** cài extension Python và Jupyter; tạo venv; lệnh cài torch bản cu128 (ghi lý do: cài mặc định trên Windows là bản CPU); `pip install -r requirements.txt`; mở notebook, chọn kernel `.venv`.
  - **Cách chạy:** "Restart" rồi "Run All"; lần đầu cần mạng để tải GPT-2 (~500MB); **chạy một lần trước giờ thuyết trình** để mô hình nằm sẵn trong cache; nếu lớp không có mạng, đặt biến môi trường `HF_HUB_OFFLINE=1` trước khi mở VS Code.
  - Danh sách file trong `figures/` và hình nào dùng cho phần nào.
  - Cấu hình máy đã chạy output lưu sẵn (GPU, CPU, phiên bản torch, transformers) — lấy từ output ô import.

- [ ] **Step 3: Kiểm tra chạy offline**: đặt `HF_HUB_OFFLINE=1` rồi chạy `nbconvert --execute`. Expected: không lỗi (mô hình lấy từ cache).

- [ ] **Step 4: Bản chạy cuối trên RTX 5060 Laptop GPU**: chạy `jupyter nbconvert --to notebook --execute --inplace self_attention_demo.ipynb` một lần cuối; mở notebook trong VS Code kiểm tra mọi hình hiện ra, chữ "trọng số đã huấn luyện của GPT-2" có ở đầu notebook và tiêu đề heatmap.

- [ ] **Step 5: Commit** `docs: uu han che, README va output cuoi`, push `main`, báo chồng kèm link repo.

## Cập nhật yêu cầu ngày 14/11/2026

- Người dùng duyệt RTX 5060 Laptop GPU/cu128 thay cấu hình RTX 4080/cu126 ban đầu.
- Demo chính ngắn: Implementation self-attention, kiểm chứng, hai heatmap và giải thích đơn giản. Đo GPU/CPU cùng các kiểm tra bổ sung nằm ở phụ lục, không cắt bỏ phần đo đã chốt.
- Bổ sung bảng so sánh **lý thuyết Transformer/CNN/RNN**, không huấn luyện ba mô hình hay làm lại bài IMDB.
- `pick_head(src, tgt)` nhận chỉ số và trả `(layer, head, value)`, tự in top 3; `plot_attention` đúng tên/API trong kế hoạch.
- Nhận xét số liệu được tạo từ kết quả lúc chạy. CPU đếm ma trận attention thật (cùng kích thước/kiểu với scores); GPU ghi đỉnh tensor gồm cả mô hình. Cả hai thiết bị warm-up 3, đo trung vị 20 lần.
- OOM tại cấp phát weight/bias/input và trong attention được bắt, ghi OOM và tiếp tục. Theo yêu cầu mới, tệp thuyết trình và ảnh dựng riêng đã được bỏ; giữ code, tài liệu kỹ thuật và bốn PNG/JSON output của notebook.
