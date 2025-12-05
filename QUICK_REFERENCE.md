# 🚀 Guía Rápida de Testing

## ✅ Estado Actual

```
✅ 19/19 Pruebas Unitarias PASADAS
⚠️ 6/15 Pruebas Integración (requiere auth real)
📊 Cobertura: 39%
⏱️ Tiempo: 1.14 segundos
```

---

## 📋 Comandos Rápidos

### Ejecutar Pruebas
```bash
# Unitarias solamente
pytest tests/unit -v

# Todas las pruebas
pytest tests/ -v

# Con resumen corto
pytest tests/unit -q

# Con cobertura HTML
pytest tests/ --cov=src --cov-report=html
```

### Script Batch (Windows)
```batch
run_tests.bat unit        # Pruebas unitarias
run_tests.bat all         # Todas las pruebas
run_tests.bat coverage    # Con cobertura
```

---

## 📁 Estructura de Archivos

```
tests/
├── conftest.py                    # Fixtures globales
├── unit/
│   ├── test_auth_api.py           # 4 tests
│   ├── test_usuarios_service.py   # 5 tests
│   ├── test_productos_service.py  # 6 tests
│   └── test_movimientos_service.py # 4 tests
├── integration/
│   ├── test_usuarios_integration.py
│   ├── test_productos_integration.py
│   └── test_movimientos_integration.py
└── pytest.ini                     # Config
```

---

## 🔍 Fixtures Disponibles

### En `conftest.py`

```python
@pytest.fixture
def client():
    """TestClient para hacer requests HTTP"""
    
@pytest.fixture
def mock_supabase():
    """Cliente Supabase mockeado"""
    
@pytest.fixture
def sample_usuario():
    """Usuario de ejemplo"""
    return {...}
    
@pytest.fixture
def sample_producto():
    """Producto de ejemplo"""
    return {...}
    
@pytest.fixture
def sample_movimiento():
    """Movimiento de ejemplo"""
    return {...}
```

---

## 🧪 Ejemplos de Uso

### Test Unitario Simple
```python
def test_crear_usuario(mock_usuario_repository, sample_usuario):
    result = usuarios_service.create_usuario(sample_usuario)
    assert result["id"] is not None
    assert result["nombres"] == sample_usuario["nombres"]
```

### Test de Integración
```python
def test_listar_usuarios(client):
    response = client.get("/usuarios")
    assert response.status_code in [200, 401]
```

---

## ⚙️ Configuración pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
addopts = --verbose --tb=short
markers =
    unit: pruebas unitarias
    integration: pruebas de integración
    asyncio: tests asincronos
```

---

## 📊 Métricas de Cobertura

### Mejor Cobertura
- `src/schemas/producto.py` - **93%** ✅
- `src/schemas/usuario.py` - **76%** ✅
- `src/api/auth.py` - **72%** ✅

### Cobertura Mejorable
- `src/api/usuarios.py` - 28% → **Objetivo: 80%**
- `src/db/repositories/usuarios_repository.py` - 11% → **Objetivo: 60%**

---

## 🔧 Troubleshooting

### Error: "ModuleNotFoundError"
```bash
# Solución: Verificar rutas en conftest.py
# Asegurarse de que sys.path incluye src/
```

### Error: "401 Unauthorized" en tests
```bash
# Solución: Los endpoints requieren token real
# Los tests de integración están diseñados para esto
```

### Error: "No tests collected"
```bash
# Solución: Verificar que los archivos inicien con test_
# Verificar que estén en directorio tests/
```

##  Referencia Rápida

| Tarea | Comando |
|-------|---------|
| Ejecutar tests | `pytest tests/unit -v` |
| Ver cobertura | `pytest tests/ --cov=src --cov-report=term` |
| Generar HTML | `pytest tests/ --cov=src --cov-report=html` |
| Test específico | `pytest tests/unit/test_auth_api.py -v` |
| Con debug | `pytest tests/ -v -s --pdb` |

---

**Última actualización:** 4 de diciembre de 2025
