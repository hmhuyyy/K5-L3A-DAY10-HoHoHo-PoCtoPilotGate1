# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `HoHoHo`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-HoHoHo-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): `S5`

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Hoàng Minh Huy | 2A202603495 | Sản phẩm và kinh doanh | x |
|   2 | Bùi Quang Huy | 2A202603469 | Kỹ sư cổng (AI Engineer) | |
|   3 | Nguyễn Mạnh Quyền | 2A202603518 | Đánh giá chất lượng (QA/Eval) | |
|   4 | Nguyễn Trường Thành | 2A202603512 | Vận hành và pháp lý | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## HoangMinhHuy-2A202603495

### Phần việc phụ trách

Trưởng nhóm / Sản phẩm và kinh doanh (Người 1).
- Phiếu A: Mục A1, A3, A4.
- Cấu hình tiêu chí nghiệm thu: `config/acceptance_criteria.json` và ký duyệt khóa Gate 1.
- Cấu hình cổng kinh doanh: `config/operating_gates.json` (mục `business`).
- Phiếu B: Mục B0 (nhật ký baseline), B1 (đánh giá baseline), B3 (bản đồ dữ liệu & data drift), chuẩn bị B8 (quyết định v1).
- Điều phối tiến độ các thành viên trong nhóm.

### Đóng góp cụ thể

- Hoàn thiện mục tiêu hệ thống, bài toán kinh tế (chi phí mỗi ticket tối đa 8.000đ, ROI >= 0.2, trần hoàn tiền 2.000.000đ/ngày).
- Thiết lập bộ 5 tiêu chí an toàn bắt buộc (hoàn sai = 0, phạt oan = 0, lộ PII = 0).
- Ký khóa nghiệm thu Gate 1 hash `5f494889`.
- Xây dựng bản đồ dữ liệu và mô hình rủi ro Data Drift mùa cao điểm Tết.

### Bằng chứng

- Commit: `596a3ad` (Sign acceptance criteria), `e1f7025` (docs: update form-a criteria and operating gates business config), `1b1eff8` (docs: update form-b baseline and data map).
- Lần chạy baseline: `R-base-before-20261118-143735-d2242a`.

### Exit ticket

Một điều học được: Bản tiêu chí nghiệm thu (Acceptance Criteria) phải được ký khóa đóng băng trước khi chạy bất kỳ vòng đánh giá nào để tránh thiên kiến điều chỉnh tiêu chí theo kết quả mô hình.
Một điều còn chưa chắc: Cách kiểm soát tỷ lệ escalation tối ưu khi bùng nổ lượng vé phức tạp trong mùa khuyến mãi lớn.

## BuiQuangHuy-2A202603469

### Phần việc phụ trách

Kỹ sư cổng (AI Engineer - Người 2).
- Trace ticket lỗi, phân tích hành vi model.
- Thiết kế và lập trình các guard phòng ngừa trong `lab10/guards.py`.
- Thiết kế monitor theo dõi trong `lab10/monitors.py`.
- Thực thi đánh giá các mốc (prepared, after) và kiểm thử hồi quy.

### Đóng góp cụ thể

- Dò trace ticket `T-002@55` phát hiện lỗ hổng agent tin lời khách khai hơn dữ liệu DB.
- Cài đặt guard kiểm tra quyền lợi thực tế và chặn ghi phạt oan hãng vận chuyển.

### Bằng chứng

- File: `lab10/guards.py`, `lab10/guards_round1.py`; monitor mới chưa thực hiện (thuộc vòng 2).
- Prepared: `R-base-prepared-20261118-151525-7c6c78`, hash `adfce180`; 110/110 đạt, không regression; 13 public tests OK.
- Có dùng trợ lý AI Codex để đọc trace, triển khai guard, chạy kiểm thử và ghi bằng chứng vòng 1.

### Exit ticket

