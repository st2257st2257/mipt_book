<script setup lang="ts">

</script>

<template>
<!--  <div class="container-head">-->
<!--    <div class="left-element button-lk">ББ: 26 единиц</div>-->
<!--    <div class="right-element button-lk">Личный кабинет</div>-->
<!--  </div>-->
</template>

<style scoped>
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