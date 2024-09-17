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
	<div class="center-dev-recover">
		<!-- <h2>Восстановление пароля</h2>-->
  		<form action="/user-api/register/" method="post">
			<h2>Восстановление пароля</h2>
    			<h4>Введите почту</h4>
    			<input type="email" name="email" v-model="email">
    			<input type="submit" value="Отправить" class="button-auth center-button">
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

.center-dev-recover{
	padding-top: 30vh;
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
