# Étape 1 : build de l'app
FROM node:22-alpine AS build
WORKDIR /app
 
COPY package*.json ./
RUN npm ci
 
COPY . .
RUN npm run build
 
# Étape 2 : serveur Nginx pour servir les fichiers
FROM nginx:alpine
 
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
 
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]