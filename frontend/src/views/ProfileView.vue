<script setup lang="ts">

import Header from "@/components/TheHeader.vue";
import {ref, type Ref, onMounted, reactive, type Reactive} from 'vue';

interface BBNumber {
  username: string,
  number_bb: number
}
interface UserName {
  first_name: string,
  last_name: string,
  third_name: string
}
interface Preference {
  name: string,
  description: string
}

let username = ref<string|null>(null);
let number_bb = ref<string|null>(null);

let token = ref<string|null>(null);

const user_name: Reactive<UserName> = reactive({
  first_name: "", last_name: "", third_name: ""
});
let institute_group: Ref<string|null> = ref(null);
let book_rating: Ref<number> = ref(1);
let preferences: Ref<Preference[]> = ref([]);


type KeyValuePair = [string, string];

let preferencesIcons: Record<string, string> = {
  "Тишина": "@/assets/cloud.svg",
  "Свежий воздух": "@/assets/cloud.svg",
  "Тихая музыка": "@/assets/cloud.svg"
};

onMounted(()=>{
  token.value = localStorage.getItem("auth-token");
  username.value = localStorage.getItem("username");
  if(token.value == null) return;
  loadInfo();
  loadPreferences();
  loadBBNumber();

});

import { useRouter } from 'vue-router';

const router = useRouter();

async function logout() {
  try {
    if (1 == 1) {
      // Удалите токен из LocalStorage
      localStorage.removeItem('auth-token');
      // Перенаправьте пользователя на страницу входа
      // this.$router.push('auth');
      // this.router.push({ path: 'auth' });
      // router.push('auth');
      router.go(0);
    } else {
      // Обработайте ошибку
    }
  } catch (error) {
    // Обработайте ошибку
  }
}

