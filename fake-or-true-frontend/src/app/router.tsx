// src/app/router.tsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./auth/login/Login";
import Register from "./auth/register/Register";
import Predict from "./predict/predict/Predict";
import History from "./predict/history/History";
import { AuthGuard } from "./shared/AuthGuard";
import AdminDashboard from "./admin/dashboard/AdminDashboard"; // ✅ Ruta corregida

const Router = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Navigate to="/login" />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/predict" element={<AuthGuard><Predict /></AuthGuard>} />
      <Route path="/history" element={<AuthGuard><History /></AuthGuard>} />
      <Route path="/admin" element={<AuthGuard><AdminDashboard /></AuthGuard>} /> {/* ✅ Sustituido */}
    </Routes>
  </BrowserRouter>
);

export default Router;
