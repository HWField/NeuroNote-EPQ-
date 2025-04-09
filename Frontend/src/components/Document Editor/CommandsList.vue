<template>
  <div class="commands-dropdown">
    <ScrollArea 
      :style="{ height: commandsHeight }"
      class="commands-scroll-area"
    >
      <div class="py-1">
        <template v-if="items.length">
          <button
            :class="{ 'is-selected': index === selectedIndex }"
            v-for="(item, index) in items"
            :key="index"
            @click="selectItem(index)"
            class="command-item"
            :id="`command-item-${index}`"
          >
            <div class="command-icon">
              <component :is="item.icon" size="18" />
            </div>
            <span>{{ item.title }}</span>
          </button>
        </template>
        <div class="empty-item" v-else>No commands found</div>
      </div>
    </ScrollArea>
  </div>
</template>

<script>
import { eventBus } from '@/components/Document Editor/EventBus.js'; // Import the event
import { ScrollArea } from "@/components/ui/scroll-area";
import { computed } from 'vue';
import {
  Heading1,
  Heading2,
  Heading3,
  Bold,
  Italic,
  Underline as UnderlineIcon,
  Strikethrough,
  List,
  ListOrdered,
  Quote,
  Youtube as YoutubeIcon,
  Image as ImageIcon,
  CheckSquare,
  Code as CodeIcon,
  AlignLeft,
  AlignCenter,
  AlignRight,
  AlignJustify,
  FoldVertical,
  Link,
} from "lucide-vue-next";

