# Phát hành và nghiệm thu (Release & Acceptance)

Tài liệu này dùng để nghiệm thu toàn diện sản phẩm trước khi thuyết trình vào ngày 14/11/2026.

---

## Danh mục kiểm tra trước khi bàn giao (Pre-release Checklist)
- [ ] File notebook `self_attention_demo.ipynb` có chứa đầy đủ output của lần chạy trên máy RTX 4080.
- [ ] Dòng chữ **"Trọng số đã huấn luyện của GPT-2"** xuất hiện rõ ràng ở phần đầu notebook và trên tiêu đề heatmap.
- [ ] Sai số giữa hàm tự viết và GPT-2 gốc được kiểm chứng $< 10^{-4}$ ở cả 12 layer.
- [ ] Thư mục `figures/` chứa đủ các file ảnh PNG phục vụ làm slide:
  - `heatmap_compare.png`
  - `heatmap_no_mask.png`
  - `heatmap_causal_mask.png`
  - `cost_gpu_cpu.png`
- [ ] Toàn bộ các nhận xét và phân tích định lượng khớp chính xác với số liệu thật.
- [ ] Thử nghiệm chế độ offline `HF_HUB_OFFLINE=1` thành công không phát sinh lỗi tải mạng.
- [ ] `README.md` hướng dẫn đầy đủ cách chạy trong VS Code bằng kernel `.venv`.
- [ ] Repo được push sạch sẽ lên nhánh `main` của GitHub.

---

## Thông tin bản phát hành bàn giao cho buổi thuyết trình
- **Thời gian bàn giao**: Trước ngày 14/11/2026.
- **Môi trường chạy demo chính thức**: VS Code trên máy trạm GPU NVIDIA GeForce RTX 4080.
- **Sản phẩm bàn giao**:
  1. Notebook tương tác: `self_attention_demo.ipynb`
  2. Thư mục ảnh slide: `figures/`
  3. Bộ tài liệu quy trình Vibe Coding: `workflow/docs/`
  4. Bộ đặc tả & kế hoạch kỹ thuật: `docs/superpowers/`
  5. Hướng dẫn vận hành: `README.md`
