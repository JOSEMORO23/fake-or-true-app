# Imagen base
FROM node:18-alpine

# Establece el directorio de trabajo
WORKDIR /app

# Copia dependencias
COPY package*.json ./

# Instala dependencias
RUN npm install

# Copia el resto del código
COPY . .

# Construye la app
RUN npm run build

# Usa una imagen NGINX para servir la app
FROM nginx:stable-alpine

# Copia los archivos construidos al directorio que Nginx sirve
COPY --from=0 /app/build /usr/share/nginx/html

# Copia configuración custom (opcional)
# COPY nginx.conf /etc/nginx/nginx.conf

# Expone el puerto 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
