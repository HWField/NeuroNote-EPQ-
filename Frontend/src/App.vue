<!-- stalling to load data from backend if already logged in -->
<template>
    <Loading v-if="!dataLoaded" />
  <div v-else>
    <!-- Render the main app UI once data is loaded -->
    <RouterView />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import {useGraphStore} from "@/stores/useGraphStore";
import Loading from "@/components/Loading.vue";
const dataLoaded = ref(false);  // Track if data is loaded
const graphStore = useGraphStore();


onMounted(async () => {
    await graphStore.fetchGraph();  // Fetch data when the app is mounted
  dataLoaded.value = true;  // Set data as loaded after the fetch is complete
});
</script>

<style>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
