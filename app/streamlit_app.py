# =============================================================
# CancerScan IA — Interface Moderne, Lumineuse & Ergonomique
# Classification du Cancer du Sein — IDC
# Université de Thiès — UFR SET — MaRT2 — 2025-2026
# =============================================================

import os, io, base64, time, json, requests, streamlit as st
from PIL import Image
from datetime import datetime

st.set_page_config(
    page_title="CancerScan IA",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = os.getenv("API_URL", "https://cancer-scan-ia.onrender.com")

# ════════════════════════════════════════════════════════════════
# CSS — Interface Claire, Moderne & Ergonomique
# ════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* BASE */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background: #f8fafc !important;
    color: #0f172a !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
    box-shadow: 2px 0 12px rgba(15,23,42,.06) !important;
}
[data-testid="stSidebar"] > div { padding: 1.5rem 1.1rem !important; }

.sb-logo {
    display: flex; align-items: center; gap: 10px;
    padding-bottom: 1.2rem; margin-bottom: 1.2rem;
    border-bottom: 1px solid #f1f5f9;
}
.sb-icon {
    width: 40px; height: 40px; border-radius: 10px;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
    box-shadow: 0 4px 12px rgba(37,99,235,.25);
}
.sb-name { font-weight: 700; font-size: .95rem; color: #0f172a; letter-spacing: -.015em; }
.sb-ver  { font-size: .62rem; color: #94a3b8; font-family: 'JetBrains Mono', monospace; }

.pill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: .5rem .85rem; border-radius: 8px;
    font-size: .78rem; font-weight: 600; width: 100%;
    margin-bottom: .4rem;
}
.pill-on  { background: #f0fdf4; border: 1px solid #bbf7d0; color: #15803d; }
.pill-off { background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; }
.dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.dot-on  { background: #22c55e; box-shadow: 0 0 0 2px rgba(34,197,94,.25); animation: pulse 2s infinite; }
.dot-off { background: #ef4444; }
@keyframes pulse { 0%,100%{box-shadow:0 0 0 2px rgba(34,197,94,.25);} 50%{box-shadow:0 0 0 5px rgba(34,197,94,.1);} }

.api-url {
    font-family: 'JetBrains Mono', monospace; font-size: .6rem;
    color: #94a3b8; background: #f8fafc; border-radius: 6px;
    padding: .25rem .5rem; margin-bottom: 1rem;
    word-break: break-all; display: block;
}

.section { margin-bottom: .9rem; }
.section-title {
    font-size: .6rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: .12em; color: #94a3b8; margin-bottom: .5rem;
    display: block;
}
.sb-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: .3rem 0; font-size: .77rem; color: #475569;
    border-bottom: 1px solid #f8fafc;
}
.sb-row:last-child { border-bottom: none; }
.sb-val { font-family: 'JetBrains Mono', monospace; font-size: .7rem; font-weight: 500; }
.green { color: #16a34a; } .blue { color: #2563eb; } .gray { color: #64748b; }

/* HERO */
.hero {
    background: linear-gradient(135deg, #1d4ed8 0%, #4338ca 60%, #6d28d9 100%);
    border-radius: 16px; padding: 2.2rem 2.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 12px 40px rgba(67,56,202,.2);
    position: relative; overflow: hidden;
}
.hero::before {
    content: ''; position: absolute;
    width: 280px; height: 280px; border-radius: 50%;
    background: rgba(255,255,255,.05);
    top: -80px; right: -60px;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(255,255,255,.15); border: 1px solid rgba(255,255,255,.25);
    border-radius: 20px; padding: .3rem .85rem;
    font-size: .7rem; font-weight: 600; color: rgba(255,255,255,.9);
    letter-spacing: .04em; margin-bottom: .9rem;
}
.hero h1 {
    font-size: 2.2rem; font-weight: 700; color: #fff;
    letter-spacing: -.03em; line-height: 1.1; margin: 0 0 .45rem;
}
.hero-sub { color: rgba(255,255,255,.65); font-size: .85rem; font-weight: 400; margin: 0; }
.hero-kpis {
    display: flex; gap: 2rem; margin-top: 1.6rem;
    padding-top: 1.2rem; border-top: 1px solid rgba(255,255,255,.12);
}
.kpi-val { font-size: 1.45rem; font-weight: 700; color: #fff; }
.kpi-lbl { font-size: .62rem; color: rgba(255,255,255,.5); text-transform: uppercase; letter-spacing: .1em; margin-top: .1rem; }

/* CARDS */
.card {
    background: #fff; border-radius: 14px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 4px rgba(15,23,42,.04);
    padding: 1.3rem; margin-bottom: 1rem;
}
.card-hd {
    font-size: .62rem; font-weight: 600; text-transform: uppercase;
    letter-spacing: .12em; color: #94a3b8; margin-bottom: 1rem;
}

/* INFO BOX */
.info-box {
    background: #eff6ff; border: 1px solid #bfdbfe;
    border-left: 3px solid #3b82f6; border-radius: 0 8px 8px 0;
    padding: .75rem 1rem; font-size: .78rem; color: #1e40af;
    line-height: 1.6; margin-bottom: .9rem;
}

/* IMAGE META */
.img-meta { display: grid; grid-template-columns: repeat(3, 1fr); gap: .5rem; margin: .7rem 0; }
.img-meta-c {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 8px; padding: .6rem; text-align: center;
}
.img-meta-v { font-family: 'JetBrains Mono', monospace; font-size: .85rem; font-weight: 600; color: #2563eb; }
.img-meta-l { font-size: .6rem; color: #94a3b8; text-transform: uppercase; letter-spacing: .08em; margin-top: .15rem; }

/* BUTTON */
.stButton > button {
    width: 100% !important; padding: .8rem 1.5rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: .9rem !important; font-weight: 600 !important;
    color: #fff !important;
    background: linear-gradient(135deg, #2563eb, #7c3aed) !important;
    border: none !important; border-radius: 10px !important;
    box-shadow: 0 4px 16px rgba(37,99,235,.25) !important;
    transition: all .25s ease !important; cursor: pointer !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(37,99,235,.35) !important;
}

/* RÉSULTAT CANCER */
.res-cancer {
    background: #fff5f5; border: 1.5px solid #fca5a5;
    border-radius: 16px; padding: 1.8rem; text-align: center;
    box-shadow: 0 4px 20px rgba(239,68,68,.08);
    animation: fadeUp .4s ease;
}
/* RÉSULTAT NÉGATIF */
.res-negative {
    background: #f0fdf4; border: 1.5px solid #86efac;
    border-radius: 16px; padding: 1.8rem; text-align: center;
    box-shadow: 0 4px 20px rgba(34,197,94,.08);
    animation: fadeUp .4s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.res-icon { font-size: 3rem; display: block; margin-bottom: .5rem; }
.res-title-cancer   { font-size: 1.65rem; font-weight: 700; color: #dc2626; letter-spacing: -.02em; }
.res-title-negative { font-size: 1.65rem; font-weight: 700; color: #16a34a; letter-spacing: -.02em; }
.res-desc { font-size: .78rem; color: #64748b; margin: .3rem 0 1rem; font-style: italic; }

/* BARRE DE CONFIANCE */
.bar-bg { height: 7px; background: #e2e8f0; border-radius: 7px; overflow: hidden; margin: .6rem 0 .3rem; }
.bar-cancer   { height: 100%; background: linear-gradient(90deg, #ef4444, #f97316); border-radius: 7px; transition: width 1s ease; }
.bar-negative { height: 100%; background: linear-gradient(90deg, #22c55e, #10b981); border-radius: 7px; transition: width 1s ease; }
.bar-pct { font-size: .78rem; color: #475569; font-weight: 600; margin-bottom: .8rem; }

/* MÉTRIQUES RÉSULTATS */
.res-metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: .5rem; }
.res-m {
    background: rgba(255,255,255,.8); border: 1px solid rgba(255,255,255,.9);
    border-radius: 8px; padding: .65rem; text-align: center;
}
.res-m-v { font-family: 'JetBrains Mono', monospace; font-size: .85rem; font-weight: 600; }
.res-m-l { font-size: .58rem; color: #94a3b8; text-transform: uppercase; letter-spacing: .08em; margin-top: .2rem; }

/* SCORE RAW */
.score-row {
    display: flex; align-items: center; justify-content: space-between;
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 8px; padding: .55rem .9rem; margin-top: .7rem;
}
.score-lbl { font-size: .73rem; color: #64748b; font-weight: 500; }
.score-val { font-family: 'JetBrains Mono', monospace; font-size: .8rem; color: #2563eb; font-weight: 600; }

/* GRAD-CAM */
.gcam-hd { display: flex; align-items: center; gap: .6rem; margin: 1.3rem 0 .7rem; }
.gcam-badge {
    background: #f5f3ff; border: 1px solid #c4b5fd;
    color: #6d28d9; font-size: .6rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: .12em;
    padding: .2rem .6rem; border-radius: 20px;
}
.gcam-title { font-size: .88rem; font-weight: 600; color: #1e293b; }
.gcam-legend {
    background: #fafafa; border: 1px solid #e2e8f0;
    border-left: 3px solid #7c3aed; border-radius: 0 8px 8px 0;
    padding: .65rem .9rem; font-size: .75rem; color: #475569;
    line-height: 1.7; margin-bottom: .7rem;
}

/* ALERTE MÉDICALE */
.med-alert {
    background: #fffbeb; border: 1px solid #fde68a;
    border-radius: 10px; padding: .85rem 1.1rem;
    font-size: .75rem; color: #78350f; line-height: 1.8;
    margin-top: 1.2rem;
}

/* BOUTONS EXPORT */
.export-row {
    display: grid; grid-template-columns: 1fr 1fr;
    gap: .6rem; margin-top: 1rem;
}
.btn-save-cancer {
    background: #fef2f2; border: 1.5px solid #fca5a5;
    color: #dc2626; border-radius: 8px; padding: .55rem .8rem;
    font-size: .78rem; font-weight: 600; text-align: center;
    cursor: pointer; transition: all .2s;
}
.btn-save-cancer:hover { background: #fee2e2; }
.btn-save-neg {
    background: #f0fdf4; border: 1.5px solid #86efac;
    color: #16a34a; border-radius: 8px; padding: .55rem .8rem;
    font-size: .78rem; font-weight: 600; text-align: center;
    cursor: pointer; transition: all .2s;
}
.btn-save-neg:hover { background: #dcfce7; }

/* EMPTY STATE */
.empty {
    background: #fff; border: 2px dashed #e2e8f0;
    border-radius: 14px; min-height: 300px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    gap: .7rem; padding: 3rem 2rem; text-align: center;
}
.empty-icon { font-size: 2.5rem; opacity: .2; animation: float 3s ease-in-out infinite; }
@keyframes float { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-7px);} }
.empty-txt { font-size: .82rem; color: #cbd5e1; font-weight: 500; }

/* HOW TO */
.how-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: .7rem; margin-top: .8rem; }
.how-step {
    background: #fff; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 1.1rem;
    transition: transform .2s, box-shadow .2s;
}
.how-step:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(15,23,42,.08); }
.how-n {
    width: 26px; height: 26px; border-radius: 7px;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    color: #fff; font-size: .72rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: .7rem;
}
.how-t { font-size: .82rem; font-weight: 600; color: #1e293b; margin-bottom: .25rem; }
.how-d { font-size: .72rem; color: #64748b; line-height: 1.5; }

/* FOOTER */
.footer {
    text-align: center; padding: 1.5rem 0;
    font-size: .7rem; color: #cbd5e1;
    border-top: 1px solid #e2e8f0; margin-top: 1.5rem;
}

/* STREAMLIT overrides */
.stCheckbox > label { font-size: .82rem !important; color: #374151 !important; font-weight: 500 !important; }
div[data-testid="stImage"] img { border-radius: 10px; box-shadow: 0 2px 12px rgba(15,23,42,.06); }
section[data-testid="stFileUploadDropzone"] {
    background: #eff6ff !important;
    border: 2px dashed #93c5fd !important;
    border-radius: 12px !important;
}
section[data-testid="stFileUploadDropzone"]:hover {
    background: #dbeafe !important; border-color: #3b82f6 !important;
}
.stDownloadButton > button {
    width: 100% !important; background: #f8fafc !important;
    border: 1.5px solid #e2e8f0 !important; color: #374151 !important;
    border-radius: 8px !important; font-weight: 600 !important;
    font-size: .8rem !important; padding: .6rem !important;
}
.stDownloadButton > button:hover { background: #f1f5f9 !important; border-color: #cbd5e1 !important; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# HELPERS
# ════════════════════════════════════════════════════════════════
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

def img_to_bytes(img: Image.Image, fmt="PNG") -> bytes:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()

def generate_pdf_report(label, conf, raw, probs, elapsed, filename, gcam_b64=None):
    """Génère un rapport PDF simple en HTML puis encodé."""
    now = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
    color = "#dc2626" if label.lower() == "cancer" else "#16a34a"
    verdict = "IDC Positif — Carcinome détecté" if label.lower() == "cancer" else "IDC Négatif — Tissu sain"
    icon = "⚠️" if label.lower() == "cancer" else "✅"
    gcam_section = ""
    if gcam_b64:
        gcam_section = f"""
        <h2 style="color:#7c3aed;margin-top:24px;">Visualisation Grad-CAM</h2>
        <img src="data:image/png;base64,{gcam_b64}"
             style="width:200px;border-radius:8px;border:1px solid #e2e8f0;" />
        <p style="font-size:11px;color:#64748b;">
            Les zones chaudes (rouge/orange) indiquent les régions déterminantes pour la décision du modèle.
        </p>
        """

    html = f"""<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"/>
<style>
  body {{ font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; color: #1e293b; }}
  h1   {{ color: #1d4ed8; font-size: 22px; }}
  h2   {{ color: #374151; font-size: 15px; border-bottom: 1px solid #e2e8f0; padding-bottom: 6px; }}
  .verdict {{ background: {'#fef2f2' if label.lower()=='cancer' else '#f0fdf4'};
              border: 2px solid {color}; border-radius: 10px;
              padding: 16px 20px; margin: 16px 0; text-align: center; }}
  .verdict-title {{ font-size: 22px; font-weight: bold; color: {color}; }}
  .kpi {{ display: inline-block; background: #f8fafc; border: 1px solid #e2e8f0;
          border-radius: 8px; padding: 8px 16px; margin: 4px;
          font-family: monospace; }}
  .kpi-lbl {{ font-size: 10px; color: #94a3b8; text-transform: uppercase; }}
  .kpi-val {{ font-size: 16px; font-weight: bold; color: #2563eb; }}
  .alert {{ background: #fffbeb; border: 1px solid #fde68a; border-radius: 8px;
            padding: 12px 16px; font-size: 11px; color: #78350f; margin-top: 20px; }}
  .footer-r {{ font-size: 10px; color: #94a3b8; margin-top: 32px; border-top: 1px solid #e2e8f0; padding-top: 10px; }}
</style></head><body>
  <h1>🔬 CancerScan IA — Rapport d'Analyse</h1>
  <p style="color:#64748b;font-size:12px;">Généré le {now}</p>
  <p style="font-size:12px;color:#64748b;">Fichier analysé : <strong>{filename}</strong></p>

  <h2>Résultat de la prédiction</h2>
  <div class="verdict">
      <div style="font-size:28px;">{icon}</div>
      <div class="verdict-title">{verdict}</div>
      <div style="font-size:13px;color:{color};margin-top:4px;">Confiance : {conf:.1f}%</div>
  </div>

  <h2>Métriques détaillées</h2>
  <div>
      <div class="kpi"><div class="kpi-lbl">P(Cancer)</div><div class="kpi-val" style="color:#dc2626;">{probs.get('Cancer',0):.2f}%</div></div>
      <div class="kpi"><div class="kpi-lbl">P(Négatif)</div><div class="kpi-val" style="color:#16a34a;">{probs.get('Negative',0):.2f}%</div></div>
      <div class="kpi"><div class="kpi-lbl">Score brut</div><div class="kpi-val">{raw:.6f}</div></div>
      <div class="kpi"><div class="kpi-lbl">Inférence</div><div class="kpi-val" style="color:#64748b;">{elapsed}s</div></div>
  </div>

  <h2 style="margin-top:20px;">Modèle utilisé</h2>
  <ul style="font-size:12px;color:#374151;line-height:2;">
      <li>Architecture : EfficientNetB0 (Transfer Learning)</li>
      <li>TensorFlow 2.15.0 — Keras 2.15.0</li>
      <li>Accuracy : 95.16% — F1-Score : 0.95</li>
      <li>Seuil de décision : 0.5</li>
      <li>Taille d'entrée : 224 × 224 pixels</li>
  </ul>

  {gcam_section}

  <div class="alert">
      ⚕️ <strong>Avertissement clinique</strong> — Ce rapport est produit par un système de recherche
      pédagogique (Deep Learning, Université de Thiès, 2025-2026). Il ne constitue pas un dispositif
      médical certifié. Tout résultat doit être validé par un médecin anatomopathologiste qualifié.
  </div>

  <div class="footer-r">
      Université de Thiès · UFR SET · Département Informatique · MaRT2 · Pr. Cheikh SARR<br/>
      Ibrahima MBAYE &amp; Thiecoura NDIAYE · Deep Learning 2025-2026
  </div>
</body></html>"""
    return html.encode("utf-8")


# ════════════════════════════════════════════════════════════════
# SIDEBAR
# ════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="sb-icon">🔬</div>
        <div>
            <div class="sb-name">CancerScan IA</div>
            <div class="sb-ver">v1.0 · MaRT2 · 2025-2026</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    api_ok, api_info = api_health()

    if api_ok:
        st.markdown(f"""
        <div class="pill pill-on">
            <div class="dot dot-on"></div> API Connectée
            <span style="margin-left:auto;font-size:.62rem;background:#bbf7d0;
                         color:#15803d;padding:.1rem .45rem;border-radius:20px;">LIVE</span>
        </div>
        <span class="api-url">{API_URL}</span>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="pill pill-off">
            <div class="dot dot-off"></div> API Hors ligne
        </div>
        <span class="api-url">{API_URL}</span>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section"><span class="section-title">⚙ Options</span></div>', unsafe_allow_html=True)
    use_gradcam = st.checkbox("🗺 Activer Grad-CAM", value=True,
        help="Génère une carte de chaleur des zones décisives du modèle.")

    if api_ok:
        th  = api_info.get("threshold", 0.5)
        tfv = api_info.get("tf_version", "2.15.0")
        st.markdown(f"""
        <div class="section" style="margin-top:.5rem;">
            <span class="section-title">🧠 Modèle IA</span>
            <div class="sb-row">Architecture <span class="sb-val blue">EfficientNetB0</span></div>
            <div class="sb-row">Seuil décision <span class="sb-val blue">{th}</span></div>
            <div class="sb-row">TensorFlow <span class="sb-val gray">{tfv}</span></div>
            <div class="sb-row">Entrée modèle <span class="sb-val blue">224×224px</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section" style="margin-top:.3rem;">
        <span class="section-title">📊 Performances</span>
        <div class="sb-row">Accuracy  <span class="sb-val green">95.16%</span></div>
        <div class="sb-row">F1-Score  <span class="sb-val green">0.95</span></div>
        <div class="sb-row">Précision Cancer <span class="sb-val green">97%</span></div>
        <div class="sb-row">Rappel Cancer <span class="sb-val green">94%</span></div>
        <div class="sb-row">Dataset <span class="sb-val gray">828 images</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section" style="margin-top:.3rem;">
        <span class="section-title">🎓 Projet</span>
        <div class="sb-row">Institution <span class="sb-val gray">Univ. Thiès</span></div>
        <div class="sb-row">Filière <span class="sb-val gray">UFR SET · MaRT2</span></div>
        <div class="sb-row">Encadrant <span class="sb-val gray">Pr. Cheikh SARR</span></div>
        <div class="sb-row">Année <span class="sb-val gray">2025-2026</span></div>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# HERO
# ════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-badge">🔬 Deep Learning · Histologie · IDC · EfficientNetB0</div>
    <h1>CancerScan IA</h1>
    <p class="hero-sub">
        Détection automatique du carcinome canalaire invasif (IDC) par deep learning —
        EfficientNetB0 fine-tuné avec explicabilité Grad-CAM intégrée
    </p>
    <div class="hero-kpis">
        <div><div class="kpi-val">95.16%</div><div class="kpi-lbl">Accuracy</div></div>
        <div><div class="kpi-val">0.95</div><div class="kpi-lbl">F1-Score</div></div>
        <div><div class="kpi-val">4.38M</div><div class="kpi-lbl">Paramètres</div></div>
        <div><div class="kpi-val">27</div><div class="kpi-lbl">Epochs</div></div>
        <div><div class="kpi-val">828</div><div class="kpi-lbl">Images</div></div>
    </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# COLONNES PRINCIPALES
# ════════════════════════════════════════════════════════════════
col_l, col_r = st.columns([1, 1], gap="large")

# ── GAUCHE : Upload ───────────────────────────────────────────
with col_l:
    st.markdown('<div class="card"><div class="card-hd">📤 Image histologique</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        Téléversez une coupe histologique colorée (H&E) du tissu mammaire.
        Le modèle analyse les caractéristiques cellulaires pour détecter
        la présence ou l'absence de <strong>carcinome canalaire invasif (IDC)</strong>.
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if uploaded:
        image = Image.open(uploaded).convert("RGB")

        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.image(image, use_column_width=True, caption="")
        w, h = image.size
        size_kb = len(uploaded.getvalue()) // 1024
        st.markdown(f"""
        <div class="img-meta">
            <div class="img-meta-c"><div class="img-meta-v">{w}px</div><div class="img-meta-l">Largeur</div></div>
            <div class="img-meta-c"><div class="img-meta-v">{h}px</div><div class="img-meta-l">Hauteur</div></div>
            <div class="img-meta-c"><div class="img-meta-v">{size_kb} Ko</div><div class="img-meta-l">Taille</div></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if not api_ok:
            st.error("⚠️ L'API est hors ligne. Vérifiez le service Render.")
        else:
            if st.button("🔬 Analyser l'image avec l'IA"):
                with st.spinner("Analyse en cours — EfficientNetB0..."):
                    t0 = time.time()
                    ok, resp = call_api(uploaded.getvalue(), use_gradcam)
                    elapsed = round(time.time() - t0, 2)
                if ok:
                    resp["_elapsed"]   = elapsed
                    resp["_filename"]  = uploaded.name
                    st.session_state["result"]   = resp
                    st.session_state["orig_img"] = image
                    st.session_state["img_bytes"] = uploaded.getvalue()
                    st.rerun()
                else:
                    st.error(f"❌ {resp.get('error', 'Erreur inconnue')}")
    else:
        st.markdown("""
        <div class="empty">
            <div class="empty-icon">🔬</div>
            <div class="empty-txt">Glissez une image ici ou cliquez pour parcourir</div>
            <div style="font-size:.7rem;color:#e2e8f0;">JPG · PNG · max 200 MB</div>
        </div>
        """, unsafe_allow_html=True)


# ── DROITE : Résultats ────────────────────────────────────────
with col_r:
    if "result" not in st.session_state:
        st.markdown("""
        <div class="empty" style="min-height:400px;">
            <div class="empty-icon">📊</div>
            <div class="empty-txt">Les résultats apparaîtront ici après l'analyse</div>
            <div style="font-size:.7rem;color:#e2e8f0;">Téléversez une image et lancez l'analyse</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        res       = st.session_state["result"]
        pred      = res.get("prediction", {})
        label     = pred.get("label", "—")
        conf      = pred.get("confidence_pct", 0)
        raw       = pred.get("raw_score", 0)
        probs     = pred.get("probabilities", {})
        elapsed   = res.get("_elapsed", "—")
        filename  = res.get("_filename", "image.jpg")
        gcam_b64  = res.get("gradcam_image")
        is_cancer = label.lower() == "cancer"

        # Résultat principal
        if is_cancer:
            st.markdown(f"""
            <div class="res-cancer">
                <span class="res-icon">⚠️</span>
                <div class="res-title-cancer">IDC Positif</div>
                <div class="res-desc">Carcinome canalaire invasif détecté</div>
                <div class="bar-bg"><div class="bar-cancer" style="width:{conf}%"></div></div>
                <div class="bar-pct">{conf:.1f}% de confiance</div>
                <div class="res-metrics">
                    <div class="res-m">
                        <div class="res-m-v" style="color:#dc2626;">{probs.get('Cancer',0):.1f}%</div>
                        <div class="res-m-l">P(Cancer)</div>
                    </div>
                    <div class="res-m">
                        <div class="res-m-v" style="color:#16a34a;">{probs.get('Negative',0):.1f}%</div>
                        <div class="res-m-l">P(Négatif)</div>
                    </div>
                    <div class="res-m">
                        <div class="res-m-v" style="color:#64748b;">{elapsed}s</div>
                        <div class="res-m-l">Inférence</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="res-negative">
                <span class="res-icon">✅</span>
                <div class="res-title-negative">IDC Négatif</div>
                <div class="res-desc">Aucun signe de carcinome canalaire détecté</div>
                <div class="bar-bg"><div class="bar-negative" style="width:{conf}%"></div></div>
                <div class="bar-pct">{conf:.1f}% de confiance</div>
                <div class="res-metrics">
                    <div class="res-m">
                        <div class="res-m-v" style="color:#dc2626;">{probs.get('Cancer',0):.1f}%</div>
                        <div class="res-m-l">P(Cancer)</div>
                    </div>
                    <div class="res-m">
                        <div class="res-m-v" style="color:#16a34a;">{probs.get('Negative',0):.1f}%</div>
                        <div class="res-m-l">P(Négatif)</div>
                    </div>
                    <div class="res-m">
                        <div class="res-m-v" style="color:#64748b;">{elapsed}s</div>
                        <div class="res-m-l">Inférence</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Score brut
        st.markdown(f"""
        <div class="score-row">
            <span class="score-lbl">Score brut (sigmoid)</span>
            <span class="score-val">{raw:.6f}</span>
        </div>
        """, unsafe_allow_html=True)

        # ── BOUTONS TÉLÉCHARGEMENT ────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="card"><div class="card-hd">💾 Sauvegarder & Exporter</div>', unsafe_allow_html=True)

        dl1, dl2 = st.columns(2)

        # Sauvegarder l'image dans le bon dossier
        img_obj = st.session_state.get("orig_img")
        if img_obj:
            folder  = "Cancer" if is_cancer else "Negative"
            ts      = datetime.now().strftime("%Y%m%d_%H%M%S")
            img_fn  = f"{folder}_{ts}.png"
            img_dl  = img_to_bytes(img_obj)
            with dl1:
                st.download_button(
                    label=f"📁 Sauvegarder ({folder})",
                    data=img_dl,
                    file_name=img_fn,
                    mime="image/png",
                    use_container_width=True,
                )

        # Export rapport HTML/PDF
        pdf_bytes = generate_pdf_report(
            label, conf, raw, probs, elapsed, filename, gcam_b64
        )
        pdf_fn = f"rapport_cancerscan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with dl2:
            st.download_button(
                label="📄 Exporter rapport PDF",
                data=pdf_bytes,
                file_name=pdf_fn,
                mime="text/html",
                use_container_width=True,
            )

        st.markdown("""
        <p style="font-size:.68rem;color:#94a3b8;margin-top:.5rem;">
            💡 L'image est sauvegardée dans le dossier correspondant au résultat.
            Le rapport s'ouvre dans le navigateur — utilisez Fichier → Imprimer → Enregistrer en PDF.
        </p>
        </div>
        """, unsafe_allow_html=True)

        # ── GRAD-CAM ──────────────────────────────────────────
        if use_gradcam and gcam_b64:
            st.markdown("""
            <div class="gcam-hd">
                <span class="gcam-badge">Grad-CAM</span>
                <span class="gcam-title">Zones d'activation du modèle</span>
            </div>
            <div class="gcam-legend">
                🔴 <strong>Rouge/Orange</strong> — zones fortement activées, déterminantes pour la décision<br>
                🔵 <strong>Bleu/Vert</strong> — zones peu activées, faible contribution au résultat
            </div>
            """, unsafe_allow_html=True)

            g1, g2 = st.columns(2)
            with g1:
                st.image(
                    st.session_state["orig_img"].resize((224, 224)),
                    caption="Image originale",
                    use_column_width=True,
                )
            with g2:
                gcam_img = b64_to_pil(gcam_b64)
                st.image(gcam_img, caption="Heatmap Grad-CAM", use_column_width=True)

                # Téléchargement heatmap
                gcam_bytes = img_to_bytes(gcam_img)
                st.download_button(
                    "⬇ Télécharger Grad-CAM",
                    data=gcam_bytes,
                    file_name=f"gradcam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
                    mime="image/png",
                    use_container_width=True,
                )

        # Alerte médicale
        st.markdown("""
        <div class="med-alert">
            ⚕️ <strong>Avertissement clinique</strong> — Ce système est un outil de recherche
            pédagogique (Deep Learning, Université de Thiès, 2025-2026). Il ne constitue pas
            un dispositif médical certifié et ne remplace en aucun cas le diagnostic d'un médecin
            anatomopathologiste qualifié.
        </div>
        """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# GUIDE D'UTILISATION
# ════════════════════════════════════════════════════════════════
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="card">
    <div class="card-hd">📖 Comment utiliser l'application ?</div>
    <div class="how-grid">
        <div class="how-step">
            <div class="how-n">1</div>
            <div class="how-t">Téléverser</div>
            <div class="how-d">Chargez une image histologique JPG/PNG du tissu mammaire.</div>
        </div>
        <div class="how-step">
            <div class="how-n">2</div>
            <div class="how-t">Vérifier</div>
            <div class="how-d">Confirmez que l'API affiche ✅ Connectée dans la barre latérale.</div>
        </div>
        <div class="how-step">
            <div class="how-n">3</div>
            <div class="how-t">Analyser</div>
            <div class="how-d">Lancez l'analyse — l'IA prédit la classe en quelques secondes.</div>
        </div>
        <div class="how-step">
            <div class="how-n">4</div>
            <div class="how-t">Exporter</div>
            <div class="how-d">Sauvegardez l'image et exportez le rapport complet en PDF.</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
    Université de Thiès · UFR SET · Département Informatique · MaRT2 · Deep Learning 2025-2026<br>
    Pr. Cheikh SARR · Ibrahima MBAYE & Thiecoura NDIAYE
</div>
""", unsafe_allow_html=True)