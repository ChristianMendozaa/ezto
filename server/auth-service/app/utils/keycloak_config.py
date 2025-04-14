from keycloak import KeycloakAdmin, KeycloakOpenID

# Admin client (usado solo para tareas administrativas como crear usuarios)
keycloak_admin = KeycloakAdmin(
    server_url="http://keycloak:8080/",
    username="admin",
    password="admin",
    realm_name="master",
    client_id="admin-cli",
    verify=False
)

# Cliente para autenticación (sin client_secret aquí)
keycloak_openid = KeycloakOpenID(
    server_url="http://keycloak:8080/",
    realm_name="master",
    client_id="ezto-client",
    client_secret_key="ezto-secret",
    verify=False
)