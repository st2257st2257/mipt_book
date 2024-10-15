<script setup lang="ts">
import {ref} from 'vue'

// setup selected time slot
const emit = defineEmits<{
  (e: "select-time-slot", time_slot: String):void
}>()

function emitSelect(){
  emit('select-time-slot', String(formatTime(selected_time.value)));
}


function fDate(hours : number, minutes : number){
  // short for factoryDate
  let out = new Date();
  out.setHours(hours); out.setMinutes(minutes)
  if (hours < 12) { // hardcoded nonsense
    out.setDate(out.getDate()+1);
  }
  return out;
}

function getDefaultTime(){
  for(let i = 0; i<times.value.length ; i++){
    if(!isOld(times.value[i])) return times.value[i];
  }
  return times.value[0];
}

let times = ref([
  fDate(9,0), fDate(10,45), fDate(12,20),
  fDate(15,30),
  fDate(17,5), fDate(18,35), fDate(20,0),
  fDate(22,0), fDate(23,59), fDate(0,0),
  fDate(1,30), fDate(3,0), fDate(4,30),
  fDate(6,0),
])

let selected_time = ref<Date>(new Date());

function onMounted(){
  selected_time.value = getDefaultTime();
}

function isOld(date : Date){
  let now = new Date();
  let result = now.getTime() > date.getTime();
  return result;
}
function formatTime(date: Date){
  return date.toLocaleTimeString("ru-RU", {hour: "2-digit", minute: "2-digit"});
}

function selectTime(time: Date){
  // emitSelect();
  if(isOld(time)) return;
  selected_time.value = time;
  emitSelect();
  // console.log(String(selected_time.value));
}

</script>

<template>
  <h3>Время бронирования</h3>
  <div class="time-selector" id="timeSelector">
    <template v-for="time in times">
      <div  class="time-option"
           :class="{selected: time.getTime() == selected_time.getTime()}"
           @click="selectTime(time)"
            v-if="!isOld(time)"
      >{{formatTime(time)}}</div>
    </template>
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
