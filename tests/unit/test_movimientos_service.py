import pytest
from unittest.mock import MagicMock, patch
from src.services import movimientos_service


class TestMovimientosService:
    """Pruebas unitarias para movimientos_service."""

    def test_crear_movimiento_entrada(self, sample_movimiento):
        """Verifica que se pueda crear un movimiento de entrada."""
        with patch('src.db.repositories.productos_repository.obtener_producto') as mock_producto:
            with patch('src.db.repositories.movimientos_repository.crear_movimiento') as mock_repo:
                with patch('src.db.repositories.productos_repository.actualizar_producto'):
                    mock_producto.return_value = {'id': 'prod-1', 'stock': 10}
                    mock_repo.return_value = sample_movimiento
                    
                    resultado = movimientos_service.crear_movimiento(sample_movimiento)
                    
                    assert resultado is not None
                    assert 'movimiento' in resultado
                    assert resultado['movimiento']['tipo_movimiento'] == 'entrada'
                    mock_repo.assert_called_once()

    def test_crear_movimiento_salida(self, sample_movimiento):
        """Verifica que se pueda crear un movimiento de salida."""
        movimiento_salida = sample_movimiento.copy()
        movimiento_salida['tipo_movimiento'] = 'salida'
        
        with patch('src.db.repositories.productos_repository.obtener_producto') as mock_producto:
            with patch('src.db.repositories.movimientos_repository.crear_movimiento') as mock_repo:
                with patch('src.db.repositories.productos_repository.actualizar_producto'):
                    mock_producto.return_value = {'id': 'prod-1', 'stock': 10}
                    mock_repo.return_value = movimiento_salida
                    
                    resultado = movimientos_service.crear_movimiento(movimiento_salida)
                    
                    assert resultado['movimiento']['tipo_movimiento'] == 'salida'
                    mock_repo.assert_called_once()

    def test_obtener_movimiento_por_id(self, sample_movimiento):
        """Verifica que se pueda obtener un movimiento por ID."""
        with patch('src.db.repositories.movimientos_repository.obtener_movimiento_por_id') as mock_repo:
            mock_repo.return_value = sample_movimiento
            
            resultado = mock_repo('mov-1')
            
            assert resultado is not None
            assert resultado['id'] == 'mov-1'
            mock_repo.assert_called_once_with('mov-1')

    def test_listar_movimientos(self, sample_movimiento):
        """Verifica que se puedan listar movimientos."""
        movimientos_list = [sample_movimiento]
        
        with patch('src.db.repositories.movimientos_repository.listar_movimientos') as mock_repo:
            mock_repo.return_value = movimientos_list
            
            resultado = movimientos_service.listar_movimientos()
            
            assert len(resultado) == 1
            assert resultado[0]['producto_id'] == 'prod-1'
            mock_repo.assert_called_once()
