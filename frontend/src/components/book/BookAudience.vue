<script setup lang="ts">
import {ref} from 'vue';

const building_arr = ref([]);
const audience_arr = ref([]);

const building_selected = ref("");
const audience_name_selected = ref(""); // Name of selected audience

// Обновление нажатия аудиторий
function update_selected(selected : string){
  for (const item in aud_arr){
    console.log(`${aud_arr[item]['number']}`);
    let button = document.getElementById(`${aud_arr[item]['number']}`)
    button!.style.backgroundColor = 'white';
    button!.style.color = 'black';

    if (`${aud_arr[item]['number']}` == selected) {
      button!.style.backgroundColor = 'lightblue';
      // button.style.color = 'white';
    }
    if (`${aud_arr[item]['building']['name']}`!= building) {
      button!.style.display = "none";
    }
    else {
      button!.style.display = "";
    }
  }
  const audience_selector = document.getElementById("audience_id")
  audience_selector!.value = selected;
}


// Обновление нажатия зданий
function update_selected_building(building : string){
  for (const item in build_arr){
    console.log(`${build_arr[item]['name']}`);
    let button = document.getElementById(`${build_arr[item]['name']}`)
    button!.style.backgroundColor = 'white';
    button!.style.color = 'black';
    if (`${build_arr[item]['name']}`== building) {
      button!.style.backgroundColor = 'lightblue';
      // button.style.color = 'white';
    }
  }
  let audience_selector = document.getElementById("audience_id")
  audience_selector!.value = building;
  update_selected(selected);
}

// Получение денных от API BACKEND
function httpGet(theUrl : URL) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", theUrl, false );
  xmlHttp.send( null );
  return xmlHttp.responseText;
}

let web_address = 'https://mipt.site:8000';
let flag  = 0;
let flag_building  = 0;
let selected = '0';
let building = 'ГК';

let build_arr = JSON.parse(httpGet(new URL('/base-info/building/?institute=%D0%9C%D0%A4%D0%A2%D0%98', web_address)));
let aud_arr = JSON.parse(httpGet(new URL('/base-info/audience/?institute=%D0%9C%D0%A4%D0%A2%D0%98', web_address)));

let node = document.getElementById('selector_building_container');
for (const item in build_arr) {
  node!.insertAdjacentHTML('afterend', `<div class="item button" id=${build_arr[item]['name']}>${build_arr[item]['name']}</div>`);

  const button = document.getElementById(`${build_arr[item]['name']}`);
  button!.addEventListener('click', () => {
    if (flag_building == 0) {
      flag_building = 1;
      building = `${build_arr[item]['name']}`;
    } else {
      if (`${build_arr[item]['name']}` != building) {
        flag_building = 1;
        building = `${build_arr[item]['name']}`;
      } else {
        flag_building = 0;
        building = 'Случайная';
        flag = 0;
        selected = 'Случайная';
      }
    }
    update_selected_building(building);
  });
}

node = document.getElementById('selector_container');
for (const item in aud_arr){
  node!.insertAdjacentHTML('afterend', `<div class="item button" id=${aud_arr[item]['number']}>${aud_arr[item]['number']}${aud_arr[item]['building']['name']}</div>`);

  const button = document.getElementById(`${aud_arr[item]['number']}`)
  button!.addEventListener('click', () => {
    if (flag_building != 0) {
      if (flag == 0) {
        flag = 1;
        selected = `${aud_arr[item]['number']}`;
      }
      else {
        if (`${aud_arr[item]['number']}` != selected) {
          flag = 1;
          selected = `${aud_arr[item]['number']}`;
        }
        else {
          flag = 0;
          selected = 'Случайная';
        }
      }
      update_selected(selected);
    }
  });
};
</script>

<template>
  <h3>Номер аудитории</h3>
  <div class="container">
    <div class="selector" id="selector_building_container">
    </div>
    <template v-for="building_item in buildings_arr">
      <div v-if="building_item == building_selected" class="item button"> {{building_item}} </div>
    </template>
  </div>
  <div class="container">
    <div class="selector" id="selector_container">
      <div class="item button">Случайная</div>
    </div>
    <template v-for="audience in audience_arr">
      <div v-if="audience.building != building_selected" class="item button"
           :class="{ selected: audience.name == audience_name_selected }"> {{audience}} </div>
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