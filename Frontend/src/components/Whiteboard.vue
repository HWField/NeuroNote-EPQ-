<script setup>
import Gapcursor from "@tiptap/extension-gapcursor";
import Code from "@tiptap/extension-code";
import Document from "@tiptap/extension-document";
import Mention from "@tiptap/extension-mention";
// import suggestion from "@/components/Document Editor/TagSuggestion.js";
import Heading from "@tiptap/extension-heading";
// import TagsList from "@/components/Document Editor/TagsList.vue";

import { Commands } from "@/components/Document Editor/commands.js";
import CommandsList, {
  commands,
} from "@/components/Document Editor/CommandsList.vue";

import { Tags } from "@/components/Document Editor/Tags.js";
import TagsList, { getTags } from "@/components/Document Editor/TagsList.vue";

import { VueRenderer } from "@tiptap/vue-3";
import tippy from "tippy.js";
import Underline from "@tiptap/extension-underline";
import Youtube from "@tiptap/extension-youtube";
import { PluginKey } from "prosemirror-state";
import OrderedList from "@tiptap/extension-ordered-list";
import BulletList from "@tiptap/extension-bullet-list";
import ListItem from "@tiptap/extension-list-item";
import Highlight from "@tiptap/extension-highlight";
import TextAlign from "@tiptap/extension-text-align";
import Placeholder from "@tiptap/extension-placeholder";
import Paragraph from "@tiptap/extension-paragraph";
import Text from "@tiptap/extension-text";
import TaskItem from "@tiptap/extension-task-item";
import TaskList from "@tiptap/extension-task-list";
import Typography from "@tiptap/extension-typography";
import Image from "@tiptap/extension-image";
import Details from "@tiptap-pro/extension-details";
import DetailsContent from "@tiptap-pro/extension-details-content";
import DetailsSummary from "@tiptap-pro/extension-details-summary";
import CodeBlockLowlight from "@tiptap/extension-code-block-lowlight";
import css from "highlight.js/lib/languages/css";
import js from "highlight.js/lib/languages/javascript";
import ts from "highlight.js/lib/languages/typescript";
import html from "highlight.js/lib/languages/xml";
import py from "highlight.js/lib/languages/python";
import csharp from "highlight.js/lib/languages/csharp";
import json from "highlight.js/lib/languages/json";
import sql from "highlight.js/lib/languages/sql";
import { createLowlight } from "lowlight";
import { Editor, EditorContent } from "@tiptap/vue-3";
import StarterKit from "@tiptap/starter-kit";
import { ColorHighlighter } from "@/components/Document Editor/ColorHighlighter.ts";
import { SmilieReplacer } from "@/components/Document Editor/SymbolReplacer.ts";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Extension } from "@tiptap/core";
import { Node } from "@tiptap/core";
import { Button } from "@/components/ui/Button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu";
import { Switch } from '@/components/ui/switch'
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Separator } from "@/components/ui/separator";
import {
  Bold as BoldIcon,
  Italic as ItalicIcon,
  Underline as UnderlineIcon,
  Strikethrough as StrikethroughIcon,
  Code as CodeIcon,
  AlignLeft as AlignLeftIcon,
  AlignCenter as AlignCenterIcon,
  AlignRight as AlignRightIcon,
  AlignJustify as AlignJustifyIcon,
  ChevronDown as ChevronDownIcon,
  Text as TextIcon,
  X as XIcon,
  Paintbrush as PaintbrushIcon,
} from "lucide-vue-next";

import { useGraphStore } from "@/stores/useGraphStore";
import axios from "../axios.js";

import { ref, onBeforeUnmount, watch } from "vue";
import { onMounted } from "vue";
const emit = defineEmits(['note-closed']);
const externalTags = ref([]);
const lowlight = createLowlight();

// lowlight languages editor can use
lowlight.register("html", html);
lowlight.register("css", css);
lowlight.register("js", js);
lowlight.register("ts", ts);
lowlight.register("py", py);
lowlight.register("csharp", csharp);
lowlight.register("json", json);
lowlight.register("sql", sql);

