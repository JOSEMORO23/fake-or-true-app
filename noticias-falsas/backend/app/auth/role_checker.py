from fastapi import Depends, HTTPException, Request
from app.auth.jwt_handler import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        token = credentials.credentials
        payload = decode_access_token(token)
        if not payload or payload.get("role") not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Acceso denegado: rol insuficiente")
    