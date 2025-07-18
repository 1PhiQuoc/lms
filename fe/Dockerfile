# Stage 1: Build Angular
FROM node:20 AS build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build -- --configuration production --base-href=/admin/

# Stage 2: Serve với NGINX
FROM nginx:1.25-alpine
RUN rm -rf /usr/share/nginx/html/*
COPY --from=build /app/dist/fe /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
