@echo off
echo 🔄 Restauration Simple des Métadonnées
echo ======================================
echo.
set /p source="📁 Dossier source (avec metadata_simple.json): "
set /p cible="📁 Dossier cible (photos traitées): "

REM Supprimer les guillemets
set source=%source:"=%
set cible=%cible:"=%

if "%source%"=="" (
    echo ❌ Dossier source requis.
    pause
    exit
)

if not exist "%source%" (
    echo ❌ Dossier source introuvable: %source%
    pause
    exit
)

if "%cible%"=="" (
    echo 💡 Aucun dossier cible spécifié, utilisation du dossier source.
    set cible=%source%
)

if not exist "%cible%" (
    echo ❌ Dossier cible introuvable: %cible%
    pause
    exit
)

echo.
echo 🔄 Restauration en cours...
echo 📁 Source: %source%
echo 📁 Cible: %cible%
echo.

cd /d "C:\Users\gwend\Documents\phototri"
C:/Users/gwend/AppData/Local/Programs/Python/Python312/python.exe restore_simple.py "%source%" "%cible%"

echo.
echo ✅ Restauration terminée!
echo.
pause
