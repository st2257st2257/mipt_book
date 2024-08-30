<script setup lang="ts">
import '@/assets/auth.css'
import {ref} from "vue";

let username = ref<String>("");
let password = ref<String>("");

</script>

<template>
  <form action="https://mipt.site:8088/token/" method="post">
    <h4>Введите логин</h4>
    <input type="text" name="username" v-model="username">
    <h4>Введите пароль</h4>
    <input type="password" name="password" v-model="password">
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