<script setup lang="ts">

import BookTime from "@/components/book/BookTime.vue";
import Header from "@/components/TheHeader.vue";
import BookAmount from "@/components/book/BookAmount.vue";
import BookAudience from "@/components/book/BookAudience.vue";

import {ref, type Ref, onMounted, reactive, type Reactive, defineExpose} from 'vue';
import type {IAudience} from "@/classes/Interfaces";
import { useRouter } from 'vue-router';

interface BookItem {
  audience: string,
  user: string,
  number_bb: number,
  pair_number: number,
  date: string,
  booking_time: string
}

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
  booking_time: string
}

let actual_book_items: Ref<ActualBookItem[]> = ref([]);

// const web_site = "mipt.site";
// const web_site = "localhost";
const web_site = "127.0.0.1";

let book_history: Ref<BookItem[]> = ref([]);

let bookings: Ref<
      Array<{
        audience: IAudience,
        number_bb: Number,
        pair_number: Number,
        date: String,
        booking_time: String,
        user: {
          username: String
        }
      }>
    > = ref([]);

let username = ref<string|null>(null);
let token = ref<string|null>(null);

onMounted(()=>{
  token.value = localStorage.getItem("auth-token");
  username.value = localStorage.getItem("username");
  if(token.value == null) return;
  loadBookHistory();
  loadActualBookHistory();
});


async function loadActualBookHistory(){
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
        // token.value = null;
        localStorage.removeItem("auth-token");
        localStorage.removeItem("username");
      }
    }

    const data_number = await response.json() as ActualBookItem[];
    actual_book_items.value = data_number;
    // audiences_gk.value = data_number.filter(item => item.building.name == 'ГК');
    // audiences_lk.value = data_number.filter(item => item.building.name == 'ЛК');

    // username.value = data_number[0].username;
    // number_bb.value = String(data_number[0].number_bb);

    console.log('Ответ от сервера header actual_book_items:', actual_book_items);
    console.log('Ответ от сервера header book_history.value[0]:', book_history.value[0]);
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

async function cancelBooking(audience_number: string){
  try {
    const response = await fetch("https://" + web_site + ":8000/stop_booking/",{
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: JSON.stringify({
        "type": "stop_booking",
        'token': token.value,
        'audience': audience_number // form_audience_name.value
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


async function loadBookHistory(){
  try {
    const response = await fetch("https://" + web_site + ":8000/base-info/history/?user=" + username.value,{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);

      if(response.status == 401){
        // token.value = null;
        localStorage.removeItem("auth-token");
        localStorage.removeItem("username");
      }
    }

    const data_number = await response.json() as BookItem[];
    book_history.value = data_number;
    // audiences_gk.value = data_number.filter(item => item.building.name == 'ГК');
    // audiences_lk.value = data_number.filter(item => item.building.name == 'ЛК');

    // username.value = data_number[0].username;
    // number_bb.value = String(data_number[0].number_bb);

    console.log('Ответ от сервера header data_number:', data_number);
    console.log('Ответ от сервера header book_history.value[0]:', book_history.value[0]);
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

</script>

<template>
  <div class="centered-div">
    <Header />

  </div>

    <h2>Актуальные бронирования:</h2>
    <table class="booking-table">
      <thead>
        <tr>
          <th>Дата</th>
          <th>Время</th>
          <th>Комната</th>
          <th>Номер пары</th>
          <th>Действие</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="actual_item in actual_book_items">
          <td>{{actual_item.date}}</td>
          <td>{{actual_item.booking_time.slice(0, 8)}}</td>
          <td>{{actual_item.audience.number}}</td>
          <td>{{actual_item.pair_number}}</td>
          <td><button class="cancel-button" @click="cancelBooking(actual_item.audience.number)">Завершить</button></td>
        </tr>
      </tbody>
     </table>

    <h2>История бронирования</h2>
    <table class="booking-table" style="padding-bottom: 70px;">
      <thead>
        <tr>
          <th>Дата</th>
          <th>Время</th>
          <th>Комната</th>
          <th>Номер пары</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="book in book_history">
          <td>{{book.date}}</td>
          <td>{{book.booking_time.slice(0, 8)}}</td>
          <td>{{book.audience}}</td>
          <td>{{book.pair_number}}</td>
        </tr>
      </tbody>
    </table>


</template>

<style scoped>

.table {
  display: flex;
}

.table-header {

}

    .booking-history {
      width: 80%;
      margin: 20px auto;
      border: 1px solid #ccc;
      border-radius: 5px;
      padding: 20px;
    }

    .booking-history h2 {
      margin-top: 0;
    }

    .booking-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }

    .booking-table th,
    .booking-table td {
      border: 1px solid #ccc;
      padding: 10px;
      text-align: left;
    }

    .booking-table th {
      background-color: #f2f2f2;
      font-weight: bold;
    }
.cancel-button {
  display: inline-block;
  padding: 8px 12px;
  background-color: #dc3545; /*Красный цвет */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.cancel-button:hover {
  background-color: #c82333; /*Более темный красный цвет */
}

.cancel-button:active {
  background-color: #b0212b; /*Еще более темный красный цвет */
  transform: translateY(2px); /*Эффект нажатия */
}

</style>
