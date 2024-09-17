<script setup lang="ts">

import TheFooter from "@/components/TheFooter.vue";
</script>


<template>
	<div id="app" :style="{ backgroundColor: 'white' }">
  		<RouterView />
  		<TheFooter />
	</div>
</template>

<style scoped>

</style>
