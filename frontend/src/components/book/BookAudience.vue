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

let building_arr = ref<Array<IBuilding>>([]);
let audience_arr = ref<Array<IAudience>>([]);

let building_name_selected = ref<String>("");
let audience_number_selected = ref<String>("");

onMounted(() =>{
  let web_address = 'https://mipt.site:8000';
  building_arr = JSON.parse(httpGet(new URL('/base-info/building/?institute=%D0%9C%D0%A4%D0%A2%D0%98', web_address)));
  audience_arr = JSON.parse(httpGet(new URL('/base-info/audience/?institute=%D0%9C%D0%A4%D0%A2%D0%98', web_address)));
});

function selectAudience(audience: IAudience){
  audience_number_selected.value = audience.number;
}

function selectBuilding(building: IBuilding){
  building_name_selected.value = building.name;
}

</script>

<template>
  <h3>Номер аудитории</h3>
  <div class="container">
    <div class="selector" id="selector_building_container">
    </div>
    <template v-for="building in building_arr">
      <div class="item button" :class="{selected: building.name== building_name_selected}" @click="selectBuilding(building)"> {{building.name}} </div>
    </template>
  </div>
  <div class="container">
    <div class="selector" id="selector_container">
      <div class="item button">Случайная</div>
    </div>
    <template v-for="audience in audience_arr">
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