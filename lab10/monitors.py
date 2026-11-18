"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))


<<<<<<< HEAD
def avg_cost_per_ticket_vnd(trials):
    """Chi phí LLM trung bình mỗi ticket (đ).
    Sáng đèn khi kho B2B hoặc ticket dài đẩy chi phí vượt ngưỡng làm tay.
    Ngưỡng cảnh báo: > 1500đ (trần LLM) hoặc > 10000đ (chi phí làm tay).
    """
    costs = [t["cost_vnd"] for t in trials if t.get("cost_vnd") is not None]
    return sum(costs) / max(1, len(costs))


def pct_tickets_over_llm_cap(trials):
    """Tỉ lệ ticket có tiền LLM vượt trần 1500đ (phần trăm, 0–1).
    Phát hiện nhóm ticket nội dung dài (kho sỉ B2B) đẩy chi phí máy quá cao.
    Sáng đèn trên S5 vì kho HCM-B2B có ticket tốn 11326đ, ticket thường tốn 2466đ > 1500đ.
    """
    LLM_CAP = 1500
    over = sum(1 for t in trials if (t.get("cost_vnd") or 0) > LLM_CAP)
    return over / max(1, len(trials))


MONITORS = {
    "escalation_rate": escalation_rate,          # có sẵn; KHÔNG tính là metric mới của đội
    "avg_cost_per_ticket_vnd": avg_cost_per_ticket_vnd,       # Mới · S5: chi phí LLM trung bình
    "pct_tickets_over_llm_cap": pct_tickets_over_llm_cap,     # Mới · S5: tỉ lệ ticket vượt trần LLM
=======
def duplicate_refund_attempts(trials):
    """Blocked attempts after an order's total entitlement has already been paid."""
    return sum(e.get("type") == "guard" and e.get("kind") == "duplicate_refund_blocked"
               for t in trials for e in t.get("events", []))


def llm_budget_blocks(trials):
    """Tickets routed to humans before an estimated over-budget model call."""
    return sum(any(e.get("type") == "guard" and e.get("kind") == "llm_budget_blocked"
                   for e in t.get("events", [])) for t in trials)


def partial_refund_adjustments(trials):
    """Writes reduced to unpaid entitlement; distinct from blocked duplicates."""
    return sum(e.get("type") == "guard" and e.get("kind") == "partial_refund_adjusted"
               for t in trials for e in t.get("events", []))


MONITORS = {
    "escalation_rate": escalation_rate,
    "duplicate_refund_attempts": duplicate_refund_attempts,
    "llm_budget_blocks": llm_budget_blocks,
    "partial_refund_adjustments": partial_refund_adjustments,
>>>>>>> ca5e74685f14994af6b448a7b526724d55c40b13
}
STARTER_MONITORS = ("escalation_rate",)
