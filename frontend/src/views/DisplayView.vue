<script setup lang="ts">

import Header from "@/components/TheHeader.vue";
import {ref, type Ref, onMounted, reactive, type Reactive, defineExpose, provide, inject} from 'vue';
import { useRouter } from 'vue-router';


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
const time_slot_dictionary = {
        "09:00": 1,
        "10:45": 2,
	"12:20": 3,
	"13:45": 4,
	"15:30": 5,
	"17:05": 6,
	"18:35": 7,
	"20:00": 8,
	"22:00": 9,
	"23:59": 10,
	"01:30": 11,
	"03:00": 12,
	"04:30": 13,
	"06:00": 14
      };

const time_slot_arr = [
	"09:00",
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

function time_slot_dictionary_func(time_slot: string){
        if (time_slot == "09:00") { return 1;
        } else if (time_slot == "10:45") { return 2;
        } else if (time_slot == "12:20") { return 3;
        } else if (time_slot == "13:45") { return 4;
        } else if (time_slot == "15:30") { return 5;
        } else if (time_slot == "17:05") { return 6;
        } else if (time_slot == "18:35") { return 7;
        } else if (time_slot == "20:00") { return 8;
        } else if (time_slot == "22:00") { return 9;
        } else if (time_slot == "23:59") { return 10;
        } else if (time_slot == "01:30") { return 11;
        } else if (time_slot == "03:00") { return 12;
        } else if (time_slot == "04:30") { return 13;
        } else if (time_slot == "06:00") { return 14;
        }
	return 0;
}

let time_slots_arr_length = 1;
let time_slots_arr: any[] = reactive([]);
// let time_slots_arr: Ref<TimeSlot[]> = ref([]);
let audiences: Ref<Audience[]> = ref([]);
let audiences_gk: Ref<Audience[]> = ref([]);
let audiences_lk: Ref<Audience[]> = ref([]);
let audiences_digit: Ref<Audience[]> = ref([]);
let audiences_arctica: Ref<Audience[]> = ref([]);
let audiences_quant: Ref<Audience[]> = ref([]);

const router = useRouter();

let token = ref<string|null>(null);
let username = ref<string|null>(null);
let form_number_bb = ref<number|null>(null);
let form_time_slot = ref<number|0>(0);
let form_end_time_slot = ref<number|0>(1);
let form_pair_number = ref<number|0>(1);
let form_audience = ref<string|null>(null);

onMounted(()=>{
  token.value = localStorage.getItem("auth-token");
  username.value = localStorage.getItem("username");
  loadAudience();
  form_number_bb.value = 0;
  form_end_time_slot.value = 0;
  form_pair_number.value = 0;
  form_end_time_slot.value = 0;
});

async function sendForm(){
  try {
    const response = await fetch("https://" + web_site + ":8000/book/",{
      method: 'POST',
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: JSON.stringify({
        "type": "book_audience",
        'token': token.value,
        'audience': form_audience.value,
        'number_bb': form_number_bb.value,
        'pair_number': form_pair_number.value,
        'time_slot': time_slot_arr[form_time_slot.value],
        'user': username.value
      })
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);
    }
    if (response.ok) {
        const data = await response.json();
        console.log('Ответ от сервера:', data);
	setTimeout(()=>{
          router.push("/book-history/").then(()=>{
            router.go(0); // force reload
          });
      	}, 2000);
    } else {
        console.error('Ошибка запроса:', response.status);
    }

  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

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
    audiences_digit.value = data_number.filter(item => item.building.name == 'Цифра');
    audiences_arctica.value = data_number.filter(item => item.building.name == 'Арктика');
    audiences_quant.value = data_number.filter(item => item.building.name == 'Квант');

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
    for (let i = 0; i < data_number.data[0].day_history.length; i++){
	time_slots_arr.push(data_number.data[0].day_history[i]);
    }
    time_slots_arr_length = time_slots_arr.length;
    console.log(time_slots_arr.length);

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
  form_audience.value = my_audience_number;
  audience_number.value = my_audience_number;
  loadTimeSlots(my_audience_number);
  showPopupRateInfo.value = true;
};

const updateTimeSlot = (time_slot_str: string) => {
  if ((time_slot_str in time_slot_dictionary)) {
  	let time_slot = time_slot_dictionary_func(time_slot_str);
    	if ((form_time_slot.value != null ) && (form_time_slot.value > time_slot)){
        	form_time_slot.value = time_slot;
        	form_pair_number.value = form_end_time_slot.value - form_time_slot.value + 1;
  	}
  	if ((form_time_slot.value != null ) && (form_end_time_slot.value < time_slot)){
        	form_end_time_slot.value = time_slot;
        	form_pair_number.value = form_end_time_slot.value - form_time_slot.value + 1;
  	}
  	if (form_time_slot.value == 0 ){
        	form_time_slot.value = time_slot;
        	form_end_time_slot.value = time_slot;
        	form_pair_number.value = form_end_time_slot.value - form_time_slot.value + 1;
  	}
  } else {
        console.error(`Ошибка: Ключ ${time_slot_str} не найден в словаре.`);
  }
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
        <div class="right-element">
                <img src="@/assets/gk_m.jpg" class="building-icon-m" alt="Рисунок ГК">
        </div>
       <div class="centered-div" style="width: 50%;text-align: center;"><h3>Аудитории ГК</h3></div>

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
                        <button @click="hideAudienceInfo" style="background-color: #dc3545; width: 100%;  color: white;padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;">Закрыть</button>
			<div style="display: flex; justify-content: space-between;">
				<p>Номер аудитории:</p>
				<p class="time">{{audience_number}} ГК  </p>
			</div>
		
			<form @submit.prevent="sendForm">
				<div v-for="time_slot in time_slots_arr">
			    		<div :class="['time-slot-new', `background_${time_slot[1]}`]">
						<div style="display: flex; justify-content: space-between;">
                                			<p class="time">{{time_slot[0]}}</p>
                                			<p v-if="time_slot[1] == 'Отсутствует для бронирования'" style="padding-left: 10px;">{{time_slot[6]}}</p>
							<p v-if="time_slot[1] == 'Забронировано'" style="padding-left: 10px;">Забронировано</p>
							<p v-if="time_slot[1] == 'Свободно'" style="padding-left: 10px;">Свободно</p>
							<input v-if="time_slot[1] == 'Забронировано'" @click="updateTimeSlot(`${time_slot[0]}`)" type="checkbox" id="scales" name="scales" style="width: 20px;"/>
							<input v-if="time_slot[1] == 'Свободно'" @click="updateTimeSlot(`${time_slot[0]}`)" type="checkbox" id="scales" name="scales" style="width: 20px;"/>
						</div>
                            		</div>
                        	</div>
				<p>Время начала: {{ time_slot_arr[form_time_slot] }}</p>
				<p>Время окончания:{{ time_slot_arr[form_end_time_slot + 1] }}</p>
				<p>Число пар: {{ form_pair_number }} шт.</p>
				<button type="submit" @click="hideAudienceInfo" style="background-color: #4caf50; width: 100%;  color: white; padding: 10px 20px;border: none;border-radius: 5px;cursor: pointer;"><h3>Занять аудиторию</h3></button>
		    	</form>
		    </div>
                </div>
	</transition>

  </div>
</div>

<div>
          <div class="right-element">
                <img src="@/assets/lk_m.jpg" class="building-icon-m" alt="Рисунок ЛК">
        </div>
       <div class="centered-div" style="width: 50%;text-align: center;"><h3>Аудитории ЛК</h3></div>
       
  <div class="room-list room-list-grid" style="padding-bottom: 70px;">
    <template v-for="audience in audiences_lk">
        <div @click="showAudienceInfo(`${audience.number}`)" :class="['room-item', `background_${audience.audience_status.name}`, `number_of_users${audience.number_of_users}`]"
        style="max-width: 150px; max-height: 100px; min-height: 100px; min-width: 150px;">
            <i class="icon fas fa-door-open status-available"></i>
            <p>Аудитория {{audience.number}} {{audience.building.name}}</p>
            <p>{{audience.audience_status.name}}</p>
        </div>
    </template>
  </div>
</div>


<div>
	<div class="right-element">
        	<img src="@/assets/arctica_m.jpg" class="building-icon-m" alt="Рисунок цифры">
        </div>
       <div class="centered-div" style="width: 50%;text-align: center;"><h3>Аудитории Цифры</h3></div>
  
  <div class="room-list room-list-grid" style="padding-bottom: 70px;">
    <template v-for="audience in audiences_digit">
        <div @click="showAudienceInfo(`${audience.number}`)" :class="['room-item', `background_${audience.audience_status.name}`, `number_of_users${audience.number_of_users}`]"
        style="max-width: 150px; max-height: 100px; min-height: 100px; min-width: 150px;">
            <i class="icon fas fa-door-open status-available"></i>
            <p>Аудитория {{audience.number}} {{audience.building.name}}</p>
            <p>{{audience.audience_status.name}}</p>
        </div>
    </template>
  </div>
</div>


<div>
         <div class="right-element">
                <img src="@/assets/arctica_m.jpg" class="building-icon-m" alt="Рисунок арктики">
        </div>
       <div class="centered-div" style="width: 50%;text-align: center;"><h3>Аудитории Арктики</h3></div>


  <div class="room-list room-list-grid" style="padding-bottom: 70px;">
    <template v-for="audience in audiences_digit">
        <div @click="showAudienceInfo(`${audience.number}`)" :class="['room-item', `background_${audience.audience_status.name}`, `number_of_users${audience.number_of_users}`]"
        style="max-width: 150px; max-height: 100px; min-height: 100px; min-width: 150px;">
            <i class="icon fas fa-door-open status-available"></i>
            <p>Аудитория {{audience.number}} {{audience.building.name}}</p>
            <p>{{audience.audience_status.name}}</p>
        </div>
    </template>
  </div>
</div>

</div>

</template>

<style scoped>


.building-icon-m {
    width: 300px;
    display: block;
    margin: 0 auto;
}

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
    .time-slot-new {
  	min-width: 70vw;
    }
  }

  @media (min-width: 768px) {
    .room-list-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(100px, 150px));
      grid-column-gap: 20px;
    }
    .time-slot-new {
        min-width: 30vw;
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

    .background_Резерв {
      background: #FF6347;
    }

    .background_Свободно {
      background: #90EE90;
    }

    .background_Скоро {
      background: #FFFFE0;
    }

    .background_Забронировано {
      background: #FFAB42;
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


/* Popup styles */
.time-slot {
  min-width: 20vw;
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
}

.time-slot p {
  margin-bottom: 5px;
}

.time-slot-new {
  border: 1px solid #ccc;
  padding: 2px;
  margin-bottom: 0px;
  border-radius: 5px;
}

.time-slot-new p {
  margin-bottom: 0px;
}

.time {
  font-weight: bold;
}

.status {
  color: #007bff; /*Пример цвета для "Забронировано" */
}

.event {
  font-style: italic;
}

.points {
  color: #333;
}

.capacity {
  color: #555;
}
</style>
