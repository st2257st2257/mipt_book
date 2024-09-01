<script setup lang="ts">
import '@/assets/auth.css'
import {ref} from "vue";

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
    const response = await fetch("/user-api/register/",{
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
<form @submit.prevent="sendForm">
  <h4>Введите логин</h4>
  <input type="text" name="username" v-model="username">
  <h4>Введите почту</h4>
  <input type="email" name="email" v-model="email">
  <h4>Введите пароль</h4>
  <input type="password" name="password" v-model="password">
  <h4>Повторите пароль</h4>
  <input type="password" v-model="password_repeat">
  <span style="color: red">{{error_message}}</span>
  <input type="submit" value="Зарегистрироваться" class="button-auth">
</form>
</template>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>