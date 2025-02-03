<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import { onMounted } from "vue";

onMounted(() => {
  document.documentElement.classList.add("dark-mode");
});
</script>

<template>
  <RouterView />
</template>

<style scoped></style>