async function loadInfo(){
  try {
    const response = await fetch("https://mipt.site:8088" + "/get-info/",{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token '+token.value
      },
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);

      if(response.status == 401){
        token.value = null;
        localStorage.removeItem("auth-token");
      }
    }

    const data = await response.json() as {
      username: string,
      name: UserName,
      email: string,
      book_rate: number,
      institute_group: string,
      user_role: string
    };

    console.log('Ответ от сервера:', data);
    user_name.first_name = data.name.first_name;
    user_name.last_name = data.name.last_name;
    user_name.third_name = data.name.third_name;
    institute_group.value = data.institute_group;
    book_rating.value = data.book_rate;
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

async function loadBBNumber(){
  try {
    const response = await fetch("https://mipt.site:8000/base-info/users_wallet/?username=st2257",{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);

      if(response.status == 401){
        token.value = null;
        localStorage.removeItem("auth-token");
      }
    }

    const data_number = await response.json() as BBNumber[];

    username.value = data_number[0].username;
    number_bb.value = String(data_number[0].number_bb);

    console.log('Ответ от сервера header data_number:', data_number[0]);
    console.log('Ответ от сервера header username:', username);
    console.log('Ответ от сервера header number_bb:', number_bb);
    console.log('Ответ от сервера header username.value:', username.value);
    console.log('Ответ от сервера header number_bb.value:', number_bb.value);
    // user_name.first_name = data.name.first_name;
    // user_name.last_name = data.name.last_name;
    // user_name.third_name = data.name.third_name;
    // institute_group.value = data.institute_group;
    // book_rating.value = data.book_rate;
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

async function loadPreferences(){
  try {
    const response = await fetch("https://mipt.site:8088" + "/base-info/preferences/",{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token '+token.value
      },
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);
    }

    const data = await response.json() as Preference[];
    console.log('Ответ от сервера:', data);

    preferences.value = data;

  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

</script>

<template>
  <div class="centered-div">
    <div v-if="token == null">
      <h3>Для доступа в личный кабинет нужно авторизоваться</h3>
    </div>

    <template v-else>
      <Header />

      <div class="class1" style="font-size: 24px;">
        <div class="left-element" style="height: 100%">
          <div style="width: 100%;">
            <span>{{user_name.first_name}}</span><br class="half-line-break">
            <div class="full_name_div"></div>
	    <span>{{user_name.third_name}}</span><br class="half-line-break">
            <div class="full_name_div"></div>
	    <span>{{user_name.last_name}}</span>
            <img class="icon-pic" src="@/assets/edit.svg" alt="Edit">
            <br>
          </div>
          <div style="position:absolute; bottom: 0; width: 100%">
            <br>
            <span>{{institute_group}}</span>
            <img class="icon-pic" src="@/assets/edit.svg" alt="Edit">
          </div>
        </div>
        <div class="right-element">
          <img src="@/assets/sania.png" class="profile-pic" alt="Ваша фотография">
        </div>
      </div>

      <div>
        <p style="font-size: 24px;">Рейтинг бронирования: <img class="icon-pic" src="@/assets/info.svg"></p>
        <div style="display: flex; justify-content: space-around">
          <template v-for="index in 7">
            <div class="star" :class="{checked : index <= book_rating}"></div>
          </template>
        </div>
      </div>

      <div>
        <p style="font-size: 24px;">Баллы бронирования</p>
        <span style="font-size: 18px;"> {{number_bb}} из 28 баллов</span><br>
        <span style="color: grey; font-size: 12px;"> следующие +4 балла через 15 часов</span>
      </div>

      <div>
        <p style="font-size: 24px;">Предпочтения:  <img class="icon-pic" src="@/assets/edit.svg" alt="Edit"></p>
          <template v-for="preference in preferences">
            <div style="font-size: 18px;">
              {{preference.name}}
	      <img class="icon-pic" :src="preferencesIcons[preference.name]" alt="">
            </div>
          </template>
      </div>
      <div style="padding-top: 10px;"><button class="logout-button" @click="logout">Выйти</button></div>
    </template>
  </div>
</template>

<style scoped>

.icon-pic {
  padding-left: 10px;
  width: 18px;
  float: right;
}


.star.checked {
  background: #F8CA00;
}

.star {
  display: inline-block;

  width: 32px;
  aspect-ratio: 1;
  background: #242424;
  clip-path: polygon(50% 0,
  calc(50%*(1 + sin(.4turn))) calc(50%*(1 - cos(.4turn))),
  calc(50%*(1 - sin(.2turn))) calc(50%*(1 - cos(.2turn))),
  calc(50%*(1 + sin(.2turn))) calc(50%*(1 - cos(.2turn))),
  calc(50%*(1 - sin(.4turn))) calc(50%*(1 - cos(.4turn)))
  );
  /* or more simple
  clip-path: polygon(50% 0,79% 90%,2% 35%,98% 35%,21% 90%);
   */
}

.profile-pic {
  border-radius: 32px;
}

.class1 {
  position: relative;
  height: 130px;
}

.container-head {
  position: relative; /* Позиционирование относительно контейнера */
  height: 100px; /* Высота контейнера (для демонстрации) */
}

.left-element, .right-element {
  position: absolute;
  top: 50%; /* Выравниваем по вертикали по центру */
  transform: translateY(-50%); /* Корректировка вертикального выравнивания */
}

.left-element {
  left: 0; /* Привязываем к левому краю */
}

.right-element {
  right: 0; /* Привязываем к правому краю */
}

.half-line-break {
  height: 0.5em;
}

.full_name_div {
	padding-top: 2px;
}

/*Базовые стили */
.logout-button {
  display: inline-block;
  padding: 10px 20px;
  background-color: #dc3545; /*Красный цвет */
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

/*Стили при наведении курсора */
.logout-button:hover {
  background-color: #c82333; /*Более темный красный цвет */
}

/*Стили при нажатии */
.logout-button:active {
  background-color: #b0212b; /*Еще более темный красный цвет */
  transform: translateY(2px); /*Небольшой эффект нажатия */
}

</style>
