<script setup lang="ts">
import TheFooter from "@/components/TheFooter.vue";
import { provide } from 'vue';

// provide('web_site', '127.0.0.1');
provide('web_site', 'mipt.site');
provide('web_site_register', 'mipt.site');


function showNotification(notificationId: string) {
    if (document.getElementById(notificationId)) {
        document.getElementById(notificationId)?.classList.add("show");
        document.getElementById(notificationId)?.classList.add("good_action");
    } else {
        console.error('Элемент с id "' + notificationId + '" не найден');
    }
}
provide('notification', { showNotification });

</script>


<template>
	<div id="app" :style="{ backgroundColor: 'white' }">
  		<RouterView />
  		<TheFooter />
	</div>
</template>

<style scoped>

</style>
