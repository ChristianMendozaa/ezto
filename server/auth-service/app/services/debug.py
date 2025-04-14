from keycloak import KeycloakOpenID

keycloak_openid = KeycloakOpenID(
    server_url="http://localhost:8080/",
    realm_name="master",
    client_id="ezto-client",
    client_secret_key="ezto-secret",  # ← asegúrate de que este valor es correcto
    verify=False
)

token = input("🔑 Pega tu access_token: ").strip()
print("🔍 Consultando introspect...")
result = keycloak_openid.introspect(token)
print("✅ Resultado:")
print(result)
