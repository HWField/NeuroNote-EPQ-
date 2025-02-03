<script setup>
import { ref } from "vue";
import { Editor, EditorContent } from "@tiptap/vue-3";
import StarterKit from "@tiptap/starter-kit";
import TextStyle from "@tiptap/extension-text-style";
import Highlight from "@tiptap/extension-highlight";
import FontFamily from "@tiptap/extension-font-family";
import { Button } from "@/components/ui/button"; // ShadCN Button
import { DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem } from "@/components/ui/dropdown-menu"; // ShadCN Dropdown

// Initialize the editor
const editor = ref(
  new Editor({
    extensions: [
      StarterKit,
      TextStyle,
      Highlight,
      FontFamily.configure({
        types: ["textStyle"],
      }),
    ],
    content: "<p>Start writing here...</p>",
  })
);

// Font options
const fonts = [
  "Arial",
  "Courier New",
  "Georgia",
  "Tahoma",
  "Times New Roman",
  "Verdana",
];

// Set font family
const setFont = (font) => {
  editor.value.chain().focus().setFontFamily(font).run();
};

// Set highlight color
const setHighlight = (color) => {
  editor.value.chain().focus().toggleHighlight({ color }).run();
};
</script>

<template>
  <div class="editor-container border rounded-lg p-4 space-y-2">
    <!-- Toolbar -->
    <div class="toolbar flex gap-2 flex-wrap">
      <Button @click="editor.chain().focus().toggleBold().run()" :class="{ 'bg-gray-300': editor.isActive('bold') }">
        Bold
      </Button>
      <Button @click="editor.chain().focus().toggleItalic().run()" :class="{ 'bg-gray-300': editor.isActive('italic') }">
        Italic
      </Button>
      <Button @click="editor.chain().focus().toggleUnderline().run()" :class="{ 'bg-gray-300': editor.isActive('underline') }">
        Underline
      </Button>
      <Button @click="editor.chain().focus().toggleStrike().run()" :class="{ 'bg-gray-300': editor.isActive('strike') }">
        Strikethrough
      </Button>

      <!-- Font Family Dropdown -->
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <Button>Font</Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem v-for="font in fonts" :key="font" @click="setFont(font)">
            {{ font }}
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      <!-- Highlight Color Dropdown -->
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <Button>Highlight</Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem @click="setHighlight('yellow')">Yellow</DropdownMenuItem>
          <DropdownMenuItem @click="setHighlight('pink')">Pink</DropdownMenuItem>
          <DropdownMenuItem @click="setHighlight('lightblue')">Blue</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>

    <!-- Editor Content -->
    <EditorContent :editor="editor" class="border p-4 rounded-md min-h-[200px]" />
  </div>
</template>

<style>
.editor-container {
  max-width: 600px;
  margin: auto;
}

.toolbar button {
  font-size: 14px;
}

.ProseMirror {
  outline: none;
  min-height: 150px;
}
</style>