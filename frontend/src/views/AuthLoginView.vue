<script setup lang="ts">
import '@/assets/auth.css'
import {ref} from "vue";
import {useRouter} from "vue-router";

const router = useRouter();

const username = ref<String>("");
const password = ref<String>("");

let error_message = ref<String>("");

async function sendForm(){
  try {
    const response = await fetch("https://mipt.site:8088" + "/token/",{
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        'username': username.value,
        'password': password.value
      })
    });

    const data = await response.json();
    console.log('Ответ от сервера:', data);

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);
      error_message.value = data?.non_field_errors[0] || "Ошибка авторизации";
    }


    if("token" in data){
      localStorage.setItem("auth-token", data.token);
      error_message.value = "Успешная авторизация!";
      setTimeout(()=>{
          router.push("/profile/").then(()=>{
            router.go(0); // force reload
          });
      }, 1000);
      return;
    }

  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

</script>

<template>
  <form @submit.prevent="sendForm">
    <h4>Введите логин</h4>
    <input type="text" name="username" v-model="username">
    <h4>Введите пароль</h4>
    <input type="password" name="password" v-model="password">
    <span style="margin: 8px">{{error_message}}</span>
    <input type="submit" value="Авторизоваться" class="button-auth">
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
