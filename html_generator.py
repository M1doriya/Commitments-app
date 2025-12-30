"""
HTML Generator Module for Kredit Lab Streamlit App
===================================================
This module generates the complete HTML report from analysis data.
"""

from datetime import datetime
from typing import Dict

TYPE_BADGE_MAP = {
    "Strict 1": '<span class="type-badge type-strict1">🔴 S1</span>',
    "Strict 2": '<span class="type-badge type-strict2">🟣 S2</span>',
    "Preference": '<span class="type-badge type-pref">🟡 Pref</span>',
    "Informational": '<span class="type-badge type-info">🔵 Info</span>',
    "Not Applicable": '<span class="type-badge type-na">⚪ N/A</span>',
}

STATUS_BADGE_MAP = {
    "PASS": '<span class="status-badge status-pass">✅ Pass</span>',
    "FAIL": '<span class="status-badge status-fail">❌ Fail</span>',
    "N/A": '<span class="status-badge status-na">⚪ N/A</span>',
    "INFO": '<span class="status-badge status-info">ℹ Info</span>',
}

GRADE_CSS_MAP = {"A": "a", "B": "b", "C": "c", "D": "d", "E": "e"}

BANK_IDS = {
    "RHB": "rhb", "Maybank": "maybank", "CIMB": "cimb",
    "Standard Chartered": "sc", "SME Bank": "sme", "Bank Rakyat": "rakyat",
}

CCRIS_PARAM_NAMES = [
    "CCRIS Vintage", "Property Ownership", "Declined (12mo)", "WC Applications (12mo)",
    "Credit App Status", "Status A (Accepted)", "Status T (Pending)", "Status P (Pending Approval)",
    "Special Attention Account", "R&R / AKPK Status", "Overdraft Utilization", "Credit Card Utilization",
    "Conduct of Account (12mo)", "Current Month Arrears", "Non-Bank Lender", "Director Personal Loan",
]

CTOS_PARAM_NAMES = ["No Legal Suits", "Legal Suit (Defendant)", "Trade Bureau", "Legal Status on Loan"]


