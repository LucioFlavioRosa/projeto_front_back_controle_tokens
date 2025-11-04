import os
from dotenv import load_dotenv

class ConfigError(Exception):
    pass

class Config:
    def __init__(self):
        # Carrega variáveis do .env, se existir
        load_dotenv()
        self.AZURE_TENANT_ID = os.getenv('AZURE_TENANT_ID')
        self.AZURE_CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
        self.AZURE_CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
        self.AZURE_WORKSPACE_ID = os.getenv('AZURE_WORKSPACE_ID')
        self.FLASK_ENV = os.getenv('FLASK_ENV', 'production')
        self.FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
        self._validate()

    def _validate(self):
        missing = []
        for var in [
            ('AZURE_TENANT_ID', self.AZURE_TENANT_ID),
            ('AZURE_CLIENT_ID', self.AZURE_CLIENT_ID),
            ('AZURE_CLIENT_SECRET', self.AZURE_CLIENT_SECRET),
            ('AZURE_WORKSPACE_ID', self.AZURE_WORKSPACE_ID)
        ]:
            if not var[1]:
                missing.append(var[0])
        if missing:
            raise ConfigError(f"Variáveis de ambiente obrigatórias ausentes: {', '.join(missing)}")

# Uso sugerido no backend:
# from config import Config, ConfigError
# try:
#     config = Config()
# except ConfigError as e:
#     print(str(e))
#     exit(1)
