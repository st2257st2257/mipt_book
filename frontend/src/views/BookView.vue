<script setup lang="ts">
import {onMounted, ref, provide, inject} from 'vue'
import { useRouter } from 'vue-router';

import Header from "@/components/TheHeader.vue";
import BookAudience from "@/components/book/BookAudience.vue";
import BookTime from "@/components/book/BookTime.vue";
import BookAmount from "@/components/book/BookAmount.vue";
import type {IAudience} from "@/classes/Interfaces";

let form_audience_name = ref<String>("");
let form_number_bb = ref<Number>(0);
let form_pair_number = ref<Number>(1);
let form_token = ref<String>("");
let form_time_slot = ref<String>("");

const router = useRouter();

interface User {
    username: string;
}

interface AudienceItem {
    number: string;
    description: string;
    audience_status: string;
}

interface ActualBookItem {
  audience: AudienceItem,
  user: User,
  number_bb: number,
  pair_number: number,
  date: string,
  booking_time: string,
  time_slot: string
}

function selectAudience(audience: IAudience) {
  form_audience_name.value = audience.number;
}
function selectAmount(amount: Number){
  form_pair_number.value = amount;
}
function selectTimeSlot(time_slot: String){
  form_time_slot.value = String(time_slot);
}

let token = ref<string|null>(null);
let username = ref<string|null>(null);
let open_number = ref<string|null>(null);

// DO THIS
// const web_site = "mipt.site";
// const web_site = "localhost";
// const web_site = "127.0.0.1";
const web_site = inject('web_site');

const showPopupAuthBBInfo = ref(false);
const showPopupBookingInfo = ref(false);
const showPopupAudNumberInfo = ref(false);
const showPopupTimeSlotInfo = ref(false);

onMounted(()=>{
  open_number.value = localStorage.getItem("open-number");
  token.value = localStorage.getItem("auth-token");
  username.value = localStorage.getItem("username");

  checkBookHistory();

  if (localStorage.getItem("open-number") == null) {
    localStorage.setItem("open-number", "1");
    router.push("/display/").then(()=>{
        router.go(0); // first go to display
    });
    console.log("Переброска на дисплей аудиторий");
  }
  else {
    localStorage.setItem("open-number", String(Number(open_number.value) + 1));
    console.log("Количество заходов на сайт: ", open_number.value);
  }


  if (localStorage.getItem("auth-token") == null) {
      setTimeout(()=>{
          showPopupBookingInfo_fun();
      }, 1000);
      setTimeout(()=>{
          router.push("/auth/login/").then(()=>{
            router.go(0); // force reload
          });
      }, 4000);
  }
  window.scrollTo({
    top: 1000,
    behavior: 'smooth'
  });
  // document.getElementById('your-element').scrollIntoView({ behavior: 'smooth' });
});

const showPopupBookingInfo_fun = () => {
  showPopupBookingInfo.value = true;
};

const hidePopupBookingInfo = () => {
  showPopupBookingInfo.value = false;
};


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
	'time_slot': form_time_slot.value,
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


