<script setup lang="ts">

import Header from "@/components/TheHeader.vue";
import {ref, type Ref, onMounted, reactive, type Reactive} from 'vue';

interface UserName {
  first_name: string,
  last_name: string,
  third_name: string
}
interface Preference {
  name: string,
  description: string
}

let token = ref<string|null>(null);

const user_name: Reactive<UserName> = reactive({
  first_name: "", last_name: "", third_name: ""
});
let institute_group: Ref<string|null> = ref(null);
let book_rating: Ref<number> = ref(1);
let preferences: Ref<Preference[]> = ref([]);

let preferencesIcons = {
  "Тишина": "",
  "Свежий воздух": "@/assets/cloud.svg",
  "Тихая музыка": ""
};

onMounted(()=>{
  token.value = localStorage.getItem("auth-token");

  if(token.value == null) return;
  loadInfo();
  loadPreferences();
});

async function loadInfo(){
  try {
    const response = await fetch("https://mipt.site:8088/get-info/",{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Token '+token.value
      },
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);
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

async function loadPreferences(){
  try {
    const response = await fetch("https://mipt.site:8088/base-info/preferences/",{
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

      <div class="class1">
        <div class="left-element" style="height: 100%">
          <div style="width: 100%;">
            <span>{{user_name.first_name}}</span><br>
            <span>{{user_name.last_name}}</span><br>
            <span>{{user_name.third_name}}</span>
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
        <h3>Рейтинг бронирования: <img class="icon-pic" src="@/assets/info.svg"></h3>
        <div style="display: flex; justify-content: space-around">
          <template v-for="index in 7">
            <div class="star" :class="{checked : index <= book_rating}"></div>
          </template>
        </div>
      </div>

      <div>
        <h3>Баллы бронирования</h3>
        <span> {{book_rating}} из 28 </span><br>
        <span style="color: grey; font-size: 0.8em"> следующие +4 балла через 15 часов</span>
      </div>

      <div>
        <h3>Предпочтения:  <img class="icon-pic" src="@/assets/edit.svg" alt="Edit"></h3>
          <template v-for="preference in preferences">
            <div>
              {{preference.name}}
<!--              <img class="icon-pic" :src="preferencesIcons[preference.name]" alt="">-->
            </div>
          </template>
      </div>
    </template>
  </div>
</template>

<style scoped>

.icon-pic {
  width: 16px;
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

.centered-div {
  /*text-align: center; Центрируем текст внутри div */
  padding: 20px; /*Добавляем отступы для лучшей читаемости */
  margin: 0 auto; /*Центрируем блок по горизонтали */
  background-color: white; /*Цвет фона для наглядности */
}

/*Стили для мобильных устройств (экраны меньше 768px) */
@media (max-width: 768px) {
  .centered-div {
    width: 80%; /*Растягиваем на всю ширину экрана */
  }
}

/*Стили для планшетов и компьютеров (экраны от 768px) */
@media (min-width: 768px) {
  .centered-div {
    width: 40%; /*Ограничиваем ширину до 80% */
  }
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
</style>