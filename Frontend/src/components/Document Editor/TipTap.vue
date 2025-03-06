<script setup>
import Gapcursor from "@tiptap/extension-gapcursor";
import Code from "@tiptap/extension-code";
import Document from "@tiptap/extension-document";
import Mention from "@tiptap/extension-mention";
import { Commands } from "@/components/Document Editor/commands.js";
import suggestion from "@/components/Document Editor/TagSuggestion.js";
import Heading from "@tiptap/extension-heading";
import TagsList from "@/components/Document Editor/TagsList.vue";
import CommandsList from "@/components/Document Editor/CommandsList.vue";
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
import { all, createLowlight } from "lowlight";
import { Editor, EditorContent } from "@tiptap/vue-3";
import StarterKit from "@tiptap/starter-kit";
import { ColorHighlighter } from "@/components/Document Editor/ColorHighlighter.ts";
import { SmilieReplacer } from "@/components/Document Editor/SymbolReplacer.ts";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Extension } from "@tiptap/core";
import { Node } from "@tiptap/core";
import { Button } from "@/components/ui/Button";

// Add after your other imports, near the top of the file
import { 
  Heading1, Heading2, Heading3, Bold, Italic, Underline as UnderlineIcon, 
  Strikethrough, List, ListOrdered, Quote, 
  Youtube as YoutubeIcon, Image as ImageIcon, CheckSquare, 
  Code as CodeIcon, AlignLeft, AlignCenter, AlignRight, 
  AlignJustify, FoldVertical 
} from "lucide-vue-next";

import axios from "../../axios.js";

import { ref, onBeforeUnmount } from "vue";
import { onMounted } from "vue";

import "katex/dist/katex.min.css";
import "@benrbray/prosemirror-math/dist/prosemirror-math.css";

import {
  makeInlineMathInputRule,
  makeBlockMathInputRule,
  REGEX_INLINE_MATH_DOLLARS,
  REGEX_BLOCK_MATH_DOLLARS,
} from "@benrbray/prosemirror-math";
import {
  mathPlugin,
  mathBackspaceCmd,
  mathSerializer,
} from "@benrbray/prosemirror-math";
import { keymap } from "@tiptap/pm/keymap";
import { inputRules } from "@tiptap/pm/inputrules";

const mathKeymap = keymap({
  Backspace: mathBackspaceCmd,
});

const MathInline = Node.create({
  name: "math_inline",
  group: "inline math",
  content: "text*",
  inline: true,
  atom: true,
  parseHTML() {
    return [{ tag: "math-inline" }];
  },
  renderHTML() {
    return ["math-inline", { class: "math-node" }, 0];
  },
});

const MathDisplay = Node.create({
  name: "math_display",
  group: "block math",
  content: "text*",
  atom: true,
  code: true,
  parseHTML() {
    return [{ tag: "math-display" }];
  },
  renderHTML() {
    return ["math-display", { class: "math-node" }, 0];
  },
});
console.error("MathInline type:", MathInline.type);
console.error("MathDisplay type:", MathDisplay.type);
const mathInputRules = inputRules({
  rules: [
    // Call the functions with regex patterns and node types
    makeInlineMathInputRule(REGEX_INLINE_MATH_DOLLARS, MathInline.type),
    makeBlockMathInputRule(REGEX_BLOCK_MATH_DOLLARS, MathDisplay.type),
  ],
});

const Math = Extension.create({
  name: "math",

  addProseMirrorPlugins() {
    return [
      mathInputRules,
      mathKeymap,
      mathPlugin, // Use directly as a plugin instance, don't call it as a function
    ];
  },
});

// create a lowlight instance
const lowlight = createLowlight(all);

// you can also register languages
lowlight.register("html", html);
lowlight.register("css", css);
lowlight.register("js", js);
lowlight.register("ts", ts);
lowlight.register("py", py);
lowlight.register("csharp", csharp);

const focusEditor = (event) => {
  if (editor) {
    editor.chain().focus().run();
  }
};

