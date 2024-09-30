<script setup lang="ts">

import Header from "@/components/TheHeader.vue";
import {ref, type Ref, onMounted, reactive, type Reactive, defineExpose} from 'vue';


interface Audience_status {
  description: string,
  name: number
}

interface Institute {
  description: string,
  name: string
}

interface Audience {
  number: string,
  number_of_users: number,
  description: string,
  building: Building,
  audience_status: Audience_status
}

interface Building {
  name: string,
  number: string,
  institute: Institute,
  description: string
}


// https://mipt.site:8000/base-info/audience/?institute=%D0%9C%D0%A4%D0%A2%D0%98
const web_site = "mipt.site";
// const web_site = "localhost";

let audiences: Ref<Audience[]> = ref([]);
let audiences_gk: Ref<Audience[]> = ref([]);
let audiences_lk: Ref<Audience[]> = ref([]);

onMounted(()=>{
  // username.value = localStorage.getItem("username");
  loadAudience();
});

async function loadAudience(){
  try {
    const response = await fetch("https://" + web_site + ":8000/base-info/audience/?institute=%D0%9C%D0%A4%D0%A2%D0%98",{
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
      }
    }

    const data_number = await response.json() as Audience[];
    audiences.value = data_number;
    audiences_gk.value = data_number.filter(item => item.building.name == 'ГК');
    audiences_lk.value = data_number.filter(item => item.building.name == 'ЛК');

    // username.value = data_number[0].username;
    // number_bb.value = String(data_number[0].number_bb);

    console.log('Ответ от сервера header data_number:', data_number);
    // console.log('Ответ от сервера header username:', username);
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

const filteredItems = () => {
   let items: { id: number, name: string, age: number }[]  = [
        { id: 1, name: 'Иван', age: 25 },
        { id: 2, name: 'Мария', age: 30 },
        { id: 3, name: 'Петр', age: 28 }
      ];

  return items; //.filter(item => item.age > 25);
};

defineExpose({ filteredItems });


</script>

<template>
  <div class="centered-div">
    <Header />
  </div>

<div class="main-room-item">

<div>
  <div class="centered-div"><h3>Аудитории ГК:</h3></div>
  <div class="room-list room-list-grid" style="padding-bottom: 70px;">
    <template v-for="audience in audiences_gk">
        <div :class="['room-item', `background_${audience.audience_status.name}`, `number_of_users${audience.number_of_users}`]"
        style="max-width: 200px; max-height: 100px; min-height: 100px; min-width: 150px;">
            <i class="icon fas fa-door-open status-available"></i>
            <p>Аудитория {{audience.number}} {{audience.building.name}}</p>
            <p>{{audience.audience_status.name}}</p>

            <!-- <p>Описание: {{audience.description}}</p>
            <p>Номер аудитории: {{audience.number}}</p>
            <p>Число пользователей: {{audience.number_of_users}}</p>
            <p>Имя института: {{audience.building.institute.name}}</p>
            <p>Название здания: {{audience.building.name}}</p>
            <p>Статус: {{audience.audience_status.name}}</p>
            <p></p> -->
        </div>
    </template>
  </div>
</div>

<div>
  <div class="centered-div"><h3>Аудитории ЛК:</h3></div>
  <div class="room-list room-list-grid" style="padding-bottom: 70px;">
    <template v-for="audience in audiences_lk">
        <div :class="['room-item', `background_${audience.audience_status.name}`, `number_of_users${audience.number_of_users}`]"
        style="max-width: 200px; max-height: 100px; min-height: 100px; min-width: 150px;">
            <i class="icon fas fa-door-open status-available"></i>
            <p>Аудитория {{audience.number}} {{audience.building.name}}</p>
            <p>{{audience.audience_status.name}}</p>

            <!-- <p>Описание: {{audience.description}}</p>
            <p>Номер аудитории: {{audience.number}}</p>
            <p>Число пользователей: {{audience.number_of_users}}</p>
            <p>Имя института: {{audience.building.institute.name}}</p>
            <p>Название здания: {{audience.building.name}}</p>
            <p>Статус: {{audience.audience_status.name}}</p>
            <p></p> -->
        </div>
    </template>
  </div>
</div>

</div>

</template>

<style scoped>
    .room-list {
      flex-wrap: wrap;
      justify-content: center;
      gap: 10px;
      grid-column-gap: 10px;
    }

  .main-room-item {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(350px, 450px));
  }

  @media (max-width: 768px) {
    .room-list-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 200px));
      grid-column-gap: 20px;
    }
  }

  @media (min-width: 768px) {
    .room-list-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 200px));
      grid-column-gap: 20px;
    }
  }


    .room-item {
      border: 1px solid #ccc;
      border-radius: 5px;
      width: 33vw;
      padding: 5px;
      height: 20vw;
      text-align: center;
      border-radius: 10px;
    }

    .number_of_users20{

    }

    .background_Занято {
      background: #FF6347;
    }

    .background_Свободно {
      background: #90EE90;
    }

    .background_Скоро {
      background: #FFFFE0;
    }

    .background_Отсутствует {
      background: #808080;
    }

    .icon {
      font-size: 24px;
    }

    .status-available {
      color: green;
    }

    .status-booked {
      color: red;
    }

    .status-reserved {
      color: orange;
    }
</style>
