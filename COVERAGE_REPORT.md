# 📊 Reporte Detallado de Cobertura de Pruebas

## Resumen General

| Métrica | Valor |
|---------|-------|
| **Líneas Ejecutadas** | 367/930 (39%) |
| **Pruebas Unitarias** | 19/19 Pasadas ✅ |
| **Pruebas Integración** | 6/15 Pasadas ⚠️ |
| **Tiempo de Ejecución** | 1.03s |
| **Warnings** | 37 (Pydantic deprecation) |

---

## 📈 Cobertura por Módulo

### ✅ Módulos con Buena Cobertura (>70%)

```
src/schemas/producto.py         93% ✅✅✅
src/schemas/usuario.py          76% ✅✅
src/api/auth.py                 72% ✅
src/schemas/movimiento.py       71% ✅
```

**Interpretación:** Los esquemas de validación y autenticación están bien cubiertos.

### ⚠️ Módulos con Cobertura Media (50-70%)

```
src/services/productos_service.py    78% ✅✅
src/api/movimientos.py               71% ✅
src/utils/helpers.py                 52% ⚠️
src/services/movimientos_service.py  59% ⚠️
src/db/repositories/movimientos_repository.py  40% ⚠️
```

### ❌ Módulos con Baja Cobertura (<50%)

```
src/api/productos.py                 58% ⚠️
src/api/reportes.py                  60% ⚠️
src/api/usuarios.py                  28% ❌
src/core/auth.py                     27% ❌
src/db/repositories/usuarios_repository.py    11% ❌
src/db/repositories/productos_repository.py   24% ❌
src/utils/pdf_generator.py          13% ❌
src/services/reportes_service.py    10% ❌
src/models/*.py                      0% ❌ (No incluidos en tests)
src/schemas/permission.py            0% ❌
src/schemas/role.py                  0% ❌
```

---

## 🎯 Análisis de Líneas No Cubiertas

### API Productos (58% - 13 líneas faltantes)
- Líneas 12, 17, 22-25: Endpoints que requieren autenticación
- Líneas 30-34, 40-41, 46-47: Manejo de errores específicos

### API Usuarios (28% - 41 líneas faltantes)
- Líneas 11-15, 20-23: Endpoints de creación y listado
- Líneas 28-31, 36-59: Operaciones CRUD
- Líneas 64-67: Endpoints especializados

### Core Auth (27% - 49 líneas faltantes)
- Líneas 24-68: Manejo de JWT y tokens
- Líneas 79-91: Validación de permisos
- Líneas 95-100: Refresh tokens

### Repositories (11-40%)
- **usuarios_repository.py**: Falta cobertura en búsquedas complejas
- **productos_repository.py**: Faltan filtros y paginación
- **movimientos_repository.py**: Faltan queries avanzadas

---

## 💡 Recomendaciones de Mejora

### Prioritario (Impacto Alto)

1. **Ampliar pruebas de autenticación**
   - Actualmente: 72% en auth.py
   - Objetivo: 100%
   - Esfuerzo: 2-3 horas
   - Beneficio: Seguridad crítica
   ```python
   # Agregar tests para:
   - refresh_token()
   - verify_token_expired()
   - decode_jwt()
   - generate_access_token()
   ```

2. **Mejorar cobertura de API de Usuarios**
   - Actualmente: 28%
   - Objetivo: 80%+
   - Esfuerzo: 4-6 horas
   - Beneficio: Endpoints core cubiertos
   ```python
   # Agregar tests de integración para:
   - POST /usuarios (create)
   - GET /usuarios (list)
   - PUT /usuarios/{id} (update)
   - DELETE /usuarios/{id} (delete)
   ```

3. **Integrar tests de repositories**
   - Actualmente: 11-40%
   - Objetivo: 60%+
   - Esfuerzo: 6-8 horas
   - Beneficio: Lógica de datos validada
   ```python
   # Agregar tests unitarios para:
   - Búsquedas complejas
   - Paginación
   - Filtros
   - Ordenamiento
   ```

### Importante (Impacto Medio)

4. **Expandir pruebas de reportes**
   - Actualmente: 10%
   - Objetivo: 50%
   - Esfuerzo: 3-4 horas
   ```python
   # Agregar tests para:
   - Generación de PDFs
   - Cálculos de reportes
   - Exportación de datos
   ```

5. **Aumentar cobertura de utilidades**
   - Actualmente: 13-52%
   - Objetivo: 70%+
   - Esfuerzo: 2-3 horas


6. **Cubrir modelos y schemas avanzados**
   - Role, Permission, RolePermission
   - Actualmente: 0%
   - Esfuerzo: 2-3 horas

## 🔧 Comandos para Generar Reportes Detallados

```bash
# Reporte de cobertura en terminal
pytest tests/unit --cov=src --cov-report=term-missing

# Reporte en HTML (más detallado)
pytest tests/unit --cov=src --cov-report=html

# Específico por módulo
pytest tests/unit --cov=src.api --cov-report=term-missing

# Con contexto de líneas no cubiertas
pytest tests/unit --cov=src --cov-report=term:skip-covered --tb=short
```

---



## ✅ Checklist de Mantenimiento

- [ ] Ejecutar pruebas antes de cada commit
- [ ] Ejecutar `pytest --cov=src` antes de merge a main
- [ ] Mantener cobertura mínima de 80% para código crítico
- [ ] Documentar casos de prueba complejos
- [ ] Revisar coverage gaps semanalmente
- [ ] Actualizar tests cuando cambien APIs