function SaveToBackend() {
  let noteContent = editor.getJSON();
  axios
    .post("/update", {
      operation: "content",
      name: "note 1(updateasjson)",
      content: noteContent,
      id: "31",
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

function LoadFromBackend() {
  axios
    .post("/load", {
      id: "31",
      operation: "content",
    })
    .then((response) => {
      console.log("Type of content:", typeof response.data.content);
      editor.commands.setContent(response.data.content);
    })
    .catch((error) => {
      console.error("Error fetching data on load:", error);
    });
}

onMounted(() => {
  LoadFromBackend();
  editor.chain().focus().run();
});

onBeforeUnmount(() => {
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

// const NoteTitle = Node.create({
//   name: 'noteTitle',
//   group: 'block',
//   content: 'heading',
//   marks: '',

//   parseHTML() {
//     return [
//       {
//         tag: 'div.note-title-container'
//       },
//     ]
//   },

//   renderHTML({ HTMLAttributes }) {
//     return ['div', { class: 'note-title-container' }, 0]
//   }
// })

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
    MathInline,
    MathDisplay,
    Math,

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
      suggestion,
    }),
    // CustomMentionTwo,
    Commands.configure({
      suggestion: {
        items: ({ query }) => {
          return [
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
            {
              title: "Bold",
              icon: Bold,
              command: ({ editor, range }) => {
                editor.chain().focus().deleteRange(range).setMark("bold").run();
              },
            },
            {
              title: "Italic",
              icon: Italic,
              command: ({ editor, range }) => {
                editor
                  .chain()
                  .focus()
                  .deleteRange(range)
                  .setMark("italic")
                  .run();
              },
            },
            {
              title: "Underline",
              icon: UnderlineIcon,
              command: ({ editor, range }) => {
                editor
                  .chain()
                  .focus()
                  .deleteRange(range)
                  .setMark("underline")
                  .run();
              },
            },
            {
              title: "Strike",
              icon: Strikethrough,
              command: ({ editor, range }) => {
                editor
                  .chain()
                  .focus()
                  .deleteRange(range)
                  .setMark("strike")
                  .run();
              },
            },
            {
              title: "Bullet List",
              icon: List,
              command: ({ editor, range }) => {
                editor
                  .chain()
                  .focus()
                  .deleteRange(range)
                  .toggleBulletList()
                  .run();
              },
            },
            {
              title: "Block Quote",
              icon: Quote,
              command: ({ editor, range }) => {
                editor
                  .chain()
                  .focus()
                  .deleteRange(range)
                  .toggleBlockquote()
                  .run();
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
                  editor
                    .chain()
                    .focus()
                    .deleteRange(range)
                    .setImage({ src: url })
                    .run();
                }
              },
            },
            {
              title: "Task List",
              icon: CheckSquare,
              command: ({ editor, range }) => {
                editor
                  .chain()
                  .focus()
                  .deleteRange(range)
                  .toggleTaskList()
                  .run();
              },
            },
            {
              title: "Ordered List",
              icon: ListOrdered,
              command: ({ editor, range }) => {
                editor
                  .chain()
                  .focus()
                  .deleteRange(range)
                  .toggleOrderedList()
                  .run();
              },
            },
            {
              title: "Code Block",
              icon: CodeIcon,
              command: ({ editor, range }) => {
                editor
                  .chain()
                  .focus()
                  .deleteRange(range)
                  .toggleCodeBlock()
                  .run();
              },
            },
            {
              title: "Details",
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
          ]
            .filter((item) =>
              item.title.toLowerCase().startsWith(query.toLowerCase())
            )
            // .slice(0, 5);
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
    <p></p>
  `,
});
</script>

<template>
  <div class="flex w-full h-full flex-col">
    <div
      class="flex justify-center mx-auto bg-primary-foreground p-3 shadow-lg rounded-lg mt-4 space-x-2 max-w-max"
    >
      <Button
        @click="editor.chain().focus().toggleHeading({ level: 1 }).run()"
        :class="{ 'is-active': editor.isActive('heading', { level: 1 }) }"
      >
        H1
      </Button>
      <Button
        @click="editor.chain().focus().toggleHeading({ level: 2 }).run()"
        :class="{ 'is-active': editor.isActive('heading', { level: 2 }) }"
      >
        H2
      </Button>
      <Button
        @click="editor.chain().focus().toggleHeading({ level: 3 }).run()"
        :class="{ 'is-active': editor.isActive('heading', { level: 3 }) }"
      >
        H3
      </Button>
      <Button
        @click="editor.chain().focus().setParagraph().run()"
        :class="{ 'is-active': editor.isActive('paragraph') }"
      >
        Paragraph
      </Button>
      <Button
        @click="editor.chain().focus().toggleBold().run()"
        :class="{ 'is-active': editor.isActive('bold') }"
      >
        Bold
      </Button>
      <Button
        @click="editor.chain().focus().toggleItalic().run()"
        :class="{ 'is-active': editor.isActive('italic') }"
      >
        Italic
      </Button>
      <Button
        @click="editor.chain().focus().toggleStrike().run()"
        :class="{ 'is-active': editor.isActive('strike') }"
      >
        Strike
      </Button>
      <Button
        @click="editor.chain().focus().toggleHighlight().run()"
        :class="{ 'is-active': editor.isActive('highlight') }"
      >
        Highlight
      </Button>
      <Button
        @click="editor.chain().focus().setTextAlign('left').run()"
        :class="{ 'is-active': editor.isActive({ textAlign: 'left' }) }"
      >
        Left
      </Button>
      <Button
        @click="editor.chain().focus().setTextAlign('center').run()"
        :class="{ 'is-active': editor.isActive({ textAlign: 'center' }) }"
      >
        Center
      </Button>
      <Button
        @click="editor.chain().focus().setTextAlign('right').run()"
        :class="{ 'is-active': editor.isActive({ textAlign: 'right' }) }"
      >
        Right
      </Button>
      <Button
        @click="editor.chain().focus().setTextAlign('justify').run()"
        :class="{ 'is-active': editor.isActive({ textAlign: 'justify' }) }"
      >
        Justify
      </Button>
    </div>

    <div class="flex justify-center">
      <ScrollArea
        class="editor w-full max-w-[2000px] h-[80vh] overflow-y-auto bg-primary-foreground rounded-lg border-4 border-gray-800 m-4"
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
    margin: 0 0 2rem;
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
    // background-color: var(--purple-light);
    border-radius: 0.4rem;
    box-decoration-break: clone;
    // color: var(--purple);
    padding: 0.1rem 0.3rem;
    @apply bg-purple-800  text-purple-200;
  }

  .note-title-container .mention {
    font-size: 0.9rem; // Smaller font size
    padding: 0.05rem 0.2rem; // Smaller padding
    vertical-align: middle; // Better alignment with title text
    @apply bg-purple-700 text-purple-100; // Slightly different color if desired
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
