from fastapi import APIRouter, HTTPException
from app.models.user import UserRegister, UserLogin
from passlib.context import CryptContext
from app.auth.jwt_handler import create_access_token
from app.core.database import get_connection

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
def register(user: UserRegister):
    conn = get_connection()
    cursor = conn.cursor()

    # Verificar si el usuario ya existe
    cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Usuario ya registrado")

    # Hashear contraseña y asignar rol
    hashed_password = pwd_context.hash(user.password)
    role = "user"
    cursor.execute(
        "INSERT INTO users (email, password, role) VALUES (%s, %s, %s)",
        (user.email, hashed_password, role)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return {"msg": "Usuario registrado correctamente ✅"}

@router.post("/login")
def login(user: UserLogin):
    conn = get_connection()
    cursor = conn.cursor()

    # Obtener contraseña y rol del usuario
    cursor.execute("SELECT password, role FROM users WHERE email = %s", (user.email,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row or not pwd_context.verify(user.password, row[0]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")

    role = row[1]
    token = create_access_token({"sub": user.email, "role": role.strip()})
    return {"access_token": token, "token_type": "bearer"}
