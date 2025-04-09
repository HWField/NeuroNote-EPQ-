<script setup>
import { ref, onMounted, watch, nextTick, computed } from "vue";
import { useGraphStore } from "@/stores/useGraphStore";
import axios from "../../axios";
import { ScrollArea } from "@/components/ui/scroll-area";

const props = defineProps({
  initialTitle: {
    type: String,
    default: "",
  },
  initialTags: {
    type: Array,
    default: () => [],
  },
});

const tagInputFocused = ref(false);
const isCreatingTag = ref(false);
const emit = defineEmits(["update:title", "update:tags", "enter-pressed"]);
const graphStore = useGraphStore();
const selectedSuggestionIndex = ref(0);
const enhancedTagSuggestions = computed(() => {
  const tagElements = graphStore.elements.filter((el) => el.type === "tag");

  return tagSuggestions.value.map((tag) => {
    // Find parent tags (tags that have this tag as a child)
    const parentTags = tagElements
      .filter((t) => t.children && t.children.includes(tag.id))
      .map((t) => t.name);

    return {
      ...tag,
      parents: parentTags,
    };
  });
});
function scrollToSelected() {
  nextTick(() => {
    const selectedElement = document.getElementById(
      `tag-suggestion-${selectedSuggestionIndex.value}`
    );
    if (selectedElement) {
      selectedElement.scrollIntoView({
        block: "nearest",
        behavior: "smooth",
      });
    }
  });
}
function handleTagInputKeydown(e) {
  if (!showSuggestions.value) return;

  if (e.key === "ArrowDown") {
    e.preventDefault();
    selectedSuggestionIndex.value =
      (selectedSuggestionIndex.value + 1) %
      (enhancedTagSuggestions.value.length + (tagInput.value.trim() ? 1 : 0));
    scrollToSelected(); // Add this to scroll to selection
  } else if (e.key === "ArrowUp") {
    e.preventDefault();
    const totalOptions =
      enhancedTagSuggestions.value.length + (tagInput.value.trim() ? 1 : 0);
    selectedSuggestionIndex.value =
      (selectedSuggestionIndex.value - 1 + totalOptions) % totalOptions;
    scrollToSelected(); // Add this to scroll to selection
  } else if (e.key === "Enter") {
    e.preventDefault();

    // If we have suggestions and a selected index
    if (enhancedTagSuggestions.value.length > 0) {
      if (selectedSuggestionIndex.value < enhancedTagSuggestions.value.length) {
        // Select the highlighted tag
        selectTag(enhancedTagSuggestions.value[selectedSuggestionIndex.value]);
      } else if (tagInput.value.trim()) {
        // Create new tag option
        handleCreateNewTag();
      }
    } else if (tagInput.value.trim()) {
      // Just create new tag
      handleCreateNewTag();
    }
  }
}

// Initialize title as empty string, let the placeholder handle "Untitled Note"
const title = ref(props.initialTitle || "");
const titleInputRef = ref(null);
const selectedTags = ref([]);
const tagInput = ref("");
const tagSuggestions = ref([]);
const showSuggestions = ref(false);
const tagInputRef = ref(null);
const showAllTags = ref(false); // State to track if we should show all tags or compact view

watch(tagSuggestions, () => {
  selectedSuggestionIndex.value = 0;
});
// Get available tags from GraphStore
const availableTags = computed(() => {
  return graphStore.elements
    .filter((el) => el.type === "tag")
    .map((tag) => ({
      id: tag.id,
      label: tag.name,
    }));
});

// Initialize tags from props
onMounted(() => {
  if (props.initialTags.length) {
    loadTags();
  }
});

