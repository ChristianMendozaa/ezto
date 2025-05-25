from fastapi import Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from firebase_admin.exceptions import FirebaseError
import logging
import traceback

# Importamos nuestras respuestas estandarizadas
from app.utils.response_standardization import ErrorResponse

# Configuración de logging
logger = logging.getLogger(__name__)


async def global_exception_dispatcher(request: Request, exc: Exception):
    # ⚠️ Errores definidos explícitamente
    if isinstance(exc, HTTPException):
        if exc.status_code == 400:
            return await bad_request_handler(request, exc)
        elif exc.status_code == 401:
            return await unauthorized_exception_handler(request, exc)
        elif exc.status_code == 403:
            return await forbidden_exception_handler(request, exc)
        elif exc.status_code == 404:
            return await not_found_exception_handler(request, exc)
        else:
            return await http_exception_handler(request, exc)

    # Errores de validación de datos (Pydantic)
    elif isinstance(exc, ValidationError):
        return await validation_exception_handler(request, exc)

    #  Errores de Firebase
    elif isinstance(exc, FirebaseError):
        return await firebase_exception_handler(request, exc)

    # Cualquier otro error no manejado
    else:
        return await general_exception_handler(request, exc)




# 🔹 Manejo global de HTTPException (Errores 400, 401, 403, 404, 422, etc.)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"❌ HTTPException ({exc.status_code}) en {request.url}: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            message=exc.detail,
            errors=[str(exc)]
        ).model_dump()
    )

# 🔹 Manejo global de errores 400 (Bad Request)
async def bad_request_handler(request: Request, exc: HTTPException):
    logger.error(f"❌ 400 Bad Request en {request.url}: {exc.detail}")
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorResponse(
            message="Solicitud incorrecta",
            errors=[str(exc)]
        ).model_dump()
    )

# 🔹 Manejo global de errores 401 (Unauthorized)
async def unauthorized_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"⚠️ 401 Unauthorized en {request.url}: {exc.detail}")
    
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=ErrorResponse(
            message="No autorizado",
            errors=[str(exc)]
        ).model_dump()
    )

# 🔹 Manejo global de errores 403 (Forbidden)
async def forbidden_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"⚠️ 403 Forbidden en {request.url}: {exc.detail}")
    
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=ErrorResponse(
            message="Acceso denegado",
            errors=[str(exc)]
        ).model_dump()
    )

# 🔹 Manejo global de errores 404 (Not Found)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"⚠️ 404 Not Found en {request.url}: {exc.detail}")
    
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ErrorResponse(
            message="Recurso no encontrado",
            errors=[str(exc)]
        ).model_dump()
    )

# 🔹 Manejo global de errores 422 (Unprocessable Entity - Errores de validación)
async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.error(f"❌ ValidationError en {request.url}: {exc.errors()}")

    error_messages = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err["loc"])  # Extraer ubicación del error
        message = err["msg"]  # Mensaje de error de Pydantic
        error_messages.append(f"'{field}': {message}")

    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            message="Error en la validación de datos",
            errors=error_messages
        ).model_dump()
    )


# 🔹 Manejo global de errores de Firebase
async def firebase_exception_handler(request: Request, exc: FirebaseError):
    logger.error(f"❌ FirebaseError en {request.url}: {str(exc)}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            message="Error al conectar con Firestore",
            errors=[str(exc)]
        ).model_dump()
    )

# 🔹 Manejo global de errores inesperados (500 Internal Server Error)
async def general_exception_handler(request: Request, exc: Exception):
    error_trace = traceback.format_exc()  # Captura la traza del error
    logger.error(f"❌ 500 Internal Server Error en {request.url}: {str(exc)}\n{error_trace}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            message="Error interno del servidor",
            errors=[str(exc)]
        ).model_dump()
    )


# 🔹 Ya deberías tener esta función
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"❌ RequestValidationError en {request.url}: {exc.errors()}")

    error_messages = [
        f"'{'.'.join(str(loc) for loc in err['loc'])}': {err['msg']}"
        for err in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            message="Error en la validación de datos",
            errors=error_messages
        ).model_dump()
    )