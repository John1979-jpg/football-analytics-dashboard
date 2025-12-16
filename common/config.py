"""
Modulo de configuracion de la aplicacion.
Carga variables de entorno y proporciona acceso centralizado a la configuracion.
"""
import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """Clase de configuracion centralizada."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not Config._initialized:
            self._load_environment()
            Config._initialized = True
    
    def _load_environment(self):
        """Carga las variables de entorno desde el archivo .env"""
        env_path = Path(__file__).parent.parent / '.env'
        load_dotenv(env_path)
        
        self.app_name = os.getenv('APP_NAME', 'Football Analytics Dashboard')
        self.app_version = os.getenv('APP_VERSION', '1.0.0')
        self.admin_user = os.getenv('ADMIN_USER', 'admin')
        self.admin_password = os.getenv('ADMIN_PASSWORD', 'admin')
        self.database_path = os.getenv('DATABASE_PATH', 'data/football.db')
        self.api_url = os.getenv('FOOTBALL_API_URL', '')
        self.api_key = os.getenv('FOOTBALL_API_KEY', '')
        self.cache_ttl = int(os.getenv('CACHE_TTL', '3600'))
    
    @property
    def db_full_path(self):
        """Retorna la ruta completa de la base de datos."""
        return Path(__file__).parent.parent / self.database_path
    
    def get_api_headers(self):
        """Retorna los headers para las peticiones a la API."""
        return {
            'X-Auth-Token': self.api_key,
            'Content-Type': 'application/json'
        }
