<template>
  <div>
    <button @click="showPopup_func">Show Popup</button>
    <transition name="fade">
      <div v-if="showPopup" class="popup">
        <div class="popup-content">
          <p v-for="(line, index) in popupContent" :key="index">{{ line }}</p>
          <button @click="hidePopup">Close</button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const showPopup = ref(false);

const popupContent = ref([
  'Line Line Line Line Line Line Line Line Line Line 1',
  'Line Line Line Line Line Line Line Line Line Line 2',
  'Line Line Line Line Line Line Line Line Line Line 3',
  'Line Line Line Line Line Line Line Line Line Line 4',
  'Line Line Line Line Line Line Line Line Line Line 5',
  'Line Line Line Line Line Line Line Line Line Line 6',
  'Line Line Line Line Line Line Line Line Line Line 7',
  'Line Line Line Line Line Line Line Line Line Line 8',
  'Line Line Line Line Line Line Line Line Line Line 9',
  'Line Line Line Line Line Line Line Line Line Line 10',
]);

const showPopup_func = () => {
  showPopup.value = true;
};

const hidePopup = () => {
  showPopup.value = false;
};
</script>

<style scoped>
.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
  z-index: 10;
}

.popup-content {
  max-height: 400px; /*Adjust as needed */
  overflow-y: auto;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}
</style>
