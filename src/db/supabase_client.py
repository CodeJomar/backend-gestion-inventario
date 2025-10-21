from supabase import create_client, Client
from src.core.config import settings

# Conexión usando configuración del proyecto
supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_KEY
)