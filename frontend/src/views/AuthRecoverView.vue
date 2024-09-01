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
  <form action="/user-api/register/" method="post">
    <h4>Введите почту</h4>
    <input type="email" name="email" v-model="email">
    <input type="submit" value="Отправить" class="button-auth">
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