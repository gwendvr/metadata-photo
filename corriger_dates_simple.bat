@echo off
chcp 65001 >nul
echo ===== Correction des dates et heures des photos =====
echo.

pushd "%~dp0"
python corriger_dates_simple.py
set rc=%ERRORLEVEL%
popd

echo.
if %rc%==0 (
	echo Terminee.
) else (
	echo Script termine avec code %rc%.
)
echo.
pause