async function checkBookHistory(){
  try {
    const response = await fetch("https://" + web_site + ":8000/base-info/book/?user=" + username.value,{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);

      if(response.status == 401){
        console.log(9);
      }
    }

    const data_number = await response.json() as ActualBookItem[];
        
    if (data_number.length > 0) {
	router.push("/book-history/");
    }

    console.log('Ответ от сервера header actual_book_items:', data_number);
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
      setTimeout(()=>{
          router.push("/book-history/").then(()=>{
            router.go(0); // force reload
          });
      }, 2000);
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

const showAuthBBInfo = () => { 
	showPopupAuthBBInfo.value = true; 
};
const hideAuthBBInfo = () => { showPopupAuthBBInfo.value = false; };

const showAudNumberInfo = () => { showPopupAudNumberInfo.value = true; };
const hideAudNumberInfo = () => { showPopupAudNumberInfo.value = false; };

const showTimeSlotInfo = () => { showPopupTimeSlotInfo.value = true; };
const hideTimeSlotInfo = () => { showPopupTimeSlotInfo.value = false; };

</script>

<template>
  <div style="padding-bottom: 70px;">
  <div class="centered-div">
    <Header />
	    <!-- <p style="color: red;">Сервис запущен в тестовом режиме, учитывает раписание занятий и стремиться к отображению максимально точной картины занятости. Однако часть студентов пока не осведомлена об этом удобном способе бронирования. Если выбранная аудитория занята, вам автоматически будет предложена другая подходящая аудитория.</p> -->
	    <p style="color: red;">Сервис запущен в тестовом режиме и в его работе возможны ошибки. Писать на почту: info@mipt.site</p>
    <form @submit.prevent="sendForm">

      <BookAudience @select-audience="selectAudience"/>
      <BookTime @select-time-slot="selectTimeSlot"/>
      <BookAmount @select-amount="selectAmount"/>

      <div class="container-head" style="height: 60px;">
        <div class="left-element">
		<h3>Автоматические ББ      <!--<img class="icon-pic image_for_click" src="@/assets/info.svg">--></h3>
        </div>
        <div class="right-element">
          <label class="toggle-switch">
            <input type="checkbox" required checked>
            <span class="slider"></span>
          </label>
	  <img @click="showAuthBBInfo()" class="icon-pic image_for_click" src="@/assets/info.svg">
        </div>
      </div>

      <input id="your-element" type="submit" class="button1" value="Забронировать" @click="showNotificationBooked();"><br><br>
    </form>
  </div>

    <div class="notification-container">
        <div class="notification" id="book_notification">
          <p>Вы забронировали аудиторию</p>
          <span class="notification-close" @click="hideNotification('book_notification')">×</span>
      </div>
  </div>

      <transition name="fade">
      <div v-if="showPopupBookingInfo" class="popup">
        <div class="popup-content">
            <h3>Для бронирования аудиторий необходимо авторизоваться с помощью почты МФТИ</h3>
	    <h5>К примеру: ivanov.ii@phystech.edu</h5>
	    <a href="https://mipt.site/auth/login/"><button style="background-color: #4caf50;color: white;padding: 10px 20px;border: none; border-radius: 5px; cursor: pointer; width:100%;">Авторизоваться</button></a>
        </div>
      </div>
    </transition>


            <transition name="fade-rate-info">
                <div v-if="showPopupAuthBBInfo" class="popup button-width">
                    <div class="popup-content">
			    <!-- <button @click="hideAuthBBInfo" style="background-color: #dc3545; width: 100%;  color: white;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;">Закрыть</button> -->
                        
			<p>
				<a href="https://mipt.site/info">ПОДРОБНЕЕ ТУТ</a>
			</p>
			
			<p>
				Баллы Бронирования (ББ) начилсяются студентам МФТИ для бронирования аудиторий. Всего не более 28 ед. и +4ББ/сутки. 
				При автоматиеском выставлении баллов
				бронирования система определяет число необходимых баллов для бронирования аудитории с шансом 90%. После чего списывает
				соответствующее число. Изначально 1ББ = 1паре, но со временем и загруженностью число может меняться.
			</p>
			<p>
				Совместное бронирование аудиторий позволяет делить число баллов бронирования на число студентов в аудитории.
			</p>

			<button @click="hideAuthBBInfo" style="background-color: #dc3545; width: 100%;  color: white;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;">Закрыть</button>
                    </div>
                </div>
        </transition>
	





  </div>
</template>

<style scoped>
@media (max-width: 768px) {
        .button-width {
                min-width: 80vw;
        }
}

@media (min-width: 768px) {
        .button-width {
                max-width: 30vw;
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

.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  z-index: 10;
}

.popup-content {
  max-height: 70vh; /*Adjust as needed */
  overflow-y: auto;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-active-rate-info,
.fade-leave-active-rate-info {
  transition: opacity 0.3s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-rate-info,
.fade-leave-to-rate-info {
  opacity: 0;
}


.icon-pic {
  width: 18px;
  float: right;
  border: 3px solid #ccc;
  border-radius: 10px;
  padding-left: 10px;
  padding-right: 10px;
}

.image_for_click{
  cursor: pointer;
}

html {
  scroll-behavior: smooth;
}

</style>
