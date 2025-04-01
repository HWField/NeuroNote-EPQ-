<template>
    <div class="tag-node" :class="{ 'active': isActive }">
      <div 
        class="tag-header" 
        @click="toggleExpand"
        :style="{ paddingLeft: `${depth * 12}px` }"
      >
        <span class="expand-icon">
          <i v-if="hasChildren" class="material-icons toggle-icon">
            {{ expanded ? 'arrow_drop_down' : 'arrow_right' }}
          </i>
          <span v-else class="placeholder-icon"></span>
        </span>
        <span class="tag-icon">
          <i class="material-icons">folder</i>
        </span>
        <span class="tag-name">{{ tag.name }}</span>
        <span class="tag-count" v-if="childTags.length || tagNotes.length">
          {{ childTags.length + tagNotes.length }}
        </span>
      </div>
      
      <transition name="slide">
        <div v-if="expanded" class="tag-children">
          <!-- Child tags -->
          <ul v-if="childTags.length" class="nested-tags">
            <li v-for="childTag in childTags" :key="`tag-${childTag.id}`">
              <tag-node :tag="childTag" :depth="depth + 1" />
            </li>
          </ul>
          
          <!-- Notes -->
          <ul v-if="tagNotes.length" class="notes-list">
            <li 
              v-for="note in tagNotes" 
              :key="`note-${note.id}`"
              class="note-item"
              @click="viewNote(note.id)"
            >
              <div class="note-content" :style="{ paddingLeft: `${(depth + 1) * 12 + 16}px` }">
                <span class="note-icon">
                  <i class="material-icons">description</i>
                </span>
                <span class="note-name">{{ note.name }}</span>
              </div>
            </li>
          </ul>
        </div>
      </transition>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue';
  import { useGraphStore } from '@/stores/useGraphStore';
  import { useRouter } from 'vue-router';
  
  const props = defineProps({
    tag: {
      type: Object,
      required: true
    },
    depth: {
      type: Number,
      default: 0
    }
  });
  
  const router = useRouter();
  const graphStore = useGraphStore();
  const expanded = ref(props.depth < 2); // Auto-expand first two levels
  const isActive = ref(false);
  
  // Get child tags for this tag
  const childTags = computed(() => {
    if (!props.tag.children || props.tag.children.length === 0) {
      return [];
    }
    
    return graphStore.elements.filter(el => 
      el.type === 'tag' && props.tag.children.includes(el.id)
    );
  });
  
  // Get notes that have this tag
  const tagNotes = computed(() => {
    const notes = [];
    
    // Find all notes with this tag
    graphStore.elements.forEach(element => {
      if (element.type === 'note' && element.tags && element.tags.includes(props.tag.id)) {
        notes.push(element);
      }
    });
    
    return notes;
  });
  
  const hasChildren = computed(() => {
    return childTags.value.length > 0 || tagNotes.value.length > 0;
  });
  
  function toggleExpand() {
    if (hasChildren.value) {
      expanded.value = !expanded.value;
    }
    isActive.value = true;
    
    // Turn off active after a while
    setTimeout(() => {
      isActive.value = false;
    }, 300);
  }
  
  function viewNote(noteId) {
    router.push({ name: 'note', params: { id: noteId } });
  }
  </script>
  
  <style scoped>
  .tag-node {
    width: 100%;
    font-size: 0.95rem;
  }
  
  .tag-header {
    display: flex;
    align-items: center;
    padding: 8px 12px;
    cursor: pointer;
    border-radius: 4px;
    transition: all 0.2s ease;
    user-select: none;
    background-color: rgba(52, 152, 219, 0.05);
    border-left: 3px solid #3498db;
  }
  
  .tag-header:hover {
    background-color: rgba(52, 152, 219, 0.15);
  }
  
  .expand-icon {
    display: inline-flex;
    width: 20px;
    justify-content: center;
    color: #666;
  }
  
  .toggle-icon {
    font-size: 20px;
  }
  
  .placeholder-icon {
    width: 20px;
  }
  
  .tag-icon {
    color: #3498db;
    margin-right: 8px;
    display: flex;
    align-items: center;
  }
  
  .tag-icon i {
    font-size: 18px;
  }
  
  .tag-name {
    flex-grow: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-weight: 500;
    color: #2c3e50;
  }
  
  .tag-count {
    font-size: 0.75rem;
    background-color: #3498db;
    color: white;
    border-radius: 12px;
    padding: 2px 8px;
    min-width: 24px;
    text-align: center;
  }
  
  .tag-children {
    overflow: hidden;
  }
  
  .nested-tags, .notes-list {
    list-style-type: none;
    padding: 0;
    margin: 4px 0;
  }
  
  .note-item {
    margin: 3px 0;
  }
  
  .note-content {
    display: flex;
    align-items: center;
    padding: 6px;
    cursor: pointer;
    border-radius: 4px;
    transition: all 0.2s ease;
    background-color: #f5f5f5;
    border-left: 3px solid #27ae60;
  }
  
  .note-content:hover {
    background-color: rgba(46, 204, 113, 0.1);
  }
  
  .note-icon {
    color: #27ae60;
    margin-right: 8px;
    display: flex;
    align-items: center;
  }
  
  .note-icon i {
    font-size: 16px;
  }
  
  .note-name {
    flex-grow: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-weight: normal;
    font-size: 0.9em;
    color: #34495e;
  }
  
  /* Animations */
  .slide-enter-active,
  .slide-leave-active {
    transition: all 0.3s ease;
    overflow: hidden;
    max-height: 1000px;
  }
  
  .slide-enter-from,
  .slide-leave-to {
    max-height: 0;
    opacity: 0;
  }
  
  .active {
    background-color: rgba(52, 152, 219, 0.15);
  }
  </style>