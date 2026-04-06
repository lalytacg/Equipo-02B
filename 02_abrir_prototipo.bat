@echo off
cd /d "%~dp0"
title Equipo 02B - Abrir prototipo HTML
if not exist "rf_model.js" (
  echo No se encontro rf_model.js.
  echo Primero ejecuta 01_generar_modelo_y_abrir.bat
  echo.
  pause
  exit /b 1
)
start "" "index.html"