const props = defineProps({
  noteId: Number || 31,
});

const focusEditor = (event) => {
  if (editor) {
    editor.chain().focus().run();
  }
};

function extractTagsFromDocument(document) {
  // Debug the document structure
  console.log(
    "Document structure:",
    JSON.stringify(document).slice(0, 200) + "..."
  );

  const uniqueTagIds = new Set();

  // Improved traversal function
  const traverse = (node) => {
    // Check if this is a mention node
    if (node.type === "mention" && node.attrs && node.attrs.id) {
      console.log("Found mention node:", node);
      uniqueTagIds.add(node.attrs.id); // Push only the ID
    }

    // Process content array if it exists
    if (node.content && Array.isArray(node.content)) {
      node.content.forEach((childNode) => traverse(childNode));
    }

    // Also check marks for mentions (sometimes they're nested in marks)
    if (node.marks && Array.isArray(node.marks)) {
      node.marks.forEach((mark) => {
        if (mark.type === "mention" && mark.attrs && mark.attrs.id) {
          uniqueTagIds.add(mark.attrs.id); // Push only the ID
        }
      });
    }
  };

  // Start traversal with the document
  if (document && document.content) {
    document.content.forEach((node) => traverse(node));
  }

  const tagIds = Array.from(uniqueTagIds);

  console.log("Tag IDs extracted:", tagIds);
  return tagIds; // Return array of IDs directly
}

