<script setup lang="ts">
import {ref, onMounted} from 'vue';
import type {IBuilding, IAudience} from "@/classes/Interfaces";

const emit = defineEmits<{
  (e: 'select-audience', arg: IAudience) : void
}>();

const web_site = "mipt.site";
// const web_site = "localhost";

let is_random_selected = ref<Boolean>(false);
let building_arr = ref<Array<IBuilding>>([]);
let audience_arr = ref<Array<IAudience>>([]);

let building_name_selected = ref<String>("");
let audience_number_selected = ref<String>("");

onMounted(async () =>{
  let web_address = '/backend-api';
  let building_path = '/base-info/building/?institute=%D0%9C%D0%A4%D0%A2%D0%98';
  let audience_path = '/base-info/audience/?institute=%D0%9C%D0%A4%D0%A2%D0%98';

  //building_arr.value = await getInfo(web_address+building_path);
  //audience_arr.value = await getInfo(web_address+audience_path);
  building_arr.value = await getInfo('https://' + web_site + ':8000'+building_path);
  audience_arr.value = await getInfo('https://' + web_site + ':8000'+audience_path);
});

async function getInfo(url: string){
  try {
    const response = await fetch(url,{
      method: 'GET',
      headers: {'Content-Type': 'application/json'},
    });

    if (!response.ok) {
      console.error('Сеть ответила с ошибкой: ' + response.status);
    }

    const data = await response.json();
    console.log('Ответ от сервера:', data);
    return data;

  } catch (error) {
    console.error('Ошибка при отправке данных:', error);
  }
}

function selectAudience(audience: IAudience | null){
  if (!audience) return;
  audience_number_selected.value = audience.number;
  is_random_selected.value = false;
  emit('select-audience', audience);
}

function selectBuilding(building: IBuilding){
  building_name_selected.value = building.name;
  is_random_selected.value = false;
  audience_number_selected.value = "";
}

function selectRandom(){
  let audiences_sel_building : IAudience[] = [];

  for(let key in audience_arr.value){
    let cur_item = audience_arr.value[key];
    if (cur_item.building.name != building_name_selected.value) continue;
    audiences_sel_building.push(cur_item);
  }

  let random_audience = audiences_sel_building[Math.floor(Math.random()*audiences_sel_building.length)];
  selectAudience(random_audience);
  is_random_selected.value = true; // it's important to place it after selecting;
}

</script>

<template>
  <h3>Номер аудитории</h3>
  <div class="container">
    <template v-for="building in building_arr" :key="building.name">
      <div class="item button" :class="{selected: building.name== building_name_selected}" @click="selectBuilding(building)"> {{building.name}} </div>
    </template>
  </div>
  <div class="container">
    <div class="item button" :class="{ selected: is_random_selected }" @click="selectRandom()">Случайная</div>
    <template v-for="audience in audience_arr" :key="audience.number">
      <div v-if="audience.building.name == building_name_selected" class="item button"
           :class="{ selected: audience.number == audience_number_selected }" @click="selectAudience(audience)"> {{audience.number}} {{audience.building.name}} </div>
    </template>
  </div>
</template>

<style scoped>
.button {
  background-color: white;
  border: none;
  cursor: pointer;
  color: black;
}

.selected, .selected.button {
  background-color: lightblue;
}
</style>
