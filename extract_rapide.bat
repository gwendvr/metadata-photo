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
python extract_simple.py "%dossier%" 2>&1
set rc=%ERRORLEVEL%
popd

echo.
echo ========================================
if exist "%dossier%\metadata_simple.json" (
    echo SUCCES! Fichier cree: %dossier%\metadata_simple.json
) else (
    echo ATTENTION: Fichier metadata_simple.json non trouve!
    echo Code retour: %rc%
    echo Verifiez les erreurs ci-dessus.
)
echo ========================================
echo.
echo Appuyez sur une touche pour fermer cette fenetre...
pause >nul
