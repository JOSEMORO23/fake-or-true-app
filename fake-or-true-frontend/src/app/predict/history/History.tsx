// src/app/predict/history/History.tsx
import { useEffect, useState } from "react";
import { getHistory } from "../predictService";
import "./History.scss";

interface HistoryItem {
  id: number;
  text: string;
  result: string;
  timestamp: string;
}

const History = () => {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await getHistory();
        setHistory(response.data); // Asumiendo que el backend devuelve una lista de predicciones
      } catch (err) {
        setError("Error al cargar el historial");
      }
    };

    fetchHistory();
  }, []);

  return (
    <div className="history-container">
      <h2>Historial de Predicciones</h2>
      {error && <p className="error">{error}</p>}
      {history.length === 0 ? (
        <p>No hay predicciones registradas aún.</p>
      ) : (
        <ul>
          {history.map((item) => (
            <li key={item.id} className={item.result === "Fake" ? "fake" : "true"}>
              <p><strong>Texto:</strong> {item.text}</p>
              <p><strong>Resultado:</strong> {item.result === "Fake" ? "🛑 FALSA" : "✅ VERDADERA"}</p>
              <p><small>{new Date(item.timestamp).toLocaleString()}</small></p>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default History;
