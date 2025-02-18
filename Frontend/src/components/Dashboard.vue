<script setup>
import Cytoscape from "@/components/Cytoscape.vue";
import { useUserStore } from "@/stores/useUserStore";

const userStore = useUserStore();
</script>

<template>
  <div style="text-align: center; margin-top: 20px">
    <h1 class="text-2xl/7">Welcome, {{ userStore.username }}</h1>
  </div>

  <div class="flex w-full h-full m-10 rounded-3xl">
    <!-- Left Column (Tall) -->
    <div class="h-full flex-1  bg-gray-300 rounded">
      <p>This is the tall left div with inset padding</p>
      <div class="h-[250px] relative">
        <Cytoscape />
      </div>
    </div>

    <!-- Right Column (Two Short Divs) -->
    <div class="flex-1 flex flex-col">
    <div class="flex-1 bg-gray-400 p-4">
      <p>First short div</p>
    </div>
    <div class="flex-1 bg-gray-500 p-4">
      <p>Second short div</p>
    </div>
  </div>
  </div>
</template>
