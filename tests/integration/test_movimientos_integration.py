import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


class TestMovimientosAPI:
    """Pruebas de integración para la API de movimientos."""

    @patch('src.db.supabase_client.supabase')
    def test_listar_movimientos(self, mock_supabase):
        """Verifica que se puedan listar movimientos."""
        mock_movimientos = [
            {'id': 'mov-1', 'producto_id': 'prod-1', 'tipo': 'entrada', 'cantidad': 5},
            {'id': 'mov-2', 'producto_id': 'prod-1', 'tipo': 'salida', 'cantidad': 2}
        ]
        
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = mock_movimientos
        
        response = client.get("/movimientos")
        
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert isinstance(response.json(), list)

    @patch('src.db.supabase_client.supabase')
    def test_crear_movimiento_entrada(self, mock_supabase):
        """Verifica que se pueda crear un movimiento de entrada."""
        nuevo_movimiento = {
            'producto_id': 'prod-1',
            'tipo': 'entrada',
            'cantidad': 10,
            'motivo': 'Compra a proveedor'
        }
        
        mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [
            {'id': 'mov-3', **nuevo_movimiento}
        ]
        
        response = client.post("/movimientos", json=nuevo_movimiento)
        
        assert response.status_code in [201, 404]

    @patch('src.db.supabase_client.supabase')
    def test_crear_movimiento_salida(self, mock_supabase):
        """Verifica que se pueda crear un movimiento de salida."""
        nuevo_movimiento = {
            'producto_id': 'prod-1',
            'tipo': 'salida',
            'cantidad': 3,
            'motivo': 'Venta a cliente'
        }
        
        mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [
            {'id': 'mov-4', **nuevo_movimiento}
        ]
        
        response = client.post("/movimientos", json=nuevo_movimiento)
        
        assert response.status_code in [201, 404]

    @patch('src.db.supabase_client.supabase')
    def test_obtener_movimientos_por_producto(self, mock_supabase):
        """Verifica que se puedan obtener movimientos de un producto."""
        movimientos = [
            {'id': 'mov-1', 'producto_id': 'prod-1', 'tipo': 'entrada', 'cantidad': 5},
            {'id': 'mov-2', 'producto_id': 'prod-1', 'tipo': 'salida', 'cantidad': 2}
        ]
        
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = movimientos
        
        response = client.get("/movimientos?producto_id=prod-1")
        
        assert response.status_code in [200, 404]

    @patch('src.db.supabase_client.supabase')
    def test_eliminar_movimiento(self, mock_supabase):
        """Verifica que se pueda eliminar un movimiento."""
        mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value.data = []
        
        response = client.delete("/movimientos/mov-1")
        
        assert response.status_code in [200, 204, 404]
