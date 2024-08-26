upstream email {
    server email:8083;
}

upstream backend {
    server backend:8000;
}

upstream users {
    server users:8088;
}

server {
    listen 80;
    listen [::]:80;

    server_name _;
    server_tokens off;

    location /email {
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Url-Scheme $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_pass http://email;
    }

    location /backend {
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Url-Scheme $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_pass http://backend;
    }

    location /users {
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Url-Scheme $scheme;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_pass http://users;
    }

    location /static/ {
        alias  /static/;
        expires 15d;
    }

     location /media/ {
        alias  /media/;
        expires 7d;
    }
}
