<template>
  <div class="dropdown-menu">
    <ScrollArea class="command-scroll-area flex flex-col overflow-y-auto">
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
              <component :is="item.icon" size="20" />
            </div>
            <span>{{ item.title }}</span>
          </button>
        </template>
        <div class="item" v-else>No result</div>
      </div>
    </ScrollArea>
  </div>
</template>
<script>
import { ScrollArea } from "@/components/ui/scroll-area";
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
      const url = window.prompt("Enter the image URL");

      if (url) {
        editor.chain().focus().deleteRange(range).setImage({ src: url }).run();
      }
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

  .command-scroll-area {
    @apply max-h-52; /* Slightly taller to show more items */
  }

  button.command-item {
    align-items: center;
    background-color: transparent;
    display: flex;
    gap: 0.5rem;
    text-align: left;
    width: 100%;
    @apply py-2 px-3 rounded-md my-0.5 transition-colors duration-150;

    .command-icon {
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