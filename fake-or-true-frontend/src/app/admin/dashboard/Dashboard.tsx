// src/app/admin/dashboard/Dashboard.tsx
import { useEffect, useState } from "react";
import "./Dashboard.scss";

const Dashboard = () => {
  const [username, setUsername] = useState<string | null>(null);

  useEffect(() => {
    // Decodificar el token para mostrar el nombre del usuario
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split(".")[1]));
        setUsername(payload.sub || "Administrador");
      } catch {
        setUsername("Administrador");
      }
    }
  }, []);

  return (
    <div className="dashboard-container">
      <h2>Panel de Administración</h2>
      <p>Bienvenido, <strong>{username}</strong>.</p>

      <div className="card-grid">
        <div className="card">
          <h3>Predicciones</h3>
          <p>Visualiza el historial y la actividad reciente.</p>
        </div>
        <div className="card">
          <h3>Usuarios (futuro)</h3>
          <p>Gestiona usuarios registrados.</p>
        </div>
        <div className="card">
          <h3>Configuraciones</h3>
          <p>Administra parámetros de la IA o seguridad.</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
