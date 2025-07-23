from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

# Configurar logs
logging.basicConfig(filename="backend.log", level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

# Manejador personalizado
def register_exception_handlers(app: FastAPI):
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logging.error(f"HTTPException: {exc.detail} | Ruta: {request.url}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": "Ocurrió un error procesando tu solicitud."}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logging.error(f"Error de validación: {exc.errors()} | Ruta: {request.url}")
        return JSONResponse(
            status_code=422,
            content={"detail": "Datos de entrada inválidos."}
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logging.exception(f"Excepción inesperada en {request.url}: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno del servidor. Intenta más tarde."}
        )
