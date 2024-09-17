<script setup lang="ts">
import '@/assets/auth.css'



</script>

<template>
  <div class="centered-div">
    <h3 style="text-align: center">Сервис бронирования аудиторий МФТИ</h3>
    <RouterLink to="/auth/login/" class="button-auth">Авторизация</RouterLink>
    <RouterLink to="/auth/register/" class="button-auth">Регистрация</RouterLink>
    <RouterLink to="/auth/recover/" class="button-auth">Восстановить пароль</RouterLink>
  </div>
</template>

<style scoped>
.centered-div {
  /*text-align: center; Центрируем текст внутри div */
  padding: 20px; /*Добавляем отступы для лучшей читаемости */
  background-color: white; /*Цвет фона для наглядности */
  margin: 0 auto; /*Центрируем блок по горизонтали */
  padding-top: 30vh;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
