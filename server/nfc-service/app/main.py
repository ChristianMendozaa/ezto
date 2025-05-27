import os, socket
import consul
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from pydantic import BaseModel

from app.routers.nfc import router as nfc_router

# --- OpenAPI metadata ---
app = FastAPI(
    title="NFC-Service",
    description="""
    Microservicio para el manejo de tarjetas NFC.  
    Incluye funcionalidades de lectura, escritura y validación de tags.
    """,
    version="1.0.0",
    contact={
        "name": "Equipo de Desarrollo",
        "url": "https://github.com/tu-org/nfc-service",
        "email": "soporte@tuempresa.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    terms_of_service="https://tuempresa.com/terminos",
    root_path="/nfc",
)


# --- CORS middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- Rutas principales ---
app.include_router(
    nfc_router,
    tags=["NFC"],
)

# --- Modelo para salud ---
class HealthResponse(BaseModel):
    status: str

# --- Endpoint de salud ---
@app.get("/health", tags=["Health"], summary="Verifica el estado del servicio", response_model=HealthResponse)
async def health():
    """
    Verifica si el microservicio está en ejecución.
    Retorna un JSON con el estado `"ok"`.
    """
    return {"status": "ok"}

# --- OpenTelemetry / Jaeger ---
resource = Resource({SERVICE_NAME: "nfc-service"})
provider = TracerProvider(resource=resource)
jaeger_exporter = JaegerExporter(
    agent_host_name=os.getenv("JAEGER_AGENT_HOST", "jaeger"),
    agent_port=int(os.getenv("JAEGER_AGENT_PORT", 6831))
)
provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))
trace.set_tracer_provider(provider)
FastAPIInstrumentor().instrument_app(app)

# --- Registro en Consul ---
SERVICE_ID = os.getenv("SERVICE_ID", "nfc-service-1")
CONSUL_HOST = os.getenv("CONSUL_HOST", "consul")
CONSUL_PORT = int(os.getenv("CONSUL_PORT", 8500))
PORT = int(os.getenv("PORT", 8003))

@app.on_event("startup")
def register_in_consul():
    c = consul.Consul(host=CONSUL_HOST, port=CONSUL_PORT)
    address = socket.gethostbyname(socket.gethostname())
    c.agent.service.register(
        name="nfc-service",
        service_id=SERVICE_ID,
        address=address,
        port=PORT,
        tags=["nfc", "fastapi"]
    )

@app.on_event("shutdown")
def deregister_from_consul():
    c = consul.Consul(host=CONSUL_HOST, port=CONSUL_PORT)
    c.agent.service.deregister(service_id=SERVICE_ID)
