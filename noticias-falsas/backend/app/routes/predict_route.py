from fastapi import APIRouter, HTTPException, Depends, Request
from app.models.prediction import NewsInput
from app.auth.jwt_bearer import JWTBearer
from app.core.database import get_connection
import joblib
import re
import spacy
from nltk.corpus import stopwords
import nltk
from jose import JWTError, jwt
import os

# Cargar variables para decodificar el token
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET")
ALGORITHM = os.getenv("JWT_ALGORITHM")

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
nlp = spacy.load("en_core_web_sm")

router = APIRouter()

# Cargar modelo
try:
    model = joblib.load("app/ml/models/fake_news_model.joblib")
    vectorizer = joblib.load("app/ml/models/vectorizer.joblib")
except Exception:
    raise HTTPException(status_code=500, detail="Error cargando el modelo o vectorizador")

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    doc = nlp(text)
    tokens = []
    for token in doc:
        if token.is_stop or token.is_punct or token.is_space:
            continue
        lemma = token.lemma_.strip()
        if lemma not in stop_words and len(lemma) > 2:
            tokens.append(lemma)
    return ' '.join(tokens)

def get_user_email_from_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=403, detail="Token no proporcionado")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=403, detail="Token inválido")

@router.post("/", dependencies=[Depends(JWTBearer())])
def predict_news(news: NewsInput, request: Request):
    combined = f"{news.title} {news.text}"
    cleaned = clean_text(combined)
    vector = vectorizer.transform([cleaned])
    prediction = model.predict(vector)[0]
    label = "Real" if prediction == 1 else "Fake"

    # Obtener email del usuario desde token
    user_email = get_user_email_from_token(request)

    # Guardar predicción en la base de datos
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO predictions (user_email, title, text, prediction) VALUES (%s, %s, %s, %s)",
            (user_email, news.title, news.text, label)
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar la predicción: {str(e)}")

    return {"prediction": label}

@router.get("/history", dependencies=[Depends(JWTBearer())])
def get_user_predictions(request: Request):
    user_email = get_user_email_from_token(request)

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, title, text, prediction, created_at FROM predictions WHERE user_email = %s ORDER BY created_at DESC",
            (user_email,)
        )
        results = cursor.fetchall()
        cursor.close()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al recuperar historial: {str(e)}")

    return results

