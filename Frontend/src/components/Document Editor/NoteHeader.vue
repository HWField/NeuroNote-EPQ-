<script setup>
import { ref, onMounted, watch, nextTick, computed } from 'vue';
import { useGraphStore } from '@/stores/useGraphStore';

const props = defineProps({
  initialTitle: {
    type: String,
    default: ''
  },
  initialTags: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update:title', 'update:tags', 'enter-pressed']);
const graphStore = useGraphStore();

// Initialize title as empty string, let the placeholder handle "Untitled Note"
const title = ref(props.initialTitle || '');
const titleInputRef = ref(null);
const selectedTags = ref([]);
const tagInput = ref('');
const tagSuggestions = ref([]);
const showSuggestions = ref(false);
const tagInputRef = ref(null);
const showAllTags = ref(false); // State to track if we should show all tags or compact view

// Get available tags from GraphStore
const availableTags = computed(() => {
  return graphStore.elements
    .filter(el => el.type === 'tag')
    .map(tag => ({
      id: tag.id,
      label: tag.name
    }));
});

// Initialize tags from props
onMounted(() => {
  if (props.initialTags.length) {
    loadTags();
  }
});

watch(() => props.initialTags, loadTags, { deep: true });
watch(() => props.initialTitle, (newTitle) => {
  // If the incoming title is "Untitled Note" or empty, use empty string
  // This will make the placeholder visible
  title.value = newTitle === 'Untitled Note' ? '' : (newTitle || '');
}, { immediate: true });

async function loadTags() {
  // Use tags from GraphStore instead of separate API call
  selectedTags.value = props.initialTags.map(tagId => {
    const foundTag = availableTags.value.find(tag => tag.id === tagId) || { id: tagId, label: `Tag ${tagId}` };
    return foundTag;
  });
}

function updateTitle(e) {
  // Update local title with exactly what the user typed
  title.value = e.target.value;
  
  // Emit the actual user input (could be empty string)
  // Let parent decide if it needs a fallback value
  emit('update:title', title.value);
}

function handleTitleKeydown(e) {
  if (e.key === 'Enter') {
    e.preventDefault(); // Prevent default Enter behavior
    emit('enter-pressed'); // Signal parent to focus editor
  }
}

async function searchTags(e) {
  if (tagInput.value.length > 0) {
    // Filter tags from GraphStore
    tagSuggestions.value = availableTags.value
      .filter(tag => 
        tag.label.toLowerCase().includes(tagInput.value.toLowerCase()) &&
        !selectedTags.value.some(selected => selected.id === tag.id)
      );
    showSuggestions.value = true;
  } else {
    showSuggestions.value = false;
  }
}

function selectTag(tag) {
  selectedTags.value.push(tag);
  tagInput.value = '';
  showSuggestions.value = false;
  emit('update:tags', selectedTags.value.map(tag => tag.id));
  nextTick(() => {
    tagInputRef.value?.focus();
  });
}

function removeTag(tag) {
  selectedTags.value = selectedTags.value.filter(t => t.id !== tag.id);
  emit('update:tags', selectedTags.value.map(tag => tag.id));
}

function addTag(e) {
  e.preventDefault();
  if (tagInput.value.trim()) {
    // Find if tag already exists in store
    const existingTag = availableTags.value.find(
      tag => tag.label.toLowerCase() === tagInput.value.trim().toLowerCase()
    );
    
    if (existingTag) {
      selectTag(existingTag);
    } else {
      // If it's a new tag, create it with a temporary ID
      // GraphStore will assign the real ID when saved
      const newTag = {
        id: `tag-${Date.now()}`,
        label: tagInput.value.trim()
      };
      selectTag(newTag);
    }
  } else if (e.shiftKey) {
    // If Shift+Enter and no tag text, focus the editor
    emit('enter-pressed');
  }
}

function toggleTagsDisplay() {
  showAllTags.value = !showAllTags.value;
}

// Close suggestions when clicking outside
function handleClickOutside(event) {
  if (tagInputRef.value && !tagInputRef.value.contains(event.target)) {
    showSuggestions.value = false;
  }
}
</script>

<template>
  <div class="note-header" @click.stop>
    <!-- Title input with improved placeholder behavior -->
    <div class="note-title-container">
      <h1>
        <input 
          ref="titleInputRef"
          type="text" 
          v-model="title" 
          class="title-input" 
          placeholder="Untitled Note"
          @input="updateTitle" 
          @keydown="handleTitleKeydown"
          @click.stop
        />
      </h1>
    </div>
    
    <!-- Tags multiselect with compact styling -->
    <div class="tags-container" @click.stop :class="{ 'expanded': showAllTags || selectedTags.length > 5 }">
      <div class="tags-header">
        <div class="tags-label">
          Tags
          <span v-if="selectedTags.length > 0" class="tag-count">{{ selectedTags.length }}</span>
        </div>
        <button
          v-if="selectedTags.length > 5"
          @click.stop="toggleTagsDisplay"
          class="expand-button"
          :aria-label="showAllTags ? 'Show fewer tags' : 'Show all tags'"
        >
          {{ showAllTags ? 'Show less' : 'Show all' }}
        </button>
      </div>
      <div class="tags-content" :class="{ 'compact': !showAllTags && selectedTags.length > 5 }">
        <div class="tags-wrapper">
          <!-- Selected tags with compact styling -->
          <div v-if="selectedTags.length" class="selected-tags">
            <span 
              v-for="(tag, index) in selectedTags" 
              :key="tag.id"
              v-show="showAllTags || index < 5" 
              class="tag"
            >
              <span class="tag-label">{{ tag.label }}</span>
              <button @click.stop="removeTag(tag)" class="tag-remove" aria-label="Remove tag">
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M18 6L6 18M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </button>
            </span>
            <span v-if="!showAllTags && selectedTags.length > 5" class="more-tags">
              +{{ selectedTags.length - 5 }} more
            </span>
          </div>
          
          <!-- Tag input with compact styling -->
          <div class="tag-input-wrapper">
            <input 
              ref="tagInputRef"
              type="text" 
              v-model="tagInput" 
              @input="searchTags"
              @keydown.enter="addTag"
              placeholder="Add tag..."
              class="tag-input" 
            />
          </div>
        </div>
      </div>
      
      <!-- Tag suggestions dropdown -->
      <div 
        v-if="showSuggestions && tagSuggestions.length" 
        class="tag-suggestions"
      >
        <div 
          v-for="tag in tagSuggestions" 
          :key="tag.id" 
          @click="selectTag(tag)"
          class="tag-suggestion-item"
        >
          {{ tag.label }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.note-header {
  top: 0;
  z-index: 10;
  background-color: var(--background);
  padding-bottom: 0.5rem;
}

.note-title-container {
  margin: 0 0 0.75rem;
  padding: 0.5rem 0; /* Reduced vertical padding */
  position: relative;
}

.note-title-container::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, #6a00f5, rgba(124, 58, 237, 0.3));
  border-radius: 2px;
}

.note-title-container h1 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 600;
  color: rgb(107, 33, 168);
}

.title-input {
  background: transparent;
  border: none;
  width: 100%;
  font-size: inherit;
  font-weight: inherit;
  color: inherit;
  font-family: inherit;
  transition: color 0.2s ease;
}

/* Enhanced placeholder styling */
.title-input::placeholder {
  color: rgba(107, 33, 168, 0.3);
  font-style: italic;
  opacity: 1;
  font-weight: 400;
  transition: opacity 0.3s ease;
}

.title-input:focus::placeholder {
  opacity: 0.2;
}

.title-input:focus {
  outline: none;
}

/* More compact tag container */
.tags-container {
  position: relative;
  margin-bottom: 0.5rem; /* Reduced margin */
  background-color: rgba(124, 58, 237, 0.05);
  border-radius: 0.75rem;
  padding: 0.4rem 0.6rem; /* Further reduced padding */
  border: 1px solid rgba(124, 58, 237, 0.1);
  transition: all 0.2s ease;
}

.tags-container:hover,
.tags-container:has(.tag-input:focus) {
  background-color: rgba(124, 58, 237, 0.08);
  border-color: rgba(124, 58, 237, 0.2);
}

.tags-container.expanded {
  padding: 0.5rem 0.75rem;
}

.tags-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.2rem; /* Even more reduced margin */
}

