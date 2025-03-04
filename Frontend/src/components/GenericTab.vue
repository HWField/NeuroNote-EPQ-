

<script setup>
// import { ref, computed } from 'vue'
// import { useGraphStore } from "@/stores/useGraphStore";
// import { useTabStore } from "@/stores/useTabStore";

// import TipTap from "@/components/Document editor/TipTap.vue";
import TipTap from '@/components/Document Editor/TipTap.vue'
// import NoteEditor from '@/components/NoteEditor.vue'


// const tabStore = useTabStore()
// const tabData = computed(() => tabStore.getTabById(props.tabId))

// const isEditingNote = ref(false)
// const selectedNoteId = ref(null)

// const openNoteEditor = (noteId) => {
//   selectedNoteId.value = noteId
//   isEditingNote.value = true
// }

// const closeNoteEditor = () => {
//   isEditingNote.value = false
//   selectedNoteId.value = null
// }
</script>


<template>
  <!-- <div class="tab-container">
    <GraphView 
      v-if="!isEditingNote"
      :filters="tabData.filters"
      @select-note="openNoteEditor"
    />
    
    <NoteEditor v-if="isEditingNote" 
      :note-id="selectedNoteId" 
      @close="closeNoteEditor"
    />
  </div> -->
  <TipTap></TipTap>

</template>