watch(() => props.initialTags, loadTags, { deep: true });
watch(
  () => props.initialTitle,
  (newTitle) => {
    // If the incoming title is "Untitled Note" or empty, use empty string
    // This will make the placeholder visible
    title.value = newTitle === "Untitled Note" ? "" : newTitle || "";
  },
  { immediate: true }
);
const suggestionHeight = computed(() => {
  // Base height for empty results or single item
  if (enhancedTagSuggestions.value.length === 0) {
    return '50px'; // Just enough for add new tag
  }
  
  // Calculate height based on number of items
  const itemCount = enhancedTagSuggestions.value.length + (tagInput.value.trim().length > 0 ? 1 : 0);
  
  if (itemCount <= 5) {
    // For 1-3 items, use content height (approximately 40px per item)
    return `${itemCount * 40}px`;
  } else {
    // For more items, cap at a reasonable maximum height
    return '250px';
  }
});
async function loadTags() {
  // Use tags from GraphStore instead of separate API call
  selectedTags.value = props.initialTags.map((tagId) => {
    const foundTag = availableTags.value.find((tag) => tag.id === tagId) || {
      id: tagId,
      label: `Tag ${tagId}`,
    };
    return foundTag;
  });
}

function updateTitle(e) {
  // Update local title with exactly what the user typed
  title.value = e.target.value;

  // Emit the actual user input (could be empty string)
  // Let parent decide if it needs a fallback value
  emit("update:title", title.value);
}

function handleTitleKeydown(e) {
  if (e.key === "Enter") {
    e.preventDefault(); // Prevent default Enter behavior
    emit("enter-pressed"); // Signal parent to focus editor
  }
}

function searchTags(e) {
  if (tagInput.value.length > 0) {
    // Filter tags from GraphStore
    tagSuggestions.value = availableTags.value.filter(
      (tag) =>
        tag.label.toLowerCase().includes(tagInput.value.toLowerCase()) &&
        !selectedTags.value.some((selected) => selected.id === tag.id)
    );
  } else {
    // Show all available tags that aren't already selected
    tagSuggestions.value = availableTags.value.filter(
      (tag) => !selectedTags.value.some((selected) => selected.id === tag.id)
    );
  }
  showSuggestions.value = true;
}

function handleTagInputFocus() {
  tagInputFocused.value = true;
  // Show all available tags immediately when focused
  searchTags();
}

function handleTagInputBlur(e) {
  // Small delay to allow clicking on suggestions
  setTimeout(() => {
    if (!e.relatedTarget?.closest(".tag-suggestions")) {
      tagInputFocused.value = false;
      showSuggestions.value = false;
    }
  }, 150);
}

function selectTag(tag) {
  selectedTags.value.push(tag);
  tagInput.value = "";
  showSuggestions.value = false;
  emit(
    "update:tags",
    selectedTags.value.map((tag) => tag.id)
  );
  nextTick(() => {
    tagInputRef.value?.focus();
  });
}

function removeTag(tag) {
  selectedTags.value = selectedTags.value.filter((t) => t.id !== tag.id);
  emit(
    "update:tags",
    selectedTags.value.map((tag) => tag.id)
  );
}

async function addTag(e) {
  e.preventDefault();
  if (tagInput.value.trim()) {
    // Find if tag already exists in store
    const existingTag = availableTags.value.find(
      (tag) => tag.label.toLowerCase() === tagInput.value.trim().toLowerCase()
    );

    if (existingTag) {
      selectTag(existingTag);
    } else {
      // Create new tag
      await createNewTag(tagInput.value.trim());
    }
  } else if (e.shiftKey) {
    // If Shift+Enter and no tag text, focus the editor
    emit("enter-pressed");
  }
}

async function createNewTag(tagName) {
  try {
    isCreatingTag.value = true;

    axios
      .post("/create", {
        type: "tag",
        name: tagName,
      })
      .then((response) => {
        graphStore.addNode(response.data);
        console.error("Tag created:", response.data);

        // Find the newly created tag in the updated store
        const newTag = graphStore.elements
          .filter((el) => el.type === "tag" && el.name === tagName)
          .map((tag) => ({
            id: tag.id,
            label: tag.name,
          }))[0];

        // Select the newly created tag
        if (newTag) {
          selectTag(newTag);
        }

        tagInput.value = "";
      });
  } catch (error) {
    console.error("Error creating new tag:", error);
    // Could add error handling/notification here
  } finally {
    isCreatingTag.value = false;
  }
}

