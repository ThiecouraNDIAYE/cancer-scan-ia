# =============================================================
# Interface Streamlit — CancerScan IA (Version améliorée)
# =============================================================

import os
import io
import base64
import requests
import streamlit as st
from PIL import Image

# =============================================================
# CONFIG
# =============================================================
st.set_page_config(
    page_title="CancerScan IA",
    page_icon="🔬",
    layout="wide",
)

API_URL = os.getenv("API_URL", "https://cancer-scan-ia.onrender.com")

if "loading" not in st.session_state:
    st.session_state["loading"] = False

# =============================================================
# FONCTIONS
# =============================================================
@st.cache_data(ttl=10)
def api_health():
    try:
        r = requests.get(f"{API_URL}/health", timeout=5)
        if r.status_code == 200:
            return True, r.json()
        return False, {"error": f"Status {r.status_code}"}
    except Exception as e:
        return False, {"error": str(e)}


def call_api(image_bytes, gradcam):
    endpoint = "/predict/gradcam" if gradcam else "/predict"
    try:
        r = requests.post(
            f"{API_URL}{endpoint}",
            files={"file": ("image.jpg", image_bytes, "image/jpeg")},
            timeout=120,
        )
        r.raise_for_status()
        return True, r.json()
    except Exception as e:
        return False, {"error": str(e)}


def b64_to_pil(b64):
    return Image.open(io.BytesIO(base64.b64decode(b64)))


# =============================================================
# SIDEBAR
# =============================================================
with st.sidebar:
    st.title("⚙️ Paramètres")

    api_ok, api_info = api_health()

    if api_ok:
        st.success("API connectée")
    else:
        st.error("API hors ligne")

    use_gradcam = st.checkbox("Afficher Grad-CAM", value=True)

# =============================================================
# HEADER
# =============================================================
st.title("🔬 CancerScan IA")
st.caption("Détection du cancer du sein avec Deep Learning")

# =============================================================
# LAYOUT
# =============================================================
col1, col2 = st.columns(2)

# =============================================================
# UPLOAD
# =============================================================
with col1:
    st.subheader("📤 Upload image")

    uploaded = st.file_uploader("Choisir une image", type=["jpg", "png", "jpeg"])

    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, use_column_width=True)

        st.info("💡 Utilisez une image nette pour de meilleurs résultats")

        analyze = st.button("🔬 Analyser", use_container_width=True)

        if analyze and not st.session_state["loading"]:
            st.session_state["loading"] = True

            with st.spinner("🧠 Analyse en cours..."):
                ok, resp = call_api(uploaded.getvalue(), use_gradcam)

            st.session_state["loading"] = False

            if ok:
                st.session_state["result"] = resp
                st.session_state["image"] = image
            else:
                st.error("Erreur API")
                st.code(resp.get("error"))

# =============================================================
# RESULTATS
# =============================================================
with col2:
    st.subheader("📊 Résultat")

    if "result" not in st.session_state:
        st.info("Les résultats apparaîtront ici")
    else:
        res = st.session_state["result"]
        pred = res.get("prediction", {})

        label = pred.get("label", "")
        conf = pred.get("confidence_pct", 0)
        probs = pred.get("probabilities", {})

        st.markdown("---")

        # RESULTAT PRINCIPAL
        if label.lower() == "cancer":
            st.error("⚠️ Cancer détecté")
        else:
            st.success("✅ Aucun cancer détecté")

        # BARRE DE CONFIANCE
        st.markdown("#### 📈 Confiance")
        st.progress(conf / 100)

        # DETAILS
        st.write({
            "Cancer (%)": round(probs.get("Cancer", 0), 2),
            "Négatif (%)": round(probs.get("Negative", 0), 2)
        })

        # GRADCAM
        gcam = res.get("gradcam_image")

        if use_gradcam and gcam:
            with st.expander("🧠 Voir Grad-CAM"):
                colA, colB = st.columns(2)

                with colA:
                    st.image(st.session_state["image"], caption="Image originale")

                with colB:
                    st.image(b64_to_pil(gcam), caption="Grad-CAM")

# =============================================================
# FOOTER
# =============================================================
st.markdown("---")
st.caption("🚀 Powered by Deep Learning • EfficientNetB0 • Streamlit")