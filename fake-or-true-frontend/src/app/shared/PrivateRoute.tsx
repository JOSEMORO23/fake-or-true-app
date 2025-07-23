import { Navigate } from "react-router-dom";
import { isTokenValid } from "./authUtils";
import { ReactNode, ReactElement } from "react";


interface Props {
  children: ReactNode;
}

const PrivateRoute = ({ children }: Props): ReactElement => {
  return isTokenValid() ? <>{children}</> : <Navigate to="/login" />;
};



export default PrivateRoute;
