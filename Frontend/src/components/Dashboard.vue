<script setup>
import Cytoscape from "@/components/Cytoscape.vue";
import { useUserStore } from "@/stores/useUserStore";
import { useGraphStore } from "@/stores/useGraphStore";
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { Calendar } from "@/components/ui/calendar";
import { Settings } from "lucide-vue-next";
import { Button } from "@/components/ui/button";
import ScrollArea from "./ui/scroll-area/ScrollArea.vue";
// import { DateValue, getLocalTimeZone, today } from '@internationalized/date';

import { useTabStore } from "@/stores/useTabStore";
const tabStore = useTabStore();

const userStore = useUserStore();
const graphStore = useGraphStore();

const screenSize = ref("small");
let active = ref(false);

const activeFilters = ref([]);
const tabData = computed(() => {
  const tab = tabStore.getTab(1);
  if (!tab) return {};
  // Return tab.state instead of the whole tab object
  return tab.state;
});
const handleFilterChange = (newFilters) => {
  activeFilters.value = newFilters;
  tabStore.updateTabState(1, {
    ...tabData.value,
    filters: newFilters,
  });
};
const OpenNote = (noteId) => {
  const Id = noteId.split("_")[1];
  console.error("Note selected", Id);
  const note = graphStore.elements.find((el) => el.id === parseInt(Id));
  const noteName = note ? note.name : `Note: ${Id}`;
  tabStore.addTab(noteName, "generic", { view: "note", noteId: Id });
};

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
  if (tabData.value.filters) {
    activeFilters.value = tabData.value.filters;
  }
  active = true;
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", updateScreenSize);
  active = false;
});

const recentNotes = computed(() => {
  // Check if userStore.recentNotes exists and has items
  if (!userStore.recentNotes || userStore.recentNotes.length === 0) {
    return [];
  }

  return userStore.recentNotes.map((noteId) => {
    // Safely check if graphStore and elements exist
    const noteElement =
      graphStore.elements && graphStore.elements.find
        ? graphStore.elements.find(
            (el) => el.type === "note" && el.id === noteId
          )
        : null;

    return {
      id: noteId,
      title: noteElement ? noteElement.name : `Note ${noteId}`,
    };
  });
});
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
      <div
        class="w-full h-full bg-primary-foreground rounded-lg 2 border-4 border-gray-800 mb-4 mr-2 overflow-hidden"
      >
        <!-- <Cytoscape 
  @note-selected="OpenNote" 
  :externalFilters="activeFilters" 
  @filters-changed="handleFilterChange"
  :hasControls="true"

  :tabId="1"  
/> -->

        <Cytoscape
          v-if="active"
          @note-selected="OpenNote"
          :hasControls="true"
          :tabId="1"
        />
      </div>

      <!-- Right Column (Two Short Divs) -->
      <div class="w-1/2 h-full flex flex-col ml-2">
        <!-- Update this div in the large layout -->
        <div
          class="h-full max-h-[40vh] bg-secondary border-gray-800 border-4 rounded-lg mb-2 flex flex-col"
        >
          <h1 class="text-2xl font-bold m-5">Recent Notes:</h1>
          <div class="flex-1 overflow-hidden  px-5 pb-5">
            <ScrollArea
              className="h-full"
              style="
                --scrollbar-thumb: rgb(255, 0, 0);
                --scrollbar-track: rgba(var(--secondary-foreground), 0.2);
                --scrollbar-thumb: rgb(var(--destructive));
                --scrollbar-track: rgba(var(--secondary-foreground), 0.2);
              "
            >
              <ul class="pr-4 space-y-2">
                <li
                  v-for="(note, index) in recentNotes"
                  :key="note.id"
                  @click="OpenNote(`note_${note.id}`)"
                  class="p-3 rounded-md bg-primary/90 text-secondary shadow-sm border border-primary/20 cursor-pointer transition-all duration-200 hover:bg-primary hover:shadow-md hover:scale-[1.01] flex items-center"
                >
                  <div
                    class="mr-3 flex-shrink-0 w-6 h-6 bg-secondary-foreground rounded-full flex items-center justify-center text-xs font-semibold text-secondary"
                  >
                    {{ index + 1 }}
                  </div>
                  <div class="mr-3 flex-shrink-0">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      class="lucide lucide-file-text"
                    >
                      <path
                        d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"
                      />
                      <polyline points="14 2 14 8 20 8" />
                      <line x1="16" x2="8" y1="13" y2="13" />
                      <line x1="16" x2="8" y1="17" y2="17" />
                      <line x1="10" x2="8" y1="9" y2="9" />
                    </svg>
                  </div>
                  <div class="truncate">{{ note.title }}</div>
                </li>
              </ul>
            </ScrollArea>
          </div>
        </div>

        <div
          class="h-full bg-secondary border-gray-800 border-4 rounded-lg mt-2"
        >
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
      <h1 class="text-2xl font-bold my-4">
        Welcome, {{ userStore.username }} :)
      </h1>
    </div>

    <div
      class="w-full bg-primary-foreground rounded-lg 2 border-4 border-gray-800 mb-4 h-1/2 overflow-hidden"
    >
      <Cytoscape
        v-if="active"
        @note-selected="OpenNote"
        :hasControls="true"
        :tabId="1"
      />
    </div>
    <div class="flex w-full h-1/2 flex-grow">
      <div
        class="w-1/2 max-h-[40vh] bg-secondary rounded-lg 2 border-4 border-gray-800 mr-2 flex flex-col"
      >
        <h1 class="text-2xl font-bold m-5">Recent Notes:</h1>
        <div class="flex-1 overflow-hidden px-5 pb-5">
          <ScrollArea
            className="h-full"
            style="
              --scrollbar-thumb: rgb(var(--primary));
              --scrollbar-track: rgba(var(--secondary-foreground), 0.2);
            "
          >
            <ul class="pr-4 space-y-2">
              <li
                v-for="(note, index) in recentNotes"
                :key="note.id"
                @click="OpenNote(`note_${note.id}`)"
                class="p-3 rounded-md bg-primary/90 text-secondary shadow-sm border border-primary/20 cursor-pointer transition-all duration-200 hover:bg-primary hover:shadow-md hover:scale-[1.01] flex items-center"
              >
                <div
                  class="mr-3 flex-shrink-0 w-6 h-6 bg-secondary-foreground rounded-full flex items-center justify-center text-xs font-semibold text-secondary"
                >
                  {{ index + 1 }}
                </div>
                <div class="mr-3 flex-shrink-0">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="lucide lucide-file-text"
                  >
                    <path
                      d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"
                    />
                    <polyline points="14 2 14 8 20 8" />
                    <line x1="16" x2="8" y1="13" y2="13" />
                    <line x1="16" x2="8" y1="17" y2="17" />
                    <line x1="10" x2="8" y1="9" y2="9" />
                  </svg>
                </div>
                <div class="truncate">{{ note.title }}</div>
              </li>
            </ul>
          </ScrollArea>
        </div>
      </div>
      <div
        class="w-1/2 bg-secondary rounded-lg 2 border-4 border-gray-800 ml-2"
      >
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
      <h1 class="text-2xl font-bold my-4">
        Welcome, {{ userStore.username }} :)
      </h1>
    </div>

    <div
      class="w-full border-4 border-gray-800 bg-primary-foreground rounded-lg h-full overflow-hidden"
    >
      <Cytoscape
        v-if="active"
        @note-selected="OpenNote"
        :hasControls="true"
        :tabId="1"
      />
    </div>
  </div>
</template>
