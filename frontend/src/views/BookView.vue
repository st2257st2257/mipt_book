<script setup lang="ts">
import {onMounted, ref} from 'vue'

import Header from "@/components/TheHeader.vue";
import BookAudience from "@/components/book/BookAudience.vue";
import BookTime from "@/components/book/BookTime.vue";
import BookAmount from "@/components/book/BookAmount.vue";
import type {IAudience} from "@/classes/Interfaces";

let form_user = ref<String>("st2257");
let form_audience_name = ref<String>("");
let form_number_bb = ref<Number>(0);
let form_pair_number = ref<Number>(1);
let form_token = ref<String>("");

function selectAudience(audience: IAudience) {
  form_audience_name.value = audience.number;
}
function selectAmount(amount: Number){
  form_pair_number.value = amount;
}

let token = ref<string|null>(null);
let username = ref<string|null>(null);

const web_site = "mipt.site";
// const web_site = "localhost";
// const web_site = "127.0.0.1";

onMounted(()=>{
  token.value = localStorage.getItem("auth-token");
  username.value = localStorage.getItem("username");
});

async function sendForm(){
  try {
    const response = await fetch("https://" + web_site + ":8000/book/",{
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: JSON.stringify({
        "type": "book_audience",
        'token': "73d854268d8c273874ec592f7b2e03f6276093df", //token.value,
        'audience': form_audience_name.value,
        'number_bb': form_number_bb.value,
        'pair_number': form_pair_number.value,
        'user': username.value
      })
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);
    }
    if (response.ok) {
        const data = await response.json();
        console.log('Ответ от сервера:', data);
    } else {
        console.error('Ошибка запроса:', response.status);
    }

  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

async function sendForm_new() {
  try {
    const data = {
      "type": "book_audience",
      "token": "73d854268d8c273874ec592f7b2e03f6276093df",
      "audience": "510",
      "number_bb": 0,
      "pair_number": "3",
      "user": "st2257"
    };

    const params = new URLSearchParams();

    // Добавляем CSRF-токен
    // params.append('csrfmiddlewaretoken', 'JYllHBzH0ofWvcYOIMGGFj5lDPS7Oi6nLq3SO1jchoRPs04lwfCMhUvrijTXtU1q');

    // Добавляем остальные данные из объекта data
    //for (const key in data) {
    //  params.append(String(key), data[key].toString());
    //}
    params.append('type', 'book_audience');
    params.append('token', '73d854268d8c273874ec592f7b2e03f6276093df');
    params.append('audience', '512');
    params.append('number_bb', '0');
    params.append('pair_number', '3');
    params.append('user', 'st2257');



    const response = await fetch("https://" + web_site + ":8000/book/", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: params.toString()
    });

    // ... остальной код ...
  } catch (error) {
    // ...
  }
}

</script>

<template>
  <div class="centered-div">
    <Header />

    <form @submit.prevent="sendForm">

      <BookAudience @select-audience="selectAudience"/>
      <BookTime />
      <BookAmount @select-amount="selectAmount"/>

      <div class="container-head" style="height: 60px;">
        <div class="left-element">
          <h3>Автоматические ББ</h3>
        </div>
        <div class="right-element">
          <label class="toggle-switch">
            <input type="checkbox">
            <span class="slider"></span>
          </label>
        </div>
      </div>

      <input type="submit" class="button1" value="Забронировать"><br><br>
    </form>
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
