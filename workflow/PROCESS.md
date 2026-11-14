# Luồng thực hiện bài self-attention

**Mã hồ sơ: PROCESS. Cập nhật: 14/11/2026.**

## Quy trình áp dụng

```mermaid
flowchart TD
    P["PDF + đặc tả + yêu cầu người dùng"] --> D["01 Define và yêu cầu"]
    D --> A["02 Design: GPT-2 và attention tự viết"]
    A --> L["03 Plan: 5 task"]
    L --> B["04 Brief một task"]
    B --> C["05 Triển khai"]
    C --> R["06 Review"]
    R --> RUN["07 Run"]
    RUN --> TEST["08 Test"]
    TEST --> OK{"Đạt điều kiện task?"}
    OK -->|Chưa| DEBUG["09 Debug có bằng chứng"]
    DEBUG --> R
    OK -->|Cần cải thiện cấu trúc| REF["10 Refactor giữ hành vi"]
    REF --> R
    OK -->|Đạt| G["11 Commit đúng phạm vi"]
    G --> E["12 Giải thích code"]
    E --> DOC["13 Đồng bộ tài liệu"]
    DOC --> END["14 Nghiệm thu theo bằng chứng"]
```

Debug/refactor không phải việc phải làm để đủ số bước. Lần viết lại hiện tại áp dụng vòng Review/Test vào chính hồ sơ và bộ kiểm soát tài liệu; không làm lại code 5 task đã có. Tài liệu lý thuyết liên quan được truy vết ở THEORY, trạng thái thực nghiệm ở TEST_RESULTS và trạng thái kết thúc ở ACCEPTANCE.

## Vòng kiểm soát file

Yêu cầu/nguồn đổi → chọn file chịu trách nhiệm → sửa nội dung và bên tham chiếu → kiểm tra nguồn/số liệu → cập nhật manifest cho phần đã duyệt → chạy checker/tests → review diff → commit/push theo quyền đã có. Không tự nâng “chưa xác minh” thành “đạt”. Chi tiết ở [CONTROL](CONTROL.md).
