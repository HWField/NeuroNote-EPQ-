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
const activeFilters = ref([]);
// Get tab data from store with fallback default state
const tabData = computed(() => {
  const tab = tabStore.getTab(tabId);
  if (!tab) return { view: "graph", noteId: null };
  // Return tab.state instead of the whole tab object
  return tab.state || { view: "graph", noteId: null };
});
const handleFilterChange = (newFilters) => {
  activeFilters.value = newFilters;
  tabStore.updateTabState(tabId, {
    ...tabData.value,
    filters: newFilters,
  });
};
// Local reactive state
const currentView = ref(tabData.value.view || "graph");
const currentNoteId = ref(tabData.value.noteId || null);

const showGraph = () => {
  currentNoteId.value = null;
  currentView.value = "graph";
  useTabStore().RenameTab(tabId, "Graph");
  tabStore.updateTabState(tabId, {
    view: currentView.value,
    noteId: currentNoteId.value,
  });
};

const showNote = (noteId) => {
  // Check if the note is already open in another tab and set active if so
  const otherTabs = tabStore.tabs.filter(
    (tab) =>
      tab.id !== tabId &&
      tab.state.noteId === noteId &&
      tab.state.view === "note"
  );

  //else open note
  if (otherTabs.length > 0) {
    // If the note is already open in another tab, make that tab active
    useTabStore().setActiveTab(otherTabs[0].id);
    return;
  }
  currentNoteId.value = noteId;
  currentView.value = "note";

  // Get the note name from the graph store
  const graphStore = useGraphStore();
  const note = graphStore.elements.find((el) => el.id === parseInt(noteId));
  const noteName = note ? note.name : `Note: ${noteId}`;

  // Use the actual note name in the tab title
  useTabStore().RenameTab(tabId, noteName);
  tabStore.updateTabState(tabId, {
    view: currentView.value,
    noteId: currentNoteId.value,
  });
};

const handleNoteSelected = (nodeData) => {
  const noteId = nodeData.split("_")[1];
  showNote(noteId);
};

onMounted(() => {
  currentView.value = tabData.value.view || "graph";
  currentNoteId.value = tabData.value.noteId;

  // Load filters
  if (tabData.value.filters) {
    activeFilters.value = tabData.value.filters;
  }

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
    <!-- Graph View with inset -->
    <div v-if="currentView === 'graph'" class="w-full h-full p-4 sm:p-6">
      <div
        class="w-full h-full bg-primary-foreground rounded-lg border border-input overflow-hidden"
      >
        <Cytoscape
          :tabId="tabId"
          :hasControls="true"
          :externalFilters="activeFilters"
          @note-selected="handleNoteSelected"
          @filters-changed="handleFilterChange"
        />
      </div>
    </div>

    <!-- Note Editor View (no inset) -->
    <div
      v-else-if="currentView === 'note'"
      class="h-full w-ful overflow-hidden"
    >
      <TipTap :noteId="currentNoteId" :tabId="tabId" @note-closed="showGraph" />
      <!-- <Whiteboard/> -->
    </div>
  </div>
</template>
