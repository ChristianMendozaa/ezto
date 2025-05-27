# app/utils/keycloak_config.py

from app.config_loader import fetch_config, decrypt_value

cfg = fetch_config().get("keycloak", {})
def _strip_and_decrypt(field_name: str) -> str:
    raw = cfg.get(field_name, "")

    if raw.startswith("{cipher}"):
        token = raw[len("{cipher}"):]
        plain = decrypt_value(token)
   
        return plain
    return raw

# 2) Extrae y desencripta los valores cifrados
server_url = "http://keycloak:8080/keycloak"
realm         = cfg["realm"]
client_id     = cfg["client_id"]
client_secret = _strip_and_decrypt("client_secret")
admin_user    = cfg.get("username", "admin")
admin_pass    = _strip_and_decrypt("password")

# 3) Inicializa KeycloakAdmin
from keycloak import KeycloakAdmin, KeycloakOpenID

keycloak_admin = KeycloakAdmin(
    server_url=server_url + "/",
    username=admin_user,
    password=admin_pass,
    realm_name=realm,
    client_id="admin-cli",
    verify=True
)
print("[keycloak_config] Initialized KeycloakAdmin")

# 4) Inicializa KeycloakOpenID
keycloak_openid = KeycloakOpenID(
    server_url=server_url + "/",
    realm_name=realm,
    client_id=client_id,
    client_secret_key=client_secret,
    verify=True
)
print("[keycloak_config] Initialized KeycloakOpenID")
