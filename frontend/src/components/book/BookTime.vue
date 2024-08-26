<script setup lang="ts">



function onMounted(){
  const timeSelector = document.getElementById('timeSelector');
  const timeOptions = document.querySelectorAll('.time-option');

  timeSelector!.addEventListener('click', (event : Event) => {
    const selectedOption = event!.target!.closest('.time-option');

    if (selectedOption) {
      timeOptions.forEach(option => option.classList.remove('selected'));
      selectedOption.classList.add('selected');

      // Получение выбранного времени
      const selectedTime = selectedOption.dataset.time;
      console.log("Выбрано время:", selectedTime);
    }
  });
}


</script>

<template>
  <h3>Время бронирования</h3>
  <div class="time-selector" id="timeSelector">
    <div class="time-option" data-time="17:00">17:00</div>
    <div class="time-option" data-time="18:00">18:00</div>
    <div class="time-option" data-time="19:30">19:30</div>
    <div class="time-option" data-time="21:00">21:00</div>
    <div class="time-option" data-time="22:30">22:30</div>
    <div class="time-option" data-time="00:00">00:00</div>
    <div class="time-option" data-time="01:30">01:30</div>
    <div class="time-option" data-time="03:00">03:00</div>
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
  border-color: blue;
}
</style>