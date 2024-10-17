FROM nginx:latest

COPY nginx.conf /etc/nginx/nginx.conf

COPY swagger-config /usr/share/nginx/html

RUN apt-get update && apt-get install -y curl && apt-get clean

