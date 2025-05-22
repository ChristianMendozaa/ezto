# app/main.py
import os
from fastapi import FastAPI, HTTPException, Body, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from git import Repo
import yaml
from cryptography.fernet import Fernet
from pathlib import Path


app = FastAPI()
security = HTTPBasic()

# 1) Clona o hace pull del repo con tus YAMLs
GIT_URL     = os.getenv("CONFIG_GIT_URL")
CLONE_PATH  = Path("/tmp/config-repo")
if CLONE_PATH.exists():
    Repo(str(CLONE_PATH)).remotes.origin.pull()
else:
    Repo.clone_from(GIT_URL, str(CLONE_PATH))

# 2) Inicializa cifrado simétrico
KEY         = os.getenv("ENCRYPT_KEY")         # e.g. Fernet.generate_key().decode()
fernet      = Fernet(KEY.encode())

def check_auth(c: HTTPBasicCredentials = Depends(security)):
    # autenticación básica para endpoints sensibles
    user, pwd = os.getenv("CFG_USER"), os.getenv("CFG_PWD")
    if not (c.username == user and c.password == pwd):
        raise HTTPException(401, "Unauthorized")

# 3) Endpoints de cifrado
@app.post("/encrypt", dependencies=[Depends(check_auth)])
async def encrypt(request: Request):
    """
    Acepta JSON {"plain": "..."} o cualquier body puro.
    """
    ct = request.headers.get("content-type", "")
    if "application/json" in ct:
        body = await request.json()
        plain = body.get("plain", "").encode()
    else:
        plain = await request.body()

    if not plain:
        raise HTTPException(400, "Empty payload")

    token = fernet.encrypt(plain)
    return {"cipher": token.decode()}


@app.post("/decrypt", dependencies=[Depends(check_auth)])
async def decrypt(request: Request):
    """
    Acepta JSON {"cipher": "..."} o texto plano con el token cifrado.
    """
    ct = request.headers.get("content-type", "")
    if "application/json" in ct:
        body = await request.json()
        cipher = body.get("cipher", "")
    else:
        cipher = (await request.body()).decode()

    if not cipher:
        raise HTTPException(400, "Empty cipher")

    try:
        plain = fernet.decrypt(cipher.encode())
        return {"plain": plain.decode()}
    except Exception:
        raise HTTPException(400, "Bad cipher")

# 4) Endpoint de configuración: /{app}/{profile}
@app.get("/{app_name}/{profile}")
def get_config(app_name: str, profile: str, label: str = "main"):
    """
    Fallback:
      1) {app_name}-{profile}.yml
      2) {app_name}.yml
      3) application-{profile}.yml
      4) application.yml
    """
    candidates = [
        f"{app_name}-{profile}.yml",
        f"{app_name}.yml",
        f"application-{profile}.yml",
        "application.yml"
    ]
    for fn in candidates:
        path = CLONE_PATH / label / fn
        if path.exists():
            data = yaml.safe_load(path.read_text())
            # aquí podrías, si quieres, descifrar automáticamente valores que estén marcados
            return data
    raise HTTPException(404, "Configuration not found")

@app.get("/health")
async def health():
    return {"status": "UP"}
