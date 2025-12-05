@echo off
REM Script para ejecutar pruebas con diferentes opciones

setlocal enabledelayedexpansion

echo ============================================
echo Backend Gestión de Inventario - Test Suite
echo ============================================
echo.

if "%1"=="" (
    echo Uso: run_tests.bat [opcion]
    echo.
    echo Opciones:
    echo   unit         - Ejecutar solo pruebas unitarias
    echo   integration  - Ejecutar solo pruebas de integración
    echo   all          - Ejecutar todas las pruebas
    echo   coverage     - Ejecutar con reporte de cobertura
    echo   watch        - Ejecutar en modo observación (watch)
    echo   verbose      - Ejecutar con salida detallada
    echo.
    exit /b 1
)

if "%1"=="unit" (
    echo Ejecutando pruebas unitarias...
    python -m pytest tests/unit -v
) else if "%1"=="integration" (
    echo Ejecutando pruebas de integración...
    python -m pytest tests/integration -v
) else if "%1"=="all" (
    echo Ejecutando todas las pruebas...
    python -m pytest tests/ -v
) else if "%1"=="coverage" (
    echo Ejecutando pruebas con cobertura...
    python -m pytest tests/ --cov=src --cov-report=html --cov-report=term-missing
    echo.
    echo Reporte de cobertura generado en: htmlcov/index.html
) else if "%1"=="watch" (
    echo Ejecutando en modo observación...
    python -m pytest tests/ -v --tb=short -s --looponfail
) else if "%1"=="verbose" (
    echo Ejecutando con salida detallada...
    python -m pytest tests/ -vv --tb=long
) else (
    echo Opción desconocida: %1
    exit /b 1
)

endlocal
