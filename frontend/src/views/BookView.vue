<script setup lang="ts">
import {ref} from 'vue'

import Header from "@/components/TheHeader.vue";
import BookAudience from "@/components/book/BookAudience.vue";
import BookTime from "@/components/book/BookTime.vue";
import BookAmount from "@/components/book/BookAmount.vue";
import type {IAudience} from "@/classes/Interfaces";

let form_user = ref<String>("st2257");
let form_audience_name = ref<String>("");
let form_number_bb = ref<Number>(0);
let form_pair_number = ref<Number>(1);
let form_token = ref<String>("");

function selectAudience(audience: IAudience) {
  form_audience_name.value = audience.number;
}
function selectAmount(amount: Number){
  form_pair_number.value = amount;
}

</script>

<template>
  <div class="centered-div">
    <Header />

    <form action="https://mipt.site:8000/book/" method="post">

      <BookAudience @select-audience="selectAudience"/>
      <BookTime />
      <BookAmount @select-amount="selectAmount"/>

      <div class="container-head" style="height: 60px;">
        <div class="left-element">
          <h3>Автоматические ББ</h3>
        </div>
        <div class="right-element">
          <label class="toggle-switch">
            <input type="checkbox">
            <span class="slider"></span>
          </label>
        </div>
      </div>


      <input type="submit" class="button1" value="Забронировать"><br><br>

      <input type="hidden" name="type" value="book_audience">
      <input type="hidden" name="token" v-model="form_token">
      <input type="hidden" name="audience" v-model="form_audience_name">
      <input type="hidden" name="user" v-model="form_user">
      <input type="hidden" name="number_bb" v-model="form_number_bb">
      <input type="hidden" name="pair_number" v-model="form_pair_number">
    </form>
  </div>
</template>

<style scoped>
.centered-div {
  /*text-align: center; Центрируем текст внутри div */
  padding: 20px; /*Добавляем отступы для лучшей читаемости */
  background-color: white; /*Цвет фона для наглядности */
}

/*Стили для мобильных устройств (экраны меньше 768px) */
@media (max-width: 768px) {
  .centered-div {
    width: 80%; /*Растягиваем на всю ширину экрана */
  }
}

/*Стили для планшетов и компьютеров (экраны от 768px) */
@media (min-width: 768px) {
  .centered-div {
    width: 30%; /*Ограничиваем ширину до 80% */
    margin: 0 auto; /*Центрируем блок по горизонтали */
  }
}
.container-head {
  position: relative; /* Позиционирование относительно контейнера */
  height: 100px; /* Высота контейнера (для демонстрации) */
}

.left-element, .right-element {
  position: absolute;
  top: 50%; /* Выравниваем по вертикали по центру */
  transform: translateY(-50%); /* Корректировка вертикального выравнивания */
}

.left-element {
  left: 0; /* Привязываем к левому краю */
}

.right-element {
  right: 0; /* Привязываем к правому краю */
}
</style>