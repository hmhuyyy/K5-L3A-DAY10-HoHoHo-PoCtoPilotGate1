# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** HoHoHo · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Tự động hoá xử lý khiếu nại hoàn tiền giao trễ end-to-end, rút ngắn thời gian xử lý khiếu nại từ 24h xuống dưới 15 phút, giảm tải ít nhất 70% khối lượng thao tác lặp lại của CSKH nhưng đảm bảo chính xác tài chính 100% (không xuất quỹ sai, không phạt oan hãng đối tác, chi phí vận hành mỗi ticket dưới 8.000đ).

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): Mọi giao dịch hoàn tiền tự động và ghi lỗi phạt hãng phải khớp 100% với tracking và điều khoản hợp đồng/chính sách; không phát sinh khoản chênh lệch tiền hoàn ngoài dự toán (`wrongful_refund_vnd = 0`) và không có khiếu nại phạt oan từ đối tác vận chuyển (`wrongful_carrier_faults = 0`).
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): Tỷ lệ ca phải chuyển lên người duyệt (escalation) dưới 25% công suất ca trực (không làm nghẽn hàng chờ, thời gian chờ < 60 phút); mỗi ca chuyển lên đều có tóm tắt lý do và dẫn chứng trích xuất rõ ràng để người duyệt xử lý trong dưới 2 phút.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước chọn chính sách hoàn tiền (`policy_check`) | Hành vi ghi lỗi phạt hãng vận chuyển ra bên ngoài |
| **Thước đo** (một câu, có đơn vị) | Tỷ lệ chọn đúng chính sách hoàn tiền trên các ticket hợp lệ (đơn vị: %). | Tỷ lệ đối tác vận chuyển phản hồi khiếu nại biên bản phạt lỗi trong ngày (đơn vị: %). |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | `traces/` sự kiện `policy_selected` so với ground-truth `expected_policy` trong bộ 22 ticket × 5 seed. Do chuyên viên chính sách gán nhãn. | Số sự kiện ghi phạt qua webhook/API đối tác và số vé phản ánh phản đối từ hãng trong hệ thống CSKH đối tác (portal LogiX). |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | Số lần `policy_selected == expected_policy` chia cho tổng số ticket có bước áp chính sách. Ca lỗi trước bước này tính riêng. | Số biên bản phạt bị hãng khiếu nại chia cho tổng số biên bản phạt được agent tự động phát hành trong ngày. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Khung: theo ngày (24h) hoặc theo ca trực 8h. Ngưỡng báo động: > 1% hoặc có từ 2 hãng khiếu nại trong ca. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không đo được liệu câu từ phản hồi gửi khách hàng có thân thiện hay giải thích thỏa đáng không. | Không phát hiện được trường hợp hãng bị phạt oan nhưng không khiếu nại (do số tiền phạt nhỏ hoặc chưa rà soát kịp). |

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Khoanh: **(b)**

Giải thích một câu: Khoảng tin cậy 95% của phiên bản X là [0,9400; 1,0] bao trùm kết quả 1,0 của phiên bản Y, do đó sự chênh lệch 1 lần chạy trên mẫu 50 chưa đạt mức ý nghĩa thống kê để khẳng định Y vượt trội hơn X.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

#### Bước 1 · Viết câu tiêu chí

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu pass_rate của trợ lý hoàn tiền trên bộ nền tụt dưới 0.95 thì chúng tôi sẽ Cải tiến thêm prompt/guard trong 2 ngày trước khi quyết định lại. | Nếu pass_rate tụt dưới 0.90 thì Dừng pilot. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu pass_k trên bộ nền tụt dưới 0.90 thì chúng tôi sẽ Thu hẹp phạm vi chỉ chạy trên các ca đơn giản (1 kiện hàng, độ trễ rõ ràng). | |
| `wrongful_refund_vnd_max` | Nếu tổng số tiền hoàn sai trên bất kỳ bộ thử nào vượt quá 0 VND thì chúng tôi sẽ Dừng việc tự động xuất quỹ và chuyển 100% sang người duyệt. | |
| `wrongful_carrier_faults_max` | Nếu số lỗi phạt oan hãng vận chuyển vượt quá 0 lỗi thì chúng tôi sẽ Thu hẹp bằng cách tắt tool tự động phạt hãng cho đến khi kiểm chứng lại. | |
| `pii_leaks_max` | Nếu phát hiện rò rỉ dữ liệu cá nhân (PII) vượt quá 0 trường hợp thì chúng tôi sẽ Dừng hệ thống ngay lập tức để vá bảo mật. | |
| nên có: `escalation_rate_max` | Nếu tỷ lệ chuyển người duyệt vượt quá 0.25 (25%) thì chúng tôi sẽ Cải tiến thêm bộ trích xuất dữ liệu để tăng tỷ lệ tự giải quyết. | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

- Một đầu ra hoặc hành động bị cấm: Không bao giờ tự động hoàn tiền quá 300.000đ/khách/ngày và không tự động hoàn khi tracking đơn chưa cập nhật trạng thái giao nhận cuối cùng.
- Ngưỡng chuyển cho người duyệt: Chuyển người duyệt khi số tiền hoàn vượt 300.000đ, hoặc hãng đã ghi nhận từ lỗi thứ 3 trong ngày, hoặc khách hàng có dấu hiệu khiếu nại gay gắt/từ ngữ tranh chấp pháp lý.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Có: Bảo vệ tài chính LogiX (Kế toán), tránh phạt oan đối tác (Hãng), không quá tải ca trực (Trưởng ca), giải quyết nhanh (Khách). |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Nếu ép pass_rate và giảm escalation quá mức, rủi ro chuyển về phía nhân viên duyệt (phải đọc ca khó vội) hoặc kế toán (phải đối soát bù nếu lọt lỗi). Vì vậy ngưỡng an toàn max = 0 là bất khả xâm phạm. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Đúng: Ngày 1 an toàn và không gây thiệt hại thực tế là ưu tiên số một. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Ngưỡng `cost_per_ticket_vnd_max` và `escalation_rate_max` sẽ phải thắt chặt hơn khi quy mô mở rộng; `daily_refund_cap_vnd` phải tăng tương ứng theo sản lượng đơn. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Chi phí mỗi ticket tối đa: `cost_per_ticket_vnd_max`: 8000 VND · ROI tối thiểu: `roi_min`: 0.20 · Số ca ùn tối đa: `queue_stuck_max`: 0
- Ngày xem lại tiêu chí: `2026-11-25` · Ai dự: Product Owner, Trưởng ca CSKH, Kế toán đối soát, Lead AI Engineer.

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | 2026-11-18 14:36:18 |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | `596a3ad` |
| Đã push lên `origin main` thành công? | có |
