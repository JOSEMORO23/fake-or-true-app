// src/app/auth/authService.ts
import axios from "axios";

const API = "http://localhost:8000/auth";

export const login = (email: string, password: string) =>
  axios.post(`${API}/login`, { email, password });

export const register = (email: string, password: string) =>
  axios.post(`${API}/register`, { email, password });
