// src/app/predict/predict/Predict.tsx
import { useState } from "react";
import { predictNews } from "../predictService";
import "./Predict.scss";


const Predict = () => {
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const [result, setResult] = useState<null | string>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

 const handlePredict = async (e: React.FormEvent) => {
  e.preventDefault();
  setResult(null);
  setError("");
  setLoading(true);
  try {
    const response = await predictNews({ title, text });
    setResult(response.data.prediction);
    // 🔧 Limpiar campos después de éxito
    setTitle("");
    setText("");
  } catch (err) {
    setError("Error al analizar la noticia. Intenta nuevamente o El texto debe contener más contenido alfabético..");
  } finally {
    setLoading(false);
  }
};


  return (
    <div className="predict-container">
      <h2>Analizar Noticia</h2>
      <form onSubmit={handlePredict}>
        <input
          type="text"
          placeholder="Título de la noticia"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <textarea
          placeholder="Ingrese la noticia ..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Analizando..." : "Analizar"}
        </button>
      </form>

      {result && (
        <div className={`result ${result === "Fake" ? "fake" : "true"}`}>
          Resultado del Analisis: {result === "Fake" ? "🛑 FALSA" : "✅ VERDADERA"}
        </div>
      )}

      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default Predict;

