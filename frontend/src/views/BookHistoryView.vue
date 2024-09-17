<script setup lang="ts">

import BookTime from "@/components/book/BookTime.vue";
import Header from "@/components/TheHeader.vue";
import BookAmount from "@/components/book/BookAmount.vue";
import BookAudience from "@/components/book/BookAudience.vue";

import {ref, type Ref} from "vue";
import type {IAudience} from "@/classes/Interfaces";

let bookings: Ref<
      Array<{
        audience: IAudience,
        number_bb: Number,
        pair_number: Number,
        date: String,
        booking_time: String,
        user: {
          username: String
        }
      }>
    > = ref([]);

</script>

<template>
  <div class="centered-div">
    <Header />

    <h3>История бронирования</h3>
    <div class="table">
      <div class="table-item, table-header">
        <span>Дата</span>
        <span>Пары</span>
        <span>Баллы</span>
        <span>№</span>
      </div>
      <div class="table-item" v-for="book in bookings">
        <span>{{book.date}}</span>
        <span>{{book.user}}</span>
        <span>{{book.number_bb}}</span>
        <span>{{book.audience.number}}</span>
      </div>
    </div>

  </div>
</template>

<style scoped>

.table {
  display: flex;
}

.table-header {

}

</style>
