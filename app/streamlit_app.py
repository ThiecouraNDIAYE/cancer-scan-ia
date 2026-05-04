# ================================================================
# CancerScan IA — Plateforme Médicale IA
# Interface Responsive Mobile-First & Dynamique
# Université de Thiès — UFR SET — MaRT2 — 2025-2026
# ================================================================

import os, io, base64, time, requests, streamlit as st
from PIL import Image
from datetime import datetime

st.set_page_config(
    page_title="CancerScan IA",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_URL = os.getenv("API_URL", "https://cancer-scan-ia.onrender.com")

# ================================================================
# CSS — RESPONSIVE MOBILE-FIRST DESIGN
# ================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── RESET & BASE ─────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    background: #f0f2f5 !important;
    color: #1a1a2e !important;
}

/* ── SIDEBAR ──────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0f172a !important;
    border-right: none !important;
}
[data-testid="stSidebar"] > div { padding: 1.2rem 1rem !important; }

.sb-logo { display:flex; align-items:center; gap:10px; margin-bottom:1.5rem; padding-bottom:1.2rem; border-bottom:1px solid rgba(255,255,255,.08); }
.sb-icon { width:38px; height:38px; background:linear-gradient(135deg,#3b82f6,#8b5cf6); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:16px; }
.sb-name { font-weight:700; font-size:.92rem; color:#f8fafc; }
.sb-ver  { font-size:.6rem; color:#475569; font-family:'JetBrains Mono',monospace; }

.sb-pill { display:flex; align-items:center; gap:8px; padding:.55rem .85rem; border-radius:8px; font-size:.75rem; font-weight:600; margin-bottom:.4rem; }
.sb-on   { background:rgba(34,197,94,.1);  border:1px solid rgba(34,197,94,.2);  color:#4ade80; }
.sb-off  { background:rgba(239,68,68,.1);  border:1px solid rgba(239,68,68,.2);  color:#f87171; }
.sb-dot  { width:6px; height:6px; border-radius:50%; }
.sb-don  { background:#22c55e; animation:sbPulse 1.8s infinite; }
.sb-doff { background:#ef4444; }
@keyframes sbPulse { 0%,100%{opacity:1;transform:scale(1);} 50%{opacity:.5;transform:scale(1.5);} }

.sb-url { font-family:'JetBrains Mono',monospace; font-size:.58rem; color:#334155; padding:.25rem .5rem; background:rgba(255,255,255,.04); border-radius:5px; word-break:break-all; display:block; margin-bottom:1rem; }

.sb-sec { margin-bottom:1rem; }
.sb-sec-t { font-size:.58rem; font-weight:600; text-transform:uppercase; letter-spacing:.14em; color:#334155; margin-bottom:.5rem; display:block; }
.sb-r { display:flex; align-items:center; justify-content:space-between; padding:.3rem 0; font-size:.74rem; color:#64748b; border-bottom:1px solid rgba(255,255,255,.03); }
.sb-r:last-child { border-bottom:none; }
.sb-v { font-family:'JetBrains Mono',monospace; font-size:.68rem; font-weight:500; }
.c-g { color:#4ade80; } .c-b { color:#60a5fa; } .c-s { color:#475569; }

/* ── NAVBAR TOP ───────────────────────────────────────── */
.navbar {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    border-radius: 16px;
    padding: 1rem 1.5rem;
    margin-bottom: 1.2rem;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 4px 24px rgba(15,23,42,.15);
}
.nav-brand { display:flex; align-items:center; gap:12px; }
.nav-icon  { width:40px; height:40px; background:linear-gradient(135deg,#3b82f6,#8b5cf6); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:18px; box-shadow:0 4px 12px rgba(59,130,246,.3); }
.nav-name  { font-weight:800; font-size:1.1rem; color:#f8fafc; letter-spacing:-.02em; }
.nav-sub   { font-size:.62rem; color:#475569; margin-top:.1rem; }
.nav-badges { display:flex; align-items:center; gap:.6rem; flex-wrap:wrap; }
.nav-badge { padding:.25rem .7rem; border-radius:20px; font-size:.65rem; font-weight:600; }
.nb-blue   { background:rgba(59,130,246,.15); border:1px solid rgba(59,130,246,.25); color:#93c5fd; }
.nb-green  { background:rgba(34,197,94,.15);  border:1px solid rgba(34,197,94,.25);  color:#86efac; }
.nb-purple { background:rgba(139,92,246,.15); border:1px solid rgba(139,92,246,.25); color:#c4b5fd; }

/* ── KPI ROW ──────────────────────────────────────────── */
.kpi-row { display:grid; grid-template-columns:repeat(4,1fr); gap:.8rem; margin-bottom:1.2rem; }
.kpi-card {
    background:#fff; border-radius:14px; padding:1.1rem 1rem;
    border:1px solid #e2e8f0;
    box-shadow:0 1px 6px rgba(15,23,42,.05);
    text-align:center; transition:transform .2s, box-shadow .2s;
    position:relative; overflow:hidden;
}
.kpi-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
}
.kpi-card.blue::before   { background:linear-gradient(90deg,#3b82f6,#6366f1); }
.kpi-card.green::before  { background:linear-gradient(90deg,#22c55e,#10b981); }
.kpi-card.purple::before { background:linear-gradient(90deg,#8b5cf6,#a855f7); }
.kpi-card.orange::before { background:linear-gradient(90deg,#f97316,#ef4444); }
.kpi-card:hover { transform:translateY(-2px); box-shadow:0 6px 20px rgba(15,23,42,.1); }
.kpi-val { font-size:1.55rem; font-weight:800; letter-spacing:-.03em; }
.kpi-lbl { font-size:.62rem; color:#94a3b8; text-transform:uppercase; letter-spacing:.1em; margin-top:.2rem; }
.kpi-card.blue   .kpi-val { color:#2563eb; }
.kpi-card.green  .kpi-val { color:#16a34a; }
.kpi-card.purple .kpi-val { color:#7c3aed; }
.kpi-card.orange .kpi-val { color:#ea580c; }

/* ── TABS ─────────────────────────────────────────────── */
.tab-nav { display:flex; gap:.5rem; background:#fff; padding:.4rem; border-radius:12px; border:1px solid #e2e8f0; margin-bottom:1.2rem; box-shadow:0 1px 4px rgba(15,23,42,.04); }
.tab-btn { flex:1; padding:.55rem .8rem; border-radius:9px; text-align:center; font-size:.78rem; font-weight:600; cursor:pointer; border:none; transition:all .2s; }
.tab-active   { background:linear-gradient(135deg,#2563eb,#7c3aed); color:#fff; box-shadow:0 2px 8px rgba(37,99,235,.25); }
.tab-inactive { background:transparent; color:#64748b; }
.tab-inactive:hover { background:#f8fafc; color:#374151; }

/* ── UPLOAD CARD ──────────────────────────────────────── */
.up-card { background:#fff; border-radius:16px; border:1px solid #e2e8f0; box-shadow:0 2px 8px rgba(15,23,42,.04); overflow:hidden; }
.up-header { background:linear-gradient(135deg,#eff6ff,#f5f3ff); padding:1rem 1.3rem; border-bottom:1px solid #e2e8f0; display:flex; align-items:center; gap:.7rem; }
.up-header-icon { width:32px; height:32px; background:linear-gradient(135deg,#3b82f6,#6366f1); border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:14px; }
.up-header-txt { font-weight:700; font-size:.88rem; color:#1e293b; }
.up-header-sub { font-size:.68rem; color:#64748b; margin-top:.1rem; }
.up-body { padding:1.2rem; }

.up-hint { background:#f8faff; border:2px dashed #bfdbfe; border-radius:12px; padding:1.5rem; text-align:center; margin-bottom:1rem; cursor:pointer; transition:all .2s; }
.up-hint:hover { background:#eff6ff; border-color:#3b82f6; }
.up-hint-ico  { font-size:2rem; margin-bottom:.5rem; }
.up-hint-txt  { font-size:.8rem; font-weight:600; color:#3b82f6; }
.up-hint-sub  { font-size:.68rem; color:#93c5fd; margin-top:.2rem; }

/* ── IMAGE META ───────────────────────────────────────── */
.img-meta { display:grid; grid-template-columns:repeat(3,1fr); gap:.5rem; margin:.7rem 0; }
.im-c { background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:.6rem; text-align:center; }
.im-v { font-family:'JetBrains Mono',monospace; font-size:.82rem; font-weight:600; color:#2563eb; }
.im-l { font-size:.58rem; color:#94a3b8; text-transform:uppercase; letter-spacing:.08em; margin-top:.15rem; }

/* ── BTN ANALYSE ──────────────────────────────────────── */
.stButton > button {
    width:100% !important; padding:.85rem 1.5rem !important;
    font-family:'Inter',sans-serif !important; font-size:.88rem !important; font-weight:700 !important;
    color:#fff !important; background:linear-gradient(135deg,#2563eb,#7c3aed) !important;
    border:none !important; border-radius:10px !important;
    box-shadow:0 4px 16px rgba(37,99,235,.3) !important;
    transition:all .25s !important; letter-spacing:.01em !important;
}
.stButton > button:hover { transform:translateY(-2px) !important; box-shadow:0 8px 28px rgba(37,99,235,.4) !important; }
.stButton > button:active { transform:translateY(0) !important; }

/* ── RESULT CARDS ─────────────────────────────────────── */
.res-wrap { animation:fadeSlide .5s cubic-bezier(.4,0,.2,1); }
@keyframes fadeSlide { from{opacity:0;transform:translateY(16px);} to{opacity:1;transform:translateY(0);} }

.res-cancer {
    background:linear-gradient(135deg,#fff5f5,#fff1f2);
    border:2px solid #fca5a5; border-radius:18px; padding:1.8rem;
    text-align:center; box-shadow:0 8px 32px rgba(239,68,68,.1);
}
.res-neg {
    background:linear-gradient(135deg,#f0fdf4,#ecfdf5);
    border:2px solid #86efac; border-radius:18px; padding:1.8rem;
    text-align:center; box-shadow:0 8px 32px rgba(34,197,94,.1);
}
.res-ico { font-size:3.2rem; display:block; margin-bottom:.5rem; animation:bounce .6s cubic-bezier(.36,.07,.19,.97); }
@keyframes bounce { 0%{transform:scale(0) rotate(-15deg);} 65%{transform:scale(1.15) rotate(3deg);} 100%{transform:scale(1) rotate(0);} }
.res-lbl-c { font-size:1.65rem; font-weight:800; color:#dc2626; letter-spacing:-.025em; margin-bottom:.3rem; }
.res-lbl-n { font-size:1.65rem; font-weight:800; color:#16a34a; letter-spacing:-.025em; margin-bottom:.3rem; }
.res-sub   { font-size:.75rem; color:#64748b; margin-bottom:1rem; font-style:italic; }

.bar-bg { height:8px; background:#e2e8f0; border-radius:8px; overflow:hidden; margin:.5rem 0 .3rem; }
.bar-c { height:100%; background:linear-gradient(90deg,#ef4444,#f97316); border-radius:8px; }
.bar-n { height:100%; background:linear-gradient(90deg,#22c55e,#10b981); border-radius:8px; }
.bar-pct { font-size:.75rem; color:#475569; font-weight:600; margin-bottom:.8rem; }

.res-mets { display:grid; grid-template-columns:repeat(3,1fr); gap:.5rem; }
.rm { background:rgba(255,255,255,.8); border:1px solid rgba(255,255,255,.9); border-radius:8px; padding:.65rem; text-align:center; }
.rm-v { font-family:'JetBrains Mono',monospace; font-size:.85rem; font-weight:700; }
.rm-l { font-size:.58rem; color:#94a3b8; text-transform:uppercase; letter-spacing:.08em; margin-top:.2rem; }

/* ── INFO BOX ─────────────────────────────────────────── */
.info-box { background:#eff6ff; border:1px solid #bfdbfe; border-left:3px solid #3b82f6; border-radius:0 8px 8px 0; padding:.7rem 1rem; font-size:.75rem; color:#1d4ed8; line-height:1.6; margin-bottom:.9rem; }

/* ── EXPORT PANEL ─────────────────────────────────────── */
.exp-panel { background:#fff; border:1px solid #e2e8f0; border-radius:14px; padding:1.2rem; margin-top:1rem; box-shadow:0 1px 4px rgba(15,23,42,.04); }
.exp-title { font-size:.62rem; font-weight:600; text-transform:uppercase; letter-spacing:.12em; color:#94a3b8; margin-bottom:.8rem; display:block; }

.stDownloadButton > button {
    width:100% !important; font-family:'Inter',sans-serif !important;
    font-size:.78rem !important; font-weight:600 !important;
    padding:.6rem .8rem !important; border-radius:8px !important;
    transition:all .2s !important;
}

/* ── SCORE RAW ────────────────────────────────────────── */
.score-row { display:flex; align-items:center; justify-content:space-between; background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:.5rem .85rem; margin-top:.6rem; }
.score-l { font-size:.72rem; color:#64748b; font-weight:500; }
.score-v { font-family:'JetBrains Mono',monospace; font-size:.78rem; color:#2563eb; font-weight:600; }

/* ── GRAD-CAM ─────────────────────────────────────────── */
.gcam-hd { display:flex; align-items:center; gap:.6rem; margin:1.2rem 0 .6rem; }
.gcam-badge { background:#f5f3ff; border:1px solid #c4b5fd; color:#6d28d9; font-size:.6rem; font-weight:700; text-transform:uppercase; letter-spacing:.12em; padding:.2rem .6rem; border-radius:20px; }
.gcam-t { font-size:.85rem; font-weight:700; color:#1e293b; }
.gcam-leg { background:#fafafa; border:1px solid #e2e8f0; border-left:3px solid #7c3aed; border-radius:0 8px 8px 0; padding:.6rem .9rem; font-size:.72rem; color:#475569; line-height:1.7; margin-bottom:.7rem; }

/* ── MED ALERT ────────────────────────────────────────── */
.med { background:#fffbeb; border:1px solid #fde68a; border-radius:10px; padding:.8rem 1rem; font-size:.72rem; color:#78350f; line-height:1.8; margin-top:1.2rem; }

/* ── EMPTY STATE ──────────────────────────────────────── */
.empty { background:#fff; border:2px dashed #e2e8f0; border-radius:14px; min-height:280px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:.7rem; padding:2.5rem 1.5rem; text-align:center; }
.e-ico { font-size:2.5rem; opacity:.2; animation:float 3s ease-in-out infinite; }
@keyframes float { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-8px);} }
.e-txt { font-size:.8rem; color:#cbd5e1; font-weight:500; }

/* ── STEPS ────────────────────────────────────────────── */
.steps { display:grid; grid-template-columns:repeat(4,1fr); gap:.7rem; }
.step { background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:1.1rem; transition:transform .2s,box-shadow .2s; }
.step:hover { transform:translateY(-3px); box-shadow:0 8px 24px rgba(15,23,42,.08); }
.step-n { width:26px; height:26px; border-radius:7px; background:linear-gradient(135deg,#2563eb,#7c3aed); color:#fff; font-size:.7rem; font-weight:800; display:flex; align-items:center; justify-content:center; margin-bottom:.7rem; }
.step-t { font-size:.82rem; font-weight:700; color:#1e293b; margin-bottom:.25rem; }
.step-d { font-size:.7rem; color:#64748b; line-height:1.5; }

/* ── CARD ─────────────────────────────────────────────── */
.card { background:#fff; border-radius:14px; border:1px solid #e2e8f0; box-shadow:0 1px 6px rgba(15,23,42,.04); padding:1.2rem; margin-bottom:1rem; }
.card-hd { font-size:.62rem; font-weight:600; text-transform:uppercase; letter-spacing:.12em; color:#94a3b8; margin-bottom:1rem; }

/* ── STATUS STRIP ─────────────────────────────────────── */
.status-strip { display:flex; align-items:center; gap:.8rem; padding:.6rem 1rem; border-radius:10px; margin-bottom:1rem; font-size:.78rem; font-weight:600; }
.ss-on  { background:#f0fdf4; border:1px solid #bbf7d0; color:#15803d; }
.ss-off { background:#fef2f2; border:1px solid #fecaca; color:#dc2626; }
.ss-dot { width:7px; height:7px; border-radius:50%; flex-shrink:0; }
.ss-don  { background:#22c55e; box-shadow:0 0 0 3px rgba(34,197,94,.2); animation:sPulse 2s infinite; }
.ss-doff { background:#ef4444; }
@keyframes sPulse { 0%,100%{box-shadow:0 0 0 3px rgba(34,197,94,.2);} 50%{box-shadow:0 0 0 6px rgba(34,197,94,.05);} }

/* ── FOOTER ───────────────────────────────────────────── */
.footer { text-align:center; padding:1.5rem 0; font-size:.68rem; color:#cbd5e1; border-top:1px solid #e2e8f0; margin-top:1.5rem; }

/* ══ RESPONSIVE MOBILE ════════════════════════════════════ */
@media (max-width: 768px) {
    .kpi-row { grid-template-columns:repeat(2,1fr) !important; gap:.6rem !important; }
    .steps   { grid-template-columns:1fr 1fr !important; }
    .res-mets { grid-template-columns:repeat(3,1fr) !important; }
    .navbar  { flex-direction:column; gap:.8rem; text-align:center; }
    .nav-badges { justify-content:center; }
    .nav-brand { flex-direction:column; }
}
@media (max-width: 480px) {
    .kpi-row { grid-template-columns:1fr 1fr !important; }
    .steps   { grid-template-columns:1fr !important; }
    .res-mets { grid-template-columns:1fr 1fr 1fr !important; }
    .img-meta { grid-template-columns:repeat(3,1fr) !important; }
    .kpi-val { font-size:1.2rem !important; }
    .hero-kpis { flex-wrap:wrap; gap:1rem; }
}

/* ── Streamlit overrides ──────────────────────────────── */
.stCheckbox > label { font-size:.82rem !important; color:#374151 !important; font-weight:500 !important; }
div[data-testid="stImage"] img { border-radius:10px; box-shadow:0 2px 10px rgba(15,23,42,.08); }
section[data-testid="stFileUploadDropzone"] { background:#f8faff !important; border:2px dashed #bfdbfe !important; border-radius:12px !important; }
section[data-testid="stFileUploadDropzone"]:hover { background:#eff6ff !important; border-color:#3b82f6 !important; }
.element-container { margin-bottom: .3rem !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════
@st.cache_data(ttl=20)
def api_health():
    try:
        r = requests.get(f"{API_URL}/health", timeout=6)
        if r.status_code == 200:
            return True, r.json()
    except Exception:
        pass
    return False, {}

def call_api(img_bytes, gradcam):
    ep = "/predict/gradcam" if gradcam else "/predict"
    try:
        r = requests.post(
            f"{API_URL}{ep}",
            files={"file": ("image.jpg", img_bytes, "image/jpeg")},
            timeout=90,
        )
        r.raise_for_status()
        return True, r.json()
    except requests.exceptions.ConnectionError:
        return False, {"error": "Impossible de joindre l'API. Vérifiez le service Render."}
    except requests.exceptions.Timeout:
        return False, {"error": "Timeout — l'API met trop de temps (90s)."}
    except Exception as e:
        return False, {"error": str(e)}

def b64_to_pil(b64):
    return Image.open(io.BytesIO(base64.b64decode(b64)))

def img_to_bytes(img, fmt="PNG"):
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()

def generate_report(label, conf, raw, probs, elapsed, filename, gcam_b64=None):
    now   = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
    color = "#dc2626" if label.lower() == "cancer" else "#16a34a"
    bg    = "#fff5f5" if label.lower() == "cancer" else "#f0fdf4"
    icon  = "⚠️" if label.lower() == "cancer" else "✅"
    verdict = "IDC Positif — Carcinome canalaire invasif détecté" if label.lower() == "cancer" else "IDC Négatif — Aucun signe de carcinome détecté"
    gcam_html = f'<img src="data:image/png;base64,{gcam_b64}" style="width:220px;border-radius:8px;border:1px solid #e2e8f0;margin-top:8px;" />' if gcam_b64 else ""

    return f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Rapport CancerScan IA</title>
<style>
  body {{ font-family:'Segoe UI',Arial,sans-serif; max-width:750px; margin:0 auto; padding:32px 20px; color:#1e293b; background:#f8fafc; }}
  .header {{ background:linear-gradient(135deg,#1d4ed8,#4338ca); color:#fff; border-radius:16px; padding:28px 32px; margin-bottom:24px; }}
  .header h1 {{ margin:0 0 4px; font-size:22px; }}
  .header p  {{ margin:0; opacity:.7; font-size:12px; }}
  .verdict {{ background:{bg}; border:2px solid {color}; border-radius:14px; padding:24px; text-align:center; margin-bottom:20px; }}
  .verdict-ico   {{ font-size:40px; }}
  .verdict-title {{ font-size:24px; font-weight:800; color:{color}; margin:8px 0 4px; }}
  .verdict-conf  {{ font-size:14px; color:{color}; font-weight:600; }}
  .section {{ background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:20px; margin-bottom:16px; }}
  .section h2 {{ font-size:13px; font-weight:700; text-transform:uppercase; letter-spacing:.1em; color:#94a3b8; margin:0 0 14px; }}
  .kpi-grid {{ display:grid; grid-template-columns:repeat(2,1fr); gap:10px; }}
  .kpi {{ background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:12px; text-align:center; }}
  .kpi-v {{ font-size:20px; font-weight:800; font-family:monospace; }}
  .kpi-l {{ font-size:10px; color:#94a3b8; text-transform:uppercase; letter-spacing:.1em; margin-top:3px; }}
  .spec-row {{ display:flex; justify-content:space-between; padding:7px 0; border-bottom:1px solid #f1f5f9; font-size:12px; }}
  .spec-row:last-child {{ border-bottom:none; }}
  .spec-v {{ font-family:monospace; font-weight:600; color:#2563eb; }}
  .alert {{ background:#fffbeb; border:1px solid #fde68a; border-radius:10px; padding:14px 18px; font-size:11px; color:#78350f; line-height:1.8; margin-top:16px; }}
  .footer {{ text-align:center; font-size:10px; color:#94a3b8; margin-top:24px; padding-top:16px; border-top:1px solid #e2e8f0; }}
  @media print {{ body{{ background:#fff; }} }}
</style></head><body>
<div class="header">
  <h1>🔬 CancerScan IA — Rapport d'Analyse</h1>
  <p>Généré le {now} · Fichier : <strong>{filename}</strong></p>
</div>

<div class="verdict">
  <div class="verdict-ico">{icon}</div>
  <div class="verdict-title">{verdict}</div>
  <div class="verdict-conf">Confiance : {conf:.1f}%</div>
</div>

<div class="section">
  <h2>Métriques de prédiction</h2>
  <div class="kpi-grid">
    <div class="kpi"><div class="kpi-v" style="color:#dc2626;">{probs.get('Cancer',0):.2f}%</div><div class="kpi-l">Probabilité Cancer</div></div>
    <div class="kpi"><div class="kpi-v" style="color:#16a34a;">{probs.get('Negative',0):.2f}%</div><div class="kpi-l">Probabilité Négatif</div></div>
    <div class="kpi"><div class="kpi-v" style="color:#2563eb;">{raw:.6f}</div><div class="kpi-l">Score brut (sigmoid)</div></div>
    <div class="kpi"><div class="kpi-v" style="color:#64748b;">{elapsed}s</div><div class="kpi-l">Temps d'inférence</div></div>
  </div>
</div>

<div class="section">
  <h2>Spécifications du modèle</h2>
  <div class="spec-row">Architecture <span class="spec-v">EfficientNetB0 (Transfer Learning)</span></div>
  <div class="spec-row">Framework <span class="spec-v">TensorFlow 2.15 · Keras 2.15</span></div>
  <div class="spec-row">Accuracy globale <span class="spec-v" style="color:#16a34a;">95.16%</span></div>
  <div class="spec-row">F1-Score <span class="spec-v" style="color:#16a34a;">0.95</span></div>
  <div class="spec-row">Précision Cancer <span class="spec-v" style="color:#16a34a;">97%</span></div>
  <div class="spec-row">Rappel Cancer <span class="spec-v" style="color:#16a34a;">94%</span></div>
  <div class="spec-row">Seuil de décision <span class="spec-v">0.5</span></div>
  <div class="spec-row">Taille d'entrée <span class="spec-v">224 × 224 px</span></div>
  <div class="spec-row">Dataset d'entraînement <span class="spec-v">828 images</span></div>
  <div class="spec-row">Epochs entraînés <span class="spec-v">27 / 50</span></div>
</div>

{'<div class="section"><h2>Visualisation Grad-CAM</h2>' + gcam_html + '<p style="font-size:11px;color:#64748b;margin-top:8px;">Les zones chaudes (rouge/orange) indiquent les régions histologiques déterminantes pour la décision du modèle.</p></div>' if gcam_html else ''}

<div class="alert">
  ⚕️ <strong>Avertissement clinique</strong> — Ce rapport est généré par un système de recherche
  pédagogique (Deep Learning, Université de Thiès, MaRT2, 2025-2026). Il ne constitue pas un dispositif
  médical certifié (CE/FDA) et ne remplace en aucun cas le diagnostic d'un médecin anatomopathologiste
  qualifié. Toute décision clinique doit être prise par un professionnel de santé compétent.
</div>

<div class="footer">
  Université de Thiès · UFR SET · Département Informatique · MaRT2 · Deep Learning 2025-2026<br/>
  Pr. Cheikh SARR · Ibrahima MBAYE &amp; Thiecoura NDIAYE<br/>
  <em>Pour imprimer en PDF : Fichier → Imprimer → Enregistrer en PDF</em>
</div>
</body></html>""".encode("utf-8")


# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="sb-icon">🔬</div>
        <div>
            <div class="sb-name">CancerScan IA</div>
            <div class="sb-ver">v1.0.0 · MaRT2 · 2025-2026</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    api_ok, api_info = api_health()
    if api_ok:
        st.markdown(f'<div class="sb-pill sb-on"><div class="sb-dot sb-don"></div>API Connectée <span style="margin-left:auto;font-size:.6rem;background:rgba(34,197,94,.15);color:#4ade80;padding:.1rem .4rem;border-radius:20px;">LIVE</span></div><span class="sb-url">{API_URL}</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="sb-pill sb-off"><div class="sb-dot sb-doff"></div>API Hors ligne</div><span class="sb-url">{API_URL}</span>', unsafe_allow_html=True)

    st.markdown('<div class="sb-sec"><span class="sb-sec-t">⚙ Options</span></div>', unsafe_allow_html=True)
    use_gradcam = st.checkbox("🗺 Activer Grad-CAM", value=True)

    if api_ok:
        th  = api_info.get("threshold", 0.5)
        tfv = api_info.get("tf_version", "2.15.0")
        st.markdown(f"""
        <div class="sb-sec" style="margin-top:.6rem;">
            <span class="sb-sec-t">🧠 Modèle</span>
            <div class="sb-r">Architecture <span class="sb-v c-b">EfficientNetB0</span></div>
            <div class="sb-r">Seuil <span class="sb-v c-b">{th}</span></div>
            <div class="sb-r">TensorFlow <span class="sb-v c-s">{tfv}</span></div>
            <div class="sb-r">Entrée <span class="sb-v c-b">224×224</span></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-sec" style="margin-top:.4rem;">
        <span class="sb-sec-t">📊 Performances</span>
        <div class="sb-r">Accuracy  <span class="sb-v c-g">95.16%</span></div>
        <div class="sb-r">F1-Score  <span class="sb-v c-g">0.95</span></div>
        <div class="sb-r">Précision <span class="sb-v c-g">97%</span></div>
        <div class="sb-r">Rappel    <span class="sb-v c-g">94%</span></div>
        <div class="sb-r">Dataset   <span class="sb-v c-s">828 imgs</span></div>
    </div>
    <div class="sb-sec" style="margin-top:.4rem;">
        <span class="sb-sec-t">🎓 Projet</span>
        <div class="sb-r">Univ. de Thiès</div>
        <div class="sb-r">UFR SET · MaRT2</div>
        <div class="sb-r">Pr. Cheikh SARR</div>
        <div class="sb-r">DL 2025-2026</div>
    </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# NAVBAR
# ═══════════════════════════════════════════════════════════════
api_ok, api_info = api_health()

st.markdown(f"""
<div class="navbar">
    <div class="nav-brand">
        <div class="nav-icon">🔬</div>
        <div>
            <div class="nav-name">CancerScan IA</div>
            <div class="nav-sub">Plateforme de détection du cancer du sein · Université de Thiès · MaRT2</div>
        </div>
    </div>
    <div class="nav-badges">
        <span class="nav-badge nb-blue">EfficientNetB0</span>
        <span class="nav-badge nb-green">Accuracy 95.16%</span>
        <span class="nav-badge nb-purple">Grad-CAM</span>
        {"<span class='nav-badge nb-green'>● API Live</span>" if api_ok else "<span class='nav-badge' style='background:rgba(239,68,68,.15);border:1px solid rgba(239,68,68,.25);color:#f87171;'>● API Off</span>"}
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# KPI ROW
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="kpi-row">
    <div class="kpi-card blue">
        <div class="kpi-val">95.16%</div>
        <div class="kpi-lbl">Accuracy</div>
    </div>
    <div class="kpi-card green">
        <div class="kpi-val">0.95</div>
        <div class="kpi-lbl">F1-Score</div>
    </div>
    <div class="kpi-card purple">
        <div class="kpi-val">4.38M</div>
        <div class="kpi-lbl">Paramètres</div>
    </div>
    <div class="kpi-card orange">
        <div class="kpi-val">828</div>
        <div class="kpi-lbl">Images train</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Statut API visible
if api_ok:
    st.markdown(f'<div class="status-strip ss-on"><div class="ss-dot ss-don"></div>API connectée et opérationnelle — <span style="font-family:\'JetBrains Mono\',monospace;font-size:.7rem;">{API_URL}</span><span style="margin-left:auto;font-size:.65rem;background:#bbf7d0;color:#15803d;padding:.15rem .5rem;border-radius:20px;">LIVE</span></div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="status-strip ss-off"><div class="ss-dot ss-doff"></div>API hors ligne — Vérifiez le service Render</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# COLONNES PRINCIPALES
# ═══════════════════════════════════════════════════════════════
col_l, col_r = st.columns([1, 1], gap="large")

# ── UPLOAD ────────────────────────────────────────────────────
with col_l:
    st.markdown("""
    <div class="up-card">
        <div class="up-header">
            <div class="up-header-icon">📤</div>
            <div>
                <div class="up-header-txt">Image histologique</div>
                <div class="up-header-sub">Coupe H&E du tissu mammaire · JPG, PNG</div>
            </div>
        </div>
        <div class="up-body">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        Téléversez une image histologique colorée (H&amp;E) du tissu mammaire.
        Le modèle analyse les caractéristiques cellulaires pour détecter
        la présence ou l'absence de <strong>carcinome canalaire invasif (IDC)</strong>.
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("image", type=["jpg","jpeg","png"], label_visibility="collapsed")
    st.markdown("</div></div>", unsafe_allow_html=True)

    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        st.markdown('<div class="card" style="margin-top:.8rem;">', unsafe_allow_html=True)
        st.image(image, use_column_width=True, caption="")
        w, h  = image.size
        size_kb = len(uploaded.getvalue()) // 1024
        st.markdown(f"""
        <div class="img-meta">
            <div class="im-c"><div class="im-v">{w}px</div><div class="im-l">Largeur</div></div>
            <div class="im-c"><div class="im-v">{h}px</div><div class="im-l">Hauteur</div></div>
            <div class="im-c"><div class="im-v">{size_kb}Ko</div><div class="im-l">Taille</div></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if not api_ok:
            st.error("⚠️ API hors ligne — Vérifiez le service Render.")
        else:
            if st.button("🔬 Analyser l'image avec l'IA"):
                with st.spinner("Analyse en cours — EfficientNetB0 + Grad-CAM..."):
                    t0 = time.time()
                    ok, resp = call_api(uploaded.getvalue(), use_gradcam)
                    elapsed  = round(time.time() - t0, 2)
                if ok:
                    resp["_elapsed"]  = elapsed
                    resp["_filename"] = uploaded.name
                    st.session_state["result"]    = resp
                    st.session_state["orig_img"]  = image
                    st.session_state["img_bytes"] = uploaded.getvalue()
                    st.rerun()
                else:
                    st.error(f"❌ {resp.get('error','Erreur inconnue')}")
    else:
        st.markdown("""
        <div class="empty" style="margin-top:.8rem;">
            <div class="e-ico">🩺</div>
            <div class="e-txt">Glissez une image ici<br>ou cliquez pour parcourir</div>
            <div style="font-size:.65rem;color:#e2e8f0;">JPG · PNG · max 200 MB</div>
        </div>
        """, unsafe_allow_html=True)


# ── RÉSULTATS ─────────────────────────────────────────────────
with col_r:
    if "result" not in st.session_state:
        st.markdown("""
        <div class="empty" style="min-height:380px;">
            <div class="e-ico">📊</div>
            <div class="e-txt">Les résultats apparaîtront ici<br>après l'analyse</div>
            <div style="font-size:.65rem;color:#e2e8f0;">Téléversez une image → Analyser</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        res      = st.session_state["result"]
        pred     = res.get("prediction", {})
        label    = pred.get("label","—")
        conf     = pred.get("confidence_pct", 0)
        raw      = pred.get("raw_score", 0)
        probs    = pred.get("probabilities", {})
        elapsed  = res.get("_elapsed","—")
        filename = res.get("_filename","image.jpg")
        gcam_b64 = res.get("gradcam_image")
        is_cancer = label.lower() == "cancer"

        st.markdown('<div class="res-wrap">', unsafe_allow_html=True)

        if is_cancer:
            st.markdown(f"""
            <div class="res-cancer">
                <span class="res-ico">⚠️</span>
                <div class="res-lbl-c">IDC Positif</div>
                <div class="res-sub">Carcinome canalaire invasif détecté</div>
                <div class="bar-bg"><div class="bar-c" style="width:{conf}%"></div></div>
                <div class="bar-pct">{conf:.1f}% de confiance</div>
                <div class="res-mets">
                    <div class="rm"><div class="rm-v" style="color:#dc2626;">{probs.get('Cancer',0):.1f}%</div><div class="rm-l">P(Cancer)</div></div>
                    <div class="rm"><div class="rm-v" style="color:#16a34a;">{probs.get('Negative',0):.1f}%</div><div class="rm-l">P(Négatif)</div></div>
                    <div class="rm"><div class="rm-v" style="color:#64748b;">{elapsed}s</div><div class="rm-l">Inférence</div></div>
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="res-neg">
                <span class="res-ico">✅</span>
                <div class="res-lbl-n">IDC Négatif</div>
                <div class="res-sub">Aucun signe de carcinome canalaire détecté</div>
                <div class="bar-bg"><div class="bar-n" style="width:{conf}%"></div></div>
                <div class="bar-pct">{conf:.1f}% de confiance</div>
                <div class="res-mets">
                    <div class="rm"><div class="rm-v" style="color:#dc2626;">{probs.get('Cancer',0):.1f}%</div><div class="rm-l">P(Cancer)</div></div>
                    <div class="rm"><div class="rm-v" style="color:#16a34a;">{probs.get('Negative',0):.1f}%</div><div class="rm-l">P(Négatif)</div></div>
                    <div class="rm"><div class="rm-v" style="color:#64748b;">{elapsed}s</div><div class="rm-l">Inférence</div></div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="score-row">
            <span class="score-l">Score brut (sigmoid)</span>
            <span class="score-v">{raw:.6f}</span>
        </div>
        </div>
        """, unsafe_allow_html=True)

        # ── EXPORT PANEL ──────────────────────────────────────
        st.markdown('<div class="exp-panel"><span class="exp-title">💾 Sauvegarder &amp; Exporter</span>', unsafe_allow_html=True)
        e1, e2 = st.columns(2)
        img_obj = st.session_state.get("orig_img")
        if img_obj:
            folder = "Cancer" if is_cancer else "Negative"
            ts     = datetime.now().strftime("%Y%m%d_%H%M%S")
            with e1:
                st.download_button(
                    f"📁 Sauvegarder ({folder})",
                    data=img_to_bytes(img_obj),
                    file_name=f"{folder}_{ts}.png",
                    mime="image/png",
                    use_container_width=True,
                )
        with e2:
            pdf = generate_report(label, conf, raw, probs, elapsed, filename, gcam_b64)
            st.download_button(
                "📄 Rapport PDF",
                data=pdf,
                file_name=f"rapport_cancerscan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                mime="text/html",
                use_container_width=True,
            )

        st.markdown("""
        <p style="font-size:.65rem;color:#94a3b8;margin-top:.4rem;">
            💡 Image sauvegardée avec label · Rapport : ouvrir dans navigateur → Fichier → Imprimer → PDF
        </p></div>
        """, unsafe_allow_html=True)

        # ── GRAD-CAM ──────────────────────────────────────────
        if use_gradcam and gcam_b64:
            st.markdown("""
            <div class="gcam-hd">
                <span class="gcam-badge">Grad-CAM</span>
                <span class="gcam-t">Zones d'activation du modèle</span>
            </div>
            <div class="gcam-leg">
                🔴 <strong>Rouge/Orange</strong> — zones fortement activées, déterminantes pour la décision<br>
                🔵 <strong>Bleu/Vert</strong> — zones peu activées, faible contribution
            </div>
            """, unsafe_allow_html=True)
            g1, g2 = st.columns(2)
            gcam_img = b64_to_pil(gcam_b64)
            with g1:
                st.image(st.session_state["orig_img"].resize((224,224)), caption="Image originale", use_column_width=True)
            with g2:
                st.image(gcam_img, caption="Heatmap Grad-CAM", use_column_width=True)
                st.download_button("⬇ Télécharger Grad-CAM", data=img_to_bytes(gcam_img),
                    file_name=f"gradcam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png", use_container_width=True)

        st.markdown("""
        <div class="med">
            ⚕️ <strong>Avertissement clinique</strong> — Outil de recherche pédagogique (Univ. Thiès, 2025-2026).
            Ne constitue pas un dispositif médical certifié. Tout résultat doit être validé
            par un médecin anatomopathologiste qualifié.
        </div>
        """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# GUIDE
# ═══════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="card">
    <div class="card-hd">📖 Mode d'emploi</div>
    <div class="steps">
        <div class="step"><div class="step-n">1</div><div class="step-t">Téléverser</div><div class="step-d">Chargez une image histologique JPG/PNG du tissu mammaire.</div></div>
        <div class="step"><div class="step-n">2</div><div class="step-t">Vérifier</div><div class="step-d">Confirmez que l'API est ✅ connectée (barre de statut verte).</div></div>
        <div class="step"><div class="step-n">3</div><div class="step-t">Analyser</div><div class="step-d">Lancez l'analyse — l'IA prédit la classe en quelques secondes.</div></div>
        <div class="step"><div class="step-n">4</div><div class="step-t">Exporter</div><div class="step-d">Sauvegardez l'image et exportez le rapport complet en PDF.</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
    Université de Thiès · UFR SET · Département Informatique · M1 · Deep Learning 2025-2026<br>
    Pr. Cheikh SARR · Ibrahima MBAYE &amp; Thiecoura NDIAYE
</div>
""", unsafe_allow_html=True)