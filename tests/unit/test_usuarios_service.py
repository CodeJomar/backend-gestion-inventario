import pytest
from unittest.mock import MagicMock, patch
from src.services import usuarios_service
from src.models.usuario import Usuario


class TestUsuariosService:
    """Pruebas unitarias para usuarios_service."""

    def test_crear_usuario_exitoso(self, sample_usuario):
        """Verifica que se pueda crear un usuario correctamente."""
        with patch('src.db.repositories.usuarios_repository.crear_usuario') as mock_repo:
            mock_repo.return_value = sample_usuario
            
            resultado = usuarios_service.crear_usuario(sample_usuario, 'admin')
            
            assert resultado is not None
            mock_repo.assert_called_once()

    def test_obtener_usuario_por_id(self, sample_usuario):
        """Verifica que se pueda obtener un usuario por ID."""
        with patch('src.db.repositories.usuarios_repository.obtener_usuario_por_id') as mock_repo:
            mock_repo.return_value = sample_usuario
            
            resultado = usuarios_service.obtener_usuario('test-user-1')
            
            assert resultado is not None
            assert resultado['id'] == 'test-user-1'
            mock_repo.assert_called_once_with('test-user-1')

    def test_listar_usuarios(self, sample_usuario):
        """Verifica que se puedan listar usuarios."""
        usuarios_list = [sample_usuario, sample_usuario]
        
        with patch('src.db.repositories.usuarios_repository.listar_usuarios') as mock_repo:
            mock_repo.return_value = usuarios_list
            
            resultado = usuarios_service.listar_usuarios()
            
            assert len(resultado) == 2
            assert resultado[0]['email'] == 'test@example.com'
            mock_repo.assert_called_once()

    def test_actualizar_usuario(self, sample_usuario):
        """Verifica que se pueda actualizar un usuario."""
        usuario_actualizado = sample_usuario.copy()
        usuario_actualizado['nombres'] = 'Carlos'
        
        with patch('src.db.repositories.usuarios_repository.actualizar_usuario') as mock_repo:
            mock_repo.return_value = usuario_actualizado
            
            resultado = usuarios_service.actualizar_usuario('test-user-1', usuario_actualizado, 'admin')
            
            assert resultado['nombres'] == 'Carlos'
            mock_repo.assert_called_once()

    def test_eliminar_usuario(self):
        """Verifica que se pueda eliminar un usuario."""
        with patch('src.db.repositories.usuarios_repository.eliminar_usuario') as mock_repo:
            mock_repo.return_value = True
            
            resultado = usuarios_service.eliminar_usuario('test-user-1')
            
            assert resultado is True
            mock_repo.assert_called_once_with('test-user-1')
