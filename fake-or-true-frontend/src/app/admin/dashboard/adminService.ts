import { axiosWithAuth } from "../../shared/TokenInterceptor";


export const getAllPredictions = () => {
  return axiosWithAuth().get("/admin/predictions");
};
