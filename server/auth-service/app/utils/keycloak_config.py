from keycloak import KeycloakAdmin, KeycloakOpenID

# Admin client
keycloak_admin = KeycloakAdmin(
    server_url="http://keycloak:8080/",
    username="admin",
    password="admin",
    realm_name="master",
    client_id="admin-cli",
    verify=False
)

# Cliente para autenticación
keycloak_openid = KeycloakOpenID(
    server_url="http://keycloak:8080/",            
    realm_name="master",
    client_id="ezto-client",
    client_secret_key="ezto-secret",
    verify=False
)