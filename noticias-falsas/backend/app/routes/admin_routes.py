from fastapi import APIRouter, Depends
from app.auth.role_checker import RoleChecker

from fastapi import APIRouter, Depends
from app.auth.role_checker import RoleChecker
from app.core.database import get_connection

router = APIRouter()
admin_only = RoleChecker(["admin"])


@router.get("/admin/predictions", dependencies=[Depends(admin_only)])
def get_all_predictions():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM predictions ORDER BY created_at DESC")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener predicciones: {str(e)}")
