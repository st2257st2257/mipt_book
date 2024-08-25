<script setup lang="ts">
import {ref, onMounted} from 'vue';
import type {IBuilding, IAudience} from "@/classes/Interfaces";

// Получение денных от API BACKEND
function httpGet(theUrl : URL) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", theUrl, false );
  xmlHttp.send( null );
  return xmlHttp.responseText;
}

let is_random_selected = ref<Boolean>(false);
let building_arr = ref<Array<IBuilding>>([]);
let audience_arr = ref<Array<IAudience>>([]);

let building_name_selected = ref<String>("");
let audience_number_selected = ref<String>("");

onMounted(() =>{
  let web_address = 'https://mipt.site:8000';
  building_arr = ref(JSON.parse(httpGet(new URL('/base-info/building/?institute=%D0%9C%D0%A4%D0%A2%D0%98', web_address))));
  audience_arr = ref(JSON.parse(httpGet(new URL('/base-info/audience/?institute=%D0%9C%D0%A4%D0%A2%D0%98', web_address))));
});

function selectAudience(audience: IAudience | null){
  if (audience) audience_number_selected.value = audience.number;
  is_random_selected.value = false;
}

function selectBuilding(building: IBuilding){
  building_name_selected.value = building.name;
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
    <div class="selector" id="selector_building_container">
    </div>
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