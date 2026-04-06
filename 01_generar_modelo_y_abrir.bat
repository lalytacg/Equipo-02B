@echo off
setlocal
cd /d "%~dp0"
title Equipo 02B - Generador del modelo HTML

echo ================================================
echo  Equipo 02B - Prototipo HTML de viralidad
echo  Generacion de rf_model.js desde un Random Forest
echo ================================================
echo.

set "MODEL="
if exist "modelo_act4.joblib" set "MODEL=modelo_act4.joblib"
if not defined MODEL if exist "modelo.joblib" set "MODEL=modelo.joblib"
if not defined MODEL if exist "random_forest.joblib" set "MODEL=random_forest.joblib"

if not defined MODEL (
  echo No se encontro un archivo .joblib en esta carpeta.
  echo.
  echo Coloca aqui tu modelo entrenado, por ejemplo:
  echo   modelo_act4.joblib
  echo.
  pause
  exit /b 1
)

echo Modelo detectado: %MODEL%
echo.

where py >nul 2>&1
if %errorlevel%==0 (
  py -3 export_rf_to_js.py --model "%MODEL%" --out rf_model.js
) else (
  where python >nul 2>&1
  if %errorlevel%==0 (
    python export_rf_to_js.py --model "%MODEL%" --out rf_model.js
  ) else (
    echo No se encontro Python instalado en este equipo.
    echo Instala Python desde python.org y vuelve a intentar.
    echo.
    pause
    exit /b 1
  )
)

if errorlevel 1 (
  echo.
  echo Ocurrio un error al exportar el modelo.
  echo Verifica que el archivo .joblib sea un RandomForestClassifier compatible.
  echo.
  pause
  exit /b 1
)

echo.
echo Modelo exportado correctamente a rf_model.js
echo Se abrira el prototipo en tu navegador.
echo.
start "" "index.html"
pause
