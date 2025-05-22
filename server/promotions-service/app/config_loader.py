# app/config_loader.py
import os, httpx, yaml

CONFIG_URL = os.getenv("CONFIG_URL")
APP_NAME   = os.getenv("APP_NAME")
PROFILE    = os.getenv("APP_PROFILE","dev")
AUTH       = (os.getenv("CFG_USER"), os.getenv("CFG_PWD"))

def fetch_config() -> dict:
    url = f"{CONFIG_URL}/{APP_NAME}/{PROFILE}"
    r   = httpx.get(url, auth=AUTH, timeout=5)
    r.raise_for_status()
    return yaml.safe_load(r.text)

def decrypt_value(cipher_text: str) -> str:
    """
    Llama al endpoint /decrypt del Config-Server para
    desencriptar un valor que vino cifrado con {cipher}…
    """
    r = httpx.post(
        f"{CONFIG_URL}/decrypt",
        json={"cipher": cipher_text},
        auth=AUTH,
        timeout=5
    )
    r.raise_for_status()
    return r.json()["plain"]