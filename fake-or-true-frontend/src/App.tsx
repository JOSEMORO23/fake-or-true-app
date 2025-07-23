import { Routes, Route } from "react-router-dom";
import Login from "./app/auth/login/Login";
import Register from "./app/auth/register/Register";
import Predict from "./app/predict/predict/Predict";
import History from "./app/predict/history/History";
import Dashboard from "./app/admin/dashboard/Dashboard";
import PrivateRoute from "./app/shared/PrivateRoute";


function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route
        path="/predict"
        element={
          <PrivateRoute>
            <Predict />
          </PrivateRoute>
        }
      />
      <Route
        path="/history"
        element={
          <PrivateRoute>
            <History />
          </PrivateRoute>
        }
      />
      <Route
        path="/admin"
        element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        }
      />
    </Routes>
  );
}


export default App;
