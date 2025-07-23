// src/app/shared/TokenInterceptor.ts
import axios from "axios";

const instance = axios.create({
  //baseURL: "http://localhost:8000",
  baseURL: process.env.REACT_APP_API_URL,
   // o tu URL del backend en producción
});

// Interceptor para agregar el token dinámicamente antes de cada request
instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export const axiosWithAuth = () => instance;
