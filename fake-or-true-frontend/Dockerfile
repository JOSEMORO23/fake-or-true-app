# Dockerfile

# Imagen base
FROM node:18-alpine AS build

# Establece el directorio de trabajo
WORKDIR /app

# Copia dependencias
COPY package*.json ./

# Instala dependencias
RUN npm install

# Copia el resto del código
COPY . .

# ⚠️⬇️ NUEVO: Define variable de entorno para React
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL

# Construye la app
RUN npm run build

# Usa una imagen NGINX para servir la app
FROM nginx:stable-alpine

# Copia los archivos construidos al directorio que Nginx sirve
COPY --from=build /app/build /usr/share/nginx/html

# Expone el puerto 80
EXPOSE 80

# Copia la configuración personalizada de Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf


CMD ["nginx", "-g", "daemon off;"]