.tags-label {
  font-size: 0.65rem; /* Smaller font */
  font-weight: 500;
  color: rgb(107, 33, 168, 0.6);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: flex;
  align-items: center;
}

.tag-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(107, 33, 168, 0.1);
  color: rgb(107, 33, 168);
  border-radius: 9999px;
  padding: 0.1rem 0.35rem;
  font-size: 0.6rem;
  margin-left: 0.3rem;
}

.expand-button {
  font-size: 0.65rem;
  color: rgb(107, 33, 168, 0.8);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.1rem 0.3rem;
  border-radius: 0.25rem;
  transition: background-color 0.2s ease;
}

.expand-button:hover {
  background-color: rgba(107, 33, 168, 0.1);
}

.tags-content {
  max-height: 300px; /* Allow room for expansion */
  overflow-y: auto; /* Add scrolling for many tags */
  transition: max-height 0.3s ease;
}

.tags-content.compact {
  max-height: 32px; /* Just enough for one row */
}

.tags-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem; /* Even smaller gap */
  align-items: center;
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem; /* Even smaller gap */
  align-items: center;
}

.tag {
  border-radius: 0.3rem;
  padding: 0.1rem 0.3rem; /* Smaller padding */
  background-color: rgb(91, 33, 182);
  color: rgb(226, 232, 240);
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
  font-size: 0.7rem; /* Smaller font */
  line-height: 1.2;
  transition: all 0.2s ease;
  max-width: 180px;
  height: 20px;
}