function SaveToBackend() {
  let noteContent = editor.getJSON();
  let noteName = "Untitled Note";
  const tags = extractTagsFromDocument(noteContent);
  if (noteContent && noteContent.content && noteContent.content.length > 0) {
    const titleNode = noteContent.content[0];

    // Extract text content from title node without mentions
    if (titleNode.content) {
      noteName = titleNode.content
        .filter((item) => item.type !== "mention")
        .map((item) => item.text || "")
        .join("")
        .trim();

      // Use default if title is empty after removing mentions
      if (!noteName) {
        noteName = "Untitled Note";
      }
    }
  }
  console.error("Note name:", noteName);
  axios
    .post("/update", {
      operation: "content",
      name: noteName,
      content: noteContent,
      tags: tags, // Send the extracted tags
      id: props.noteId,
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

function LoadFromBackend() {
  axios
    .post("/load", {
      id: props.noteId,
      operation: "content",
    })
    .then((response) => {
      // Clone the content to avoid direct mutation
      const content = JSON.parse(JSON.stringify(response.data.content));

      // Set content first
      editor.commands.setContent(content);
      
      // Wait for content to be properly set
      setTimeout(() => {
        try {
          if (response.data.name) {
            // Make sure we can find the title node
            const titleNode = editor.state.doc.content.firstChild;
            
            if (titleNode && titleNode.type.name === "title") {
              // Now safely select and modify the title
              editor
                .chain()
                .focus()
                .setNodeSelection(1)
                .deleteSelection()
                .insertContent({
                  type: "title",
                  content: [
                    { type: "text", text: response.data.name },
                    { type: "text", text: " " }
                  ],
                })
                .run();
            }
          }
          
          editor.commands.focus("end");
        } catch (e) {
          console.error("Error updating title:", e);
        }
      }, 10); // Small delay to ensure content is set
    });
}

onMounted(() => {
  LoadFromBackend();
  editor.chain().focus().run();
});

onBeforeUnmount(() => {
  console.error("Saving to backend...");
  SaveToBackend();
  if (editor) {
    editor.destroy();
  }
});

const CustomDocument = Document.extend({
  content: "title block+ ",
});

const Title = Heading.extend({
  name: "title",
  marks: "",
  group: "title",
  content: "inline*",
  defining: true,
  selectable: false,

  parseHTML() {
    return [{ tag: "div.note-title-container h1" }, { tag: "h1:first-child" }];
  },

  renderHTML({ HTMLAttributes }) {
    return [
      "div",
      { class: "note-title-container" },
      ["h1", HTMLAttributes, 0],
    ];
  },
}).configure({ levels: [1] });



let editor = new Editor({
  extensions: [
    Document,
    Details.configure({
      persist: true,
      HTMLAttributes: {
        class: "details",
      },
    }),
    DetailsSummary,
    DetailsContent,
    Paragraph,
    Heading,
    Underline,
    Text,
    Title,
    TaskList,
    TaskItem.configure({
      nested: true,
    }),
    Youtube.configure({
      controls: true,
      nocookie: true,
      modestBranding: true,
    }),
    Code,
    CodeBlockLowlight.configure({
      lowlight,
    }),
    OrderedList,
    BulletList,
    ListItem,
    Typography,
    ColorHighlighter,
    SmilieReplacer,
    CustomDocument,
    StarterKit.configure({
      document: false,
    }),
    TextAlign.configure({
      types: ["heading", "paragraph"],
    }),
    Highlight.configure({ multicolor: true }),
    Mention.configure({
      HTMLAttributes: {
        class: "mention",
      },
      // suggestion,
    }),
    Extension.create({
      name: "customSelectAll",

      addKeyboardShortcuts() {
        return {
          "Mod-a": ({ editor }) => {
            const { state } = editor;
            const { doc } = state;

            // Skip the title node (first node) and find the position right after it
            if (doc.firstChild && doc.childCount > 1) {
              // Get the position after the first node (title)
              const startPos = doc.firstChild.nodeSize;

              // Set selection from start of content to end of document
              editor.commands.setTextSelection({
                from: startPos,
                to: doc.content.size,
              });

              return true;
            }

            return false;
          },
        };
      },
    }),
    Commands.configure({
      suggestion: {
        items: ({ query }) => {
          return commands.filter((command) => {
            return command.title.toLowerCase().includes(query.toLowerCase());
          });
        },
        render: () => {
          // Your existing render function with VueRenderer and tippy
          // ...
          let component;
          let popup;

          return {
            onStart: (props) => {
              component = new VueRenderer(CommandsList, {
                // using vue 2:
                // parent: this,
                // propsData: props,
                // using vue 3:
                props,
                editor: props.editor,
              });

              if (!props.clientRect) {
                return;
              }

              popup = tippy("body", {
                getReferenceClientRect: props.clientRect,
                appendTo: () => document.body,
                content: component.element,
                showOnCreate: true,
                interactive: true,
                trigger: "manual",
                placement: "bottom-start",
              });
            },

            onUpdate(props) {
              component.updateProps(props);

              if (!props.clientRect) {
                return;
              }

              popup[0].setProps({
                getReferenceClientRect: props.clientRect,
              });
            },

            onKeyDown(props) {
              if (props.event.key === "Escape") {
                popup[0].hide();

                return true;
              }

              return component.ref?.onKeyDown(props);
            },

            onExit() {
              popup[0].destroy();
              component.destroy();
            },
          };
        },
      },
    }),
    Tags.configure({
      suggestion: {
        items: ({ query }) => {
          return getTags(query);
        },
        render: () => {
          let component;
          let popup;

          return {
            onStart: (props) => {
              component = new VueRenderer(TagsList, {
                props,
                editor: props.editor,
              });

              if (!props.clientRect) {
                return;
              }

              popup = tippy("body", {
                getReferenceClientRect: props.clientRect,
                appendTo: () => document.body,
                content: component.element,
                showOnCreate: true,
                interactive: true,
                trigger: "manual",
                placement: "bottom-start",
              });
            },

            onUpdate(props) {
              component.updateProps(props);

              if (!props.clientRect) {
                return;
              }

              popup[0].setProps({
                getReferenceClientRect: props.clientRect,
              });
            },

            onKeyDown(props) {
              if (props.event.key === "Escape") {
                popup[0].hide();
                return true;
              }

              return component.ref?.onKeyDown(props);
            },

            onExit() {
              popup[0].destroy();
              component.destroy();
            },
          };
        },
      },
    }),
    Image,
    Gapcursor,
    Placeholder.configure({
      // emptyEditorClass: 'h1',
      showOnlyCurrent: false,
      placeholder: ({ node }) => {
        if (node.type.name === "title") {
          return "Untitled Note:";
        }

        // return "Lets get writing...";
      },
    }),
  ],
  editorProps: {
    attributes: {
      class: "",
    },
  },
  content: `
     <div class="note-title-container">
    <h1>Untitled Note</h1>
  </div>
  <div class="tags-container"></div>
  <p></p>
  `,
});
</script>

<template>
  <div class="flex w-full h-full flex-col">
    <!-- Floating Toolbar -->
    <div class="h-24 w-full mb-0 relative">
      <div class="absolute top-6 w-full z-50 px-4 flex justify-center">
        <div
          class="bg-primary-foreground shadow-lg rounded-lg p-3 max-w-[90%] mx-auto"
        >
          <div class="flex items-center gap-1">
            <!-- above flex wrap -->
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    @click="emit('note-closed')"
                    class="mr-2 bg-red-100 dark:bg-red-900/20 hover:bg-red-200 dark:hover:bg-red-800/30"
                  >
                    <XIcon class="h-4 w-4 text-red-500 dark:text-red-400" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>Close Note</TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <Separator orientation="vertical" class="h-6 mx-1" />
            <!-- Basic Text Formatting -->
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    @click="editor.chain().focus().toggleBold().run()"
                    :class="{ 'bg-primary/20': editor.isActive('bold') }"
                  >
                    <BoldIcon class="h-4 w-4" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>Bold</TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    @click="editor.chain().focus().toggleItalic().run()"
                    :class="{ 'bg-primary/20': editor.isActive('italic') }"
                  >
                    <ItalicIcon class="h-4 w-4" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>Italic</TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    @click="editor.chain().focus().toggleUnderline().run()"
                    :class="{ 'bg-primary/20': editor.isActive('underline') }"
                  >
                    <UnderlineIcon class="h-4 w-4" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>Underline</TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    @click="editor.chain().focus().toggleStrike().run()"
                    :class="{ 'bg-primary/20': editor.isActive('strike') }"
                  >
                    <StrikethroughIcon class="h-4 w-4" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>Strikethrough</TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    @click="editor.chain().focus().toggleCode().run()"
                    :class="{ 'bg-primary/20': editor.isActive('code') }"
                  >
                    <CodeIcon class="h-4 w-4" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>Emphasis</TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <Separator orientation="vertical" class="h-6 mx-1" />

            <!-- Heading Dropdown -->
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="ghost"
                  size="sm"
                  class="flex gap-1 items-center"
                >
                  <TextIcon class="h-4 w-4" />
                  <span>Headings</span>
                  <ChevronDownIcon class="h-3 w-3 opacity-50" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent>
                <DropdownMenuItem
                  @click="editor.chain().focus().setParagraph().run()"
                >
                  <span :class="{ 'font-bold': editor.isActive('paragraph') }"
                    >Paragraph</span
                  >
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem
                  @click="
                    editor.chain().focus().toggleHeading({ level: 1 }).run()
                  "
                >
                  <span
                    :class="{
                      'font-bold': editor.isActive('heading', { level: 1 }),
                    }"
                    >Heading 1</span
                  >
                </DropdownMenuItem>
                <DropdownMenuItem
                  @click="
                    editor.chain().focus().toggleHeading({ level: 2 }).run()
                  "
                >
                  <span
                    :class="{
                      'font-bold': editor.isActive('heading', { level: 2 }),
                    }"
                    >Heading 2</span
                  >
                </DropdownMenuItem>
                <DropdownMenuItem
                  @click="
                    editor.chain().focus().toggleHeading({ level: 3 }).run()
                  "
                >
                  <span
                    :class="{
                      'font-bold': editor.isActive('heading', { level: 3 }),
                    }"
                    >Heading 3</span
                  >
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            <Separator orientation="vertical" class="h-6 mx-1" />

            <!-- Alignment Options -->
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    @click="editor.chain().focus().setTextAlign('left').run()"
                    :class="{
                      'bg-primary/20': editor.isActive({ textAlign: 'left' }),
                    }"
                  >
                    <AlignLeftIcon class="h-4 w-4" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>Align left</TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    @click="editor.chain().focus().setTextAlign('center').run()"
                    :class="{
                      'bg-primary/20': editor.isActive({ textAlign: 'center' }),
                    }"
                  >
                    <AlignCenterIcon class="h-4 w-4" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>Align center</TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    @click="editor.chain().focus().setTextAlign('right').run()"
                    :class="{
                      'bg-primary/20': editor.isActive({ textAlign: 'right' }),
                    }"
                  >
                    <AlignRightIcon class="h-4 w-4" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>Align right</TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    @click="
                      editor.chain().focus().setTextAlign('justify').run()
                    "
                    :class="{
                      'bg-primary/20': editor.isActive({
                        textAlign: 'justify',
                      }),
                    }"
                  >
                    <AlignJustifyIcon class="h-4 w-4" />
                  </Button>
                </TooltipTrigger>
                <TooltipContent>Justify</TooltipContent>
              </Tooltip>
            </TooltipProvider>

            <Separator orientation="vertical" class="h-6 mx-1" />

            <!-- Highlight Colors Dropdown -->
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="ghost"
                  size="sm"
                  class="flex gap-1 items-center"
                >
                  <PaintbrushIcon class="h-4 w-4" />
                  <span>Highlight</span>
                  <ChevronDownIcon class="h-3 w-3 opacity-50" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent>
                <div class="flex flex-wrap gap-1 p-2 w-48">
                  <Button
                    variant="outline"
                    size="sm"
                    class="h-7 w-7 bg-yellow-200 hover:bg-yellow-300 border-yellow-400"
                    @click="
                      editor
                        .chain()
                        .focus()
                        .toggleHighlight({ color: '#fef08a' })
                        .run()
                    "
                    :class="{
                      'ring-2 ring-offset-1': editor.isActive('highlight', {
                        color: '#fef08a',
                      }),
                    }"
                  />

                  <Button
                    variant="outline"
                    size="sm"
                    class="h-7 w-7 bg-green-200 hover:bg-green-300 border-green-400"
                    @click="
                      editor
                        .chain()
                        .focus()
                        .toggleHighlight({ color: '#bbf7d0' })
                        .run()
                    "
                    :class="{
                      'ring-2 ring-offset-1': editor.isActive('highlight', {
                        color: '#bbf7d0',
                      }),
                    }"
                  />

                  <Button
                    variant="outline"
                    size="sm"
                    class="h-7 w-7 bg-blue-200 hover:bg-blue-300 border-blue-400"
                    @click="
                      editor
                        .chain()
                        .focus()
                        .toggleHighlight({ color: '#bfdbfe' })
                        .run()
                    "
                    :class="{
                      'ring-2 ring-offset-1': editor.isActive('highlight', {
                        color: '#bfdbfe',
                      }),
                    }"
                  />

                  <Button
                    variant="outline"
                    size="sm"
                    class="h-7 w-7 bg-pink-200 hover:bg-pink-300 border-pink-400"
                    @click="
                      editor
                        .chain()
                        .focus()
                        .toggleHighlight({ color: '#fbcfe8' })
                        .run()
                    "
                    :class="{
                      'ring-2 ring-offset-1': editor.isActive('highlight', {
                        color: '#fbcfe8',
                      }),
                    }"
                  />

                  <Button
                    variant="outline"
                    size="sm"
                    class="h-7 w-7 bg-purple-200 hover:bg-purple-300 border-purple-400"
                    @click="
                      editor
                        .chain()
                        .focus()
                        .toggleHighlight({ color: '#e9d5ff' })
                        .run()
                    "
                    :class="{
                      'ring-2 ring-offset-1': editor.isActive('highlight', {
                        color: '#e9d5ff',
                      }),
                    }"
                  />

                  <Button
                    variant="outline"
                    size="sm"
                    class="h-7 w-7 bg-orange-200 hover:bg-orange-300 border-orange-400"
                    @click="
                      editor
                        .chain()
                        .focus()
                        .toggleHighlight({ color: '#fed7aa' })
                        .run()
                    "
                    :class="{
                      'ring-2 ring-offset-1': editor.isActive('highlight', {
                        color: '#fed7aa',
                      }),
                    }"
                  />

                  <Button
                    variant="outline"
                    size="sm"
                    class="h-7 w-7 bg-red-200 hover:bg-red-300 border-red-400"
                    @click="
                      editor
                        .chain()
                        .focus()
                        .toggleHighlight({ color: '#fecaca' })
                        .run()
                    "
                    :class="{
                      'ring-2 ring-offset-1': editor.isActive('highlight', {
                        color: '#fecaca',
                      }),
                    }"
                  />

                  <Button
                    variant="outline"
                    size="sm"
                    class="h-7 w-7 bg-gray-200 hover:bg-gray-300 border-gray-400"
                    @click="
                      editor
                        .chain()
                        .focus()
                        .toggleHighlight({ color: '#e5e7eb' })
                        .run()
                    "
                    :class="{
                      'ring-2 ring-offset-1': editor.isActive('highlight', {
                        color: '#e5e7eb',
                      }),
                    }"
                  />

                  <Button
                    variant="outline"
                    size="sm"
                    class="h-7 w-7 flex items-center justify-center"
                    @click="editor.chain().focus().unsetHighlight().run()"
                  >
                    <XIcon class="h-4 w-4" />
                  </Button>
                </div>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </div>
    </div>

    <div class="flex justify-center flex-1">
      <ScrollArea
        class="editor w-full max-w-[2000px] h-[calc(100vh-12rem)] overflow-y-auto bg-primary-foreground rounded-lg border border-input m-4"
        @click="focusEditor"
      >
        <editor-content class="p-4" :editor="editor" />
      </ScrollArea>
    </div>
  </div>