function handleCreateNewTag() {
  if (tagInput.value.trim()) {
    createNewTag(tagInput.value.trim());
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
  <div
    class="top-0 z-10 bg-primary-foreground dark:bg-slate-900 pb-2"
    @click.stop
  >
    <!-- Title input with improved placeholder behavior -->
    <div class="mb-3 py-2 relative">
      <div
        class="absolute bottom-0 left-0 right-0 h-0.5 bg-gradient-to-r from-purple-700 to-purple-300/30 rounded"
      ></div>
      <h1
        class="m-0 text-3xl font-semibold text-purple-800 dark:text-purple-300"
      >
        <input
          ref="titleInputRef"
          type="text"
          v-model="title"
          class="bg-transparent border-0 w-full font-inherit text-inherit transition-colors duration-200 placeholder:text-purple-800/30 dark:placeholder:text-purple-300/30 placeholder:italic placeholder:font-normal focus:outline-none focus:placeholder:opacity-20"
          placeholder="Untitled Note"
          @input="updateTitle"
          @keydown="handleTitleKeydown"
          @click.stop
        />
      </h1>
    </div>

    <!-- Tags multiselect with compact styling -->
    <div
      class="relative mb-2 bg-purple-100/5 dark:bg-purple-900/5 rounded-xl py-1.5 px-2.5 border border-purple-300/10 dark:border-purple-600/10 transition-all duration-200 hover:bg-purple-100/8 dark:hover:bg-purple-900/8 hover:border-purple-300/20 dark:hover:border-purple-600/20"
      @click.stop
      :class="{ 'py-2 px-3': showAllTags || selectedTags.length > 5 }"
    >
      <div class="flex justify-between items-center mb-0.5">
        <div
          class="text-[0.65rem] font-medium text-purple-800/60 dark:text-purple-300/60 uppercase tracking-wider flex items-center"
        >
          Tags
          <span
            v-if="selectedTags.length > 0"
            class="inline-flex items-center justify-center bg-purple-800/10 dark:bg-purple-300/10 text-purple-800 dark:text-purple-300 rounded-full py-0.5 px-1.5 text-[0.6rem] ml-1.5"
          >
            {{ selectedTags.length }}
          </span>
        </div>
        <button
          v-if="selectedTags.length > 5"
          @click.stop="toggleTagsDisplay"
          class="text-[0.65rem] text-purple-800/80 dark:text-purple-300/80 bg-transparent border-0 cursor-pointer py-0.5 px-1.5 rounded transition-colors duration-200 hover:bg-purple-800/10 dark:hover:bg-purple-300/10"
          :aria-label="showAllTags ? 'Show fewer tags' : 'Show all tags'"
        >
          {{ showAllTags ? "Show less" : "Show all" }}
        </button>
      </div>
      <div
        class="max-h-[300px] overflow-y-auto transition-all duration-300"
        :class="{ 'max-h-8': !showAllTags && selectedTags.length > 5 }"
      >
        <div class="flex flex-wrap gap-1 items-center">
          <!-- Selected tags with compact styling -->
          <div
            v-if="selectedTags.length"
            class="flex flex-wrap gap-1 items-center"
          >
            <span
              v-for="(tag, index) in selectedTags"
              :key="tag.id"
              v-show="showAllTags || index < 5"
              class="rounded-md py-0.5 px-1.5 bg-purple-800 dark:bg-purple-700 text-slate-100 inline-flex items-center gap-0.5 text-xs leading-tight transition-all duration-200 max-w-[180px] h-5 hover:bg-purple-900 dark:hover:bg-purple-800 hover:-translate-y-px"
            >
              <span class="whitespace-nowrap overflow-hidden text-ellipsis">{{
                tag.label
              }}</span>
              <button
                @click.stop="removeTag(tag)"
                class="flex items-center justify-center border-0 bg-transparent text-inherit opacity-70 cursor-pointer p-0 w-3 h-3 rounded-full transition-opacity duration-200 hover:opacity-100"
                aria-label="Remove tag"
              >
                <svg
                  width="10"
                  height="10"
                  viewBox="0 0 24 24"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M18 6L6 18M6 6L18 18"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </button>
            </span>
            <span
              v-if="!showAllTags && selectedTags.length > 5"
              class="text-xs text-purple-800/80 dark:text-purple-300/80 bg-purple-800/10 dark:bg-purple-300/10 py-0.5 px-1.5 rounded-md cursor-pointer hover:bg-purple-800/15 dark:hover:bg-purple-300/15"
            >
              +{{ selectedTags.length - 5 }} more
            </span>
          </div>

          <!-- Tag input with compact styling -->
          <div class="flex-1 min-w-[60px] relative">
            <input
              ref="tagInputRef"
              type="text"
              v-model="tagInput"
              @input="searchTags"
              @keydown="handleTagInputKeydown"
              @focus="handleTagInputFocus"
              @blur="handleTagInputBlur"
              placeholder="Add tag..."
              class="bg-transparent border-0 py-0.5 px-0 text-xs w-full h-5 placeholder:text-purple-800/30 dark:placeholder:text-purple-300/30 placeholder:italic focus:outline-none focus:text-purple-800 dark:focus:text-purple-300 focus:placeholder:opacity-20"
              :class="{
                'text-purple-800 dark:text-purple-300': tagInputFocused,
              }"
            />
            <div
              v-if="isCreatingTag"
              class="absolute right-2 top-1/2 -translate-y-1/2"
            >
              <span
                class="inline-block w-3 h-3 border-2 border-purple-300/30 dark:border-purple-600/30 border-t-purple-600 dark:border-t-purple-300 rounded-full animate-spin"
              ></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Tag suggestions dropdown -->
      <div
        v-if="showSuggestions"
        class="absolute top-[calc(100%+4px)] left-0 w-full z-20 bg-white dark:bg-slate-800 border border-purple-300/20 dark:border-purple-600/20 rounded-lg shadow-lg animate-fadeIn overflow-hidden"
      >
      <ScrollArea
      :style="{ height: suggestionHeight }"
      class="tag-suggestions"
    >
          <div
            v-if="enhancedTagSuggestions.length === 0"
            class="py-1.5 px-2.5 text-xs text-purple-800/50 dark:text-purple-300/50 italic text-center"
          >
           
          </div>

          <div
            v-for="(tag, index) in enhancedTagSuggestions"
            :key="tag.id"
            :id="`tag-suggestion-${index}`"
            @click="selectTag(tag)"
            @mouseover="selectedSuggestionIndex = index"
            class="py-2 px-2.5 cursor-pointer transition-colors duration-150 text-xs rounded mx-1 my-0.5"
            :class="{
              'bg-purple-100/15 dark:bg-purple-800/25':
                index === selectedSuggestionIndex,
            }"
          >
            <div class="flex flex-col">
              <div class="font-medium">{{ tag.label }}</div>
              <div
                v-if="tag.parents && tag.parents.length"
                class="mt-0.5 text-[0.65rem] text-purple-800/60 dark:text-purple-300/60 italic"
              >
                Parents: {{ tag.parents.join(", ") }}
              </div>
            </div>
          </div>

          <!-- Create tag button always shows when text is entered -->
          <div
            v-if="tagInput.trim().length > 0"
            :id="`tag-suggestion-${enhancedTagSuggestions.length}`"
            @click="handleCreateNewTag"
            @mouseover="selectedSuggestionIndex = enhancedTagSuggestions.length"
            class="py-2 px-2.5 cursor-pointer transition-colors duration-150 text-xs rounded mx-1 my-0.5 flex items-center text-purple-800 dark:text-purple-300 font-medium"
            :class="{
              'bg-purple-100/15 dark:bg-purple-800/25':
                selectedSuggestionIndex === enhancedTagSuggestions.length,
            }"
          >
            <span class="mr-1.5 font-bold">+</span> Create tag "{{ tagInput }}"
          </div>
        </ScrollArea>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
:deep(.tag-suggestions) {
  transition: height 0.2s ease;
}
.animate-fadeIn {
  animation: fadeIn 0.2s ease;
}
</style>
