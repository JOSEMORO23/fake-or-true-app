

// src/app/admin/dashboard/AdminDashboard.tsx
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { useEffect, useState } from "react";
import { getAllPredictions } from "./adminService";
import { Bar } from "react-chartjs-2";
import "./AdminDashboard.scss";
// REGISTRO OBLIGATORIO de los módulos que usas
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);



interface Prediction {
  id: number;
  title: string;
  text: string;
  result: string;
  created_at?: string;
}

const AdminDashboard = () => {
  const [predictions, setPredictions] = useState<Prediction[]>([]);

  useEffect(() => {
    getAllPredictions().then((res: any) => {
      setPredictions(res.data);
    });
  }, []);

  const trueCount = predictions.filter(p => p.result === "True").length;
  const fakeCount = predictions.filter(p => p.result === "Fake").length;

  const data = {
    labels: ["Falsas", "Verdaderas"],
    datasets: [{
      label: "Noticias clasificadas",
      data: [fakeCount, trueCount],
      backgroundColor: ["#F44C4C", "#4CAF50"]
    }]
  };

  return (
    <div className="admin-dashboard">
      <h2>Panel de Administración</h2>
      <div className="chart-container">
        <Bar data={data} />
      </div>
    </div>
  );
};

export default AdminDashboard;
