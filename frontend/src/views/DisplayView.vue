<script setup lang="ts">

import Header from "@/components/TheHeader.vue";
import {ref, type Ref, onMounted, reactive, type Reactive, defineExpose, provide, inject} from 'vue';


interface Audience_status {
  description: string,
  name: number
}

interface Institute {
  description: string,
  name: string
}

interface TimeSlot {
  number: string,
  pair_number: number,
  event_name: string,
  bb_number: string,
  people_number: string
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

// DO THIS
// const web_site = "mipt.site";
// const web_site = "localhost";
// const web_site = "127.0.0.1";
const web_site = inject('web_site');

let time_slots_arr_length = 1;
let time_slots_arr: any[] = reactive([]);
// let time_slots_arr: Ref<TimeSlot[]> = ref([]);
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
        localStorage.removeItem("auth-token");
      }
    }

    const data_number = await response.json() as Audience[];
    audiences.value = data_number;
    audiences_gk.value = data_number.filter(item => item.building.name == 'ГК');
    audiences_lk.value = data_number.filter(item => item.building.name == 'ЛК');

    console.log('Ответ от сервера header data_number:', data_number);
  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}


async function loadTimeSlots(my_audience_number: string){
  try {
    const response = await fetch("https://" + web_site + ":8000/timetable/?type=get_timetable&audience_number=" + my_audience_number,{
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);
    }


    time_slots_arr.length = 0;
    const data_number = await response.json();
    console.log('============', data_number.data[0].day_history);
    for (let i = 1; i < data_number.data[0].day_history.length; i++){
	time_slots_arr.push(data_number.data[0].day_history[i]);
    }
    time_slots_arr_length = time_slots_arr.length;
    console.log(time_slots_arr.length);
    // time_slots_arr
    // audiences.value = data_number;
    // audiences_gk.value = data_number.filter(item => item.building.name == 'ГК');
    // audiences_lk.value = data_number.filter(item => item.building.name == 'ЛК');

    console.log('Ответ от сервера header data_number:', data_number);
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


/* pop up functions */
const showPopupRateInfo = ref(false);
let audience_number = ref<string|null>(null);


const showAudienceInfo = (my_audience_number: string) => {
  audience_number.value = my_audience_number;
  loadTimeSlots(my_audience_number);
  showPopupRateInfo.value = true;
};

const hideAudienceInfo = () => {
  showPopupRateInfo.value = false;
};


</script>

<template>
  <div class="centered-div">
    <Header />
  </div>

<div class="main-room-item">

<div>
  <div class="centered-div"><h3>Аудитории ГК:</h3></div>
  <!-- <p style="font-size: 24px;">SHOW <img class="icon-pic image_for_click" @click="showAudienceInfo" src="@/assets/info.svg"></p>
  --><div class="room-list room-list-grid" style="padding-bottom: 70px;">
    <template v-for="audience in audiences_gk">
	    <div @click="showAudienceInfo(`${audience.number}`)" :class="['room-item', `background_${audience.audience_status.name}`, `number_of_users${audience.number_of_users}`]"
        style="max-width: 150px; max-height: 100px; min-height: 100px; min-width: 150px;">
            <i class="icon fas fa-door-open status-available"></i>
            <p>Аудитория {{audience.number}} {{audience.building.name}}</p>
            <p>{{audience.audience_status.name}}</p>
        </div>
    </template>

    	<transition name="fade-rate-info">
                <div v-if="showPopupRateInfo" class="popup">
                    <div class="popup-content">
                        <button @click="hideAudienceInfo" style="background-color: #dc3545;color: white;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;">Закрыть</button>
			<p>Номер аудитории: {{audience_number}}</p>
			<p v-for="time_slot in time_slots_arr">Время:{{time_slot[0]}} Статус:{{time_slot[1]}} Мероприятие:{{time_slot[2]}} Баллы Бронирования:{{time_slot[3]}} Вместимость:{{time_slot[4]}}человек</p>
                    </div>
                </div>
	</transition>

  </div>
</div>

<div>
  <div class="centered-div"><h3>Аудитории ЛК:</h3></div>
  <div class="room-list room-list-grid" style="padding-bottom: 70px;">
    <template v-for="audience in audiences_lk">
        <div :class="['room-item', `background_${audience.audience_status.name}`, `number_of_users${audience.number_of_users}`]"
        style="max-width: 150px; max-height: 100px; min-height: 100px; min-width: 150px;">
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
      grid-template-columns: repeat(auto-fit, minmax(100px, 150px));
      grid-column-gap: 20px;
    }
  }

  @media (min-width: 768px) {
    .room-list-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(100px, 150px));
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


/*styles for popup*/
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

</style>
