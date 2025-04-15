<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from "vue";
import { useTabStore } from "@/stores/useTabStore";
import Whiteboard from "@/components/Whiteboard.vue";
import TipTap from "@/components/Document Editor/TipTap.vue";
import { useGraphStore } from "@/stores/useGraphStore";

const graphStore = useGraphStore(); 
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

// Determine note type from graph store
const noteType = computed(() => {
  if (!currentNoteId.value) return null;
  
  // Find the note in graph store elements
  const note = graphStore.elements.find(
    el => el.type === 'note' && el.id === parseInt(currentNoteId.value)
  );
  
  // Return the format if found, default to 'document' if not specified
  return note?.format || 'document';
});

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
    <!-- Note Editor View conditionally rendered based on type -->
    <div class="h-full w-full overflow-hidden">
      <!-- Show TipTap for document notes -->
      <TipTap 
        v-if="noteType === 'document'" 
        :noteId="currentNoteId" 
        :tabId="tabId" 
        @note-closed="closeTab" 
      />
      
      <!-- Show Whiteboard for whiteboard notes -->
      <Whiteboard 
        v-else-if="noteType === 'whiteboard'" 
        :noteId="currentNoteId" 
        @note-closed="closeTab"
      />
      
      <!-- Fallback message if note type is unknown -->
      <div v-else class="flex h-full w-full items-center justify-center">
        <p class="text-muted-foreground">Unknown note type or note not found</p>
      </div>
    </div>
  </div>
</template>
