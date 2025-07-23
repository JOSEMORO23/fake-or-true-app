// src/app/predict/predictService.ts
import { axiosWithAuth } from "../shared/TokenInterceptor";

// El backend espera un objeto con: { title: string, text: string }
export const predictNews = (payload: { title: string; text: string }) => {
  return axiosWithAuth().post("/predict/", payload);
};

// Ruta para historial (está dentro de /predict/)
export const getHistory = () => {
  return axiosWithAuth().get("/predict/history");
};
