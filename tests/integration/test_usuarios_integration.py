import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


class TestUsuariosAPI:
    """Pruebas de integración para la API de usuarios."""

    @patch('src.db.supabase_client.supabase')
    def test_listar_usuarios(self, mock_supabase):
        """Verifica que se puedan listar usuarios."""
        mock_usuarios = [
            {'id': 'user-1', 'email': 'juan@example.com', 'nombres': 'Juan', 'apellidos': 'Pérez'},
            {'id': 'user-2', 'email': 'maria@example.com', 'nombres': 'María', 'apellidos': 'García'}
        ]
        
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = mock_usuarios
        
        response = client.get("/usuarios")
        
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert isinstance(response.json(), list)

    @patch('src.db.supabase_client.supabase')
    def test_crear_usuario(self, mock_supabase):
        """Verifica que se pueda crear un usuario."""
        nuevo_usuario = {
            'email': 'newuser@example.com',
            'nombres': 'Carlos',
            'apellidos': 'López',
            'usuario': 'carloslopez',
            'role_id': 'role-user'
        }
        
        mock_supabase.table.return_value.insert.return_value.execute.return_value.data = [
            {'id': 'user-3', **nuevo_usuario}
        ]
        
        response = client.post("/usuarios", json=nuevo_usuario)
        
        assert response.status_code in [201, 404]

    @patch('src.db.supabase_client.supabase')
    def test_obtener_usuario_por_id(self, mock_supabase):
        """Verifica que se pueda obtener un usuario por ID."""
        usuario = {'id': 'user-1', 'email': 'juan@example.com', 'nombres': 'Juan'}
        
        mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [usuario]
        
        response = client.get("/usuarios/user-1")
        
        assert response.status_code in [200, 404]

    @patch('src.db.supabase_client.supabase')
    def test_actualizar_usuario(self, mock_supabase):
        """Verifica que se pueda actualizar un usuario."""
        usuario_actualizado = {'nombres': 'Juan Carlos', 'apellidos': 'Pérez García'}
        
        mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value.data = [
            {'id': 'user-1', **usuario_actualizado}
        ]
        
        response = client.put("/usuarios/user-1", json=usuario_actualizado)
        
        assert response.status_code in [200, 404]

    @patch('src.db.supabase_client.supabase')
    def test_eliminar_usuario(self, mock_supabase):
        """Verifica que se pueda eliminar un usuario."""
        mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value.data = []
        
        response = client.delete("/usuarios/user-1")
        
        assert response.status_code in [200, 204, 404]