.tag:hover {
  background-color: rgb(76, 29, 149);
  transform: translateY(-1px);
}

.more-tags {
  font-size: 0.7rem;
  color: rgb(107, 33, 168, 0.8);
  background-color: rgba(107, 33, 168, 0.1);
  padding: 0.1rem 0.35rem;
  border-radius: 0.3rem;
  cursor: pointer;
}

.more-tags:hover {
  background-color: rgba(107, 33, 168, 0.15);
}

.tag-label {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.tag-remove {
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: none;
  color: inherit;
  opacity: 0.7;
  cursor: pointer;
  padding: 0;
  width: 12px; /* Even smaller remove button */
  height: 12px;
  border-radius: 50%;
  transition: opacity 0.2s ease;
}

.tag-remove:hover {
  opacity: 1;
}

.tag-input-wrapper {
  flex: 1;
  min-width: 60px; /* Smaller min-width */
}

.tag-input {
  background: transparent;
  border: none;
  padding: 0.1rem 0; /* Reduced padding */
  font-size: 0.75rem; /* Smaller font */
  width: 100%;
  color: inherit;
  height: 20px; /* Match height of tags */
}

/* Enhanced placeholder styling for tags too */
.tag-input::placeholder {
  color: rgba(107, 33, 168, 0.3);
  font-style: italic;
  opacity: 1;
  transition: opacity 0.3s ease;
}

.tag-input:focus::placeholder {
  opacity: 0.2;
}

.tag-input:focus {
  outline: none;
}

.tag-suggestions {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  width: 100%;
  max-height: 140px;
  overflow-y: auto;
  z-index: 20;
  background-color: white;
  border: 1px solid rgba(124, 58, 237, 0.2);
  border-radius: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}

.tag-suggestion-item {
  padding: 0.35rem 0.6rem; /* Reduced padding */
  cursor: pointer;
  transition: background-color 0.15s ease;
  font-size: 0.75rem; /* Smaller font */
}

.tag-suggestion-item:hover {
  background-color: rgba(124, 58, 237, 0.1);
}

/* Dark mode adjustments */
:global(.dark) .note-title-container h1 {
  color: rgb(216, 180, 254);
}

:global(.dark) .title-input::placeholder {
  color: rgba(216, 180, 254, 0.3);
}

:global(.dark) .tags-label {
  color: rgba(216, 180, 254, 0.6);
}

:global(.dark) .tag-count {
  background-color: rgba(216, 180, 254, 0.1);
  color: rgb(216, 180, 254, 0.9);
}

:global(.dark) .more-tags {
  color: rgb(216, 180, 254, 0.8);
  background-color: rgba(216, 180, 254, 0.1);
}

:global(.dark) .expand-button {
  color: rgb(216, 180, 254, 0.8);
}

:global(.dark) .expand-button:hover {
  background-color: rgba(216, 180, 254, 0.1);
}

:global(.dark) .tag-input::placeholder {
  color: rgba(216, 180, 254, 0.3);
}

:global(.dark) .tag-suggestions {
  background-color: #1f2937;
  border-color: rgba(124, 58, 237, 0.3);
}

:global(.dark) .tags-container {
  background-color: rgba(124, 58, 237, 0.08);
  border-color: rgba(124, 58, 237, 0.2);
}

:global(.dark) .tags-container:hover,
:global(.dark) .tags-container:has(.tag-input:focus) {
  background-color: rgba(124, 58, 237, 0.12);
  border-color: rgba(124, 58, 237, 0.3);
}

:global(.dark) .note-title-container::after {
  background: linear-gradient(90deg, rgb(124, 58, 237), rgba(124, 58, 237, 0.15));
}
</style>