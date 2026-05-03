# =============================================================
# CancerScan IA — Interface Ultra-Moderne
# Classification du Cancer du Sein
# Université de Thiès — MaRT2 — 2025-2026
# =============================================================

import os, io, base64, time, requests, streamlit as st
from PIL import Image

# ─── Config page ───────────────────────────────────────────────
st.set_page_config(
    page_title="CancerScan IA",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = os.getenv("API_URL", "https://cancer-scan-ia.onrender.com")

# ─── CSS Ultra-Moderne ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Outfit:wght@300;400;500;600&display=swap');

/* ══ Reset & Base ══════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'Outfit', sans-serif;
    background: #020308 !important;
    color: #e2e8f0;
}

/* ══ Arrière-plan animé ════════════════════════════════════ */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 10% 20%, rgba(6,182,212,.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 80%, rgba(139,92,246,.05) 0%, transparent 60%),
        radial-gradient(ellipse 40% 30% at 50% 50%, rgba(16,185,129,.03) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
    animation: bgPulse 8s ease-in-out infinite alternate;
}
@keyframes bgPulse {
    0%   { opacity: .6; }
    100% { opacity: 1; }
}

/* ══ Grid de points ════════════════════════════════════════ */
.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image: radial-gradient(rgba(6,182,212,.12) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
    mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 30%, transparent 80%);
}

/* ══ Sidebar ═══════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: rgba(2,3,8,.95) !important;
    border-right: 1px solid rgba(6,182,212,.15) !important;
    backdrop-filter: blur(20px);
}
[data-testid="stSidebar"] > div { padding: 1.5rem 1rem; }

/* ══ Sidebar titre ═════════════════════════════════════════ */
.sb-logo {
    display: flex;
    align-items: center;
    gap: .7rem;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid rgba(6,182,212,.12);
}
.sb-logo-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #06b6d4, #8b5cf6);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    box-shadow: 0 0 20px rgba(6,182,212,.3);
}
.sb-logo-text {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: #f1f5f9;
    letter-spacing: -.01em;
}
.sb-logo-sub {
    font-size: .65rem;
    color: #475569;
    font-family: 'Space Mono', monospace;
}

/* ══ Status badge ══════════════════════════════════════════ */
.status-badge {
    display: flex;
    align-items: center;
    gap: .6rem;
    padding: .7rem 1rem;
    border-radius: 10px;
    margin-bottom: .8rem;
    font-size: .82rem;
    font-weight: 500;
    transition: all .3s ease;
}
.status-online {
    background: rgba(16,185,129,.08);
    border: 1px solid rgba(16,185,129,.2);
    color: #34d399;
}
.status-offline {
    background: rgba(239,68,68,.08);
    border: 1px solid rgba(239,68,68,.2);
    color: #f87171;
}
.status-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    animation: pulse 2s ease infinite;
}
.dot-online  { background: #10b981; box-shadow: 0 0 8px #10b981; }
.dot-offline { background: #ef4444; box-shadow: 0 0 8px #ef4444; animation: none; }
@keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50%       { transform: scale(1.4); opacity: .6; }
}

/* ══ Sidebar sections ══════════════════════════════════════ */
.sb-section {
    margin-bottom: 1rem;
    padding: .9rem;
    background: rgba(255,255,255,.02);
    border: 1px solid rgba(255,255,255,.05);
    border-radius: 12px;
}
.sb-section-title {
    font-family: 'Space Mono', monospace;
    font-size: .62rem;
    text-transform: uppercase;
    letter-spacing: .15em;
    color: #334155;
    margin-bottom: .7rem;
}
.sb-item {
    display: flex;
    align-items: center;
    gap: .5rem;
    padding: .35rem 0;
    font-size: .78rem;
    color: #64748b;
    border-bottom: 1px solid rgba(255,255,255,.03);
}
.sb-item:last-child { border-bottom: none; }
.sb-item-val {
    margin-left: auto;
    font-family: 'Space Mono', monospace;
    font-size: .72rem;
    color: #06b6d4;
}

/* ══ Hero ══════════════════════════════════════════════════ */
.hero {
    position: relative;
    padding: 3rem 3rem 2.5rem;
    margin-bottom: 2rem;
    border-radius: 20px;
    overflow: hidden;
    background: linear-gradient(135deg,
        rgba(6,182,212,.04) 0%,
        rgba(2,3,8,.8) 40%,
        rgba(139,92,246,.04) 100%);
    border: 1px solid rgba(6,182,212,.12);
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(6,182,212,.08) 0%, transparent 70%);
    pointer-events: none;
    animation: heroGlow 4s ease-in-out infinite alternate;
}
@keyframes heroGlow {
    0%   { transform: scale(1);    opacity: .5; }
    100% { transform: scale(1.2);  opacity: 1; }
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: .5rem;
    font-family: 'Space Mono', monospace;
    font-size: .65rem;
    text-transform: uppercase;
    letter-spacing: .2em;
    color: #06b6d4;
    margin-bottom: 1rem;
    padding: .35rem .8rem;
    background: rgba(6,182,212,.06);
    border: 1px solid rgba(6,182,212,.15);
    border-radius: 20px;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -.03em;
    color: #f8fafc;
    margin-bottom: .6rem;
}
.hero-title span {
    background: linear-gradient(90deg, #06b6d4, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: .9rem;
    color: #475569;
    font-weight: 300;
    max-width: 500px;
    line-height: 1.7;
}
.hero-stats {
    display: flex;
    gap: 2rem;
    margin-top: 1.8rem;
    padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,.04);
}
.hero-stat-val {
    font-family: 'Syne', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #06b6d4;
}
.hero-stat-lbl {
    font-size: .7rem;
    color: #334155;
    text-transform: uppercase;
    letter-spacing: .08em;
    font-family: 'Space Mono', monospace;
}

