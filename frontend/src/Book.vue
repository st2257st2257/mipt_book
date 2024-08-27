<script setup lang="ts">
import Header from "@/components/TheHeader.vue";
import BookAudience from "@/components/book/BookAudience.vue";
import BookTime from "@/components/book/BookTime.vue";
import BookAmount from "@/components/book/BookAmount.vue";
</script>

<template>
  <div class="centered-div">
    <Header />

    <form action="https://mipt.site:8000/book/" method="post">

      <BookAudience />
      <BookTime />
      <BookAmount />

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

      User : <input type="text" name="user" value="st2257"><br><br>
      Number bb : <input type="text" name="number_bb" ><br><br>
      Pair Number : <input type="text" name="pair_number" ><br><br>
      Type: <input type="text" name="type" value="book_audience"><br><br>
      Token : <input type="text" name="token" ><br><br>
      Audience : <input type="text"  name="audience" id="audience_id" value="Случайная"><br><br>
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