<script setup lang="ts">
import {ref, onUpdated} from "vue";

const emit = defineEmits<{
  (e: "select-amount", amount: Number):void
}>()

let amount = ref<Number>(1);

function emitSelect(){
  emit('select-amount', amount.value);
}

</script>

<template>
  <h3>Количество пар</h3>
  <output>1</output>
  <input type="range" value="1" min="1" max="6" style="width: 80%;"
         v-model="amount" @input="emitSelect">
  <output>6</output><br><br>
</template>

<style scoped>
input[type=range] {
  -webkit-appearance: none;
  width: 200px;
  height: 8px;
  background: #ddd;
  outline: none;
  border-radius: 10px;
/*Добавляем тень для полосы ползунка */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

input[type=range]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #4CAF50;
  cursor: pointer;
  /*Добавляем тень для ползунка */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

input[type=range]::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #4CAF50;
  cursor: pointer;
  /*Добавляем тень для ползунка (Firefox) */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}
</style>