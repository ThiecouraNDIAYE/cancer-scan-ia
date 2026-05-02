@echo off
:: =============================================================
:: SETUP COMPLET — CancerScan IA
:: Université de Thiès — Projet Deep Learning 2025-2026
:: Lance ce fichier une seule fois pour tout installer
:: =============================================================

echo.
echo ========================================================
echo    SETUP CancerScan IA — Cancer du Sein
echo    Universite de Thies — Deep Learning 2025-2026
echo ========================================================
echo.

:: Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou pas dans le PATH.
    echo Telechargez Python 3.10 sur https://python.org
    pause
    exit /b 1
)

echo [OK] Python detecte.
echo.

:: ─── Créer l'environnement virtuel ───────────────────────────
echo [1/5] Creation de l'environnement virtuel...
if exist venv (
    echo      L'environnement virtuel existe deja. On continue.
) else (
    python -m venv venv
    echo      Environnement virtuel cree : venv\
)
echo.

:: ─── Activer l'environnement virtuel ─────────────────────────
echo [2/5] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat
echo      Environnement active.
echo.

:: ─── Mettre à jour pip ───────────────────────────────────────
echo [3/5] Mise a jour de pip...
python -m pip install --upgrade pip --quiet
echo      pip mis a jour.
echo.

:: ─── Installer les dépendances API ───────────────────────────
echo [4/5] Installation des dependances API...
pip install -r api\requirements.txt --quiet
echo      Dependances API installees.
echo.

:: ─── Installer les dépendances APP ───────────────────────────
echo [5/5] Installation des dependances Interface Streamlit...
pip install -r app\requirements.txt --quiet
echo      Dependances Interface installees.
echo.

:: ─── Vérifier que le modèle existe ───────────────────────────
if not exist models\model_clean.h5 (
    echo [ATTENTION] Le fichier models\model_clean.h5 est introuvable.
    echo             Copiez votre modele dans le dossier models\
    echo             Exemple : copier model_clean.h5 dans cancer_project\models\
    echo.
)

echo ========================================================
echo    SETUP TERMINE ! Pour lancer le projet :
echo    1. Double-cliquez sur start_api.bat
echo    2. Double-cliquez sur start_app.bat
echo ========================================================
echo.
pause