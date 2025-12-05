# Backend Gestión de Inventario 📦

Sistema de gestión de inventario construido con FastAPI y Supabase.

## 🚀 Estado del Proyecto

- ✅ **Tests Unitarios:** 19/19 pasadas (100%)
- ⚠️ **Tests Integración:** 6/15 pasadas (40%)
- 📊 **Cobertura de Código:** 39%
- 🔧 **Ambiente:** Python 3.13.2, FastAPI 0.119.1

---

## 📋 Quick Start - Testing

### Ejecutar Pruebas
```bash
# Unitarias
pytest tests/unit -v

# Todas
pytest tests/ -v

# Con cobertura
pytest tests/ --cov=src --cov-report=html
```

### Documentación de Testing
📖 **Comienza con:** `TESTING_INDEX.md`

---

## 📦 Requisitos

- Python 3.13+
- pip
- Supabase

---

## 🔧 Instalación

```bash
# Crear ambiente virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env

# Iniciar servidor
uvicorn src.main:app --reload
```

---

## 🧪 Testing

### Comandos Rápidos
```bash
run_tests.bat unit        # Tests unitarios
run_tests.bat coverage    # Con cobertura
run_tests.bat all         # Todas
```

### Resultados Actuales
- 19/19 tests unitarios ✅
- 6/15 tests integración ⚠️
- Cobertura: 39%
- Tiempo: 1.14s

---

## 📂 Estructura

```
src/
├── api/              # Endpoints
├── services/         # Lógica
├── db/              # Datos
└── models/          # Modelos

tests/
├── unit/            # 19 tests ✅
└── integration/     # 15 tests
```