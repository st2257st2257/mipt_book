<script setup lang="ts">
import {ref} from 'vue'

function fDate(hours : number, minutes : number){
  // short for factoryDate
  let out = new Date();
  out.setHours(hours); out.setMinutes(minutes)
  if (hours < 12) { // hardcoded nonsense
    out.setDate(out.getDate()+1);
  }
  return out;
}

let times = ref([
  fDate(17,0), fDate(18,0), fDate(19,30),
  fDate(21,0), fDate(22,30), fDate(0,0),
  fDate(1,30), fDate(3,0),
])

let selected_time = ref<Date>(new Date());

function onMounted(){}

function isOld(date : Date){
  let now = new Date();
  let result = now.getTime() > date.getTime();
  return result;
}
function formatTime(date: Date){
  return date.toLocaleTimeString("ru-RU", {hour: "2-digit", minute: "2-digit"});
}

function selectTime(time: Date){
  if(isOld(time)) return;
  selected_time.value = time;
}

</script>

<template>
  <h3>Время бронирования</h3>
  <div class="time-selector" id="timeSelector">
    <div v-for="time in times" class="time-option"
         :class="{old: isOld(time), selected: time.getTime() == selected_time.getTime()}"
         @click="selectTime(time)"
    >{{formatTime(time)}}</div>
  </div>
</template>

<style scoped>
.time-selector {
  width: 100%;
  overflow: scroll;
}

.time-option {
  display: inline-block;
  padding: 5px 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 10px;
  margin-top: 10px;
  cursor: pointer;
}

.time-option.selected {
  background-color: lightblue;
}
.time-option.old.selected {
  background-color: #5a6971;
}
.time-option.old {
  background-color: #5a6971;
}

</style>