@echo off
:: =============================================================
:: Lancement de l'interface Streamlit — CancerScan IA
:: =============================================================
echo.
echo [CancerScan] Demarrage de l'interface Streamlit...
echo [CancerScan] URL : http://localhost:8501
echo.
echo [ATTENTION] Assurez-vous que l'API tourne dans un autre terminal
echo             (start_api.bat doit etre lance en premier)
echo.

:: Activer l'environnement virtuel
call venv\Scripts\activate.bat

:: Définir l'URL de l'API
set API_URL=http://localhost:8000

:: Lancer Streamlit
cd app
streamlit run streamlit_app.py --server.port 8501

pause