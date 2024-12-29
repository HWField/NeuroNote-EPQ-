<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router";
import { useDark, useToggle } from "@vueuse/core";
import { onMounted } from "vue";

const isDark = useDark();
const toggleDark = useToggle(isDark);

onMounted(() => {
  if (!isDark.value) {
    toggleDark();
  }
});
</script>

<template>
  <RouterView />
</template>

<style scoped></style>
