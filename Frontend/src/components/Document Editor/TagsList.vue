<!-- filepath: /Users/Henry/Desktop/EPQ/Frontend/src/components/Document Editor/TagsList.vue -->
<template>
  <div class="dropdown-menu">
    <ScrollArea class="tags-scroll-area flex flex-col overflow-y-auto">
      <div class="py-1">
        <template v-if="items.length">
          <button
            :class="{ 'is-selected': index === selectedIndex }"
            v-for="(item, index) in items"
            :key="index"
            @click="selectItem(index)"
            class="tag-item"
            :id="`tag-item-${index}`"
          >
            <div class="tag-icon">
              <component :is="tagIcon" size="18" />
            </div>
            <span>{{ item.title }}</span>
          </button>
        </template>
        <div class="item" v-else>No tags found</div>
      </div>
    </ScrollArea>
  </div>
</template>

<script>
import { ScrollArea } from "@/components/ui/scroll-area";
import { Hash } from "lucide-vue-next";
import { computed } from "vue";
import { useGraphStore } from '@/stores/useGraphStore';

// Export the tags data retrieval function
export function getTags(query = "") {
  const graphStore = useGraphStore();
  
  const tagElements = graphStore.elements.filter((el) => el.type === "tag");

  return tagElements
    .filter(tag => tag.name.toLowerCase().includes(query.toLowerCase()))
    // .slice(0, 100)
    .map(tag => ({
      id: tag.id,
      title: tag.name
    }));
}

export default {
  components: {
    ScrollArea,
  },
  
  props: {
    items: {
      type: Array,
      required: true,
    },
    command: {
      type: Function,
      required: true,
    },
  },

  data() {
    return {
      selectedIndex: 0,
      tagIcon: Hash
    }
  },

  watch: {
    items() {
      this.selectedIndex = 0
    },
  },

  methods: {
    onKeyDown({ event }) {
      if (event.key === 'ArrowUp') {
        this.upHandler()
        return true
      }

      if (event.key === 'ArrowDown') {
        this.downHandler()
        return true
      }

      if (event.key === 'Enter') {
        event.preventDefault();
        this.enterHandler()
        return true
      }

      return false
    },

    upHandler() {
      this.selectedIndex = ((this.selectedIndex + this.items.length) - 1) % this.items.length
      this.$nextTick(() => this.scrollToSelected())
    },

    downHandler() {
      this.selectedIndex = (this.selectedIndex + 1) % this.items.length
      this.$nextTick(() => this.scrollToSelected())
    },

    scrollToSelected() {
      this.$nextTick(() => {
        const selectedElement = document.getElementById(`tag-item-${this.selectedIndex}`);
        if (selectedElement) {
          selectedElement.scrollIntoView({
            block: "nearest",
            behavior: "smooth"
          });
        }
      });
    },

    enterHandler() {
      this.selectItem(this.selectedIndex)
    },

    selectItem(index) {
      
      const item = this.items[index]
      

      if (item) {
        this.command(item)
      }
    },
  },
}
</script>

<style lang="scss">
/* Dropdown menu */
.dropdown-menu {
  background: var(--white);
  border: 1px solid var(--gray-1);
  border-radius: 0.75rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  padding: 0.25rem;
  position: relative;
  @apply bg-slate-700 border border-slate-600 text-white;

  .tags-scroll-area {
    @apply max-h-52;
  }

  button.tag-item {
    align-items: center;
    background-color: transparent;
    display: flex;
    gap: 0.5rem;
    text-align: left;
    width: 100%;
    @apply py-2 px-3 rounded-md my-0.5 transition-colors duration-150;

    .tag-icon {
      @apply flex items-center justify-center text-slate-300 min-w-[24px];
    }

    span {
      @apply font-medium;
    }

    &:hover,
    &:hover.is-selected {
      @apply bg-slate-600;
    }

    &.is-selected {
      @apply bg-slate-500;
    }
  }

  .item {
    @apply py-3 text-center text-sm text-slate-400;
  }
}
</style>