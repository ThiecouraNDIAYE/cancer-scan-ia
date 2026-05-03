# =============================================================
# CancerScan IA — Interface Streamlit (VERSION PRO STABLE)
# =============================================================

import os
import io
import base64
import requests
import streamlit as st
from PIL import Image

# ================= PDF SAFE =================
try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
    from reportlab.lib.styles import getSampleStyleSheet
    PDF_AVAILABLE = True
except:
    PDF_AVAILABLE = False

# ================= CONFIG =================
st.set_page_config(
    page_title="CancerScan IA",
    page_icon="🔬",
    layout="centered"
)

API_URL = os.getenv("API_URL", "https://cancer-scan-ia.onrender.com")

if "loading" not in st.session_state:
    st.session_state["loading"] = False

# ================= STYLE =================
st.markdown("""
<style>
.title {text-align:center;font-size:2.5rem;font-weight:bold;color:#6366f1;}
.subtitle {text-align:center;color:#94a3b8;margin-bottom:2rem;}
.result-box {padding:20px;border-radius:12px;text-align:center;}
.pos {background:#2b0c0c;color:#ff6b6b;}
.neg {background:#062d1a;color:#34d399;}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
st.markdown('<div class="title">🔬 CancerScan IA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Détection du cancer du sein avec Deep Learning</div>', unsafe_allow_html=True)

# ================= FUNCTIONS =================
def call_api(image_bytes):
    try:
        r = requests.post(
            f"{API_URL}/predict",
            files={"file": ("img.jpg", image_bytes)},
            timeout=60
        )
        r.raise_for_status()
        return True, r.json()
    except Exception as e:
        return False, {"error": str(e)}

def b64_to_pil(b64):
    return Image.open(io.BytesIO(base64.b64decode(b64)))

def make_pdf(image, label, conf, probs):
    if not PDF_AVAILABLE:
        return None

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("CancerScan IA - Rapport", styles["Title"]))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"Résultat : {label}", styles["Heading2"]))
    elements.append(Paragraph(f"Confiance : {conf:.1f}%", styles["Normal"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        f"P(Cancer) : {probs.get('Cancer',0):.1f}%<br/>"
        f"P(Négatif) : {probs.get('Negative',0):.1f}%",
        styles["Normal"]
    ))

    elements.append(Spacer(1, 15))

    img_buf = io.BytesIO()
    image.save(img_buf, format="PNG")
    img_buf.seek(0)

    elements.append(RLImage(img_buf, width=250, height=250))

    doc.build(elements)
    buffer.seek(0)

    return buffer

# ================= UPLOAD =================
uploaded = st.file_uploader("📤 Charger une image", type=["jpg", "png", "jpeg"])

if uploaded:
    image = Image.open(uploaded).convert("RGB")
    st.image(image, use_column_width=True)

    st.info("💡 Utilisez une image nette pour de meilleurs résultats")

    # DOWNLOAD IMAGE
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")

    st.download_button(
        "📥 Télécharger l'image",
        data=img_bytes.getvalue(),
        file_name="image.png",
        mime="image/png",
        use_container_width=True
    )

    # ANALYSE
    analyze = st.button("🚀 Lancer l'analyse", use_container_width=True)

    if analyze and not st.session_state["loading"]:
        st.session_state["loading"] = True

        with st.spinner("🧠 Analyse en cours..."):
            ok, res = call_api(uploaded.getvalue())

        st.session_state["loading"] = False

        if not ok:
            st.error("❌ Erreur API")
            st.code(res.get("error"))
        else:
            pred = res.get("prediction", {})
            label = pred.get("label", "")
            conf = pred.get("confidence_pct", 0)
            probs = pred.get("probabilities", {})

            st.markdown("---")

            # RESULTAT
            if label.lower() == "cancer":
                st.markdown(
                    f'<div class="result-box pos">⚠️ Cancer détecté<br>{conf:.1f}%</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="result-box neg">✅ Aucun cancer détecté<br>{conf:.1f}%</div>',
                    unsafe_allow_html=True
                )

            # BARRE
            st.progress(conf / 100)

            # DETAILS
            st.subheader("📊 Détails")
            st.write({
                "Cancer (%)": round(probs.get("Cancer", 0), 2),
                "Négatif (%)": round(probs.get("Negative", 0), 2)
            })

            # GRADCAM
            if "gradcam_image" in res:
                with st.expander("🧠 Grad-CAM"):
                    st.image(b64_to_pil(res["gradcam_image"]))

            # PDF EXPORT
            pdf_buffer = make_pdf(image, label, conf, probs)

            if PDF_AVAILABLE and pdf_buffer:
                st.download_button(
                    "📄 Télécharger rapport PDF",
                    data=pdf_buffer,
                    file_name="rapport.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            else:
                st.warning("⚠️ PDF indisponible (installer reportlab)")

# ================= FOOTER =================
st.markdown("---")
st.caption("🚀 Deep Learning • EfficientNetB0 • Streamlit")