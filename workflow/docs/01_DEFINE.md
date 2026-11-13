# Define — Bài tập Demo Self-Attention và Causal Mask

## What — Làm gì?
- **Bài toán**: Hiện thực hóa cơ chế Self-Attention và Causal Mask bằng PyTorch từ đầu (từng bước tính toán ma trận), nạp trọng số đã huấn luyện của GPT-2 (bản nhỏ `gpt2`, 124M tham số).
- **Sản phẩm và người sử dụng**: Một notebook duy nhất `self_attention_demo.ipynb` chạy trong VS Code. Người sử dụng và đánh giá là giảng viên môn Deep Learning (chuyên gia từ doanh nghiệp quan tâm hiệu năng, chi phí, độ trễ) và các thành viên nhóm thuyết trình.
- **Chức năng chính**:
  1. Tự cài đặt hàm self-attention từng bước: chiếu $Q, K, V$, nhân $Q K^T / \sqrt{d}$, áp dụng causal mask, softmax, nhân $V$.
  2. Kiểm chứng độ chính xác so với output attention của GPT-2 gốc (sai số lớn nhất $< 10^{-4}$).
  3. Trực quan hóa: vẽ 2 heatmap attention trước và sau causal mask cạnh nhau (cùng thang màu) trên câu ví dụ chuẩn.
  4. Benchmark thực tế: đo thời gian suy luận (ms) và bộ nhớ (MB) trên cả GPU (RTX 4080) và CPU với độ dài chuỗi tăng dần (128 đến 2048).
  5. Đánh giá chuyên sâu: phân tích ưu điểm, hạn chế (độ phức tạp $O(n^2)$, hiện tượng attention sink, phụ thuộc xa, chi phí phần cứng doanh nghiệp).

## Why — Vì sao?
- **Vấn đề của cách làm hiện tại**: Việc gọi các thư viện dựng sẵn (`nn.MultiheadAttention`, `F.scaled_dot_product_attention`) che giấu bản chất tính toán và tác động thực sự của causal mask. Trọng số ngẫu nhiên chỉ tạo ra ma trận nhiễu không có cấu trúc ngôn ngữ thực tế.
- **Giá trị mong muốn**: 
  - Thấy rõ từng phép tính toán học và cơ chế chặn tương lai (causal mask) trong mô hình sinh (autoregressive).
  - Trọng số GPT-2 pretrained giúp heatmap phản ánh ngữ nghĩa thật (từ *"it"* liên kết mạnh tới *"animal"*).
  - Số liệu benchmark thật trên GPU RTX 4080 và CPU cung cấp góc nhìn thực tế cho bài toán triển khai tại doanh nghiệp.
- **Dấu hiệu hoặc chỉ số thành công**:
  - Hàm tự viết khớp hoàn toàn GPT-2 gốc ở cả 12 layer (max diff $< 10^{-4}$).
  - Heatmap trực quan rõ ràng, nửa trên đường chéo sau mask triệt tiêu hoàn toàn về 0.
  - Đồ thị benchmark thể hiện đúng tính chất $O(n^2)$ và sự chênh lệch hiệu năng giữa GPU và CPU.

## When — Khi nào?
- **Tình huống/kích hoạt nghiệp vụ**: Báo cáo bài tập lớn môn Deep Learning.
- **Thời hạn và mốc thực hiện**: Thuyết trình ngày **14/11/2026**. Notebook và tài liệu phải hoàn tất, kiểm thử và lưu output trước ngày thuyết trình.

## Where — Ở đâu?
- **Nơi dùng, thiết bị, môi trường**: Máy trạm cá nhân trang bị GPU NVIDIA GeForce RTX 4080, hệ điều hành Windows, Python 3.10+, PyTorch 2.9.1 (CUDA 12.6).
- **Môi trường demo / triển khai**: Chạy trực tiếp trong VS Code (Jupyter extension) chọn kernel môi trường ảo `.venv`. Hỗ trợ chế độ offline (`HF_HUB_OFFLINE=1`) khi phòng học không có kết nối internet.

## Which — Chọn gì, giới hạn gì?
- **Phạm vi bản đầu**:
  - File notebook `self_attention_demo.ipynb` tự chứa toàn bộ code thực thi và giải thích bằng tiếng Việt.
  - Câu ví dụ chuẩn: `"The animal didn't cross the street because it was too tired"`.
  - Bộ trọng số: `gpt2` (124M tham số) tải từ Hugging Face.
  - Các hình ảnh xuất ra thư mục `figures/` để phục vụ làm slide.
- **Ngoài phạm vi**:
  - Không tự huấn luyện hay fine-tune mô hình.
  - Không thêm bản trọng số ngẫu nhiên để so sánh.
  - Không làm slide thuyết trình (trưởng nhóm tự chuẩn bị từ hình ảnh xuất ra).
  - Không xây dựng giao diện tương tác web/app ngoài notebook.
  - Hủy bỏ hoàn toàn bài so sánh Transformer vs RNN/LSTM trên IMDB cũ.
- **Công nghệ bắt buộc**: PyTorch 2.9.1 (cu126), Hugging Face `transformers`, `matplotlib`, VS Code Jupyter.
- **Ràng buộc đạo đức & học thuật**: Tuyệt đối không gian lận số liệu benchmark; tiêu chí chọn layer/head để vẽ heatmap phải được thuật toán quét tự động và ghi rõ trong notebook.

## How — Hướng thực hiện
- **Cách giải quyết tổng quát**: Áp dụng quy trình Vibe Coding theo chuẩn kỹ sư (Spec-driven development):
  - Định nghĩa rõ Spec và Plan 5 Task tuần tự.
  - Test-Driven Development (TDD): Viết ô kiểm tra `assert` trước, chạy thấy lỗi, sau đó mới hoàn thiện hàm.
  - Tự động hóa kiểm thử bằng `jupyter nbconvert --to notebook --execute --inplace`.
- **AI hỗ trợ**: Hỗ trợ sinh mã nguồn chuẩn, viết tài liệu kỹ thuật, phân tích dữ liệu benchmark và đồng bộ theo đúng ràng buộc trong `AGENTS.md`.
- **Người chịu trách nhiệm quyết định và kiểm tra**: Thành viên nhóm thực hiện (chạy code trên GPU RTX 4080) và Trưởng nhóm (thuyết trình, duyệt slide).
- **Cách kiểm chứng dự kiến**: Chạy lệnh `nbconvert` từ đầu đến cuối không lỗi, kiểm tra diff số học ma trận $< 10^{-4}$, kiểm tra các file ảnh PNG sinh ra trong `figures/`.

## Câu hỏi và giả định chưa chốt
| Nội dung | Tác động nếu sai | Ai xác nhận | Trạng thái |
| --- | --- | --- | --- |
| Lớp/đầu attention nào thể hiện rõ nhất liên kết "it" $\rightarrow$ "animal"? | Heatmap khó nhận xét trực quan | Code tự động quét top 3 | Đã có thuật toán tự chọn |
| Mạng phòng học có thể mất kết nối internet? | Không tải được GPT-2 lúc mở máy | Thành viên thực hiện | Đã giải quyết: cache offline `HF_HUB_OFFLINE=1` |
