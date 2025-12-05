import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from src.main import app
from src.core.config import settings


@pytest.fixture
def client():
    """Proporciona un cliente de prueba para la aplicación FastAPI."""
    return TestClient(app)


@pytest.fixture
def mock_supabase():
    """Mock del cliente de Supabase."""
    with patch('src.db.supabase_client.supabase') as mock:
        yield mock


@pytest.fixture
def mock_auth():
    """Mock de autenticación."""
    mock = MagicMock()
    mock.sign_in_with_password = MagicMock()
    mock.sign_up = MagicMock()
    return mock


@pytest.fixture
def sample_usuario():
    """Usuario de ejemplo para pruebas."""
    return {
        'id': 'test-user-1',
        'email': 'test@example.com',
        'nombres': 'Juan',
        'apellidos': 'Pérez',
        'usuario': 'juanperez',
        'celular': '1234567890',
        'dni': '12345678',
        'role_id': 'role-user',
        'created_at': '2024-12-01T00:00:00Z'
    }


@pytest.fixture
def sample_producto():
    """Producto de ejemplo para pruebas."""
    return {
        'id': 'prod-1',
        'nombre': 'Laptop',
        'descripcion': 'Laptop de prueba',
        'stock': 10,
        'precio': 999.99,
        'created_at': '2024-12-01T00:00:00Z'
    }


@pytest.fixture
def sample_movimiento():
    """Movimiento de ejemplo para pruebas."""
    return {
        'id': 'mov-1',
        'producto_id': 'prod-1',
        'tipo_movimiento': 'entrada',
        'cantidad': 5,
        'motivo': 'Compra inicial',
        'created_at': '2024-12-01T00:00:00Z'
    }
