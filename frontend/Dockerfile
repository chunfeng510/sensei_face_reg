# ---- Stage 1: Build React App ----
FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# 使用相對路徑 /api，讓 nginx 反向代理處理
ENV REACT_APP_API_URL=/api

RUN npm run build

# ---- Stage 2: Serve with Nginx ----
FROM nginx:alpine

# 複製編譯後的靜態檔案
COPY --from=build /app/build /usr/share/nginx/html

# 複製 nginx 設定
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
