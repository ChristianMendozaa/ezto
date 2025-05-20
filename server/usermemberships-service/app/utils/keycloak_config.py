import os
from dotenv import load_dotenv
from keycloak import KeycloakAdmin, KeycloakOpenID

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener variables del entorno
KEYCLOAK_URL            = os.getenv("KEYCLOAK_SERVER_URL").rstrip("/")
KEYCLOAK_REALM          = os.getenv("KEYCLOAK_REALM")
KEYCLOAK_ADMIN_USER     = os.getenv("KEYCLOAK_ADMIN_USER")
KEYCLOAK_ADMIN_PASSWORD = os.getenv("KEYCLOAK_ADMIN_PASSWORD")
KEYCLOAK_CLIENT_ID      = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET  = os.getenv("KEYCLOAK_CLIENT_SECRET")

# Admin client (para administración de Keycloak)
keycloak_admin = KeycloakAdmin(
    server_url=f"{KEYCLOAK_URL}/",
    username=KEYCLOAK_ADMIN_USER,
    password=KEYCLOAK_ADMIN_PASSWORD,
    realm_name=KEYCLOAK_REALM,
    client_id="admin-cli",
    verify=False
)

# Cliente para autenticación OpenID (para el flujo de login)
keycloak_openid = KeycloakOpenID(
    server_url=f"{KEYCLOAK_URL}/",
    realm_name=KEYCLOAK_REALM,
    client_id=KEYCLOAK_CLIENT_ID,
    client_secret_key=KEYCLOAK_CLIENT_SECRET,
    verify=False
)
