<script setup lang="ts">

import BookTime from "@/components/book/BookTime.vue";
import Header from "@/components/TheHeader.vue";
import BookAmount from "@/components/book/BookAmount.vue";
import BookAudience from "@/components/book/BookAudience.vue";

import {ref, type Ref, onMounted, reactive, type Reactive, defineExpose} from 'vue';
import type {IAudience} from "@/classes/Interfaces";

interface BookItem {
  audience: string,
  user: string,
  number_bb: number,
  pair_number: number,
  date: string,
  booking_time: string
}

const web_site = "mipt.site";
// const web_site = "localhost";
// const web_site = "127.0.0.1";

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
});


async function loadActualBookHistory(){
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
    // console.log('Ответ от сервера header number_bb:', number_bb);
    // console.log('Ответ от сервера header username.value:', username.value);
    // console.log('Ответ от сервера header number_bb.value:', number_bb.value);
    // user_name.first_name = data.name.first_name;
    // user_name.last_name = data.name.last_name;
    // user_name.third_name = data.name.third_name;
    // institute_group.value = data.institute_group;
    // book_rating.value = data.book_rate;
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
    // console.log('Ответ от сервера header number_bb:', number_bb);
    // console.log('Ответ от сервера header username.value:', username.value);
    // console.log('Ответ от сервера header number_bb.value:', number_bb.value);
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
  <div class="centered-div">
    <Header />

  </div>

    <h2>История бронирования</h2>
    <table class="booking-table">
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
          <td>{{book.booking_time}}</td>
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


</style>
