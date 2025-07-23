import jwt_decode from "jwt-decode";

interface JwtPayload {
  exp: number;
  sub: string;
  role?: string;
}

export const isTokenValid = (): boolean => {
  const token = localStorage.getItem("token");
  if (!token) return false;

  try {
    const decoded = jwt_decode<JwtPayload>(token);
    const currentTime = Date.now() / 1000;
    return decoded.exp > currentTime;
  } catch (e) {
    return false;
  }
};
