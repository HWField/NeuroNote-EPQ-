<script setup>
import Code from "@tiptap/extension-code";
import Document from "@tiptap/extension-document";
import Mention from "@tiptap/extension-mention";
import Highlight from "@tiptap/extension-highlight";
import TextAlign from "@tiptap/extension-text-align";
import Paragraph from "@tiptap/extension-paragraph";
import Text from "@tiptap/extension-text";
import Typography from "@tiptap/extension-typography";
import Image from "@tiptap/extension-image";
import { Editor, EditorContent } from "@tiptap/vue-3";
import StarterKit from "@tiptap/starter-kit";
import { ColorHighlighter } from "@/components/Document Editor/ColorHighlighter.ts";
import { SmilieReplacer } from "@/components/Document Editor/SymbolReplacer.ts";
import suggestion from "@/components/Document Editor/suggestion.js";
import { ScrollArea } from "@/components/ui/scroll-area";

import { Button } from "@/components/ui/Button";

import axios from "../../axios.js";


import { ref, onBeforeUnmount } from 'vue';
import { onMounted } from 'vue';


function SaveToBackend() {
  let noteContent = editor.getJSON()
  axios
    .post("/update", {
      operation: "content",
      name: "note 1(updateasjson)",
      content: noteContent,
      id: 1,
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

function LoadFromBackend() {
  axios
    .post("/load", {
      id: '1',
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


let editor = new Editor({
  extensions: [
    Document,
    Paragraph,
    Text,
    Code,
    Typography,
    ColorHighlighter,
    SmilieReplacer,
    StarterKit,
    TextAlign.configure({
      types: ["heading", "paragraph"],
    }),
    Highlight,
    Mention.configure({
      HTMLAttributes: {
        class: "mention",
      },
      suggestion,
    }),
    Image,
  ],
  editorProps: {
    attributes: {
      class: "",
    },
  },
  content: `
        <p>
          → With the Typography extension, Tiptap understands »what you mean« and adds correct characters to your text — it’s like a “typography nerd” on your side.
        </p>
        <p>
          Try it out and type <code>(c)</code>, <code>-></code>, <code>>></code>, <code>1/2</code>, <code>!=</code>, <code>--</code> or <code>1x1</code> here:
        </p>
        <p></p>
        <p>
          Or add completely custom input rules. We added a custom extension here that replaces smilies like <code>:-)</code>, <code><3</code> or <code>>:P</code> with emojis. Try it out:
        </p>
        <p></p>
        <p>
          You can also teach the editor new things. For example to recognize hex colors and add a color swatch on the fly: #FFF, #0D0D0D, #616161, #A975FF, #FB5151, #FD9170, #FFCB6B, #68CEF8, #80cbc4, #9DEF8F
        </p>

        
        <h3 style="text-align:center">
          Devs Just Want to Have Fun by Cyndi Lauper
        </h3>
        <img src="https://placehold.co/600x400" />
        <p style="text-align:center">
          I come home in the morning light<br>
          My mother says, <mark>“When you gonna live your life right?”</mark><br>
          Oh mother dear we’re not the fortunate ones<br>
          And devs, they wanna have fun<br>
          Oh devs just want to have fun</p>
        <p style="text-align:center">
          The phone rings in the middle of the night<br>
          My father yells, "What you gonna do with your life?"<br>
          Oh daddy dear, you know you’re still number one<br>
          But <s>girls</s>devs, they wanna have fun<br>
          Oh devs just want to have
        </p>
        <p style="text-align:center">
          That’s all they really want<br>
          Some fun<br>
          When the working day is done<br>
          Oh devs, they wanna have fun<br>
          Oh devs just wanna have fun<br>
          (devs, they wanna, wanna have fun, devs wanna have)
        </p>
      
      `,
});



</script>

<template>

   <div class="flex w-full h-full flex-col"> 
    <div class="flex justify-center mx-auto bg-primary-foreground p-3 shadow-lg rounded-lg mt-4 space-x-2 max-w-max">
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

    <div class="flex justify-center ">
      <ScrollArea class="editor w-full max-w-[2000px] h-[80vh] overflow-y-auto  bg-primary-foreground rounded-lg border-4 border-gray-800 m-4">
        <editor-content class="p-4" :editor="editor" />
      </ScrollArea>
      </div>
   
    </div>
  
  
</template>

<style lang="scss">
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
.tiptap {
  caret-color: #6a00f5;


  &:focus {
    outline: none;
  }
  // :first-child {
  //   margin-top: 0;
  // }

  /* Code and preformatted text styles */
  code {
    background-color: var(--purple-light);
    border-radius: 0.4rem;
    color: var(--black);
    font-size: 0.85rem;
    padding: 0.25em 0.3em;
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

  .mention {
    background-color: var(--purple-light);
    border-radius: 0.4rem;
    box-decoration-break: clone;
    color: var(--purple);
    padding: 0.1rem 0.3rem;
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

  /* Code and preformatted text styles */
  code {
    background-color: var(--purple-light);
    border-radius: 0.4rem;
    color: var(--black);
    font-size: 0.85rem;
    padding: 0.25em 0.3em;
  }

  pre {
    background: var(--black);
    border-radius: 0.5rem;
    color: var(--white);
    font-family: "JetBrainsMono", monospace;
    margin: 1.5rem 0;
    padding: 0.75rem 1rem;

    code {
      background: none;
      color: inherit;
      font-size: 0.8rem;
      padding: 0;
    }
  }

  mark {
    background-color: #faf594;
    border-radius: 0.4rem;
    box-decoration-break: clone;
    padding: 0.1rem 0.3rem;
  }

  blockquote {
    border-left: 3px solid var(--gray-3);
    margin: 1.5rem 0;
    padding-left: 1rem;
  }

  hr {
    border: none;
    border-top: 1px solid var(--gray-2);
    margin: 2rem 0;
  }
}
</style>
