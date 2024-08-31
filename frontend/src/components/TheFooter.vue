<script setup lang="ts">
import {onMounted, ref} from "vue";

let token = ref<string|null>(null);

onMounted(()=>{
  token.value = localStorage.getItem("auth-token");
  // if(token.value == null) return;
});

</script>

<template>
<footer>
  <RouterLink to="/" custom v-slot="{navigate}">
    <div role="link" @click="navigate">
      <img src="@/assets/book.svg" class="icon-pic"><br>
      Home
    </div>
  </RouterLink>
<!--  <RouterLink to="/auth/" custom v-slot="{navigate}">-->
<!--    <div role="link" @click="navigate">-->
<!--      <img src="@/assets/book.svg">-->
<!--      Auth-->
<!--    </div>-->
<!--  </RouterLink>-->
  <RouterLink to="/profile/" custom v-slot="{navigate}">
    <div role="link" @click="navigate">
      <img src="@/assets/profile.svg" class="icon-pic"><br>
      <span v-if="token">Profile</span>
      <span v-else>Auth</span>
    </div>
  </RouterLink>
  <RouterLink to="/book-history/" custom v-slot="{navigate}">
    <div role="link" @click="navigate">
      <img src="@/assets/book.svg" class="icon-pic"><br>
      BookHistory
    </div>
  </RouterLink>
</footer>
</template>

<style scoped>
footer {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100%;
  text-align: center;

  border-top: solid #999999 1px;
  background-color: white;
  padding: 5px;

  display: flex;
  justify-content: space-evenly;
}

[role="link"] {
  display: inline-block;
  padding: 4px;
  border-radius: 5px;
  color: #999999;

  font-size: 0.5em;

  filter: invert(40%) sepia(100%) hue-rotate(190deg) saturate(500%) grayscale(100%) ;

  -webkit-transition: 0.5s -webkit-filter ease;
  -moz-transition: 0.5s -moz-filter ease;
  -moz-transition: 0.5s filter ease;
  -ms-transition: 0.5s -ms-filter ease;
  -o-transition: 0.5s -o-filter ease;
  transition: color 1s, 0.5s filter ease, 0.5s -webkit-filter ease;
}

[role="link"]:hover {
  cursor: pointer;
  color: #5c7aff;

  filter: invert(40%) sepia(100%) hue-rotate(190deg) saturate(500%);
}

.icon-pic {
  width: 32px;
}


</style>