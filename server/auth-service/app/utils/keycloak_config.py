from keycloak import KeycloakAdmin, KeycloakOpenID
from app.utils.env_config import require_env_var  # Usamos la misma función de validación

# ===============================
# Variables de entorno seguras
# ===============================

# Keycloak Admin (administración de usuarios)
KEYCLOAK_SERVER_URL = require_env_var("KEYCLOAK_SERVER_URL")
KEYCLOAK_ADMIN_USER = require_env_var("KEYCLOAK_ADMIN")
KEYCLOAK_ADMIN_PASSWORD = require_env_var("KEYCLOAK_ADMIN_PASSWORD")
KEYCLOAK_ADMIN_REALM = require_env_var("KEYCLOAK_ADMIN_REALM")
KEYCLOAK_ADMIN_CLIENT_ID = require_env_var("KEYCLOAK_ADMIN_CLIENT_ID")

# Keycloak OpenID Connect (autenticación de usuarios)
KEYCLOAK_REALM = require_env_var("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = require_env_var("KEYCLOAK_CLIENT_ID")
KEYCLOAK_CLIENT_SECRET = require_env_var("KEYCLOAK_CLIENT_SECRET")

# ===============================
# Inicializar Keycloak Admin Client
# ===============================
keycloak_admin = KeycloakAdmin(
    server_url=KEYCLOAK_SERVER_URL,
    username=KEYCLOAK_ADMIN_USER,
    password=KEYCLOAK_ADMIN_PASSWORD,
    realm_name=KEYCLOAK_ADMIN_REALM,
    client_id=KEYCLOAK_ADMIN_CLIENT_ID,
    verify=False  # Cambia a True si usas HTTPS con certificados válidos
)

# ===============================
# Inicializar Keycloak OpenID Client
# ===============================
keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_SERVER_URL,
    realm_name=KEYCLOAK_REALM,
    client_id=KEYCLOAK_CLIENT_ID,
    client_secret_key=KEYCLOAK_CLIENT_SECRET,
    verify=False  # Cambia a True si usas HTTPS con certificados válidos
)
