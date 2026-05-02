@echo off
:: =============================================================
:: Lancement de l'API FastAPI — CancerScan IA
:: =============================================================
echo.
echo [CancerScan] Demarrage de l'API FastAPI...
echo [CancerScan] URL : http://localhost:8000
echo [CancerScan] Docs: http://localhost:8000/docs
echo.

:: Activer l'environnement virtuel
call venv\Scripts\activate.bat

:: Définir le chemin du modèle
set MODEL_PATH=models\model_clean.h5
set PARAMS_PATH=models\preprocessing_params.pkl

:: Lancer l'API
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause