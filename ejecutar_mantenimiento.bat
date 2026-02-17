@echo off
REM Script para ejecutar mantenimiento de datos de demostración
REM Este script se puede programar para ejecutarse automáticamente

cd /d "%~dp0"

echo ========================================
echo Mantenimiento de Datos MultiParking
echo ========================================
echo.

REM Activar entorno virtual si existe
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM Ejecutar script de mantenimiento
python mantener_datos_demo.py

echo.
echo ========================================
echo Proceso completado
echo ========================================
pause
