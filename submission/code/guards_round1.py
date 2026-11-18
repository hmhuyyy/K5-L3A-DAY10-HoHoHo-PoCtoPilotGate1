"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if policy is None:
        return Verdict.escalate("No effective policy; human review required")
    return Verdict.allow(policy_id=policy["policy_id"])


def write_gate(ctx, action):
    tool = action.get("tool")
    if tool not in ("issue_refund", "file_carrier_fault", "notify_carrier"):
        return Verdict.allow()
    order = ctx.tools.lookup_order(action.get("order_id") or
                                   action.get("payload", {}).get("order_id"))
    policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
    if (not order or not policy or not order.get("parcels")
            or order["order_id"] != ctx.ticket.get("order_id")
            or order["customer_id"] != ctx.ticket.get("customer_id")):
        return Verdict.escalate("Missing or inconsistent authoritative order/policy")
    if ctx.ticket.get("parcel_id") and not any(
            p["parcel_id"] == ctx.ticket["parcel_id"] for p in order["parcels"]):
        return Verdict.escalate("Requested parcel does not belong to order")
    parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
    delay = H.db_delay_days(parcel, ctx.as_of)
    limits = ctx.tools.ops_limits()

    # Gate 1: verify policy entitlement before any money leaves the ledger.
    if tool == "issue_refund":
        cause = parcel.get("delay_cause")
        if cause is None and delay > 0:
            return Verdict.escalate("Delay cause missing; verify before refund")
        entitled = H.entitlement_vnd(policy, order, delay, cause)
        ctx.log("refund_entitlement_checked", db_delay_days=delay,
                entitled_vnd=entitled, proposed_vnd=action.get("amount_vnd"))
        if entitled <= 0:
            return Verdict.deny("Tracking and effective policy give no refund entitlement")
        if ctx.tools.ledger_rows(order_id=order["order_id"]):
            return Verdict.deny("Order already has a refund; prevent duplicate write")
        if (action.get("amount_vnd") != entitled or action.get("payer") != "LOGIX"
                or action.get("basis") == "fail_open"):
            return Verdict.escalate("Unverified refund proposal; human review required")
        approval_id = action.get("approval_id")
        if entitled > policy["auto_limit_vnd"] or approval_id:
            approvals = ctx.tools.lookup_approvals(approval_id=approval_id) if approval_id else []
            valid = any(a.get("status") == "valid"
                        and a.get("ticket_id") == ctx.ticket["ticket_id"]
                        and a.get("order_id") == order["order_id"]
                        and a.get("customer_id") == order["customer_id"]
                        and a.get("expires_at", "") >= ctx.as_of
                        and a.get("max_vnd", 0) >= entitled
                        for a in approvals)
            if not valid:
                return Verdict.escalate("Missing, expired or mismatched approval")
        return Verdict.allow()

    # Gate 2: carrier fault must be supported by the selected parcel's tracking.
    if tool == "file_carrier_fault":
        if not H.carrier_at_fault(policy, parcel, delay):
            return Verdict.deny("Tracking does not establish carrier fault")
        cap = limits.get("max_auto_strikes_per_carrier_per_day")
        strikes = ctx.tools.fault_rows(carrier_id=parcel["carrier_id"])
        if cap is not None and len(strikes) >= cap:
            return Verdict.deny("Automatic carrier strike limit reached; manual review required")
        expected = {"parcel_id": parcel["parcel_id"], "carrier_id": parcel["carrier_id"],
                    "driver_id": parcel.get("driver_id"), "delay_days": delay}
        if any(action.get(k) != v for k, v in expected.items()):
            return Verdict.modify("Use authoritative parcel tracking", **expected)
        return Verdict.allow()

    # Gate 3: send only policy-approved structured fields, never customer free text.
    payload = {"order_id": order["order_id"], "parcel_id": parcel["parcel_id"],
               "district": order["recipient"]["district"], "delay_days": delay}
    fields = set(policy.get("carrier_notice_fields", []))
    blocked = set((ctx.gates or {}).get("legal", {}).get(
        "pii_fields_blocked_to_third_party", []))
    payload = {k: v for k, v in payload.items() if k in fields and k not in blocked}
    return Verdict.modify("Send minimum policy-approved carrier notice",
                          carrier_id=parcel["carrier_id"], payload=payload)
