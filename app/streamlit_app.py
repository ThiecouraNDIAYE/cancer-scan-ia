# =============================================================
# CancerScan IA — Version Premium (UI/UX + Dashboard + PDF)
# =============================================================

import os
import io
import base64
import requests
import datetime as dt
import streamlit as st
from PIL import Image
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet

# -------------------- CONFIG --------------------
st.set_page_config(page_title="CancerScan IA", page_icon="🔬", layout="centered")

API_URL = os.getenv("API_URL", "https://cancer-scan-ia.onrender.com")

if "loading" not in st.session_state:
    st.session_state["loading"] = False
if "history" not in st.session_state:
    st.session_state["history"] = []  # liste de dicts {date, label, conf}

# -------------------- STYLE --------------------
st.markdown("""
<style>
/* Typography */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=DM+Serif+Display&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Header */
.header {
    text-align:center;
    margin-bottom: 1.5rem;
}
.title {
    font-family: 'DM Serif Display', serif;
    font-size: 2.4rem;
    color: #6366f1;
    margin-bottom: .2rem;
}
.subtitle {
    color:#94a3b8;
    font-size:.9rem;
}

/* Card */
.card {
    background: rgba(17, 24, 39, .6);
    backdrop-filter: blur(8px);
    border: 1px solid #1f2937;
    border-radius: 16px;
    padding: 1.2rem;
}

/* Result */
.result-pos { background: linear-gradient(135deg,#2b0c0c,#3b1111); border:1px solid #ef4444; }
.result-neg { background: linear-gradient(135deg,#071612,#0e2a22); border:1px solid #10b981; }
.result {
    border-radius: 14px;
    padding: 1.2rem;
    text-align:center;
}
.res-title { font-family:'DM Serif Display', serif; font-size:1.5rem; }
.res-sub { font-size:.85rem; color:#94a3b8; }

/* Small */
.muted { color:#64748b; font-size:.8rem; }
</style>
""", unsafe_allow_html=True)

# -------------------- HELPERS --------------------
def call_api(image_bytes, gradcam=False):
    endpoint = "/predict/gradcam" if gradcam else "/predict"
    try:
        r = requests.post(
            f"{API_URL}{endpoint}",
            files={"file": ("img.jpg", image_bytes, "image/jpeg")},
            timeout=120,
        )
        r.raise_for_status()
        return True, r.json()
    except Exception as e:
        return False, {"error": str(e)}

def b64_to_pil(b64):
    return Image.open(io.BytesIO(base64.b64decode(b64)))

def make_pdf(image: Image.Image, label: str, conf: float, probs: dict) -> bytes:
    """Génère un PDF simple (reportlab)"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elems = []

    elems.append(Paragraph("CancerScan IA — Rapport", styles["Title"]))
    elems.append(Spacer(1, 10))
    elems.append(Paragraph(f"Date: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}", styles["Normal"]))
    elems.append(Spacer(1, 10))
    elems.append(Paragraph(f"Résultat: {label} — Confiance: {conf:.1f}%", styles["Heading2"]))
    elems.append(Spacer(1, 10))
    elems.append(Paragraph(
        f"P(Cancer): {probs.get('Cancer',0):.1f}% | P(Négatif): {probs.get('Negative',0):.1f}%",
        styles["Normal"]
    ))
    elems.append(Spacer(1, 14))

    # Image
    img_buf = io.BytesIO()
    image.save(img_buf, format="PNG")
    img_buf.seek(0)
    elems.append(RLImage(img_buf, width=300, height=300))

    doc.build(elems)
    buffer.seek(0)
    return buffer.read()

# -------------------- HEADER --------------------
st.markdown("""
<div class="header">
  <div class="title">🔬 CancerScan IA</div>
  <div class="subtitle">Détection du carcinome canalaire invasif (IDC) — EfficientNetB0</div>
</div>
""", unsafe_allow_html=True)

# -------------------- CONTROLS --------------------
colA, colB = st.columns([1,1])
with colA:
    uploaded = st.file_uploader("📤 Charger une image", type=["jpg","jpeg","png"], label_visibility="visible")
with colB:
    use_gradcam = st.toggle("Afficher Grad-CAM", value=True)

# -------------------- UPLOAD VIEW --------------------
if uploaded:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, use_column_width=True, caption="Image chargée")
    st.info("💡 Astuce : image nette = meilleure précision")

    analyze = st.button("🚀 Lancer l’analyse", use_container_width=True)

    if analyze and not st.session_state["loading"]:
        st.session_state["loading"] = True

        with st.spinner("🧠 Analyse en cours..."):
            ok, res = call_api(uploaded.getvalue(), gradcam=use_gradcam)

        st.session_state["loading"] = False

        if not ok:
            st.error("❌ Erreur API")
            st.code(res.get("error",""))
        else:
            pred = res.get("prediction", {})
            label = pred.get("label","")
            conf  = pred.get("confidence_pct",0)
            probs = pred.get("probabilities",{})

            # Save history
            st.session_state["history"].append({
                "date": dt.datetime.now().strftime("%H:%M:%S"),
                "label": label,
                "conf": conf
            })

            st.markdown("---")

            # RESULT CARD
            if label.lower() == "cancer":
                st.markdown(f"""
                <div class="result result-pos">
                  <div class="res-title">⚠️ Cancer détecté</div>
                  <div class="res-sub">{conf:.1f}% de confiance</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="result result-neg">
                  <div class="res-title">✅ Aucun cancer détecté</div>
                  <div class="res-sub">{conf:.1f}% de confiance</div>
                </div>
                """, unsafe_allow_html=True)

            # Confidence bar
            st.markdown("#### 📈 Confiance")
            st.progress(min(max(conf/100, 0.0), 1.0))

            # Details
            st.markdown("#### 📊 Détails")
            st.write({
                "Cancer (%)": round(probs.get("Cancer", 0), 2),
                "Négatif (%)": round(probs.get("Negative", 0), 2)
            })

            # Grad-CAM
            gcam = res.get("gradcam_image")
            if use_gradcam and gcam:
                with st.expander("🧠 Visualiser Grad-CAM"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.image(image, caption="Original", use_column_width=True)
                    with c2:
                        st.image(b64_to_pil(gcam), caption="Grad-CAM", use_column_width=True)

            # Export PDF
            pdf_bytes = make_pdf(image, label, conf, probs)
            st.download_button(
                "📄 Télécharger le rapport PDF",
                data=pdf_bytes,
                file_name="cancerscan_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# -------------------- DASHBOARD --------------------
st.markdown("---")
st.markdown("### 📊 Historique des analyses")

if not st.session_state["history"]:
    st.info("Aucune analyse pour le moment")
else:
    # simple stats
    total = len(st.session_state["history"])
    cancers = sum(1 for x in st.session_state["history"] if x["label"].lower()=="cancer")
    negs = total - cancers

    m1, m2, m3 = st.columns(3)
    m1.metric("Total", total)
    m2.metric("Cancer", cancers)
    m3.metric("Négatif", negs)

    # table
    st.dataframe(st.session_state["history"], use_container_width=True)

# -------------------- FOOTER --------------------
st.markdown("---")
st.caption("🚀 Deep Learning • EfficientNetB0 • Streamlit • Version Premium")