#!/bin/bash
# Script para ejecutar todas las pruebas con reporte completo

echo "========================================="
echo "Ejecutando Pruebas Unitarias..."
echo "========================================="
python -m pytest tests/unit -v --tb=short --color=yes

echo ""
echo "========================================="
echo "Ejecutando Pruebas de Integración..."
echo "========================================="
python -m pytest tests/integration -v --tb=short --color=yes

echo ""
echo "========================================="
echo "Generando Reporte de Cobertura..."
echo "========================================="
python -m pytest tests/ --cov=src --cov-report=html --cov-report=term

echo ""
echo "Reporte HTML generado en: htmlcov/index.html"