export const commands = [
  {
    title: "Heading 1",
    icon: Heading1,
    command: ({ editor, range }) => {
      console.log("Executing command:", { range });
      editor
        .chain()
        .focus()
        .deleteRange(range)
        .setNode("heading", { level: 1 })
        .run();
    },
  },
  {
    title: "Heading 2",
    icon: Heading2,
    command: ({ editor, range }) => {
      editor
        .chain()
        .focus()
        .deleteRange(range)
        .setNode("heading", { level: 2 })
        .run();
    },
  },
  // {
  //   title: "Bold",
  //   icon: Bold,
  //   command: ({ editor, range }) => {
  //     editor.chain().focus().deleteRange(range).setMark("bold").run();
  //   },
  // },
  // {
  //   title: "Italic",
  //   icon: Italic,
  //   command: ({ editor, range }) => {
  //     editor.chain().focus().deleteRange(range).setMark("italic").run();
  //   },
  // },
  // {
  //   title: "Underline",
  //   icon: UnderlineIcon,
  //   command: ({ editor, range }) => {
  //     editor.chain().focus().deleteRange(range).setMark("underline").run();
  //   },
  // },
  // {
  //   title: "Strike",
  //   icon: Strikethrough,
  //   command: ({ editor, range }) => {
  //     editor.chain().focus().deleteRange(range).setMark("strike").run();
  //   },
  // },
  {
    title: "Bullet List",
    icon: List,
    command: ({ editor, range }) => {
      editor.chain().focus().deleteRange(range).toggleBulletList().run();
    },
  },
  {
    title: "Block Quote",
    icon: Quote,
    command: ({ editor, range }) => {
      editor.chain().focus().deleteRange(range).toggleBlockquote().run();
    },
  },
  {
    title: "YouTube",
    icon: YoutubeIcon,
    command: ({ editor, range }) => {
      const url = window.prompt("Enter the YouTube video URL");

      if (url) {
        editor
          .chain()
          .focus()
          .deleteRange(range)
          .setYoutubeVideo({ src: url })
          .run();
      }
    },
  },
  {
    title: "Image",
    icon: ImageIcon,
    command: ({ editor, range }) => {
      editor.chain().focus().deleteRange(range).run();
      // Emit an event instead of calling the function directly
      eventBus.emit('open-image-modal');
    },
  },
  {
    title: "Task List",
    icon: CheckSquare,
    command: ({ editor, range }) => {
      editor.chain().focus().deleteRange(range).toggleTaskList().run();
    },
  },
  {
    title: "Ordered List",
    icon: ListOrdered,
    command: ({ editor, range }) => {
      editor.chain().focus().deleteRange(range).toggleOrderedList().run();
    },
  },
  {
    title: "Code Block",
    icon: CodeIcon,
    command: ({ editor, range }) => {
      editor.chain().focus().deleteRange(range).toggleCodeBlock().run();
    },
  },
  {
    title: 'Link',
    description: 'Add a hyperlink',
    icon: Link, // Use appropriate icon
    command: ({ editor, range }) => {
      editor.chain()
        .focus()
        .deleteRange(range)
        .setHyperlink({ href: '' })
        .run();
    }
  },
  {
    title: "Collapsible",
    icon: FoldVertical,
    command: ({ editor, range }) => {
      editor
        .chain()
        .focus()
        .deleteRange(range)
        .insertContent({
          type: "details",
          content: [
            {
              type: "detailsSummary",
              content: [{ type: "text", text: "\u200B" }],
            },
            {
              type: "detailsContent",
              content: [
                {
                  type: "paragraph",
                  content: [{ type: "text", text: "\u200B" }],
                },
              ],
              HTMLAttributes: {
                open: true,
              },
            },
          ],
        })
        .run();
    },
  },
];
export default {
  components: {
    ScrollArea, // Add this line
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
    };
  },
  computed: {
    commandsHeight() {
      // Base height for empty results or single item
      if (this.items.length === 0) {
        return '50px';
      }
      
      // Calculate height based on number of items
      const itemCount = this.items.length;
      
      if (itemCount <= 5) {
        // For 1-5 items, use content height (approximately 40px per item)
        return `${itemCount * 40}px`;
      } else {
        // For more items, cap at a reasonable maximum height
        return '250px';
      }
    }
  },
  watch: {
    items() {
      this.selectedIndex = 0;
    },
  },

  methods: {
    onKeyDown({ event }) {
      if (event.key === "ArrowUp") {
        this.upHandler();
        return true;
      }

      if (event.key === "ArrowDown") {
        this.downHandler();
        return true;
      }

      if (event.key === "Enter") {
        this.enterHandler();
        return true;
      }

      return false;
    },

    upHandler() {
      this.selectedIndex =
        (this.selectedIndex + this.items.length - 1) % this.items.length;
      this.$nextTick(() => this.scrollToSelected());
    },

    downHandler() {
      this.selectedIndex = (this.selectedIndex + 1) % this.items.length;
      this.$nextTick(() => this.scrollToSelected());
    },

    scrollToSelected() {
      this.$nextTick(() => {
        const selectedElement = document.getElementById(
          `command-item-${this.selectedIndex}`
        );
        if (selectedElement) {
          selectedElement.scrollIntoView({
            block: "nearest",
            behavior: "smooth",
          });
        }
      });
    },
    enterHandler() {
      this.selectItem(this.selectedIndex);
    },

    selectItem(index) {
      const item = this.items[index];

      if (item) {
        this.command(item);
      }
    },
  },
};
</script>

<style scoped>
.commands-dropdown {
  /* Base styling */
  @apply bg-white dark:bg-slate-800 
         border border-slate-200 dark:border-slate-700
         rounded-xl shadow-lg p-1;
         
  /* Animation */
  animation: fadeIn 0.2s ease-out;
}

.commands-scroll-area {
  transition: height 0.2s ease;
}

.command-item {
  @apply flex items-center gap-2 w-full text-left
         py-2 px-2.5 rounded-md mx-1 my-0.5
         text-sm font-medium
         text-slate-700 dark:text-slate-200
         transition-colors duration-150;
}

.command-icon {
  @apply text-slate-500 dark:text-slate-400 flex-shrink-0;
}

.command-item:hover, .command-item.is-selected {
  @apply bg-slate-100 dark:bg-slate-700;
}

.empty-item {
  @apply py-3 text-center text-sm text-slate-400 dark:text-slate-500 italic;
}

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
</style>