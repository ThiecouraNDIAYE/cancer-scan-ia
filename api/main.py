# =============================================================
# API FastAPI — CancerScan IA
# Classification du Cancer du Sein — EfficientNetB0
# Université de Thiès — MaRT2 — 2025-2026
# =============================================================

import os
import io
import pickle
import base64
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.applications.efficientnet import preprocess_input
from PIL import Image
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

MODEL_PATH  = os.getenv("MODEL_PATH",  "models/model_clean.h5")
PARAMS_PATH = os.getenv("PARAMS_PATH", "models/preprocessing_params.pkl")

DEFAULT_CONFIG = {
    "target_size"  : (224, 224),
    "threshold"    : 0.5,
    "class_indices": {"Cancer": 0, "Negative": 1},
}

app = FastAPI(
    title="CancerScan IA — API",
    description="API de classification d'images histologiques du cancer du sein.\n\n**⚠️ Usage pédagogique uniquement.**",
    version="1.0.0",
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

model        = None
config       = DEFAULT_CONFIG.copy()
class_labels = {}


@app.on_event("startup")
async def startup():
    global model, config, class_labels

    # ── 1. Params de preprocessing ───────────────────────────
    if os.path.exists(PARAMS_PATH):
        try:
            with open(PARAMS_PATH, "rb") as f:
                saved = pickle.load(f)
            config.update(saved)
            print(f"✅ Params chargés : {PARAMS_PATH}")
            print(f"   class_indices  : {config.get('class_indices')}")
            print(f"   threshold      : {config.get('threshold')}")
        except Exception as e:
            print(f"⚠️  Params non chargés ({e}) — valeurs par défaut utilisées.")
    else:
        print(f"⚠️  {PARAMS_PATH} introuvable — valeurs par défaut utilisées.")

    class_labels = {v: k for k, v in config["class_indices"].items()}
    print(f"   class_labels   : {class_labels}")

    # ── 2. Chargement modèle — 5 tentatives ──────────────────
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Modèle introuvable : {MODEL_PATH}")
        models_dir = os.path.dirname(MODEL_PATH)
        if os.path.exists(models_dir):
            print("   Fichiers disponibles dans models/ :")
            for f in os.listdir(models_dir):
                print(f"   - {f}")
        model = None
        return

    # Tentative 1 : chargement normal
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        print(f"✅ Modèle chargé (normal) : {MODEL_PATH}")
        print(f"   Input shape : {model.input_shape}")
        return
    except Exception as e1:
        print(f"⚠️  Tentative 1 échouée : {e1}")

    # Tentative 2 : sans compilation
    try:
        model = tf.keras.models.load_model(MODEL_PATH, compile=False)
        print(f"✅ Modèle chargé (sans compilation) : {MODEL_PATH}")
        print(f"   Input shape : {model.input_shape}")
        return
    except Exception as e2:
        print(f"⚠️  Tentative 2 échouée : {e2}")

    # Tentative 3 : reconstruction + chargement des poids
    try:
        from tensorflow.keras.applications import EfficientNetB0
        from tensorflow.keras import layers, models as km
        print("⚙️  Tentative 3 : reconstruction architecture...")
        base   = EfficientNetB0(weights=None, include_top=False, input_shape=(224, 224, 3))
        x      = base.output
        x      = layers.GlobalAveragePooling2D()(x)
        x      = layers.BatchNormalization()(x)
        x      = layers.Dense(256, activation="relu")(x)
        x      = layers.Dropout(0.5)(x)
        output = layers.Dense(1, activation="sigmoid")(x)
        rebuilt = km.Model(inputs=base.input, outputs=output)
        rebuilt.load_weights(MODEL_PATH, by_name=False)
        model = rebuilt
        print(f"✅ Modèle reconstruit : {MODEL_PATH}")
        return
    except Exception as e3:
        print(f"⚠️  Tentative 3 échouée : {e3}")

    # Tentative 4 : essayer model_final.keras
    keras_path = os.path.join(os.path.dirname(MODEL_PATH), "model_final.keras")
    if os.path.exists(keras_path):
        try:
            model = tf.keras.models.load_model(keras_path, compile=False)
            print(f"✅ Modèle chargé depuis model_final.keras")
            return
        except Exception as e4:
            print(f"⚠️  Tentative 4 (.keras) échouée : {e4}")

    # Tentative 5 : essayer model.h5
    h5_path = os.path.join(os.path.dirname(MODEL_PATH), "model.h5")
    if os.path.exists(h5_path):
        try:
            model = tf.keras.models.load_model(h5_path, compile=False)
            print(f"✅ Modèle chargé depuis model.h5")
            return
        except Exception as e5:
            print(f"⚠️  Tentative 5 (model.h5) échouée : {e5}")

    print("❌ Toutes les tentatives ont échoué. Modèle non disponible.")
    model = None


# =============================================================
# Fonctions utilitaires
# =============================================================

def preprocess_image(image: Image.Image) -> np.ndarray:
    target = tuple(config["target_size"])
    img    = image.convert("RGB").resize(target)
    arr    = np.array(img, dtype=np.float32)
    arr    = np.expand_dims(arr, axis=0)
    arr    = preprocess_input(arr)
    return arr


def run_gradcam(img_array: np.ndarray, orig_img: Image.Image):
    conv_layer = None
    for name in ["top_conv", "top_activation", "block7a_project_conv"]:
        try:
            model.get_layer(name)
            conv_layer = name
            break
        except ValueError:
            continue

    if conv_layer is None:
        for layer in reversed(model.layers):
            if "conv" in layer.name.lower():
                conv_layer = layer.name
                break

    if conv_layer is None:
        return None

    try:
        grad_model   = tf.keras.models.Model(model.inputs, [model.get_layer(conv_layer).output, model.output])
        with tf.GradientTape() as tape:
            conv_output, preds = grad_model(img_array)
            class_channel      = preds[:, 0]
        grads        = tape.gradient(class_channel, conv_output)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        conv_output  = conv_output[0]
        heatmap      = conv_output @ pooled_grads[..., tf.newaxis]
        heatmap      = tf.squeeze(heatmap)
        heatmap      = tf.maximum(heatmap, 0)
        max_val      = tf.math.reduce_max(heatmap)
        if max_val > 0:
            heatmap = heatmap / max_val
        heatmap         = heatmap.numpy()
        img_np          = np.array(orig_img.resize((224, 224)))
        heatmap_resized = cv2.resize(heatmap, (224, 224))
        heatmap_uint8   = np.uint8(255 * heatmap_resized)
        heatmap_color   = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
        heatmap_color   = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)
        superposed      = cv2.addWeighted(img_np, 0.6, heatmap_color, 0.4, 0)
        buf = io.BytesIO()
        Image.fromarray(superposed.astype(np.uint8)).save(buf, format="PNG")
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")
    except Exception as e:
        print(f"⚠️  Grad-CAM échoué : {e}")
        return None


