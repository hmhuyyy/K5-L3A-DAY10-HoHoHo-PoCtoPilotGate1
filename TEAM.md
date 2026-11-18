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

Vận hành và pháp lý (Operations / Legal Engineer, Người 4).
- `config/operating_gates.json` mục `operations` và `legal` (đề xuất giá trị vòng 1; xem ghi chú ở Bằng chứng).
- Phiếu B: B5 (checklist 9 nhóm việc, lần 1), B7.5 (Runbook phần 1–3), B7.6 (Giờ cao điểm).
- Phiếu C: C10 (Risk register), C11 (cập nhật checklist, Runbook phần 4–5).
- Cùng PO kiểm `submission/submission.json` và gom bài nộp.

### Đóng góp cụ thể

- Đặt cổng vận hành và pháp lý từ `data/world.json`: PIC `NV-TUNG` (người giữ công tắc), người duyệt `NV-HANH` (đúng người nhân viên tin theo `staff_behavior.trust_conditions`), 1 người trực, 6 ca/giờ (`ops_facts`), chờ tối đa 60 phút (`ops_limits.review_sla_minutes`), 4 điều kiện dừng, bật ghi chú quyết định và kiểm mẫu 10%; chặn `recipient_contact`, `customer_note` gửi hãng; chỉ ghi lỗi hãng khi tracking có nguyên nhân.
- Viết Runbook 1–3 và Giờ cao điểm có số đo thật: thử 2 người trực rồi trả lại 1 người để đo chi phí (4.457đ → 5.821đ/ticket, ROI 1.2 → 0.69).
- Thẻ S5: viết 6 dòng Risk register (hoàn trùng, kho sỉ HCM-B2B, tiền LLM, hoàn thiếu `S5-21`, hash bản chốt vòng 1, giờ trong nhật ký) và Runbook 4–5 (khiếu nại hoàn trùng, thu hồi và đối soát sổ cái); cập nhật lại theo số cuối sau khi bàn sửa cổng.
- Phát hiện và báo cho bàn: (1) cổng vòng 1 từ chối cả đơn đã hoàn một phần làm `S5-21` hỏng, cần hoàn phần còn thiếu; (2) `guards_round1.py` được chốt khi tệp còn đuôi dòng CRLF nên hash lệch `round1.lock` trên bản clone sạch (PO đã sửa ở `ed6cdf4`); (3) `core.autocrlf=true` làm đổi hash tiêu chí trên máy Windows; (4) mã kho `WH-HN-01`, `WH-SG-01` không có trong `data/world.json`; (5) `cost_budget_per_ticket_vnd` = 8.000 cao hơn trần LLM 1.500đ (đã thử 1.500: ticket đắt nhất 2.466đ → 764đ, bộ nền không hỏng ca nào).

### Bằng chứng

- Commit: `1b32bc2` (nhánh `ops-legal-part4`: config operations/legal, B5, B7.5, B7.6; phần runbook được PO đưa vào `main` ở `611120c`), `7dce7f1` (C10, C11, Runbook 4–5; vào `main` qua PR #1, `93b3ada`), `11f0a69` (cập nhật C10/C11 theo số cuối và mục này).
- Lần chạy (trên máy cá nhân): `R-base-after-20261118-145802-ab0e5b` (cổng operations/legal trên bộ nền), `R-base-after-20261118-152827-790008` (thử 2 người trực), `R-S5-grade-20261118-163546-8a2954` (S5 trước khi sửa), `R-S5-after-20261118-163738-831c3b` và `R-base-after-20261118-163739-831c3b` (thử ngân sách LLM 1.500đ), `R-S5-grade-20261118-171227-b1c825` (kiểm lại trên `main`: PASS-VISIBLE).
- Phiếu: B5, B7.5, B7.6 trong `templates/form-b-evaluation-gates.md`; C10, C11 trong `templates/form-c-incident.md`.
- Ghi chú: giá trị `operations`/`legal` đang ở `main` và bản chốt vòng 1 là bản bàn đã gộp, chưa phải giá trị trong `1b32bc2`.
- Có dùng trợ lý AI (Claude Code) để đọc code của lab, chạy các lệnh kiểm tra, dò nguyên nhân lỗi hash và soạn nháp câu chữ cho phiếu; các con số đều lấy từ report và `data/world.json`, tôi kiểm lại trước khi nộp.

### Exit ticket

Một điều học được: Phải luôn có giới hạn vận hành (Ops Limits) và runbook ngắt khẩn cấp trước khi cho bất kỳ AI Agent nào chạy production.
Một điều còn chưa chắc: Cách phân định trách nhiệm pháp lý khi đối tác vận chuyển khiếu nại quyết định do AI đưa ra nhưng có người duyệt sơ sài.
