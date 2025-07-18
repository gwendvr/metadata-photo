@echo off
echo 📸 Extracteur Simple - Donnez juste le dossier!
echo ===============================================
echo.
set /p dossier="📁 Dossier des photos: "

if "%dossier%"=="" (
    echo ❌ Aucun dossier spécifié.
    pause
    exit
)

REM Supprimer les guillemets
set dossier=%dossier:"=%

if not exist "%dossier%" (
    echo ❌ Dossier introuvable: %dossier%
    pause
    exit
)

echo.
echo 🚀 Extraction en cours...
echo.

cd /d "C:\Users\gwend\Documents\phototri"
C:/Users/gwend/AppData/Local/Programs/Python/Python312/python.exe extract_simple.py "%dossier%"

echo.
echo ✅ Terminé! Fichier créé: %dossier%\metadata_simple.json
echo.
pause