/* ══ Upload zone ═══════════════════════════════════════════ */
.upload-zone {
    border: 2px dashed rgba(6,182,212,.2);
    border-radius: 16px;
    padding: 2.5rem 1.5rem;
    text-align: center;
    background: rgba(6,182,212,.02);
    transition: all .3s ease;
    margin-bottom: 1rem;
    cursor: pointer;
}
.upload-zone:hover {
    border-color: rgba(6,182,212,.5);
    background: rgba(6,182,212,.04);
}
.upload-icon { font-size: 2.5rem; margin-bottom: .8rem; }
.upload-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #94a3b8;
    margin-bottom: .3rem;
}
.upload-sub { font-size: .78rem; color: #334155; }

/* ══ Info box ══════════════════════════════════════════════ */
.info-box {
    background: rgba(6,182,212,.04);
    border: 1px solid rgba(6,182,212,.12);
    border-left: 3px solid #06b6d4;
    border-radius: 0 10px 10px 0;
    padding: .8rem 1rem;
    font-size: .8rem;
    color: #64748b;
    line-height: 1.7;
    margin-bottom: 1rem;
}

/* ══ Métriques image ═══════════════════════════════════════ */
.img-meta {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: .6rem;
    margin: .8rem 0;
}
.img-meta-card {
    background: rgba(255,255,255,.02);
    border: 1px solid rgba(255,255,255,.05);
    border-radius: 10px;
    padding: .7rem;
    text-align: center;
}
.img-meta-val {
    font-family: 'Space Mono', monospace;
    font-size: .9rem;
    color: #06b6d4;
    font-weight: 700;
}
.img-meta-lbl {
    font-size: .62rem;
    color: #334155;
    text-transform: uppercase;
    letter-spacing: .08em;
    margin-top: .2rem;
}

/* ══ Bouton analyser ═══════════════════════════════════════ */
.stButton > button {
    width: 100% !important;
    padding: .85rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: .95rem !important;
    font-weight: 700 !important;
    letter-spacing: .03em !important;
    color: #020308 !important;
    background: linear-gradient(135deg, #06b6d4, #0891b2) !important;
    border: none !important;
    border-radius: 12px !important;
    cursor: pointer !important;
    transition: all .3s ease !important;
    box-shadow: 0 0 30px rgba(6,182,212,.25) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 50px rgba(6,182,212,.45) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ══ Résultat cards ════════════════════════════════════════ */
.result-card {
    border-radius: 18px;
    padding: 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
    animation: fadeInUp .5s ease forwards;
}
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
}
.result-cancer {
    background: linear-gradient(135deg, rgba(239,68,68,.08), rgba(185,28,28,.05));
    border: 1px solid rgba(239,68,68,.25);
    box-shadow: 0 0 60px rgba(239,68,68,.08) inset;
}
.result-negative {
    background: linear-gradient(135deg, rgba(16,185,129,.08), rgba(5,150,105,.05));
    border: 1px solid rgba(16,185,129,.25);
    box-shadow: 0 0 60px rgba(16,185,129,.08) inset;
}
.result-icon {
    font-size: 3.5rem;
    margin-bottom: .8rem;
    display: block;
    animation: iconBounce .6s cubic-bezier(.36,.07,.19,.97) forwards;
}
@keyframes iconBounce {
    0%   { transform: scale(0) rotate(-20deg); }
    60%  { transform: scale(1.2) rotate(5deg); }
    100% { transform: scale(1)   rotate(0deg); }
}
.result-title-main {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: -.02em;
    margin-bottom: .3rem;
}
.result-cancer  .result-title-main { color: #fca5a5; }
.result-negative .result-title-main { color: #6ee7b7; }
.result-subtitle {
    font-size: .8rem;
    color: #475569;
    margin-bottom: 1.2rem;
    font-style: italic;
}

/* ══ Barre confiance ════════════════════════════════════════ */
.conf-bar-wrap { margin: 1rem 0 .4rem; }
.conf-bar-bg {
    height: 6px;
    background: rgba(255,255,255,.06);
    border-radius: 6px;
    overflow: hidden;
}
.conf-bar-fill {
    height: 100%;
    border-radius: 6px;
    transition: width 1s cubic-bezier(.4,0,.2,1);
}
.fill-cancer   { background: linear-gradient(90deg, #ef4444, #f97316); }
.fill-negative { background: linear-gradient(90deg, #10b981, #06b6d4); }
.conf-pct {
    font-family: 'Space Mono', monospace;
    font-size: .82rem;
    margin-top: .4rem;
    color: #94a3b8;
}

/* ══ Mini métriques ════════════════════════════════════════ */
.metrics-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: .6rem;
    margin-top: 1rem;
}
.metric-mini {
    background: rgba(255,255,255,.02);
    border: 1px solid rgba(255,255,255,.05);
    border-radius: 10px;
    padding: .8rem .5rem;
    text-align: center;
}
.metric-mini-val {
    font-family: 'Space Mono', monospace;
    font-size: .9rem;
    font-weight: 700;
}
.metric-mini-lbl {
    font-size: .6rem;
    color: #334155;
    text-transform: uppercase;
    letter-spacing: .1em;
    margin-top: .3rem;
}

/* ══ Grad-CAM section ══════════════════════════════════════ */
.gcam-header {
    display: flex;
    align-items: center;
    gap: .8rem;
    margin: 1.5rem 0 .8rem;
    padding-bottom: .8rem;
    border-bottom: 1px solid rgba(255,255,255,.04);
}
.gcam-badge {
    font-family: 'Space Mono', monospace;
    font-size: .6rem;
    text-transform: uppercase;
    letter-spacing: .15em;
    color: #8b5cf6;
    background: rgba(139,92,246,.08);
    border: 1px solid rgba(139,92,246,.2);
    padding: .2rem .6rem;
    border-radius: 20px;
}
.gcam-title {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #94a3b8;
}
.gcam-legend {
    font-size: .75rem;
    color: #475569;
    padding: .6rem .8rem;
    background: rgba(139,92,246,.04);
    border: 1px solid rgba(139,92,246,.1);
    border-radius: 8px;
    margin-bottom: .8rem;
    line-height: 1.6;
}

/* ══ Alert médical ═════════════════════════════════════════ */
.medical-alert {
    background: rgba(234,179,8,.04);
    border: 1px solid rgba(234,179,8,.15);
    border-left: 3px solid #eab308;
    border-radius: 0 10px 10px 0;
    padding: .9rem 1.2rem;
    font-size: .78rem;
    color: #78716c;
    line-height: 1.8;
    margin-top: 1.5rem;
}

/* ══ Empty state ═══════════════════════════════════════════ */
.empty-state {
    border: 1px solid rgba(255,255,255,.04);
    border-radius: 16px;
    padding: 4rem 2rem;
    text-align: center;
    background: rgba(255,255,255,.01);
    height: 100%;
    min-height: 300px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: .8rem;
}
.empty-icon {
    font-size: 3rem;
    opacity: .3;
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-10px); }
}
.empty-text { color: #1e293b; font-size: .85rem; }

/* ══ Divider ═══════════════════════════════════════════════ */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(6,182,212,.15), transparent);
    margin: 1.5rem 0;
}

/* ══ Steps bas de page ═════════════════════════════════════ */
.how-to {
    margin-top: 2rem;
    padding: 1.5rem;
    background: rgba(255,255,255,.01);
    border: 1px solid rgba(255,255,255,.04);
    border-radius: 16px;
}
.how-title {
    font-family: 'Syne', sans-serif;
    font-size: .85rem;
    font-weight: 600;
    color: #334155;
    text-transform: uppercase;
    letter-spacing: .1em;
    margin-bottom: 1rem;
}
.steps-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: .8rem; }
.step {
    padding: .9rem;
    background: rgba(255,255,255,.02);
    border: 1px solid rgba(255,255,255,.04);
    border-radius: 10px;
    position: relative;
}
.step-num {
    font-family: 'Space Mono', monospace;
    font-size: .7rem;
    color: #06b6d4;
    margin-bottom: .4rem;
}
.step-title { font-size: .82rem; color: #94a3b8; font-weight: 500; margin-bottom: .25rem; }
.step-desc  { font-size: .72rem; color: #334155; line-height: 1.5; }

/* ══ Footer ════════════════════════════════════════════════ */
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    font-family: 'Space Mono', monospace;
    font-size: .62rem;
    color: #1e293b;
    letter-spacing: .08em;
    text-transform: uppercase;
}

/* ══ Override Streamlit éléments ═══════════════════════════ */
.stFileUploader > div { background: transparent !important; border: none !important; }
.stCheckbox > label { color: #64748b !important; font-size: .82rem !important; }
.stSpinner > div { border-color: #06b6d4 !important; }
div[data-testid="stImage"] img { border-radius: 12px; }
.stAlert { border-radius: 10px !important; }
section[data-testid="stFileUploadDropzone"] {
    background: rgba(6,182,212,.02) !important;
    border: 2px dashed rgba(6,182,212,.2) !important;
    border-radius: 14px !important;
    padding: 1.5rem !important;
}
section[data-testid="stFileUploadDropzone"]:hover {
    border-color: rgba(6,182,212,.5) !important;
    background: rgba(6,182,212,.04) !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Helpers ───────────────────────────────────────────────────
@st.cache_data(ttl=15)
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
        return False, {"error": "Impossible de joindre l'API."}
    except requests.exceptions.Timeout:
        return False, {"error": "Timeout — l'API prend trop de temps (90s dépassé)."}
    except Exception as e:
        return False, {"error": str(e)}

def b64_to_pil(b64):
    return Image.open(io.BytesIO(base64.b64decode(b64)))


# ─── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="sb-logo-icon">🔬</div>
        <div>
            <div class="sb-logo-text">CancerScan IA</div>
            <div class="sb-logo-sub">v1.0 · 2025-2026</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    api_ok, api_info = api_health()

    if api_ok:
        st.markdown(f"""
        <div class="status-badge status-online">
            <div class="status-dot dot-online"></div>
            API Connectée
            <span style="font-size:.7rem;color:#065f46;margin-left:auto;">LIVE</span>
        </div>
        <div style="font-size:.7rem;color:#1e3a2f;font-family:'Space Mono',monospace;
                    padding:.3rem .6rem;margin-bottom:1rem;word-break:break-all;">
            {API_URL}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="status-badge status-offline">
            <div class="status-dot dot-offline"></div>
            API Hors ligne
        </div>
        <div style="font-size:.7rem;color:#3b1a1a;font-family:'Space Mono',monospace;
                    padding:.3rem .6rem;margin-bottom:1rem;word-break:break-all;">
            {API_URL}
        </div>
        """, unsafe_allow_html=True)

    # Options
    st.markdown("""
    <div class="sb-section">
        <div class="sb-section-title">⚙ Options d'analyse</div>
    </div>
    """, unsafe_allow_html=True)
    use_gradcam = st.checkbox("🗺 Activer Grad-CAM", value=True,
        help="Génère une carte de chaleur montrant les zones décisives du modèle.")

    # Infos modèle
    if api_ok:
        th  = api_info.get("threshold", 0.5)
        cls = api_info.get("class_labels", {"0":"Cancer","1":"Negative"})
        tfv = api_info.get("tf_version", "2.15.0")
        st.markdown(f"""
        <div class="sb-section" style="margin-top:.5rem;">
            <div class="sb-section-title">🧠 Modèle</div>
            <div class="sb-item">Architecture<span class="sb-item-val">EfficientNetB0</span></div>
            <div class="sb-item">Seuil<span class="sb-item-val">{th}</span></div>
            <div class="sb-item">TensorFlow<span class="sb-item-val">{tfv}</span></div>
            <div class="sb-item">Classes<span class="sb-item-val">2</span></div>
        </div>
        """, unsafe_allow_html=True)

    # Performances
    st.markdown("""
    <div class="sb-section" style="margin-top:.5rem;">
        <div class="sb-section-title">📊 Performances</div>
        <div class="sb-item">Accuracy<span class="sb-item-val" style="color:#10b981;">95.16%</span></div>
        <div class="sb-item">F1-Score<span class="sb-item-val" style="color:#10b981;">0.95</span></div>
        <div class="sb-item">Dataset<span class="sb-item-val">828 imgs</span></div>
        <div class="sb-item">Epochs<span class="sb-item-val">27 / 50</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Projet
    st.markdown("""
    <div class="sb-section" style="margin-top:.5rem;">
        <div class="sb-section-title">🎓 Projet</div>
        <div class="sb-item">Université de Thiès</div>
        <div class="sb-item">UFR SET · MaRT2</div>
        <div class="sb-item">Pr. Cheikh SARR</div>
        <div class="sb-item">Deep Learning · 2025-2026</div>
    </div>
    """, unsafe_allow_html=True)


# ─── Hero ──────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">
        <span>⬡</span> Classification histologique · IDC · EfficientNetB0
    </div>
    <h1 class="hero-title">
        Cancer<span>Scan</span> IA
    </h1>
    <p class="hero-sub">
        Détection automatique du carcinome canalaire invasif (IDC) par deep learning.
        Modèle fine-tuné avec explicabilité Grad-CAM intégrée.
    </p>
    <div class="hero-stats">
        <div>
            <div class="hero-stat-val">95.16%</div>
            <div class="hero-stat-lbl">Précision</div>
        </div>
        <div>
            <div class="hero-stat-val">0.95</div>
            <div class="hero-stat-lbl">F1-Score</div>
        </div>
        <div>
            <div class="hero-stat-val">4.38M</div>
            <div class="hero-stat-lbl">Paramètres</div>
        </div>
        <div>
            <div class="hero-stat-val">224px</div>
            <div class="hero-stat-lbl">Input size</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── Colonnes principales ───────────────────────────────────────
col_l, col_r = st.columns([1, 1], gap="large")

# ══ Colonne gauche : Upload ══════════════════════════════════════
with col_l:
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:.75rem;font-weight:600;
                text-transform:uppercase;letter-spacing:.15em;color:#334155;margin-bottom:.8rem;">
        ▲ Image histologique
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        Téléversez une coupe histologique du tissu mammaire (JPG/PNG).
        Le modèle analyse les caractéristiques cellulaires pour détecter
        la présence ou l'absence de carcinome canalaire invasif (IDC).
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Image histologique",
        type=["jpg","jpeg","png"],
        label_visibility="collapsed",
    )

    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, use_column_width=True, caption="")

        w, h = image.size
        size_kb = len(uploaded.getvalue()) // 1024
        st.markdown(f"""
        <div class="img-meta">
            <div class="img-meta-card">
                <div class="img-meta-val">{w}px</div>
                <div class="img-meta-lbl">Largeur</div>
            </div>
            <div class="img-meta-card">
                <div class="img-meta-val">{h}px</div>
                <div class="img-meta-lbl">Hauteur</div>
            </div>
            <div class="img-meta-card">
                <div class="img-meta-val">{size_kb}Ko</div>
                <div class="img-meta-lbl">Taille</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if not api_ok:
            st.error("⚠️ L'API est hors ligne. Vérifiez la connexion Render.")
        else:
            if st.button("⬡ Analyser l'image avec l'IA"):
                with st.spinner("Inférence EfficientNetB0 en cours..."):
                    t0 = time.time()
                    ok, resp = call_api(uploaded.getvalue(), use_gradcam)
                    elapsed = time.time() - t0

                if ok:
                    resp["_elapsed"] = round(elapsed, 2)
                    st.session_state["result"]   = resp
                    st.session_state["orig_img"] = image
                    st.rerun()
                else:
                    st.error(f"❌ {resp.get('error','Erreur inconnue')}")
    else:
        st.markdown("""
        <div class="empty-state" style="min-height:280px;">
            <div class="empty-icon">🔬</div>
            <div class="empty-text">Glissez une image ici<br>ou cliquez pour parcourir</div>
            <div style="font-size:.7rem;color:#0f172a;margin-top:.5rem;">JPG · PNG · max 200MB</div>
        </div>
        """, unsafe_allow_html=True)


# ══ Colonne droite : Résultats ═══════════════════════════════════
with col_r:
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:.75rem;font-weight:600;
                text-transform:uppercase;letter-spacing:.15em;color:#334155;margin-bottom:.8rem;">
        ◈ Résultat de l'analyse
    </div>
    """, unsafe_allow_html=True)

    if "result" not in st.session_state:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📊</div>
            <div class="empty-text">Les résultats apparaîtront ici<br>après l'analyse</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        res     = st.session_state["result"]
        pred    = res.get("prediction", {})
        label   = pred.get("label", "—")
        conf    = pred.get("confidence_pct", 0)
        raw     = pred.get("raw_score", 0)
        probs   = pred.get("probabilities", {})
        elapsed = res.get("_elapsed", "—")
        is_cancer = label.lower() == "cancer"

        if is_cancer:
            st.markdown(f"""
            <div class="result-card result-cancer">
                <span class="result-icon">⚠️</span>
                <div class="result-title-main">IDC Positif</div>
                <div class="result-subtitle">Carcinome canalaire invasif détecté</div>
                <div class="conf-bar-wrap">
                    <div class="conf-bar-bg">
                        <div class="conf-bar-fill fill-cancer" style="width:{conf}%"></div>
                    </div>
                    <div class="conf-pct">{conf:.1f}% de confiance</div>
                </div>
                <div class="metrics-row">
                    <div class="metric-mini">
                        <div class="metric-mini-val" style="color:#fca5a5;">{probs.get('Cancer',0):.1f}%</div>
                        <div class="metric-mini-lbl">P(Cancer)</div>
                    </div>
                    <div class="metric-mini">
                        <div class="metric-mini-val" style="color:#6ee7b7;">{probs.get('Negative',0):.1f}%</div>
                        <div class="metric-mini-lbl">P(Négatif)</div>
                    </div>
                    <div class="metric-mini">
                        <div class="metric-mini-val" style="color:#94a3b8;">{elapsed}s</div>
                        <div class="metric-mini-lbl">Inférence</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-card result-negative">
                <span class="result-icon">✅</span>
                <div class="result-title-main">IDC Négatif</div>
                <div class="result-subtitle">Aucun signe de carcinome détecté</div>
                <div class="conf-bar-wrap">
                    <div class="conf-bar-bg">
                        <div class="conf-bar-fill fill-negative" style="width:{conf}%"></div>
                    </div>
                    <div class="conf-pct">{conf:.1f}% de confiance</div>
                </div>
                <div class="metrics-row">
                    <div class="metric-mini">
                        <div class="metric-mini-val" style="color:#fca5a5;">{probs.get('Cancer',0):.1f}%</div>
                        <div class="metric-mini-lbl">P(Cancer)</div>
                    </div>
                    <div class="metric-mini">
                        <div class="metric-mini-val" style="color:#6ee7b7;">{probs.get('Negative',0):.1f}%</div>
                        <div class="metric-mini-lbl">P(Négatif)</div>
                    </div>
                    <div class="metric-mini">
                        <div class="metric-mini-val" style="color:#94a3b8;">{elapsed}s</div>
                        <div class="metric-mini-lbl">Inférence</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Score brut
        st.markdown(f"""
        <div style="margin-top:.8rem;padding:.6rem .9rem;background:rgba(255,255,255,.02);
                    border:1px solid rgba(255,255,255,.04);border-radius:10px;
                    display:flex;align-items:center;gap:.8rem;">
            <span style="font-size:.72rem;color:#334155;text-transform:uppercase;
                         letter-spacing:.08em;font-family:'Space Mono',monospace;">Score brut</span>
            <span style="font-family:'Space Mono',monospace;font-size:.88rem;
                         color:#06b6d4;margin-left:auto;">{raw:.6f}</span>
        </div>
        """, unsafe_allow_html=True)

        # Grad-CAM
        gcam = res.get("gradcam_image")
        if use_gradcam and gcam:
            st.markdown("""
            <div class="gcam-header">
                <span class="gcam-badge">Grad-CAM</span>
                <span class="gcam-title">Zones d'activation</span>
            </div>
            <div class="gcam-legend">
                🔴 <strong>Rouge/Jaune</strong> = zones fortement activées — déterminantes pour la décision<br>
                🔵 <strong>Bleu/Vert</strong> = zones peu activées — faible contribution au résultat
            </div>
            """, unsafe_allow_html=True)

            g1, g2 = st.columns(2)
            with g1:
                st.image(
                    st.session_state["orig_img"].resize((224,224)),
                    caption="Image originale",
                    use_column_width=True,
                )
            with g2:
                st.image(
                    b64_to_pil(gcam),
                    caption="Heatmap Grad-CAM",
                    use_column_width=True,
                )

        st.markdown("""
        <div class="medical-alert">
            ⚕️ <strong>Avertissement clinique</strong> — Ce système est un outil de recherche
            pédagogique (Deep Learning, Université de Thiès). Il ne constitue pas un dispositif
            médical certifié et ne remplace en aucun cas un diagnostic médical professionnel.
            Tout résultat doit être validé par un médecin anatomopathologiste qualifié.
        </div>
        """, unsafe_allow_html=True)


# ─── Guide d'utilisation ────────────────────────────────────────
st.markdown("""
<div class="divider"></div>
<div class="how-to">
    <div class="how-title">// Mode d'emploi</div>
    <div class="steps-grid">
        <div class="step">
            <div class="step-num">01 ──</div>
            <div class="step-title">Téléverser</div>
            <div class="step-desc">Chargez une image histologique JPG/PNG du tissu mammaire.</div>
        </div>
        <div class="step">
            <div class="step-num">02 ──</div>
            <div class="step-title">Vérifier</div>
            <div class="step-desc">Confirmez que l'API est ✅ connectée dans la barre latérale.</div>
        </div>
        <div class="step">
            <div class="step-num">03 ──</div>
            <div class="step-title">Analyser</div>
            <div class="step-desc">Lancez l'analyse IA — EfficientNetB0 prédit en ~2 secondes.</div>
        </div>
        <div class="step">
            <div class="step-num">04 ──</div>
            <div class="step-title">Interpréter</div>
            <div class="step-desc">Lisez le résultat, la confiance et explorez la heatmap Grad-CAM.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Footer ─────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    Université de Thiès · UFR SET · Département Informatique · MaRT2
    · Deep Learning 2025-2026 · Pr. Cheikh SARR
    · Ibrahima MBAYE & Thiecoura NDIAYE
</div>
""", unsafe_allow_html=True)