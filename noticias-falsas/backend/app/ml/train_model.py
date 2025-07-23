import pandas as pd
import numpy as np
import re
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Preprocesamiento
import nltk
import spacy
nltk.download('stopwords')
from nltk.corpus import stopwords

# Cargar modelo de spaCy
nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words('english'))

# 📂 Cargar datasets
true_df = pd.read_csv("../data/True.csv")
fake_df = pd.read_csv("../data/Fake.csv")


# Etiquetar
true_df['label'] = 1
fake_df['label'] = 0

# Combinar
df = pd.concat([true_df, fake_df], axis=0).sample(frac=1, random_state=42).reset_index(drop=True)

# 🧽 Función de limpieza
def clean_text(text):
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

# Limpiar título y texto
df['title'] = df['title'].apply(clean_text)
df['text'] = df['text'].apply(clean_text)

# Unir para entrada final
df['input'] = df['title'] + " " + df['text']

# Separar variables
X = df['input']
y = df['label']

# 🧪 División
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# TF-IDF
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1,2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 🌳 Entrenar modelo
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train_vec, y_train)

# 🧾 Reporte
y_pred = clf.predict(X_test_vec)
print(classification_report(y_test, y_pred))

# 📂 Guardar
os.makedirs("app/ml/models", exist_ok=True)
joblib.dump(clf, "app/ml/models/fake_news_model.joblib")
joblib.dump(vectorizer, "app/ml/models/vectorizer.joblib")
print("✅ Modelo y vectorizador guardados correctamente.")