def generate_html_report(data: Dict) -> str:
    """Generate complete HTML report from analysis data."""
    company_name = data.get("company", {}).get("name", "Unknown Company")
    company = data.get("company", {})
    meta = data.get("meta", {})
    c = data.get("consolidated", {})
    banks = data.get("banks", {})
    
    score = c.get("score", 0)
    s1_pass, s1_total = c.get("strict1_pass", 0), c.get("strict1_total", 0)
    s2_pass, s2_total = c.get("strict2_pass", 0), c.get("strict2_total", 0)
    pref_pass, pref_total = c.get("preference_pass", 0), c.get("preference_total", 0)
    s1_pct = round((s1_pass / s1_total * 100) if s1_total > 0 else 100, 1)
    s2_pct = round((s2_pass / s2_total * 100) if s2_total > 0 else 100, 1)
    pref_pct = round((pref_pass / pref_total * 100) if pref_total > 0 else 0, 1)
    
    final_grade = c.get("final_grade", "C")
    raw_grade = c.get("raw_grade", "C")
    fg_lower = GRADE_CSS_MAP.get(final_grade, "c")
    rg_lower = GRADE_CSS_MAP.get(raw_grade, "c")
    is_pass = final_grade in ["A", "B", "C"]
    status_class = "pass" if is_pass else "fail"
    status_text = "ELIGIBLE" if is_pass else "NOT ELIGIBLE"
    reason = "Strict 1 Failed" if final_grade == "E" else "Strict 2 Failed" if final_grade == "D" else "All Strict Passed"
    
    entities = data.get("entities", [])
    entity_rows = f'<tr><td><span class="type-badge type-info">Company</span></td><td>{company.get("name", "N/A")}</td><td>{company.get("reg_no", "N/A")}</td><td>—</td></tr>'
    for e in entities:
        t = e.get("type", "Director")
        tc = "type-strict2" if t == "Director" else "type-pref"
        entity_rows += f'<tr><td><span class="type-badge {tc}">{t}</span></td><td>{e.get("name", "N/A")}</td><td>{e.get("ic", "N/A")}</td><td>{e.get("shareholding", "—")}</td></tr>'
    
    bank_cards = ""
    for bn in ["RHB", "Maybank", "CIMB", "Standard Chartered", "SME Bank", "Bank Rakyat"]:
        bd = banks.get(bn, {})
        fg = bd.get("final_grade", "C")
        rg = bd.get("raw_grade", "C")
        sc = bd.get("score", 0)
        s1 = f"{bd.get('strict1_pass', 0)}/{bd.get('strict1_total', 0)}"
        s2 = f"{bd.get('strict2_pass', 0)}/{bd.get('strict2_total', 0)}"
        pf = f"{bd.get('preference_pass', 0)}/{bd.get('preference_total', 0)}"
        fgl = GRADE_CSS_MAP.get(fg, "c")
        bank_cards += f'<div class="summary-card"><h3>{bn}</h3><div class="summary-grade grade-{fgl}">{fg}</div><div class="summary-score">Score: {sc}%</div><div class="summary-raw">Raw: {rg} → Final: {fg}</div><div style="margin-top: 8px; font-size: 10px; color: var(--text-muted);">🔴 {s1} • 🟣 {s2} • 🟡 {pf}</div></div>'
    
    bank_tabs = ""
    bank_contents = ""
    first = True
    for bn, bid in BANK_IDS.items():
        ac = "active" if first else ""
        bank_tabs += f'<div class="bank-tab {ac}" onclick="showBank(\'{bid}\')">{bn}</div>'
        bd = banks.get(bn, {})
        ccris = bd.get("ccris", [])
        ctos = bd.get("ctos", [])
        
        ccris_rows = ""
        for i, p in enumerate(ccris):
            cl = p.get("classification", "Not Applicable")
            st = p.get("status", "N/A")
            cr = p.get("criteria", "—")
            ev = p.get("evidence", "—")
            tb = TYPE_BADGE_MAP.get(cl, TYPE_BADGE_MAP["Not Applicable"])
            sb = STATUS_BADGE_MAP.get(st, STATUS_BADGE_MAP["N/A"])
            pname = CCRIS_PARAM_NAMES[i] if i < len(CCRIS_PARAM_NAMES) else f"Param {i+1}"
            ccris_rows += f'<tr><td>{i+1}</td><td>{pname}</td><td>{tb}</td><td>{cr}</td><td>{sb}</td><td>{ev}</td></tr>'
        
        ctos_rows = ""
        for i, p in enumerate(ctos):
            cl = p.get("classification", "Not Applicable")
            st = p.get("status", "N/A")
            cr = p.get("criteria", "—")
            ev = p.get("evidence", "—")
            tb = TYPE_BADGE_MAP.get(cl, TYPE_BADGE_MAP["Not Applicable"])
            sb = STATUS_BADGE_MAP.get(st, STATUS_BADGE_MAP["N/A"])
            pname = CTOS_PARAM_NAMES[i] if i < len(CTOS_PARAM_NAMES) else f"Param {i+1}"
            ctos_rows += f'<tr><td>{i+1}</td><td>{pname}</td><td>{tb}</td><td>{cr}</td><td>{sb}</td><td>{ev}</td></tr>'
        
        sc = bd.get("score", 0)
        rg = bd.get("raw_grade", "C")
        fg = bd.get("final_grade", "C")
        
        bank_contents += f'''<div id="bank-{bid}" class="bank-content {ac}"><div class="table-card"><h3 style="margin-bottom: 12px; color: var(--text-main);">CCRIS Parameters (16)</h3><div class="table-wrapper"><table><thead><tr><th>#</th><th>Parameter</th><th>Type</th><th>Criteria</th><th>Status</th><th>Evidence</th></tr></thead><tbody>{ccris_rows}</tbody></table></div><h3 style="margin: 24px 0 12px; color: var(--text-main);">CTOS Parameters (4)</h3><div class="table-wrapper"><table><thead><tr><th>#</th><th>Parameter</th><th>Type</th><th>Criteria</th><th>Status</th><th>Evidence</th></tr></thead><tbody>{ctos_rows}</tbody><tfoot><tr><td colspan="4" class="text-right">{bn} Score:</td><td colspan="2" class="value-highlight">{sc}% — Raw {rg} → Final {fg}</td></tr></tfoot></table></div></div></div>'''
        first = False
    
    strengths = data.get("strengths", [])
    attention = data.get("attention_items", [])
    sh = "".join([f'<div class="badge badge-ok" style="width: fit-content;"><span class="icon">✓</span> {s}</div>' for s in strengths]) or '<div style="color: var(--text-muted); font-size: 12px;">No notable strengths identified</div>'
    ah = "".join([f'<div class="badge badge-fail" style="width: fit-content;"><span class="icon">✗</span> {a}</div>' for a in attention]) or '<div style="color: var(--text-muted); font-size: 12px;">No critical issues identified</div>'
    
    css = ''':root { --bg: #0f172a; --bg-alt: #020617; --card-bg: #0b1120; --border-subtle: #1e293b; --accent: #22c55e; --danger: #ef4444; --warn: #f59e0b; --info: #3b82f6; --text-main: #e5e7eb; --text-soft: #9ca3af; --text-muted: #6b7280; --grade-a: #10b981; --grade-a-bg: rgba(16,185,129,0.15); --grade-b: #3b82f6; --grade-b-bg: rgba(59,130,246,0.15); --grade-c: #f59e0b; --grade-c-bg: rgba(245,158,11,0.15); --grade-d: #f97316; --grade-d-bg: rgba(249,115,22,0.15); --grade-e: #ef4444; --grade-e-bg: rgba(239,68,68,0.15); --strict1-red: #ef4444; --strict1-red-bg: rgba(239,68,68,0.15); --strict2-purple: #a855f7; --strict2-purple-bg: rgba(168,85,247,0.15); --pref-yellow: #eab308; --pref-yellow-bg: rgba(234,179,8,0.15); --info-blue: #3b82f6; --info-blue-bg: rgba(59,130,246,0.15); --shadow-soft: 0 18px 45px rgba(15,23,42,0.8); --radius-lg: 20px; --radius-md: 14px; --radius-sm: 10px; --radius-pill: 999px; }
* { box-sizing: border-box; }
body { margin: 0; padding: 32px 16px 40px; font-family: system-ui, -apple-system, sans-serif; background: radial-gradient(circle at top left, #1e293b, #020617 40%, #000); color: var(--text-main); min-height: 100vh; }
.page { max-width: 1400px; margin: 0 auto; } h1, h2, h3, h4 { margin: 0; font-weight: 600; }
.header-card { background: radial-gradient(circle at top left, rgba(56,189,248,0.22), rgba(15,23,42,0.98)); border-radius: 24px; padding: 20px 24px 18px; border: 1px solid rgba(148,163,184,0.3); box-shadow: var(--shadow-soft); }
.header-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 16px; margin-bottom: 16px; }
.title-block { flex: 1; }
.pill { display: inline-flex; align-items: center; gap: 6px; padding: 4px 10px; border-radius: var(--radius-pill); border: 1px solid rgba(148,163,184,0.35); background: radial-gradient(circle at top left, #0f172a, #020617); color: var(--text-soft); font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 10px; }
.title-block h1 { font-size: 24px; display: flex; align-items: center; gap: 12px; }
.title-icon { width: 32px; height: 32px; border-radius: 10px; display: inline-flex; align-items: center; justify-content: center; background: radial-gradient(circle at 30% 10%, #8b5cf6, #6d28d9); box-shadow: 0 0 0 1px rgba(139,92,246,0.8), 0 12px 25px rgba(109,40,217,0.7); font-size: 18px; }
.title-block p { margin: 8px 0 0; color: var(--text-soft); font-size: 13px; }
.header-meta { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px 24px; font-size: 12px; }
.meta-label { color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; font-size: 10px; margin-bottom: 3px; }
.meta-value { color: #e5e7eb; font-weight: 500; }
.header-bottom { display: flex; justify-content: space-between; gap: 12px; align-items: center; padding-top: 12px; border-top: 1px solid rgba(148,163,184,0.2); }
.badges { display: flex; flex-wrap: wrap; gap: 8px; }
.badge { font-size: 11px; padding: 4px 10px; border-radius: var(--radius-pill); display: inline-flex; align-items: center; gap: 6px; border: 1px solid transparent; }
.badge-ok { border-color: rgba(34,197,94,0.5); background: rgba(22,163,74,0.18); color: #bbf7d0; }
.badge-fail { border-color: rgba(239,68,68,0.6); background: rgba(239,68,68,0.15); color: #fca5a5; }
.badge-info { border-color: rgba(59,130,246,0.6); background: rgba(59,130,246,0.15); color: #93c5fd; }
.card { background: linear-gradient(135deg, rgba(15,23,42,0.96), rgba(2,6,23,0.97)); border-radius: var(--radius-lg); border: 1px solid rgba(30,64,175,0.75); box-shadow: var(--shadow-soft); padding: 18px 18px 16px; }
.card h2 { font-size: 15px; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
.dashboard-grid { display: grid; grid-template-columns: 1fr 320px; gap: 18px; margin-top: 20px; }
.kpi-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }
.kpi { border-radius: var(--radius-md); padding: 12px 14px; background: radial-gradient(circle at top left, #020617, #020617 45%, #020617); border: 1px solid rgba(148,163,184,0.35); }
.kpi-label { font-size: 10px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }
.kpi-value { font-size: 18px; font-weight: 600; margin-bottom: 4px; }
.kpi-chip { font-size: 11px; color: var(--text-soft); }
.kpi-positive .kpi-value { color: #4ade80; } .kpi-negative .kpi-value { color: #f87171; } .kpi-highlight .kpi-value { color: #facc15; }
.gauge-container { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px; }
.grade-display { width: 140px; height: 140px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 72px; font-weight: 700; }
.grade-display.grade-a { background: linear-gradient(135deg, var(--grade-a-bg), rgba(16,185,129,0.3)); border: 4px solid var(--grade-a); box-shadow: 0 0 40px rgba(16,185,129,0.4); color: var(--grade-a); }
.grade-display.grade-b { background: linear-gradient(135deg, var(--grade-b-bg), rgba(59,130,246,0.3)); border: 4px solid var(--grade-b); box-shadow: 0 0 40px rgba(59,130,246,0.4); color: var(--grade-b); }
.grade-display.grade-c { background: linear-gradient(135deg, var(--grade-c-bg), rgba(245,158,11,0.3)); border: 4px solid var(--grade-c); box-shadow: 0 0 40px rgba(245,158,11,0.4); color: var(--grade-c); }
.grade-display.grade-d { background: linear-gradient(135deg, var(--grade-d-bg), rgba(249,115,22,0.3)); border: 4px solid var(--grade-d); box-shadow: 0 0 40px rgba(249,115,22,0.4); color: var(--grade-d); }
.grade-display.grade-e { background: linear-gradient(135deg, var(--grade-e-bg), rgba(239,68,68,0.3)); border: 4px solid var(--grade-e); box-shadow: 0 0 40px rgba(239,68,68,0.4); color: var(--grade-e); }
.grade-status { margin-top: 16px; padding: 8px 20px; border-radius: var(--radius-pill); font-size: 13px; font-weight: 600; text-transform: uppercase; }
.grade-status.status-pass { background: var(--grade-a-bg); color: var(--grade-a); border: 1px solid var(--grade-a); }
.grade-status.status-fail { background: var(--grade-d-bg); color: var(--grade-d); border: 1px solid var(--grade-d); }
.section { margin-top: 24px; }
.section-header { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 12px; }
.section-title { font-size: 15px; font-weight: 600; display: flex; align-items: center; gap: 8px; }
.section-subtitle { font-size: 11px; color: var(--text-muted); margin-top: 2px; }
.table-card { background: linear-gradient(145deg, #020617, #020617); border-radius: var(--radius-lg); border: 1px solid rgba(31,41,55,0.9); box-shadow: var(--shadow-soft); padding: 16px; overflow: hidden; }
.table-wrapper { overflow-x: auto; }
table { width: 100%; border-collapse: collapse; font-size: 12px; }
thead th { text-align: left; padding: 10px 12px; background: radial-gradient(circle at top left, #020617, #020617); color: #9ca3af; font-weight: 500; text-transform: uppercase; letter-spacing: 0.06em; border-bottom: 1px solid rgba(55,65,81,0.9); white-space: nowrap; }
tbody td { padding: 8px 12px; border-bottom: 1px solid rgba(31,41,55,0.7); }
tbody tr:nth-child(even) { background: rgba(15,23,42,0.9); }
tbody tr:nth-child(odd) { background: rgba(15,23,42,0.98); }
tbody tr:hover { background: rgba(30,64,175,0.15); }
tfoot td { padding: 10px 12px; background: linear-gradient(90deg, rgba(250,204,21,0.12), rgba(55,65,81,0.95)); border-top: 1px solid rgba(250,204,21,0.95); font-weight: 600; }
.text-right { text-align: right; } .value-positive { color: #4ade80; } .value-negative { color: #f87171; } .value-highlight { color: #facc15; font-weight: 600; }
.status-badge { display: inline-flex; align-items: center; gap: 4px; padding: 4px 10px; border-radius: var(--radius-pill); font-size: 10px; font-weight: 600; text-transform: uppercase; }
.status-pass { background: rgba(34,197,94,0.15); color: #22c55e; border: 1px solid #22c55e; }
.status-fail { background: var(--strict1-red-bg); color: var(--strict1-red); border: 1px solid var(--strict1-red); }
.status-na { background: rgba(107,114,128,0.15); color: #9ca3af; border: 1px solid #6b7280; }
.status-info { background: var(--info-blue-bg); color: var(--info-blue); border: 1px solid var(--info-blue); }
.type-badge { display: inline-flex; align-items: center; gap: 4px; padding: 3px 8px; border-radius: var(--radius-pill); font-size: 9px; font-weight: 600; text-transform: uppercase; }
.type-strict1 { background: var(--strict1-red-bg); color: var(--strict1-red); border: 1px solid var(--strict1-red); }
.type-strict2 { background: var(--strict2-purple-bg); color: var(--strict2-purple); border: 1px solid var(--strict2-purple); }
.type-pref { background: var(--pref-yellow-bg); color: var(--pref-yellow); border: 1px solid var(--pref-yellow); }
.type-info { background: var(--info-blue-bg); color: var(--info-blue); border: 1px solid var(--info-blue); }
.type-na { background: rgba(107,114,128,0.15); color: #9ca3af; border: 1px solid #6b7280; }
.bank-tabs { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
.bank-tab { padding: 10px 16px; border-radius: var(--radius-md); font-size: 12px; font-weight: 500; cursor: pointer; transition: all 0.2s ease; border: 1px solid rgba(148,163,184,0.3); background: rgba(15,23,42,0.8); color: var(--text-soft); }
.bank-tab:hover { background: rgba(139,92,246,0.15); border-color: rgba(139,92,246,0.5); }
.bank-tab.active { background: rgba(139,92,246,0.25); border-color: #a855f7; color: #c4b5fd; box-shadow: 0 0 12px rgba(139,92,246,0.3); }
.bank-content { display: none; } .bank-content.active { display: block; }
.summary-grid { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 12px; margin-top: 20px; }
.summary-card { border-radius: var(--radius-md); padding: 16px; background: radial-gradient(circle at top left, #020617, #0f172a); border: 1px solid rgba(148,163,184,0.25); text-align: center; }
.summary-card h3 { font-size: 12px; color: var(--text-soft); margin-bottom: 8px; }
.summary-grade { font-size: 36px; font-weight: 700; margin-bottom: 8px; }
.summary-grade.grade-a { color: var(--grade-a); } .summary-grade.grade-b { color: var(--grade-b); } .summary-grade.grade-c { color: var(--grade-c); } .summary-grade.grade-d { color: var(--grade-d); } .summary-grade.grade-e { color: var(--grade-e); }
.summary-score { font-size: 14px; color: var(--text-main); font-weight: 600; }
.summary-raw { font-size: 11px; color: var(--text-muted); margin-top: 4px; }
.progress-container { margin-top: 12px; }
.progress-label { display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 4px; }
.progress-bar { height: 8px; background: rgba(55,65,81,0.4); border-radius: 4px; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 4px; }
.progress-fill.strict1 { background: linear-gradient(90deg, #ef4444, #f87171); }
.progress-fill.strict2 { background: linear-gradient(90deg, #a855f7, #c084fc); }
.progress-fill.pref { background: linear-gradient(90deg, #eab308, #facc15); }
.consolidated-card { border-radius: var(--radius-lg); padding: 32px; text-align: center; margin-top: 24px; box-shadow: var(--shadow-soft); }
.consolidated-card.grade-a-border { border: 2px solid var(--grade-a); background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(15,23,42,0.98)); }
.consolidated-card.grade-b-border { border: 2px solid var(--grade-b); background: linear-gradient(135deg, rgba(59,130,246,0.15), rgba(15,23,42,0.98)); }
.consolidated-card.grade-c-border { border: 2px solid var(--grade-c); background: linear-gradient(135deg, rgba(245,158,11,0.15), rgba(15,23,42,0.98)); }
.consolidated-card.grade-d-border { border: 2px solid var(--grade-d); background: linear-gradient(135deg, rgba(249,115,22,0.15), rgba(15,23,42,0.98)); }
.consolidated-card.grade-e-border { border: 2px solid var(--grade-e); background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(15,23,42,0.98)); }
.consolidated-card h2 { justify-content: center; font-size: 18px; margin-bottom: 20px; }
.consolidated-grades { display: flex; justify-content: center; gap: 48px; margin-bottom: 24px; }
.consolidated-grade-box { text-align: center; }
.consolidated-grade-label { font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 12px; }
.consolidated-grade-value { width: 100px; height: 100px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 48px; font-weight: 700; margin: 0 auto; }
.consolidated-grade-value.grade-a { background: var(--grade-a-bg); border: 3px solid var(--grade-a); color: var(--grade-a); }
.consolidated-grade-value.grade-b { background: var(--grade-b-bg); border: 3px solid var(--grade-b); color: var(--grade-b); }
.consolidated-grade-value.grade-c { background: var(--grade-c-bg); border: 3px solid var(--grade-c); color: var(--grade-c); }
.consolidated-grade-value.grade-d { background: var(--grade-d-bg); border: 3px solid var(--grade-d); color: var(--grade-d); }
.consolidated-grade-value.grade-e { background: var(--grade-e-bg); border: 3px solid var(--grade-e); color: var(--grade-e); }
.consolidated-grade-desc { font-size: 11px; color: var(--text-soft); margin-top: 8px; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
.icon { font-size: 16px; }
.footer { margin-top: 32px; padding: 16px 24px; background: rgba(15,23,42,0.6); border-radius: var(--radius-md); border: 1px solid rgba(148,163,184,0.2); display: flex; justify-content: space-between; font-size: 11px; color: var(--text-muted); }
@media (max-width: 1200px) { .dashboard-grid { grid-template-columns: 1fr; } .summary-grid { grid-template-columns: repeat(3, 1fr); } .kpi-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .summary-grid { grid-template-columns: repeat(2, 1fr); } .two-col { grid-template-columns: 1fr; } .consolidated-grades { flex-direction: column; gap: 24px; } }'''
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><title>Kredit Lab Report - {company_name}</title><meta name="viewport" content="width=device-width, initial-scale=1.0"><style>{css}</style></head>
<body><div class="page">
<div class="header-card"><div class="header-top"><div class="title-block"><div class="pill"><span>📊</span> Kredit Lab v3.1</div><h1><span class="title-icon">🏦</span> EXPERIAN REPORT ANALYSIS</h1><p>CCRIS & CTOS Multi-Bank Eligibility Assessment • 16 CCRIS + 4 CTOS Parameters</p></div><div class="header-meta"><div><div class="meta-label">Company</div><div class="meta-value">{company.get("name", "N/A")}</div></div><div><div class="meta-label">Registration No</div><div class="meta-value">{company.get("reg_no", "N/A")}</div></div><div><div class="meta-label">Report Date</div><div class="meta-value">{meta.get("report_date", "N/A")}</div></div><div><div class="meta-label">Analysis Date</div><div class="meta-value">{meta.get("analysis_date", "N/A")}</div></div></div></div><div class="header-bottom"><div class="badges"><div class="badge badge-info"><span>ℹ</span> 6 Banks Evaluated</div></div></div></div>
<div class="dashboard-grid"><div class="card"><h2><span class="icon">📈</span> Consolidated Scoring Summary</h2><div class="kpi-grid"><div class="kpi kpi-positive"><div class="kpi-label">Strict 1</div><div class="kpi-value">{s1_pass}/{s1_total}</div><div class="kpi-chip">{s1_pct}% Pass</div></div><div class="kpi kpi-negative"><div class="kpi-label">Strict 2</div><div class="kpi-value">{s2_pass}/{s2_total}</div><div class="kpi-chip">{s2_pct}% Pass</div></div><div class="kpi"><div class="kpi-label">Preference</div><div class="kpi-value">{pref_pass}/{pref_total}</div><div class="kpi-chip">{pref_pct}% Pass</div></div><div class="kpi kpi-highlight"><div class="kpi-label">Overall Score</div><div class="kpi-value">{score}%</div><div class="kpi-chip">All Banks</div></div></div><div class="progress-container"><div class="progress-label"><span>Strict 1 — 30% Weight</span><span class="value-positive">{s1_pass}/{s1_total} ({s1_pct}%)</span></div><div class="progress-bar"><div class="progress-fill strict1" style="width: {s1_pct}%;"></div></div></div><div class="progress-container"><div class="progress-label"><span>Strict 2 — 30% Weight</span><span class="value-negative">{s2_pass}/{s2_total} ({s2_pct}%)</span></div><div class="progress-bar"><div class="progress-fill strict2" style="width: {s2_pct}%;"></div></div></div><div class="progress-container"><div class="progress-label"><span>Preference — 40% Weight</span><span style="color: var(--pref-yellow);">{pref_pass}/{pref_total} ({pref_pct}%)</span></div><div class="progress-bar"><div class="progress-fill pref" style="width: {pref_pct}%;"></div></div></div></div><div class="card"><h2><span class="icon">🏆</span> Consolidated Grade</h2><div class="gauge-container"><div class="grade-display grade-{fg_lower}">{final_grade}</div><div class="grade-status status-{status_class}">{status_text}</div><p style="margin-top: 12px; font-size: 12px; color: var(--text-soft); text-align: center;">{c.get("explanation", "")}</p></div></div></div>
<div class="section"><div class="section-header"><div><div class="section-title"><span class="icon">👥</span> Entity Information</div><div class="section-subtitle">Company, Directors, and Related Parties</div></div></div><div class="table-card"><div class="table-wrapper"><table><thead><tr><th>Entity Type</th><th>Name</th><th>IC/Registration</th><th>Shareholding</th></tr></thead><tbody>{entity_rows}</tbody></table></div></div></div>
<div class="section"><div class="section-header"><div><div class="section-title"><span class="icon">🏦</span> Bank-by-Bank Summary</div><div class="section-subtitle">Raw Grade (Potential) vs Final Grade (Eligibility)</div></div></div><div class="summary-grid">{bank_cards}</div></div>
<div class="section"><div class="section-header"><div><div class="section-title"><span class="icon">📊</span> Detailed Evaluation by Bank</div><div class="section-subtitle">16 CCRIS + 4 CTOS Parameters per Bank</div></div></div><div class="bank-tabs">{bank_tabs}</div>{bank_contents}</div>
<div class="section"><div class="two-col"><div class="card"><h2><span class="icon">✅</span> Key Strengths</h2><div style="display: flex; flex-direction: column; gap: 8px;">{sh}</div></div><div class="card"><h2><span class="icon">⚠️</span> Items Requiring Attention</h2><div style="display: flex; flex-direction: column; gap: 8px;">{ah}</div></div></div></div>
<div class="consolidated-card grade-{fg_lower}-border"><h2><span class="icon">🏆</span> Final Assessment — Raw vs Final Grade</h2><div class="consolidated-grades"><div class="consolidated-grade-box"><div class="consolidated-grade-label">Raw Grade</div><div class="consolidated-grade-value grade-{rg_lower}">{raw_grade}</div><div class="consolidated-grade-desc">Company Potential<br>Score: {score}%</div></div><div class="consolidated-grade-box"><div class="consolidated-grade-label">Final Grade</div><div class="consolidated-grade-value grade-{fg_lower}">{final_grade}</div><div class="consolidated-grade-desc">Actual Eligibility<br>{reason}</div></div></div><p style="margin-top: 16px; color: var(--text-soft); font-size: 14px; max-width: 700px; margin-left: auto; margin-right: auto;">{c.get("explanation", "")}</p><div style="margin-top: 20px; display: flex; justify-content: center; gap: 24px; font-size: 12px; color: var(--text-muted);"><div>🔴 Strict 1: <span class="value-positive">{s1_pass}/{s1_total} ({s1_pct}%)</span></div><div>🟣 Strict 2: <span class="value-negative">{s2_pass}/{s2_total} ({s2_pct}%)</span></div><div>🟡 Preference: <span style="color: var(--pref-yellow);">{pref_pass}/{pref_total} ({pref_pct}%)</span></div></div></div>
<div class="footer"><div><strong>Kredit Lab Report v3.1</strong><br>16 CCRIS + 4 CTOS Parameters • 6-Bank Assessment</div><div style="text-align: right;">Prepared by: {meta.get("prepared_by", "Kredit Lab System")}<br>Date: {meta.get("analysis_date", datetime.now().strftime("%Y-%m-%d"))}</div></div>
</div>
<script>function showBank(bankId) {{ document.querySelectorAll('.bank-content').forEach(el => el.classList.remove('active')); document.querySelectorAll('.bank-tab').forEach(el => el.classList.remove('active')); document.getElementById('bank-' + bankId).classList.add('active'); event.target.classList.add('active'); }}</script>
</body></html>'''
