<script setup lang="ts">

import Header from "@/components/TheHeader.vue";
import {ref, type Ref, onMounted, reactive, type Reactive, defineExpose, provide, inject, defineComponent} from 'vue';
import { useRouter } from 'vue-router';

interface Pair {
  name: string,
  time_slot_index: number,
  week_day_index: number,
  description: string,
}

interface SearchItem {
  name: string,
  description: string,
  pair: Pair,
  owner_user_wallet: string,
  audience_number: string,
}

// DO THIS
// const web_site = "mipt.site";
// const web_site = "localhost";
// const web_site = "127.0.0.1";
const web_site = inject('web_site');

const router = useRouter();

let token = ref<string|null>(null);
let username = ref<string|null>(null);
let search_data: Ref<SearchItem[]> = ref([]);
let search_text = ref<string|null>(null);

const week_day_arr = [
	    "Понедел.",
        "Вторник",
        "Среда",
        "Четвер",
        "Пятница",
        "Суббота",
        "Воскрес."
      ];

const time_slot_arr = [
        "09:00",
        "10:45",
        "12:20",
        "13:45",
        "15:30",
        "17:05",
        "18:35",
        "20:00",
        "22:00",
        "23:59",
        "01:30",
        "03:00",
        "04:30",
        "06:00"
      ];

onMounted(()=>{
  token.value = localStorage.getItem("auth-token");
  username.value = localStorage.getItem("username");
  // loadSearch("Б02-");
});


async function loadSearch(){
  try {
    const response = await fetch("https://" + web_site + ":8000/base-info/event_item/?search_text="+search_text.value,{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);

      if(response.status == 401){
        localStorage.removeItem("auth-token");
      }
    }

    const data_number = await response.json() as SearchItem[];
    search_data.value = data_number;

    console.log('Ответ от сервера header data_number:', data_number);
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}


</script>

<template>
<div class="container-search">
    <div class="centered-div-back">
        <p class="above_title">Поиск по парам:</p>
        <form @submit.prevent="loadSearch">
            <div style="display: flex;">
                <div style="border-radius: 10px;">
                    <input type="text" class="container-search-text" id="scales" name="scales" v-model="search_text" placeholder="Б02-003, Загряд, Мат ан..."/>
                </div>
                <div class="container-search-for-button">
                    <button class="container-search-button" type="submit">Искать</button>
                </div>
            </div>
		</form>
	</div>
</div>

<div>
    <h1>Результат поиска:</h1>
    <template v-for="search_item in search_data">
        <div class="container-res-item">
            <div class="info-container" style="display: flex; flex-direction: column; flex-wrap: wrap; padding-left: 3vw; max-width: 40vw;">
                <div><p>{{search_item.name}}</p></div>
                <div><p> Ауд. {{search_item.audience_number}}</p></div>
            </div>
            <div class="time-container">
                <div class="container-show-time">{{ week_day_arr[search_item.pair.week_day_index-1] }}</div>
                <div class="container-show-time">{{ time_slot_arr[search_item.pair.time_slot_index-1] }}</div>
            </div>
        </div>



	    <!-- <div style="padding-top: 10px;">
            <p>Мероприятие: {{search_item.name}}</p>
            <p>Описание: {{search_item.description}}</p>
            <p>Владелец: {{search_item.owner_user_wallet}}</p>
            <p>Пара: {{search_item.pair.name}}</p>
            <p>Временной слот: {{search_item.pair.time_slot_index}}</p>
            <p>День недели: {{search_item.pair.week_day_index}}</p>
            <p>Описание пары: {{search_item.pair.description}}</p>
        </div> -->
    </template>
</div>

</template>

<style scoped>

.container-search {
  background-image: url('@/assets/back_1.jpg');
}

.centered-div-back {
  padding: 20px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .media-container {
  	min-width: 90vw;
  }
  .container-search-button {
    min-width: 20vw;
    border-radius: 10px;
    border: none;
  }
  .container-res-item {
    min-height: 20vw;
  }
  .container-show-time {
    min-width: 20vw;
    min-height: 7.5vw;
  }
  .container-search-text {
    min-height: 7.5vw;
    min-width: 65vw;
  }
  .container-search-for-button {
    
  }
}

@media (min-width: 768px) {
  .media-container {
    min-width: 40vw;
  }
  .container-search-button {
    min-width: 20vw;
    border-radius: 10px;
    border: none;
  }
  .container-res-item {
    height: 10vw;
  }
  .container-show-time {
    min-width: 10vw;
    min-height: 3.75vw;
  }
  .container-search-text {
    min-height: 3.75vw;
    min-width: 65vw;
  }
  .container-search-for-button {
    
  }
}

.container-search-text {
  font-size: 18px;
  padding-left: 10px;
  border-radius: 10px;
}

.container-search-button {
  height: 100%;
  color: white;
  font-size: 16px;
  background-color: #275ff2;
}

.above_title {
  color: white;
  font-size: 60px;
}

.container-res-item {
  padding-top: 10px;
  width: 95%;
  display: flex;
  justify-content: space-between;

  background-color: #fefdf9;
  min-width: 90vw;
  font-size: 22px;
  top: 50%;
  left: 50%;
  border: 1px solid black;
  border-radius: 10px;
}

.container-show-time {
  color: white;
  background-color: #275ff2;
  border-radius: 10px;
  padding: 5px;
  text-align: center;
}

.container-search-for-button {
  background: #275ff2;
  border-radius: 10px;
}

.time-container {
  width: 33%;
  display: flex; 
  flex-direction: column; 
  justify-content: center;
  flex-wrap: wrap;
  row-gap: 5px;
}

.info-container {
  width: 66%;
  word-wrap: break-word;
  display: flex; 
  flex-direction: column; 
  flex-wrap: wrap;
  padding-left: 3vw; 
  max-width: 40vw;
}

</style>