def build_prediction(raw_score: float) -> dict:
    threshold    = config["threshold"]
    predicted_id = 1 if raw_score > threshold else 0
    label        = class_labels.get(predicted_id, str(predicted_id))
    confidence   = raw_score if predicted_id == 1 else (1.0 - raw_score)
    return {
        "class_id"      : predicted_id,
        "label"         : label,
        "confidence_pct": round(confidence * 100, 2),
        "raw_score"     : round(float(raw_score), 4),
        "threshold"     : threshold,
        "probabilities" : {
            "Cancer"  : round((1.0 - raw_score) * 100, 2),
            "Negative": round(raw_score * 100, 2),
        },
    }


# =============================================================
# Routes
# =============================================================

@app.get("/", tags=["Général"])
def root():
    return {
        "service"      : "CancerScan IA — API",
        "version"      : "1.0.0",
        "model_loaded" : model is not None,
        "config"       : {"target_size": config["target_size"], "threshold": config["threshold"], "classes": class_labels},
        "endpoints"    : {"GET  /health": "Statut détaillé", "POST /predict": "Prédiction simple", "POST /predict/gradcam": "Prédiction + Grad-CAM"},
    }


@app.get("/health", tags=["Général"])
def health():
    return {
        "status"       : "ok" if model is not None else "degraded",
        "model_loaded" : model is not None,
        "model_path"   : MODEL_PATH,
        "params_path"  : PARAMS_PATH,
        "threshold"    : config["threshold"],
        "class_labels" : class_labels,
        "tf_version"   : tf.__version__,
    }


@app.post("/predict", tags=["Prédiction"])
async def predict(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(503, "Modèle non chargé. Vérifiez les logs de l'API.")
    if file.content_type not in ("image/jpeg", "image/jpg", "image/png"):
        raise HTTPException(400, f"Format non supporté : {file.content_type}.")
    try:
        contents   = await file.read()
        image      = Image.open(io.BytesIO(contents)).convert("RGB")
        img_array  = preprocess_image(image)
        raw_score  = float(model.predict(img_array, verbose=0)[0][0])
        prediction = build_prediction(raw_score)
        return JSONResponse({"success": True, "prediction": prediction, "warning": "Résultat à des fins de recherche uniquement."})
    except Exception as e:
        raise HTTPException(500, f"Erreur : {e}")


@app.post("/predict/gradcam", tags=["Prédiction"])
async def predict_gradcam(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(503, "Modèle non chargé.")
    if file.content_type not in ("image/jpeg", "image/jpg", "image/png"):
        raise HTTPException(400, f"Format non supporté : {file.content_type}.")
    try:
        contents   = await file.read()
        image      = Image.open(io.BytesIO(contents)).convert("RGB")
        img_array  = preprocess_image(image)
        raw_score  = float(model.predict(img_array, verbose=0)[0][0])
        prediction = build_prediction(raw_score)
        gradcam    = run_gradcam(img_array, image)
        return JSONResponse({"success": True, "prediction": prediction, "gradcam_image": gradcam, "gradcam_available": gradcam is not None, "warning": "Résultat à des fins de recherche uniquement."})
    except Exception as e:
        raise HTTPException(500, f"Erreur : {e}")