<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from "vue";
import { useTabStore } from "@/stores/useTabStore";
import Cytoscape from "@/components/Cytoscape.vue";
import Whiteboard from "@/components/Whiteboard.vue";
import TipTap from "@/components/Document Editor/TipTap.vue";
import { useGraphStore } from "@/stores/useGraphStore";
// Define props, using current tab ID as default

const tabStore = useTabStore();
const tabId = tabStore.GetActiveTabID();

// Get tab data from store with fallback default state
const tabData = computed(() => {
  const tab = tabStore.getTab(tabId);
  if (!tab) return { view: "graph", noteId: null };
  // Return tab.state instead of the whole tab object
  return tab.state || { view: "graph", noteId: null };
});

// Local reactive state
const currentView = ref(tabData.value.view || "graph");
const currentNoteId = ref(tabData.value.noteId || null);

const showGraph = () => {
  currentNoteId.value = null;
  currentView.value = "graph";
  useTabStore().RenameTab(tabId, "New Tab:");
};

const showNote = (noteId) => {
  currentNoteId.value = noteId;
  currentView.value = "note";
  
  
    // Get the note name from the graph store
    const graphStore = useGraphStore();
  const note = graphStore.elements.find(el => el.id === parseInt(noteId));
  const noteName = note ? note.name : `Note: ${noteId}`;
  
  // Use the actual note name in the tab title
  useTabStore().RenameTab(tabId, noteName);
};

const handleNoteSelected = (nodeData) => {
  const noteId = nodeData.split("_")[1];
  showNote(noteId);
};

onMounted(() => {
  currentView.value = tabData.value.view || "graph";

  currentNoteId.value = tabData.value.noteId;
  if (!tabData.value.view) {
    showGraph();
  }
});

onBeforeUnmount(() => {
  tabStore.updateTabState(tabId, {
    view: currentView.value,
    noteId: currentNoteId.value,
  });
});
</script>

<template>
  <div class="h-full w-full">
    <!-- Graph View -->
    <Cytoscape
      v-if="currentView === 'graph'"
      :tabId="tabId"
      :hasControls="true"
      @note-selected="handleNoteSelected"
    />

    <!-- Note Editor View -->
    <div v-else-if="currentView === 'note'" class="h-full w-full">
      <TipTap :noteId="currentNoteId" @note-closed="showGraph" />
      <!-- <Whiteboard/> -->
    </div>
  </div>
</template>
