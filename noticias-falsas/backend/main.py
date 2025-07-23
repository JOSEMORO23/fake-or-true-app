from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth_routes import router as AuthRouter
from app.routes.predict_route import router as PredictRouter
from app.core.exception_handler import register_exception_handlers
from app.routes.admin_routes import router as AdminRouter




app = FastAPI(title="Fake News Detector API")

# Middleware CORS para permitir acceso desde frontend Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ⚠️ cámbialo a dominio específico en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(AuthRouter, prefix="/auth", tags=["auth"])
app.include_router(PredictRouter, prefix="/predict", tags=["predict"])

@app.get("/")
def root():
    return {"message": "API de detección de noticias falsas funcionando ✅"}


from app.core.database import get_connection
from fastapi import HTTPException

@app.get("/ping-db")
def ping_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db = cursor.fetchone()
        cursor.close()
        conn.close()
        return {"message": f"Conectado a la base de datos: {db[0]} ✅"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error de conexión: {str(e)}")
    
  
register_exception_handlers(app)
app.include_router(AdminRouter, tags=["admin"])

