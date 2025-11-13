@echo off
chcp 65001 >nul
echo Restauration Simple des Metadonnees
echo ================================
echo.
set /p source="Dossier source (avec metadata_simple.json): "
set /p cible="Dossier cible (photos traitees): "

REM Supprimer les guillemets
set source=%source:"=%
set cible=%cible:"=%

if "%source%"=="" (
    echo Dossier source requis.
    pause
    exit /b 1
)

if not exist "%source%" (
    echo Dossier source introuvable: %source%
    pause
    exit /b 1
)

if "%cible%"=="" (
    echo Aucun dossier cible specifie, utilisation du dossier source.
    set cible=%source%
)

if not exist "%cible%" (
    echo Dossier cible introuvable: %cible%
    pause
    exit /b 1
)

echo.
echo Restauration en cours...
echo Source: %source%
echo Cible: %cible%
echo.

pushd "%~dp0"
python restore_simple.py "%source%" "%cible%"
set rc=%ERRORLEVEL%
popd

echo.
if %rc%==0 (
    echo Terminee avec succes.
) else (
    echo Script termine avec code %rc%. Verifiez la sortie pour details.
)
echo.
pause
