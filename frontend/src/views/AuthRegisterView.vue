<script setup lang="ts">
import '@/assets/auth.css'
import {ref} from "vue";

let username = ref<String>("");
let email = ref<String>("");
let password = ref<String>("");
let password_repeat = ref<String>("");

enum AuthError {
  OK, RepeatPasswordWrong
}

const AuthErrorMsg = {
  OK : "",
  RepeatPasswordWrong : "Неправильно "
}

// function validate(): {e: AuthError, msg: String}{
//
// }

</script>

<template>
<form action="https://mipt.site:8088/register/" method="post">
  <h4>Введите логин</h4>
  <input type="text" name="username" v-model="username">
  <h4>Введите почту</h4>
  <input type="email" name="email" v-model="email">
  <h4>Введите пароль</h4>
  <input type="password" name="password" v-model="password">
  <h4>Повторите пароль</h4>
  <input type="password" v-model="password_repeat">
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