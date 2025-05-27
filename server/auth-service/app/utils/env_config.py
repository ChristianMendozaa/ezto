import os
from dotenv import load_dotenv

# Cargar solo una vez el .env
load_dotenv()

def require_env_var(var_name: str) -> str:
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"Falta la variable de entorno: {var_name}")
    return value
