<script setup>
import Cytoscape from "@/components/Cytoscape.vue";
import { useUserStore } from "@/stores/useUserStore";
import { ref, onMounted, onBeforeUnmount } from "vue";
import { Calendar } from "@/components/ui/calendar";
import { Settings } from "lucide-vue-next";
import { Button } from "@/components/ui/button";
// import { DateValue, getLocalTimeZone, today } from '@internationalized/date';

const userStore = useUserStore();

const screenSize = ref("small");

const updateScreenSize = () => {
  const width = window.innerWidth;
  if (width >= 1024) {
    screenSize.value = "large";
  } else if (width >= 768) {
    screenSize.value = "medium";
  } else {
    screenSize.value = "small";
  }
};

onMounted(() => {
  updateScreenSize();
  window.addEventListener("resize", updateScreenSize);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", updateScreenSize);
});

const mockNotes = ref([
  { id: 1, title: "Note 1", content: "Content for note 1" },
  { id: 2, title: "Note 2", content: "Content for note 2" },
  { id: 3, title: "Note 3", content: "Content for note 3" },
  { id: 4, title: "Note 4", content: "Content for note 4" },
  { id: 5, title: "Note 5", content: "Content for note 5" },
]);
</script>

<template>
  <!-- desktop layout -->
  <div v-if="screenSize === 'large'" class="flex w-full h-full flex-col p-8">
    <!-- md:pl-20 md:pr-20 md:pb-4 -->
    <div class="flex flex-col items-center justify-center m-5">
      <h1 class="text-4xl font-bold my-8">
        Welcome, {{ userStore.username }} :)
      </h1>
    </div>
    <div class="flex flex-row w-full h-full">
      <!-- Left Column (Tall) -->
      <div class="w-full h-full bg-primary-foreground rounded-lg 2 border-4 border-gray-800 mb-4 mr-2 overflow-hidden">
        <Cytoscape />
      </div>

      <!-- Right Column (Two Short Divs) -->
      <div class="w-1/2 h-full flex flex-col ml-2">
        <div class="h-full bg-secondary border-gray-800 border-4 rounded-lg mb-2">
          <h1 class="text-2xl font-bold m-5">Recent Notes:</h1>
          <ul>
            <li
              v-for="note in mockNotes.slice(0, 5)"
              :key="note.id"
              class="m-2 p-2 rounded bg-primary text-secondary"
            >
              {{ note.title }}
            </li>
          </ul>
        </div>
        <div class="h-full bg-secondary border-gray-800 border-4 rounded-lg mt-2">
          <div class="flex justify-between items-center m-5">
            <h1 class="text-2xl font-bold">Shortcuts</h1>
            <Settings class="" />
          </div>
          <div class="grid grid-cols-2 gap-2 text-secondary m-5">
            <Button class="bg-primary p-2 rounded">Shortcut 1</Button>
            <Button class="bg-primary p-2 rounded">Shortcut 2</Button>
            <Button class="bg-primary p-2 rounded">Shortcut 3</Button>
            <Button class="bg-primary p-2 rounded">Shortcut 4</Button>
            <Button class="bg-primary p-2 rounded">Shortcut 5</Button>
            <Button class="bg-primary p-2 rounded">Shortcut 6</Button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- medium layout -->
  <div v-if="screenSize === 'medium'" class="flex w-full h-full flex-col p-4">
    <div class="flex flex-col items-center justify-center m-5">
      <h1 class="text-2xl font-bold my-4">Welcome, {{ userStore.username }} :)</h1>
    </div>

    <div class="w-full  bg-primary-foreground rounded-lg 2 border-4 border-gray-800 mb-4 h-1/2 overflow-hidden">
      <KeepAlive>
        <Cytoscape />
      </KeepAlive>
    </div>
    <div class="flex w-full h-1/2 flex-grow">
      <div class="w-1/2 bg-secondary rounded-lg 2 border-4 border-gray-800 mr-2">
        <h1 class="text-xl font-bold m-5">Recent Notes</h1>
          <ul>
            <li
              v-for="note in mockNotes.slice(0, 5)"
              :key="note.id"
              class="m-2 p-2 rounded bg-primary text-secondary"
            >
              {{ note.title }}
            </li>
          </ul>
      </div>
      <div class="w-1/2 bg-secondary rounded-lg 2 border-4 border-gray-800 ml-2">
        <div class="flex justify-between items-center m-5">
            <h1 class="text-xl font-bold">Shortcuts</h1>
            <Settings class="" />
          </div>
          <div class="grid grid-cols-2 gap-2 text-secondary m-2">
            <Button class="bg-primary p-2 rounded">Shortcut 1</Button>
            <Button class="bg-primary p-2 rounded">Shortcut 2</Button>
            <Button class="bg-primary p-2 rounded">Shortcut 3</Button>
            <Button class="bg-primary p-2 rounded">Shortcut 4</Button>
            <Button class="bg-primary p-2 rounded">Shortcut 5</Button>
            <Button class="bg-primary p-2 rounded">Shortcut 6</Button>
          </div>
      </div>
    </div>
  </div>


  <!-- small layout -->
  <div v-if="screenSize === 'small'" class="flex w-full h-full flex-col p-4">
    <div class="flex flex-col items-center justify-center m-5">
      <h1 class="text-2xl font-bold my-4">Welcome, {{ userStore.username }} :)</h1>
    </div>

    <div class="w-full border-4 border-gray-800 bg-primary-foreground rounded-lg h-full overflow-hidden">
      <KeepAlive>
        <Cytoscape />
      </KeepAlive>
    </div>
   
  </div>
</template>