</template>

<style lang="scss">
math-inline {
  font-family: "KaTeX_Main", serif;
  min-width: 1em;
  min-height: 1em;
  font-size: 1em;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  @apply bg-purple-600;
}

math-inline.ProseMirror-selectednode {
  outline: 2px solid #6a00f5;
  background-color: rgba(106, 0, 245, 0.1);
}

math-display {
  display: block;
  font-family: "KaTeX_Main", serif;
  font-size: 1.2em;
  padding: 0.5rem 0;
  cursor: pointer;
}

math-display.ProseMirror-selectednode {
  outline: 2px solid #6a00f5;
  background-color: rgba(106, 0, 245, 0.1);
}

/* Additional KaTeX-related styles */
.katex-html {
  display: none;
}
/* Basic editor styles */

// .ProseMirror:focus {
//     outline: none;
//   }
//   .ProseMirror {
//   min-height: 100px;
//   max-height: 100%;
//   overflow: scroll;
// }
// *,
// *::before,
// *::after {
//   box-sizing: border-box;
// }
::selection {
  background: #6a00f5;
  color: white;
}

.tiptap {
  caret-color: #6a00f5;

  &:focus {
    outline: none;
  }
  &.ProseMirror-selectednode {
    outline: 3px solid var(--purple);
  }
  // :first-child {
  //   margin-top: 0;
  // }
  .editor h1:first-child {
    font-size: 1.5rem;
    font-weight: bold;
    color: #333;
    border-bottom: 2px solid #ddd;
    margin-bottom: 8px;
    padding-bottom: 4px;
  }

  /* Color swatches */
  .color {
    white-space: nowrap;

    &::before {
      background-color: var(--color);
      border: 1px solid rgba(128, 128, 128, 0.3);
      border-radius: 2px;
      content: " ";
      display: inline-block;
      height: 1em;
      margin-bottom: 0.15em;
      margin-right: 0.1em;
      vertical-align: middle;
      width: 1em;
    }
  }

  // Note title container styling
  .note-title-container {
    position: relative;
    margin: 0 0 1rem;
    padding: 1rem 0;
    border-bottom: 2px solid #6a00f5;

    // Pseudo-elements for visual distinction
    // &::before {
    //   content: '';
    //   position: absolute;
    //   top: 0;
    //   left: 0;
    //   right: 0;
    //   height: 1px;
    //   @apply bg-purple-600;
    // }
    // .is-empty::before,
    h1 {
      margin: 0;
      font-size: 1.8rem;
      @apply text-purple-800 dark:text-purple-300;
      // float: left;
      // height: 0;
    }

    // Add a subtle background for visual emphasis
    @apply bg-purple-100/30 dark:bg-purple-900/10 rounded-md px-4;
  }
  .mention {
    border-radius: 0.4rem;
    box-decoration-break: clone;
    padding: 0.1rem 0.3rem 0.1rem 0.2rem; /* Adjust padding to account for the @ */
    @apply bg-purple-800 text-purple-200;
    position: relative;

    &::first-letter {
      /* Style for the @ symbol */
      @apply text-purple-300; /* Lighter color for better contrast */
      font-weight: 300; /* Lighter weight */
      opacity: 0.2;
      /* Optional: add a subtle spacing after @ */
      margin-right: 10px;
    }
    // /* Add a subtle tag symbol */
    // &::before {
    //   content: "@";
    //   opacity: 0.7;
    //   margin-right: 2px;
    //   position: relative;
    //   display: inline;
    // }
  }

  .note-title-container .mention {
    font-size: 0.9rem; // Smaller font size
    padding: 0.05rem 0.2rem; // Smaller padding
    vertical-align: middle; // Better alignment with title text
    @apply bg-purple-700 text-purple-100; // Slightly different color if desired
  }

  .note-title-container .mention::first-letter {
    @apply text-purple-200;
    opacity: 0.1;
  }



  /* Task list specific styles */
  ul[data-type="taskList"] {
    list-style: none;
    margin-left: 0;
    padding: 0;

    li {
      align-items: flex-start;
      display: flex;

      > label {
        flex: 0 0 auto;
        margin-right: 0.5rem;
        user-select: none;
      }

      > div {
        flex: 1 1 auto;
      }
    }

    input[type="checkbox"] {
      cursor: pointer;
    }

    ul[data-type="taskList"] {
      margin: 0;
    }
  }

  ul,
  ol {
    padding: 0 1rem;
    margin: 1.25rem 1rem 1.25rem 0.4rem;

    li p {
      margin-top: 0.25em;
      margin-bottom: 0.25em;
    }
  }

  ul {
    list-style-type: disc;
  }

  ol {
    list-style-type: decimal;
  }

  /* Heading styles */
  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    line-height: 1.1;
    margin-top: 2.5rem;
    text-wrap: pretty;
  }

  h1,
  h2 {
    margin-top: 3.5rem;
    margin-bottom: 1.5rem;
  }

  h1 {
    font-size: 1.4rem;
  }

  h2 {
    font-size: 1.2rem;
  }

  h3 {
    font-size: 1.1rem;
  }

  h4,
  h5,
  h6 {
    font-size: 1rem;
  }

  /* Details */
  .details {
    display: flex;
    gap: 0.25rem;
    margin: 1.5rem 0;
    border: 1px solid;
    @apply border border-gray-600;
    border-radius: 0.5rem;
    padding: 0.5rem;

    summary {
      font-weight: 700;
    }

    > button {
      align-items: center;
      background: transparent;
      border-radius: 4px;
      display: flex;
      font-size: 0.625rem;
      height: 1.25rem;
      justify-content: center;
      line-height: 1;
      margin-top: 0.1rem;
      padding: 0;
      width: 1.25rem;

      &:hover {
        background-color: var(--gray-3);
        @apply bg-slate-600 rounded;
      }

      &::before {
        content: "\25B6";
      }
    }

    &.is-open > button::before {
      transform: rotate(90deg);
    }

    > div {
      display: flex;
      flex-direction: column;
      gap: 1rem;
      width: 100%;

      > [data-type="detailsContent"] > :last-child {
        margin-bottom: 0.5rem;
      }
    }

    .details {
      margin: 0.5rem 0;
    }
  }
  /* Code and preformatted text styles */
  code {
    background-color: #c8a2c8;
    border-radius: 0.4rem;
    // color: #C8A2C8;
    font-size: 0.85rem;
    padding: 0.25em 0.3em;
  }
  pre {
    @apply bg-gray-800 text-gray-200 dark:bg-slate-800 dark:text-gray-200;
    border-radius: 0.5rem;
    font-family: "JetBrainsMono", monospace;
    margin: 1.5rem 0;
    padding: 0.75rem 1rem;

    code {
      background: none;
      color: inherit;
      font-size: 0.8rem;
      padding: 0;
    }

    /* Code styling */
    .hljs-comment,
    .hljs-quote {
      @apply text-gray-400;
    }

    .hljs-variable,
    .hljs-template-variable,
    .hljs-attribute,
    .hljs-tag,
    .hljs-name,
    .hljs-regexp,
    .hljs-link,
    .hljs-name,
    .hljs-selector-id,
    .hljs-selector-class {
      @apply text-rose-400;
    }

    .hljs-number,
    .hljs-meta,
    .hljs-built_in,
    .hljs-builtin-name,
    .hljs-literal,
    .hljs-type,
    .hljs-params {
      @apply text-orange-300;
    }

    .hljs-string,
    .hljs-symbol,
    .hljs-bullet {
      @apply text-lime-200;
    }

    .hljs-title,
    .hljs-section {
      @apply text-yellow-200;
    }

    .hljs-keyword,
    .hljs-selector-tag {
      @apply text-sky-300;
    }

    .hljs-emphasis {
      font-style: italic;
    }

    .hljs-strong {
      font-weight: 700;
    }
  }

  mark {
    background-color: #faf594;
    border-radius: 0.4rem;
    box-decoration-break: clone;
    padding: 0.1rem 0.3rem;
  }

  blockquote {
    border-left: 3px solid;
    @apply border-l-4 border-l-gray-600;
    margin: 1.5rem 0;
    padding-left: 1rem;
  }

  // hr {
  //   border: none;
  //   border-top: 1px solid var(--gray-2);
  //   margin: 2rem 0;
  // }
  hr {
    border: none;
    border-top: solid;
    @apply border-t border-t-gray-600;
    cursor: pointer;
    margin: 2rem 0;

    &.ProseMirror-selectednode {
      border-top: solid;
      @apply border-t  border-t-purple-600;
    }
  }

  img {
    display: block;
    height: auto;
    margin: 2.5rem 0;
    max-width: 40%;
    border-radius: 0.25rem;

    &.ProseMirror-selectednode {
      outline: 3px solid #6a00f5;
      border-radius: 0.25rem;
      display: inline-block; /* Prevent selection from extending - might break later so watch */
    }
  }

  .is-empty::before {
    // color: var(--gray-4);
    content: attr(data-placeholder);
    float: left;
    height: 0;
    pointer-events: none;

    margin: 0;
    font-size: 1.8rem;
    @apply text-purple-800 dark:text-purple-300;
  }
}
</style>
