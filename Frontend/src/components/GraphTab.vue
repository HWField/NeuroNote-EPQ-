<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from "vue";
import { useTabStore } from "@/stores/useTabStore";
import { useGraphStore } from "@/stores/useGraphStore";
import Cytoscape from "./Cytoscape.vue";
// Define props, using current tab ID as default

const tabStore = useTabStore();
const tabId = tabStore.GetActiveTabID();
const activeFilters = ref([]);
// Get tab data from store with fallback default state
const tabData = computed(() => {
  const tab = tabStore.getTab(tabId);
  if (!tab) return { };
  // Return tab.state instead of the whole tab object
  return tab.state || {};
});
const handleFilterChange = (newFilters) => {
  activeFilters.value = newFilters;
  tabStore.updateTabState(tabId, {
    ...tabData.value,
    filters: newFilters,
  });
};



// function OpenNote(noteid) {
//   // Function implementation here
//   tabStore.addTab("note", "note", {noteId: noteid, creationTabId: tabId});
//   tabStore.addTab(note.name, "note", {noteId: Id, creationTabId: 1});
// }

const OpenNote = (nodeData) => {
  const noteId = nodeData.split("_")[1];
    tabStore.addTab("note", "note", {noteId: noteId, creationTabId: tabId});
 
};

// const handleNoteSelected = (nodeData) => {
//   const noteId = nodeData.split("_")[1];
//   OpenNote(noteId);
// };

onMounted(() => {
  // Load filters
  if (tabData.value.filters) {
    activeFilters.value = tabData.value.filters;
  }
});

onBeforeUnmount(() => {
    // Save filters
    // tabStore.updateTabState(tabId, {
    //     ...tabData.value,
    //     filters: activeFilters.value,
    // });

});
</script>
<template>
  <div class="h-full w-full">
    <!-- Graph View with inset -->
    <div class="w-full h-full p-4 sm:p-6">
      <div
        class="w-full h-full bg-primary-foreground rounded-lg border border-input overflow-hidden"
      >
        <Cytoscape
          :tabId="tabId"
          :hasControls="true"
          :externalFilters="activeFilters"
          @note-selected="OpenNote"
          @filters-changed="handleFilterChange"
        />
      </div>
    </div>

 
  </div>
</template>
