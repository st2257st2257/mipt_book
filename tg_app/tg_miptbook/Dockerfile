# Используем образ Node.js с нужной версией (замените на актуальную)
FROM node:18

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем package.json и package-lock.json для установки зависимостей
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем остальные файлы приложения
COPY . .

# Экспонируем порт, на котором работает React-приложение (обычно 3000)
EXPOSE 3000

# Запускаем приложение с помощью npm start
# CMD ["npm", "start"]
# CMD ["HTTPS=true", "npm", "start"]
#CMD ["sh", "-c", "HTTPS=true npm start"]
CMD ["sh", "-c", "HTTPS=true SSL_CRT_FILE=mipt.crt SSL_KEY_FILE=mipt.key npm start"]
