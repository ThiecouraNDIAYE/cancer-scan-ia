# =============================================================
# Interface Streamlit — CancerScan IA
# Classification du Cancer du Sein
# Université de Thiès — MaRT2 — 2025-2026
# =============================================================

import os
import io
import base64
import requests
import streamlit as st
from PIL import Image

# =============================================================
# Configuration de la page
# =============================================================
st.set_page_config(
    page_title="CancerScan IA",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = os.getenv("API_URL", "https://cancer-scan-ia.onrender.com")

# =============================================================
# CSS
# =============================================================
st.markdown("""
<style>
/* ── Typographie ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=DM+Serif+Display:ital@0;1&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── Header ── */
.hero {
    background: linear-gradient(135deg, #0c0f1a 0%, #131929 60%, #0c0f1a 100%);
    border: 1px solid #1e2d45;
    border-radius: 16px;
    padding: 2.5rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::after {
    content: '';
    position: absolute;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 50% at 20% 50%, rgba(99,102,241,.07) 0%, transparent 70%),
        radial-gradient(ellipse 50% 40% at 80% 50%, rgba(16,185,129,.05) 0%, transparent 70%);
    pointer-events: none;
}
.hero-chip {
    display: inline-block;
    background: rgba(99,102,241,.12);
    color: #818cf8;
    border: 1px solid rgba(99,102,241,.25);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: .05em;
    margin-bottom: .8rem;
}
.hero h1 {
    font-family: 'DM Serif Display', serif;
    font-size: 2.2rem;
    color: #f1f5f9;
    margin: 0 0 .4rem;
}
.hero p { color: #94a3b8; font-size: .9rem; font-weight: 300; margin: 0; }

/* ── Cartes résultat ── */
.card-cancer {
    background: linear-gradient(135deg,#1a0a0a,#2d1515);
    border: 1px solid #ef4444;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
}
.card-negative {
    background: linear-gradient(135deg,#071612,#0d2820);
    border: 1px solid #10b981;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
}
.result-emoji  { font-size: 2.8rem; margin-bottom: .4rem; }
.result-title  {
    font-family: 'DM Serif Display', serif;
    font-size: 1.7rem;
    margin-bottom: .3rem;
}
.result-sub    { font-size: .8rem; color: #94a3b8; font-weight: 300; }

/* ── Barre de confiance ── */
.bar-bg {
    background: #1e293b;
    border-radius: 8px;
    height: 10px;
    margin: .9rem 0 .3rem;
    overflow: hidden;
}
.bar-fill-cancer   { height: 100%; background: linear-gradient(90deg,#ef4444,#dc2626); border-radius: 8px; }
.bar-fill-negative { height: 100%; background: linear-gradient(90deg,#10b981,#059669); border-radius: 8px; }

/* ── Mini métriques ── */
.metric {
    background: #1e293b;
    border: 1px solid #2d3f56;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}
.metric-lbl { font-size: 10px; text-transform: uppercase; letter-spacing: .08em; color: #64748b; margin-bottom: .4rem; }
.metric-val { font-family: 'DM Serif Display', serif; font-size: 1.5rem; color: #e2e8f0; }

/* ── Alertes ── */
.alert-warn {
    background: rgba(234,179,8,.07);
    border: 1px solid rgba(234,179,8,.25);
    border-radius: 10px;
    padding: .9rem 1.1rem;
    color: #fbbf24;
    font-size: .82rem;
    margin-top: 1.2rem;
    line-height: 1.6;
}
.alert-info {
    background: rgba(99,102,241,.07);
    border: 1px solid rgba(99,102,241,.2);
    border-radius: 10px;
    padding: .9rem 1.1rem;
    color: #a5b4fc;
    font-size: .82rem;
    margin-bottom: .9rem;
    line-height: 1.6;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] { background: #0c0f1a !important; }
.sb-card {
    background: #131929;
    border: 1px solid #1e2d45;
    border-radius: 10px;
    padding: .9rem;
    margin-bottom: .8rem;
}
.sb-title { font-size: 10px; text-transform: uppercase; letter-spacing: .1em; color: #475569; font-weight: 600; margin-bottom: .6rem; }

/* ── Bouton ── */
.stButton > button {
    background: linear-gradient(135deg,#4f46e5,#6d28d9) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    width: 100% !important;
    padding: .55rem 0 !important;
}
.stButton > button:hover { opacity: .88 !important; }

/* ── Empty state ── */
.empty-state {
    background: #131929;
    border: 2px dashed #1e2d45;
    border-radius: 14px;
    padding: 3rem 1rem;
    text-align: center;
    color: #475569;
}

/* ── Steps bas de page ── */
.step-card {
    background: #131929;
    border: 1px solid #1e2d45;
    border-radius: 10px;
    padding: .9rem;
    display: flex;
    gap: .7rem;
    align-items: flex-start;
}
.step-num {
    background: #1e1b4b;
    color: #a5b4fc;
    width: 26px; height: 26px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 600; flex-shrink: 0;
}
</style>
""", unsafe_allow_html=True)


# =============================================================
# Fonctions
# =============================================================

@st.cache_data(ttl=10)
def api_health():
    try:
        r = requests.get(f"{API_URL}/health", timeout=5)
        if r.status_code == 200:
            return True, r.json()
    except Exception:
        pass
    return False, {}


def call_api(image_bytes: bytes, gradcam: bool) -> tuple[bool, dict]:
    endpoint = "/predict/gradcam" if gradcam else "/predict"
    try:
        r = requests.post(
            f"{API_URL}{endpoint}",
            files={"file": ("image.jpg", image_bytes, "image/jpeg")},
            timeout=60,
        )
        r.raise_for_status()
        return True, r.json()
    except requests.exceptions.ConnectionError:
        return False, {"error": "Impossible de joindre l'API. Lancez start_api.bat d'abord."}
    except requests.exceptions.Timeout:
        return False, {"error": "L'API met trop de temps (timeout 60s). Modèle trop lourd ?"}
    except Exception as e:
        return False, {"error": str(e)}


def b64_to_pil(b64: str) -> Image.Image:
    return Image.open(io.BytesIO(base64.b64decode(b64)))


# =============================================================
# Sidebar
# =============================================================
with st.sidebar:
    st.markdown(
        '<p style="font-family:DM Serif Display,serif;font-size:1.3rem;'
        'color:#e2e8f0;margin-bottom:1.2rem;">⚙️ Paramètres</p>',
        unsafe_allow_html=True,
    )

    api_ok, api_info = api_health()
    s_col, s_txt = ("#10b981", "✅ Connectée") if api_ok else ("#ef4444", "❌ Hors ligne")
    st.markdown(f"""
    <div class="sb-card">
        <div class="sb-title">Statut API</div>
        <div style="color:{s_col};font-size:.88rem;font-weight:500;">{s_txt}</div>
        <div style="color:#475569;font-size:.76rem;margin-top:3px;">{API_URL}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sb-card"><div class="sb-title">Options</div>', unsafe_allow_html=True)
    use_gradcam = st.checkbox("Afficher Grad-CAM", value=True,
                              help="Carte de chaleur montrant les zones analysées par le modèle.")
    st.markdown('</div>', unsafe_allow_html=True)

    if api_ok:
        th = api_info.get("threshold", 0.5)
        cls = api_info.get("class_labels", {})
        st.markdown(f"""
        <div class="sb-card">
            <div class="sb-title">Modèle</div>
            <div style="color:#94a3b8;font-size:.8rem;line-height:1.9;">
                🏗️ EfficientNetB0<br>
                🎯 Seuil : {th}<br>
                📦 Classe 0 : {cls.get('0','Cancer')}<br>
                📦 Classe 1 : {cls.get('1','Negative')}<br>
                🔢 TF : {api_info.get('tf_version','—')}
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class="sb-card">
        <div class="sb-title">Projet</div>
        <div style="color:#475569;font-size:.78rem;line-height:1.8;">
            Université de Thiès<br>UFR SET · MaRT2<br>
            Deep Learning 2025-2026<br>Pr. Cheikh SARR
        </div>
    </div>""", unsafe_allow_html=True)


# =============================================================
# Hero
# =============================================================
st.markdown("""
<div class="hero">
    <div class="hero-chip">🔬 Deep Learning · Images histologiques · IDC</div>
    <h1>CancerScan IA</h1>
    <p>Détection du carcinome canalaire invasif (IDC) — EfficientNetB0 fine-tuné + Grad-CAM</p>
</div>
""", unsafe_allow_html=True)


# =============================================================
# Colonnes principales
# =============================================================
col_left, col_right = st.columns([1, 1], gap="large")

# ── Colonne gauche : upload ───────────────────────────────────
with col_left:
    st.markdown("#### 📤 Image histologique")
    st.markdown("""
    <div class="alert-info">
        Téléversez une image histologique du tissu mammaire (JPG ou PNG).
        Le modèle prédit la présence ou l'absence d'IDC (carcinome canalaire invasif).
    </div>""", unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Choisir une image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, use_column_width=True, caption="Image chargée")

        # Infos rapides
        c1, c2, c3 = st.columns(3)
        for col_m, lbl, val in zip(
            [c1, c2, c3],
            ["Largeur", "Hauteur", "Taille"],
            [f"{image.size[0]}px", f"{image.size[1]}px", f"{len(uploaded.getvalue())//1024} Ko"],
        ):
            with col_m:
                st.markdown(
                    f'<div class="metric"><div class="metric-lbl">{lbl}</div>'
                    f'<div class="metric-val" style="font-size:1.1rem">{val}</div></div>',
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)

        if not api_ok:
            st.error("❌ L'API n'est pas disponible. Lancez **start_api.bat** dans un terminal séparé.")
        else:
            if st.button("🔬 Analyser l'image"):
                with st.spinner("Analyse en cours — EfficientNetB0..."):
                    ok, resp = call_api(uploaded.getvalue(), gradcam=use_gradcam)

                if ok:
                    st.session_state["result"] = resp
                    st.session_state["orig_img"] = image
                    st.success("✅ Analyse terminée !")
                else:
                    st.error(f"❌ {resp.get('error', 'Erreur inconnue')}")


# ── Colonne droite : résultats ────────────────────────────────
with col_right:
    st.markdown("#### 📊 Résultat de l'analyse")

    if "result" not in st.session_state:
        st.markdown("""
        <div class="empty-state">
            <div style="font-size:3rem;margin-bottom:.8rem;">🔬</div>
            <p style="margin:0;font-size:.9rem;">
                Les résultats s'afficheront ici<br>après l'analyse.
            </p>
        </div>""", unsafe_allow_html=True)

    else:
        res   = st.session_state["result"]
        pred  = res.get("prediction", {})
        cid   = pred.get("class_id", 0)
        label = pred.get("label", "—")
        conf  = pred.get("confidence_pct", 0)
        raw   = pred.get("raw_score", 0)
        probs = pred.get("probabilities", {})

        is_cancer = (label.lower() == "cancer")

        if is_cancer:
            st.markdown(f"""
            <div class="card-cancer">
                <div class="result-emoji">⚠️</div>
                <div class="result-title" style="color:#fca5a5;">IDC Positif</div>
                <div class="result-sub">Carcinome canalaire invasif détecté</div>
                <div class="bar-bg">
                    <div class="bar-fill-cancer" style="width:{conf}%"></div>
                </div>
                <div style="color:#fca5a5;font-size:.85rem;font-weight:500;">{conf:.1f}% de confiance</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="card-negative">
                <div class="result-emoji">✅</div>
                <div class="result-title" style="color:#6ee7b7;">IDC Négatif</div>
                <div class="result-sub">Aucun signe de carcinome canalaire invasif</div>
                <div class="bar-bg">
                    <div class="bar-fill-negative" style="width:{conf}%"></div>
                </div>
                <div style="color:#6ee7b7;font-size:.85rem;font-weight:500;">{conf:.1f}% de confiance</div>
            </div>""", unsafe_allow_html=True)

        # Métriques
        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        metrics = [
            ("Score brut", f"{raw:.4f}", "#e2e8f0"),
            ("P(Cancer)",  f"{probs.get('Cancer',0):.1f}%", "#fca5a5"),
            ("P(Négatif)", f"{probs.get('Negative',0):.1f}%", "#6ee7b7"),
        ]
        for col_m, (lbl, val, color) in zip([m1, m2, m3], metrics):
            with col_m:
                st.markdown(
                    f'<div class="metric"><div class="metric-lbl">{lbl}</div>'
                    f'<div class="metric-val" style="color:{color}">{val}</div></div>',
                    unsafe_allow_html=True,
                )

        # Grad-CAM
        gcam = res.get("gradcam_image")    
        if use_gradcam and gcam:
            st.markdown("#### 🗺️ Visualisation Grad-CAM")
            st.markdown("""
            <div class="alert-info" style="margin-bottom:.7rem;">
                Les zones <strong style="color:#ef4444">chaudes (rouge/orange)</strong>
                indiquent les régions cellulaires décisives pour la prédiction du modèle.
            </div>""", unsafe_allow_html=True)

            g1, g2 = st.columns(2)
            with g1:
                st.image(
                    st.session_state["orig_img"].resize((224, 224)),
                    caption="Image originale",
                    use_column_width=True,
                )
            with g2:
                st.image(
                    b64_to_pil(gcam),
                    caption="Grad-CAM (zones analysées)",
                    use_column_width=True,
                )
        elif use_gradcam and not res.get("gradcam_available", False):
            st.info("ℹ️ Grad-CAM non disponible pour ce modèle.")

        # Avertissement médical
        st.markdown("""
        <div class="alert-warn">
            ⚠️ <strong>Avertissement :</strong> Ce système est un outil de recherche pédagogique.
            Il ne constitue pas un dispositif médical certifié et ne remplace en aucun cas
            un diagnostic médical professionnel. Consultez toujours un médecin spécialiste.
        </div>""", unsafe_allow_html=True)


# =============================================================
# Guide en bas de page
# =============================================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("#### 📖 Comment utiliser l'application ?")

steps = [
    ("1", "Téléverser",  "Chargez une image histologique du tissu mammaire (JPG/PNG)."),
    ("2", "Vérifier",    "Assurez-vous que le statut API affiche ✅ dans la barre latérale."),
    ("3", "Analyser",    "Cliquez sur 'Analyser l'image' pour lancer la prédiction IA."),
    ("4", "Interpréter", "Lisez le résultat, la confiance et la heatmap Grad-CAM."),
]
cols = st.columns(4)
for col_s, (n, title, desc) in zip(cols, steps):
    with col_s:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-num">{n}</div>
            <div>
                <div style="color:#e2e8f0;font-weight:500;font-size:.85rem;margin-bottom:.25rem;">{title}</div>
                <div style="color:#475569;font-size:.78rem;line-height:1.5;">{desc}</div>
            </div>
        </div>""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;color:#1e2d45;font-size:.76rem;margin-top:2rem;padding:1rem;">
    Université de Thiès · UFR SET · Département Informatique · MaRT2 · Pr. Cheikh SARR · 2025-2026
</div>""", unsafe_allow_html=True)
