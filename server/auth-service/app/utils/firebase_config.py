# app/utils/firebase_config.py

import firebase_admin
from firebase_admin import credentials, firestore
from app.config_loader import fetch_config, decrypt_value

# 1) Baja la sección “firebase”
cfg = fetch_config().get("firebase", {})

# Función de debug para imprimir los valores recibidos
def _maybe_decrypt(val: str) -> str:
    """
    Si val arranca con "{cipher}", quita ese prefijo y
    llama a /decrypt. Si no, lo devuelve tal cual.
    """
    if isinstance(val, str) and val.startswith("{cipher}"):
        cipher_text = val[len("{cipher}"):]
        result = decrypt_value(cipher_text)
        return result
    return val

def _normalize_newlines(s: str) -> str:
    # Convierte las barras invertidas dobles en saltos reales:
    return s.replace("\\n", "\n")
# 2) Reconstruye el dict de credenciales,
#    desencriptando únicamente los campos cifrados
service_account_info = {
    "type":                        _maybe_decrypt(cfg.get("type", "")),
    "project_id":                  _maybe_decrypt(cfg.get("project_id", "")),
    "private_key_id":              _maybe_decrypt(cfg.get("private_key_id", "")),
    "private_key":                  _normalize_newlines(_maybe_decrypt(cfg.get("private_key",""))),
    "client_email":                _maybe_decrypt(cfg.get("client_email", "")),
    "client_id":                   _maybe_decrypt(cfg.get("client_id", "")),
    "auth_uri":                    _maybe_decrypt(cfg.get("auth_uri", "")),
    "token_uri":                   _maybe_decrypt(cfg.get("token_uri", "")),
    "auth_provider_x509_cert_url": _maybe_decrypt(cfg.get("auth_provider_x509_cert_url", "")),
    "client_x509_cert_url":        _maybe_decrypt(cfg.get("client_x509_cert_url", "")),
    "universe_domain":             _maybe_decrypt(cfg.get("universe_domain", "")),
}

# 3) Inicializa Firebase solo una vez
if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred)

# 4) Exporta el cliente de Firestore
db = firestore.client()
