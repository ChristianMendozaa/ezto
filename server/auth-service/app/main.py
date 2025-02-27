from fastapi import FastAPI
from app.controllers.register_controller import router as register_router

app = FastAPI(
    title="Registro de Usuarios - Plataforma EzTo",
    description="Microservicio para el registro de usuarios con FastAPI y Firebase.",
    version="1.0.0"
)

# Incluir las rutas del registro de usuarios
app.include_router(register_router, prefix="/auth", tags=["Registro de Usuarios"])
