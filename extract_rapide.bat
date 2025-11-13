@echo off
REM Utilitaire: wrapper pour lancer extract_simple.py
REM -> utilise le `python` disponible dans le PATH (évite les chemins codés en dur)

REM Essayer d'utiliser une page de code UTF-8 pour améliorer l'affichage (optionnel)
chcp 65001 >nul

echo Extracteur Simple - Donnez juste le dossier!
echo ============================================
echo.
set /p dossier="Dossier des photos: "

if "%dossier%"=="" (
    echo Aucun dossier spécifie.
    pause
    exit /b 1
)

REM Supprimer les guillemets si présent
set dossier=%dossier:"=%

if not exist "%dossier%" (
    echo Dossier introuvable: %dossier%
    pause
    exit /b 1
)

echo.
echo Extraction en cours...
echo.

REM Lancer le script Python depuis le répertoire du script (ne pas se baser sur un cd fixe)
pushd "%~dp0"
python extract_simple.py "%dossier%"
set rc=%ERRORLEVEL%
popd

echo.
if exist "%dossier%\metadata_simple.json" (
    echo Terminé! Fichier crée: %dossier%\metadata_simple.json
) else (
    echo Script termine (code retour %rc%). Verifiez la sortie pour d'eventuelles erreurs.
)
echo.
pause
