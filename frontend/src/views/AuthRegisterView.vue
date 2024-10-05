<script setup lang="ts">
import '@/assets/auth.css'
import {ref} from "vue";

// DO THIS
const web_site = "mipt.site";
// const web_site = "localhost";
// const web_site = "127.0.0.1";

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

  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

</script>

<template>
	<div class="center-div-reg">
		<!-- <h2>Регистрация в сервисе бронирования</h2>-->
		<form @submit.prevent="sendForm">
			<h2>Регистрация</h2>
  			<h4>Введите логин</h4>
  			<input type="text" name="username" v-model="username">
  
			<h4>Введите почту</h4>
  			<input type="email" name="email" v-model="email">
 
			<h4>Введите пароль</h4>
  			<input type="password" name="password" v-model="password">
  
			<h4>Повторите пароль</h4>
  			<input type="password" v-model="password_repeat">
  
			<span style="color: red">{{error_message}}</span>
  			<input type="submit" value="Зарегистрироваться" class="button-auth center-button">
		</form>
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
	padding-top: 20vh;
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

</style>
