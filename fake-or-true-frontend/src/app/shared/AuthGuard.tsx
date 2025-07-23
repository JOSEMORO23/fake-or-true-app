// src/app/shared/AuthGuard.tsx
import { Navigate } from "react-router-dom";
import { ReactNode } from "react";

export const AuthGuard = ({ children }: { children: ReactNode }) => {
  const token = localStorage.getItem("token");
  return token ? <>{children}</> : <Navigate to="/login" />;
};