Một điều học được: Guard tầng ngoài model là bắt buộc để ngăn chặn các hành vi không thể đảo ngược như xuất tiền quỹ hay ghi phạt pháp lý.
Một điều còn chưa chắc: Làm thế nào để guard không làm tăng quá nhiều độ trễ xử lý (latency) của luồng tổng thể.

### Bổ sung đóng góp vòng 2 — S5

- Sửa guard theo quyền lợi còn lại thay vì chặn toàn bộ đơn có sổ cái; chặn hoàn trùng và retry, bảo toàn ca hoàn bù S5-21.
- Ước tính chi phí toàn luồng trước LLM, bao gồm checkout_note và retry; thêm ba monitor duplicate_refund_attempts, llm_budget_blocks, partial_refund_adjustments.
- Áp dụng scope HN/HCM/DN/CT theo phân công PO; chạy grade S5 PASS-VISIBLE (`R-S5-grade-20261118-163306-de8e77`), regression 110/110, public tests 13/13.
- Dùng Codex hỗ trợ đọc trace, triển khai code, chạy kiểm chứng và ghi bằng chứng C7/C8. Chưa chạy hidden tests.

## NguyenManhQuyen-2A202603518

### Phần việc phụ trách

Đánh giá chất lượng (QA / Evaluation Engineer - Người 3).
- Thực thi kiểm thử 13 public tests (`pytest tests/`).
- Lập bảng phân tích lỗi cho ticket `T-002@55` ở Phiếu B mục B2.
- Phân tích rủi ro hệ thống qua HAZOP (B4) và Pre-mortem (B6).
- Đo lường và xác minh kết quả sau mỗi lần cập nhật guard.

### Đóng góp cụ thể

- Phân loại lỗi `T-002@55` thuộc nhóm Lỗi chìm (Silent Failure) gây thất thoát quỹ và phạt oan đối tác.
- Thực hiện kiểm thử bộ test cơ sở đảm bảo không phát sinh regression lỗi.

### Bằng chứng

- Bảng soát lỗi mục B2, bảng HAZOP mục B4 trong `templates/form-b-evaluation-gates.md`.

### Exit ticket

Một điều học được: Phân biệt rõ giữa Lỗi ngữ cảnh và Lỗi chìm; lỗi chìm nguy hiểm nhất vì hệ thống và người dùng đều không biết mình sai.
Một điều còn chưa chắc: Phương pháp giả lập các corner-case hiếm gặp trong production bằng synthetic data test suite.

## NguyenTruongThanh-2A202603512

### Phần việc phụ trách

Vận hành và pháp lý (Operations / Legal Engineer - Người 4).
- Cấu hình vận hành và pháp lý trong `config/operating_gates.json` (mục `operations` và `legal`).
- Lập Checklist 9 nhóm việc go-live (Phiếu B mục B5).
- Xây dựng Runbook xử lý sự cố hàng chờ và kế hoạch ứng phó giờ cao điểm (B7.5, B7.6).
- Hoàn thiện hồ sơ nộp bài `submission/submission.json`.

### Đóng góp cụ thể

- Thiết lập giới hạn vận hành ca trực (1 người trực duyệt tối đa 6 ca/giờ, SLA hàng chờ < 60 phút).
- Quy định các trường dữ liệu PII tuyệt đối không gửi sang bên thứ 3 (`phone`, `customer_name`, `street`).
- Xây dựng checklist 9 nhóm việc rõ ràng có chỉ định PIC cụ thể.

### Bằng chứng

- File: `config/operating_gates.json` (mục `operations`, `legal`), mục B5, B7 Phiếu B, `submission/submission.json`.

### Exit ticket

Một điều học được: Phải luôn có giới hạn vận hành (Ops Limits) và runbook ngắt khẩn cấp trước khi cho bất kỳ AI Agent nào chạy production.
Một điều còn chưa chắc: Cách phân định trách nhiệm pháp lý khi đối tác vận chuyển khiếu nại quyết định do AI đưa ra nhưng có người duyệt sơ sài.
