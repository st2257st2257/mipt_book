<script setup lang="ts">
import '@/assets/auth.css'
import {ref, provide, inject} from "vue";

// DO THIS
// const web_site = "mipt.site";
// const web_site = "localhost";
// const web_site = "127.0.0.1";
const web_site = inject('web_site_register');

let username = ref<String>("");
let email = ref<String>("");
let password = ref<String>("");
let password_repeat = ref<String>("");

let error_message = ref<String>("");

function validateForm(): {e: Boolean, msg: String} {
  if(password.value != password_repeat.value)
    return {e: false, msg: "Неправильно повторили пароль"};

  return {e: true, msg: ""};
}

import { useRouter } from 'vue-router';
const router = useRouter();

async function sendForm(){
  const validate = validateForm() as {e: Boolean, msg: String};
  if (!validate.e) {
    error_message.value = validate.msg;
    return;
  }

  try {
    const response = await fetch("https://" + web_site + ":8088/register/",{
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        'username': username.value,
        'email': email.value,
        'password': password.value
      })
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);
    }

    const data = await response.json();
    console.log('Ответ от сервера:', data);
    showNotification("register_notification");
    setTimeout(hideNotification, 2000, "register_notification");
    setTimeout(router.push, 1000, '/auth/login');

  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}


    function showNotification(notificationId: string) {
      if (document.getElementById(notificationId)) {
        document.getElementById(notificationId)?.classList.add("show");
        document.getElementById(notificationId)?.classList.add("good_action");
      } else {
        console.error('Элемент с id "' + notificationId + '" не найден');
      }
    }
    function hideNotification(notificationId: string) {
      if (document.getElementById(notificationId)) {
        document.getElementById(notificationId)?.classList.remove("show");
        document.getElementById(notificationId)?.classList.add("good_action");
      } else {
        console.error('Элемент с id "' + notificationId + '" не найден');
      }
    }
	
</script>

<template>
	<div class="center-div-reg">
		<!-- <h2>Регистрация в сервисе бронирования</h2>-->
		<form @submit.prevent="sendForm">
			<h2>Регистрация</h2>
  			<h4>Введите логин</h4>
  			<input class="center-button reg-input" type="text" name="username" v-model="username">
  
			<h4>Введите почту</h4>
  			<input class="center-button reg-input" type="email" name="email" v-model="email">
 
			<h4>Введите пароль</h4>
  			<input class="center-button reg-input" type="password" name="password" v-model="password">
  
			<h4>Повторите пароль</h4>
  			<input class="center-button reg-input" type="password" v-model="password_repeat">
  
			<span style="color: red">{{error_message}}</span>
  			<input type="submit" value="Зарегистрироваться" class="button-auth center-button">
		</form>

    <div class="notification-container">
        <div class="notification" id="register_notification">
            <p>Вы успешно зарегистрировались</p>
            <p>Код подтверждения отправлен на почту</p>
            <span class="notification-close" @click="hideNotification('register_notification')">×</span>
        </div>
    </div>
		
	</div>
</template>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.center-div-reg{
	padding-top: 10vh;
}

/*Стили для мобильных устройств (экраны меньше 768px) */
@media (max-width: 768px) {
    .center-button {
        width: 80%; /*Растягиваем на всю ширину экрана */
    }
}

/*Стили для планшетов и компьютеров (экраны от 768px) */
@media (min-width: 768px) {
    .center-button {
        width: 30%; /*Ограничиваем ширину до 80% */
    }
}

    .notification-container {
      position: fixed;
      top: 10px;
      right: 10px;
      z-index: 1000;
    }
    .good_action {
        background-color: #cfc;
    }
    .warning_action {
        background-color: #ffc;
    }
    .bad_action {
        background-color: #fcc;
    }
    .notification {
      border-radius: 5px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
      padding: 15px;
      margin-bottom: 10px; /*Отступ между уведомлениями */
      opacity: 0;
      transition: opacity 0.3s ease-in-out;
      display: none;
    }
    .notification.show {
      opacity: 1;
      display: block;
    }
    .notification-close {
      position: absolute;
      top: 10px;
      right: 10px;
      cursor: pointer;
    }
/*Базовые стили */
.reg-input {
  /* width: 100%; */
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box; /*Чтобы паддинг и бордер не увеличивали ширину */
  font-size: 16px;
  margin-bottom: 10px; /*Отступ снизу */
}
/*Стили при фокусе */
.reg-input:focus {
  outline: none; /*Убираем стандартный контур */
  border-color: #007bff; /*Синий цвет границы при фокусе */
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.2); /*Небольшой эффект тени */
}
/*Стили при ошибке */
.reg-input.error {
  border-color: #dc3545; /*Красный цвет границы при ошибке */
  box-shadow: 0 0 5px rgba(220, 53, 69, 0.2); /*Красная тень при ошибке */
}

	
</style>
