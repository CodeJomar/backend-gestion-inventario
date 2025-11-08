from src.db.repositories import usuarios_repository

def crear_usuario(data, creado_por):
    return usuarios_repository.crear_usuario(data, creado_por)

def listar_usuarios():
    return usuarios_repository.listar_usuarios()

def obtener_usuario(usuario_id):
    return usuarios_repository.obtener_usuario_por_id(usuario_id)

def actualizar_usuario(usuario_id, data, modifier_id):
    return usuarios_repository.actualizar_usuario(usuario_id, data, modifier_id)

def eliminar_usuario(usuario_id):
    return usuarios_repository.eliminar_usuario(usuario_id)
