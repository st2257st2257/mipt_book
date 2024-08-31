<script setup lang="ts">

</script>

<template>
<footer>
  <RouterLink to="/">Home</RouterLink> |
  <RouterLink to="/auth/">Auth</RouterLink> |
  <RouterLink to="/profile/">Profile</RouterLink> |
  <RouterLink to="/book-history/">BookHistory</RouterLink>
</footer>
</template>

<style scoped>
footer {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  text-align: center;
}
</style>