import pytest
from unittest.mock import MagicMock, patch
from src.services import productos_service
from fastapi import HTTPException


class TestProductosService:
    """Pruebas unitarias para productos_service."""

    def test_crear_producto_exitoso(self, sample_producto):
        """Verifica que se pueda crear un producto correctamente."""
        with patch('src.db.repositories.productos_repository.crear_producto') as mock_repo:
            mock_repo.return_value = sample_producto
            
            resultado = productos_service.crear_producto(sample_producto)
            
            assert resultado is not None
            assert resultado['nombre'] == 'Laptop'
            assert resultado['precio'] == 999.99
            mock_repo.assert_called_once()

    def test_obtener_producto_por_id(self, sample_producto):
        """Verifica que se pueda obtener un producto por ID."""
        with patch('src.db.repositories.productos_repository.obtener_producto') as mock_repo:
            mock_repo.return_value = sample_producto
            
            resultado = productos_service.obtener_producto('prod-1')
            
            assert resultado is not None
            assert resultado['id'] == 'prod-1'
            mock_repo.assert_called_once_with('prod-1')

    def test_listar_productos(self, sample_producto):
        """Verifica que se puedan listar productos."""
        productos_list = [sample_producto]
        
        with patch('src.db.repositories.productos_repository.listar_productos') as mock_repo:
            mock_repo.return_value = productos_list
            
            resultado = productos_service.listar_productos()
            
            assert len(resultado) == 1
            assert resultado[0]['nombre'] == 'Laptop'
            mock_repo.assert_called_once()

    def test_actualizar_producto(self, sample_producto):
        """Verifica que se pueda actualizar un producto."""
        producto_actualizado = sample_producto.copy()
        producto_actualizado['cantidad'] = 15
        
        with patch('src.db.repositories.productos_repository.obtener_producto') as mock_get:
            with patch('src.db.repositories.productos_repository.actualizar_producto') as mock_update:
                mock_get.return_value = sample_producto
                mock_update.return_value = producto_actualizado
                
                resultado = productos_service.actualizar_producto('prod-1', producto_actualizado)
                
                assert resultado['cantidad'] == 15
                mock_update.assert_called_once()

    def test_obtener_producto_no_encontrado(self):
        """Verifica que se lance excepción cuando producto no existe."""
        with patch('src.db.repositories.productos_repository.obtener_producto') as mock_repo:
            mock_repo.return_value = None
            
            with pytest.raises(HTTPException):
                productos_service.obtener_producto('prod-inexistente')

    def test_desactivar_producto(self):
        """Verifica que se pueda desactivar un producto."""
        sample = {'id': 'prod-1', 'nombre': 'Laptop'}
        with patch('src.db.repositories.productos_repository.obtener_producto') as mock_get:
            with patch('src.db.repositories.productos_repository.desactivar_producto') as mock_deactivate:
                mock_get.return_value = sample
                
                resultado = productos_service.desactivar_producto('prod-1')
                
                assert resultado['mensaje'] == 'Producto desactivado correctamente'
                mock_deactivate.assert_called_once()
