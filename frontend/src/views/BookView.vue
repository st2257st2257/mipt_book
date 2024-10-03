<script setup lang="ts">
import {onMounted, ref} from 'vue'

import Header from "@/components/TheHeader.vue";
import BookAudience from "@/components/book/BookAudience.vue";
import BookTime from "@/components/book/BookTime.vue";
import BookAmount from "@/components/book/BookAmount.vue";
import type {IAudience} from "@/classes/Interfaces";

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

// const web_site = "mipt.site";
// const web_site = "localhost";
const web_site = "127.0.0.1";

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
        'token': token.value,
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

  function showNotificationBooked() {
      if (document.getElementById("book_notification")) {
        document.getElementById("book_notification")?.classList.add("show");
        document.getElementById("book_notification")?.classList.add("good_action");
      } else {
        console.error('Элемент с id "' + "book_notification" + '" не найден');
      }
      setTimeout(hideNotification, 2000, "book_notification");
    }

  function showNotification_id(audience_number: string) {
      if (document.getElementById(String(audience_number))) {
        document.getElementById(String(audience_number))?.classList.add("show");
        document.getElementById(String(audience_number))?.classList.add("good_action");

        let array_id = ["date_", "time_", "number_", "pair_", "button_"];
        for (let i = 0; i < 5; i++) {
            if (document.getElementById(array_id[i] + String(audience_number))) {
                document.getElementById(array_id[i] + String(audience_number))?.classList.add("item_hidden");
            }
            else {
                console.error('Элемент с id "' + array_id[i] + audience_number + '" не найден');
            }
        }
      } else {
        console.error('Элемент с id "' + audience_number + '" не найден');
      }

      setTimeout(hideNotification, 2000, String(audience_number));
    }

    function showNotification(notificationId: string) {
      if (document.getElementById(notificationId)) {
        document.getElementById(notificationId)?.classList.add("show");
      } else {
        console.error('Элемент с id "' + notificationId + '" не найден');
      }

    }

    function hideNotification(notificationId: string) {
      if (document.getElementById(notificationId)) {
        document.getElementById(notificationId)?.classList.remove("show");
      } else {
        console.error('Элемент с id "' + notificationId + '" не найден');
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

      <input type="submit" class="button1" value="Забронировать" @click="showNotificationBooked();"><br><br>
    </form>
  </div>

    <div class="notification-container">
        <div class="notification" id="book_notification">
          <p>Вы забронировали аудиторию</p>
          <span class="notification-close" @click="hideNotification('book_notification')">×</span>
      </div>
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

    .notification-container {
      position: fixed;
      top: 10px;
      right: 10px;
      z-index: 1000;
    }

    .good_action {
        background-color: #cfc;
    }

    .warning_action {
        background-color: #ffc;
    }

    .bad_action {
        background-color: #fcc;
    }

    .notification {
      border-radius: 5px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
      padding: 15px;
      margin-bottom: 10px; /*Отступ между уведомлениями */
      opacity: 0;
      transition: opacity 0.3s ease-in-out;
      display: none;
    }

    .notification.show {
      opacity: 1;
      display: block;
    }

    .notification-close {
      position: absolute;
      top: 10px;
      right: 10px;
      cursor: pointer;
    }

</style>
