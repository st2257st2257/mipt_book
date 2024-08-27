     const { createProxyMiddleware } = require('http-proxy-middleware');
     const fs = require('fs');
     const path = require('path');

     module.exports = function(app) {
       app.use(
         createProxyMiddleware('/api', { // Замените '/api' на свой маршрут, если нужно
           target: 'https://localhost:3000', // Ваш адрес и порт
           changeOrigin: true,
           ssl: {
             cert: fs.readFileSync(path.join(__dirname, 'mipt.crt')),
             key: fs.readFileSync(path.join(__dirname, 'mipt.key'))
           }
         })
       );
     };

