<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from "vue";
import { useTabStore } from "@/stores/useTabStore";
import Whiteboard from "@/components/Whiteboard.vue";
import TipTap from "@/components/Document Editor/TipTap.vue";
import { useGraphStore } from "@/stores/useGraphStore";


const tabStore = useTabStore();
const tabId = tabStore.GetActiveTabID();
// Get tab data from store with fallback default state
const tabData = computed(() => {
  const tab = tabStore.getTab(tabId);
  if (!tab) 
    return {noteId: null, creationTabId: null };
  // Return tab.state instead of the whole tab object
  return tab.state || {noteId: null, creationTabId: null};
});

// Local reactive state
const currentNoteId = ref(tabData.value.noteId || null);
const creationTabId = ref(tabData.value.creationTabId || null);

function closeTab() {
  tabStore.removeTab(tabId, creationTabId.value);

}

onMounted(() => {
  currentNoteId.value = tabData.value.noteId;
creationTabId.value = tabData.value.creationTabId;
});

onBeforeUnmount(() => {});
</script>
<template>
  <div class="h-full w-full">
    <!-- Graph View with inset -->

    <!-- Note Editor View (no inset) -->
    <div class="h-full w-ful overflow-hidden">
      <TipTap :noteId="currentNoteId" :tabId="tabId" @note-closed="closeTab" />
      <!-- <Whiteboard/> -->
    </div>
  </div>
</template>
