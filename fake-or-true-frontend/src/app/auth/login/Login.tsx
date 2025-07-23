// src/app/auth/login/Login.tsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../authService";
import jwt_decode from "jwt-decode";
import "./Login.scss";

interface JwtPayload {
  exp: number;
  sub: string;
  role?: string;
}

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    try {
      const res = await login(email, password);
      console.log("Respuesta login:", res);  // 👈 agrega esto
      const token = res.data.access_token;
      localStorage.setItem("token", token);

      const decoded = jwt_decode<JwtPayload>(token);
      console.log("Token decodificado:", decoded);

      if (decoded.sub === "morocho@gmail.com" && decoded.role?.trim() === "admin") {
  navigate("/admin");
} else {
  navigate("/predict");
}

    } catch (err) {
      setError("Credenciales incorrectas");
    }
  };

  return (
    <div className="auth-container">
      <h2>Iniciar Sesión</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Correo"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Contraseña"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Entrar</button>
      </form>
      {error && <p className="error">{error}</p>}
      <p>¿No tienes cuenta? <a onClick={() => navigate("/register")}>Regístrate</a></p>
    </div>
  );
};

export default Login;
