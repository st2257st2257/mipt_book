<script setup lang="ts">

import {ref, type Ref, onMounted, reactive, type Reactive, provide} from 'vue';

interface UserName {
  first_name: string,
  last_name: string,
  third_name: string
}
interface BBNumber {
  username: string,
  number_bb: number
}

// DO THIS
const web_site = "mipt.site";
// const web_site = "localhost";
// const web_site = "127.0.0.1";

let token = ref<string|null>(null);

let username = ref<string|null>(null);
let number_bb = ref<string|null>(null);


onMounted(()=>{
  username.value = localStorage.getItem("username");
  loadBBNumber();
});

async function loadBBNumber(){
  try {
    const response = await fetch("https://" + web_site + ":8000/base-info/users_wallet/?username=" + username.value,{
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

    // username.value = data_number[0].username;
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

</script>

<template>
  <div class="container-head">
    <div class="left-element button-lk">ББ: {{number_bb}} единиц</div>
    <div class="right-element button-lk">Личный кабинет</div>
  </div>
</template>

<style scoped>
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
