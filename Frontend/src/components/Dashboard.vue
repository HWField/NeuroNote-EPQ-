<script setup>
import Cytoscape from "@/components/Cytoscape.vue";
import { useUserStore } from "@/stores/useUserStore";

const userStore = useUserStore();
</script>

<template>
  <div class="flex flex-col items-center justify-center m-5">
    <h1 class="text-2xl/7">Welcome, {{ userStore.username }} :)</h1>
  </div>

  <!-- mobile layout -->

  <div class="flex lg:hidden w-full h-full flex-col">
    <div class="w-full bg-gray-200 rounded mb-4 h-1/2 flex-grow max-h-1/2">
      <Cytoscape />
    </div>
    <div class="flex w-full h-1/2 flex-grow">
      <div class="w-1/2 bg-gray-300 rounded mr-2">
        <p>Left half-width div</p>
      </div>
      <div class="w-1/2 bg-gray-400 rounded ml-2">
        <p>Right half-width div</p>
      </div>
    </div>
  </div>

  <!-- desktop layout -->
  <div class="hidden lg:flex w-full h-full">

    <!-- Left Column (Tall) -->
    <div class="w-1/2 h-full bg-gray-300 rounded mb-4 mr-2">
      <div class="h-full">
        <Cytoscape />
      </div>
    </div>

    <!-- Right Column (Two Short Divs) -->
    <div class="w-1/2 h-full flex flex-col ml-2">
      <div class="h-full bg-gray-400 rounded mb-2">
        <p>First short div</p>
      </div>
      <div class="h-full bg-gray-500 rounded mt-s">
        <p>Second short div</p>
      </div>
    </div>
  </div>
</template>
