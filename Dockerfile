FROM nginx:1.17

COPY nginx.conf /etc/nginx/nginx.conf
COPY content /app/content
