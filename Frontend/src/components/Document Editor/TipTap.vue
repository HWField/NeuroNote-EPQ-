<script setup>
import chemistry from './Chemistry/Extension.js'
import Gapcursor from "@tiptap/extension-gapcursor";
import Code from "@tiptap/extension-code";
import Document from "@tiptap/extension-document";
import Mention from "@tiptap/extension-mention";
import 'katex/dist/katex.min.css' //import base katex css
import 'katex/contrib/mhchem'; // Import the further katex chemistry extension
import Mathematics from '@tiptap-pro/extension-mathematics'
import { Hyperlink } from "@docs.plus/extension-hyperlink";
import { HyperMultimediaKit } from "@docs.plus/extension-hypermultimedia";
import previewHyperlinkModal from "@/components/Document Editor/modals/previewHyperlink.ts";
import setHyperlinks from "@/components/Document Editor/modals/setHyperlink.ts";
import "tippy.js/dist/svg-arrow.css";
import FileHandler from "@tiptap-pro/extension-file-handler";
// import suggestion from "@/components/Document Editor/TagSuggestion.js";
import Heading from "@tiptap/extension-heading";
import { eventBus } from "@/components/Document Editor/EventBus.js";
import Loading from "@/components/Loading.vue";
// import TagsList from "@/components/Document Editor/TagsList.vue";
import {
  Upload as UploadIcon,
  ImageIcon,
  Link2 as LinkIcon,
} from "lucide-vue-next";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { debounce } from "lodash";
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
import NoteHeader from "@/components/Document Editor/NoteHeader.vue";
import { Button } from "@/components/ui/Button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu";
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
  Link,
} from "lucide-vue-next";

import { useGraphStore } from "@/stores/useGraphStore";
import { useTabStore } from "@/stores/useTabStore";
import { useUserStore } from "@/stores/useUserStore";
import axios, { getBaseUrl } from "../../axios.js";
import { useToast } from "@/components/ui/toast/use-toast";
import { ref, onBeforeUnmount, watch } from "vue";
import { onMounted } from "vue";
import { set } from "@vueuse/core";
const emit = defineEmits(["note-closed"]);
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
  noteId: Number || 0,
  tabId: Number || 0,
});

const saveInterval = ref(null);

const focusEditor = (event) => {
  if (editor) {
    editor.chain().focus().run();
  }
};

const handleHeaderEnter = () => {
  focusEditor(); // Call focusEditor without an event
};

const noteTitle = ref("Untitled Note");
const noteTags = ref([]);
const { toast } = useToast();
// Add to your imports at the top
import { Camera } from "lucide-vue-next"; // You already have UploadIcon


// Add these refs
const cameraInputRef = ref(null);

// Simple function to trigger the camera
const triggerCamera = () => {
  cameraInputRef.value.click();
};

// Handle the photo capture
const handleCameraCapture = () => {
  if (cameraInputRef.value && cameraInputRef.value.files?.length) {
    const file = cameraInputRef.value.files[0];
    uploadImageFile(file)
      .then(() => {
        closeImageModal();
        // Reset input so the same file can be selected again
        cameraInputRef.value.value = "";
      })
      .catch((error) => console.error("Error uploading camera image:", error));
  }
};

const imageUrlInput = ref("");
const showImageModal = ref(false);
const fileInputRef = ref(null);

const isLoading = ref(true);
const uploadImageFile = (file) => {
  const selection = editor.state.selection;
  const pos = selection.$head.pos;

  const formData = new FormData();
  formData.append("file", file);

  // Use your existing endpoint
  return axios
    .post("/upload-file", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
    .then((response) => {
      if (response.data && response.data.url) {
        // Insert the image at the current cursor position
        editor
          .chain()
          .focus()
          .setImage({ src: getBaseUrl() + response.data.url })
          .run();
        return response.data.url; // Return something for chaining
      } else {
        console.error("Invalid response format:", response.data);
        throw new Error("Invalid response format");
      }
    })
    .catch((error) => {
      console.error("Error uploading image:", error);
      throw error; // Re-throw to propagate the error
    });
};

const openImageModal = () => {
  imageUrlInput.value = "";
  showImageModal.value = true;
};

const closeImageModal = () => {
  showImageModal.value = false;
  imageUrlInput.value = "";
};

const handleFileSelected = () => {
  if (fileInputRef.value && fileInputRef.value.files?.length) {
    const file = fileInputRef.value.files[0];
    uploadImageFile(file)
      .then(() => {
        closeImageModal();
      })
      .catch((error) => {
        console.error("Error in file upload:", error);
        // You might want to show an error message to the user here
      });
  }
};

const handleUrlSubmit = () => {
  if (imageUrlInput.value) {
    editor.commands.setImage({ src: imageUrlInput.value });
    closeImageModal();
  }
};

// Update your insertImageUrl method to use the modal
const insertImageUrl = () => {
  openImageModal();
};

// Simplify your ImageUpload extension - just delegate to our utility function
const ImageUpload = Extension.create({
  name: "imageUpload",

  addCommands() {
    return {
      uploadImage:
        ({ file }) =>
        ({ editor }) => {
          uploadImageFile(file);
          return true;
        },
    };
  },
});

function extractTagsFromDocument(document) {
  const uniqueTagIds = new Set();

  // Recursive function to traverse the document
  const traverse = (node) => {
    // Check if this is a mention node
    if (node.type === "mention" && node.attrs && node.attrs.id) {
      uniqueTagIds.add(node.attrs.id);
    }

    // Process content array if it exists
    if (node.content && Array.isArray(node.content)) {
      node.content.forEach((childNode) => traverse(childNode));
    }
  };

  // Start traversal with the document
  if (document && document.content) {
    document.content.forEach((node) => {
      // For tags container, extract all mention IDs
      if (node.type === "tagsContainer" && node.content) {
        node.content.forEach((tagNode) => {
          if (tagNode.type === "mention" && tagNode.attrs && tagNode.attrs.id) {
            uniqueTagIds.add(tagNode.attrs.id);
          }
        });
      }

      // Continue normal traversal
      traverse(node);
    });
  }

  return Array.from(uniqueTagIds);
}

async function SaveToBackend() {
  //  Don't save if still loading
  if (isLoading.value) {
    console.error("Editor is still loading, skipping save.");
    return false;
    
  }
 
  let noteContent = editor.getJSON();
  const title = noteTitle.value || "Untitled Note";
  const tags = noteTags.value;

  const graphStore = useGraphStore();
  graphStore.updateNoteName(props.noteId, title);
  graphStore.replaceNoteTags(props.noteId, tags);

  try {
    await axios.post("/update", {
      operation: "content",
      name: title,
      content: noteContent,
      tags: tags,
      id: props.noteId,
    });
    return true; // Successful save
  } catch (error) {
    console.error("Error saving note:", error);
    return false; // Failed save
  }
}

async function LoadFromBackend() {
  try {
    isLoading.value = true;
    const response = await axios.post("/load", {
      id: props.noteId,
      operation: "content",
    });

    // Set the title in our ref
    noteTitle.value = response.data.name || "Untitled Note";

    // Extract tags if they exist in the response
    if (response.data.tags) {
      noteTags.value = response.data.tags;
    } else {
      // If no tags in response, extract them from content
      noteTags.value = extractTagsFromDocument(response.data.content);
    }

    // Set content
    if (response.data.content) {
      editor.commands.setContent(response.data.content);
    }
    isLoading.value = false;
    return true; // Successfully loaded
  } catch (error) {
    // Display error toast
    toast({
      title: "Note not found",
      description: "The requested note could not be loaded.",
      variant: "destructive",
    });

    // Close the note view
    emit("note-closed");

    console.error("Error loading note:", error);
    isLoading.value = false;
    return false; // Failed to load
  } 
}

// Update title from the header component
function updateNoteTitle(newTitle) {
  noteTitle.value = newTitle;
  useTabStore().RenameTab(props.tabId, newTitle); //update tab live
}

// Update tags from the header component
function updateNoteTags(newTags) {
  noteTags.value = newTags;
}

async function closeNote() {
  if (isLoading.value) {
    return;
  }
  
  try {
    // Try to save before closing
    const saveResult = await SaveToBackend();
    
    if (saveResult) {
      // Only close if save was successful
      console.error("Note saved successfully before closing");
      isLoading.value = false;
      emit("note-closed");
    } else {
      // If save failed, show error and don't close
      toast({
        title: "Save error",
        description: "Unable to save your note. Please try again.",
        variant: "destructive",
      });
      isLoading.value = false;
    
    }
  } catch (error) {
    console.error("Error saving note before close:", error);
    toast({
      title: "Save error",
      description: "Failed to save your note. Please try again.",
      variant: "destructive",
    });
  
  }
}
const handleEscapeKey = (event) => {
  if (event.key === "Escape") {
    closeNote();
  }
};
onMounted(async () => {
  // Wait for content to load before proceeding
  const loaded = await LoadFromBackend();

  // Only proceed with the rest if loading was successful
  if (loaded) {
    useUserStore().addToRecentNotes(props.noteId);
    editor.chain().focus().run();

    // Add event listener for tag updates
    eventBus.on("open-image-modal", openImageModal);

    window.addEventListener("keydown", handleEscapeKey);

    // Full save every minute
    saveInterval.value = setInterval(async () => {
      await SaveToBackend();
    }, 60000);
    isLoading.value = false;
    // console.error("Editor loaded successfully", isLoading.value);
  }
});

onBeforeUnmount(async () => {
  // Wait for save to complete before destroying editor
  window.removeEventListener("keydown", handleEscapeKey);
  if (saveInterval.value) {
    clearInterval(saveInterval.value);
    saveInterval.value = null;
    console.error("Save interval cleared");
  }

  // Only save if loading is complete
  if (!isLoading.value) {
    try {
      await SaveToBackend();
    } catch (error) {
      console.error("Failed to save note before unmount:", error);
    }
  }
  
  // Clean up event listeners
  eventBus.off("open-image-modal", openImageModal);
  if (editor) {
    editor.destroy();
  }
});

const CustomDocument = Document.extend({
  content: "block+",
});

let editor = new Editor({
  //save every 5seconds to backend on modification
  onUpdate: debounce(async () => {
    // Skip saving during loading state
    if (!isLoading.value) {
      await SaveToBackend();
    }
  }, 1000),
  extensions: [
    Document,
    chemistry,
    Mathematics.configure({
      // Add proper configuration
      render: true,
      katex: {
        displayMode: false,
        throwOnError: false,
        output: 'html',
      },
      HTMLAttributes: {
        class: 'math-node',
      },
    }),
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
    // HyperMultimediaKit.configure({
    //   Image,
    //   Youtube,
    //   Vimeo: {
    //     modal: vimeoModal, // default modal
    //     inline: true, // default false
    //   },
    //   SoundCloud: false,
    //   Twitter: false,
    // }),
    Hyperlink.configure({
      openOnClick: true,
      modals: {
        previewHyperlink: (data) => {
          return previewHyperlinkModal(data);
        },
        setHyperlink: (data) => {
          return setHyperlinks(data);
        },
      },
      HTMLAttributes: {
        class: "link",
      },
    }),
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
    Image.configure({
      HTMLAttributes: {
        class: "editor-image",
      },
    }),
    FileHandler.configure({
      allowedMimeTypes: ["image/jpeg", "image/png", "image/gif", "image/webp"],

      onDrop: (currentEditor, files) => {
        files.forEach((file) => {
          uploadImageFile(file);
        });
        return true;
      },

      onPaste: (currentEditor, files) => {
        if (files.length) {
          files.forEach((file) => {
            uploadImageFile(file);
          });
          return true;
        }
        return false;
      },
    }),
    ImageUpload,
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
  content: "<p></p>",
});
</script>

<template>
  <div class="flex w-full h-full flex-col">
    <!-- Floating Toolbar -->
    <Loading v-if="isLoading" />
    <div v-else>
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
                      @click="closeNote();"
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
                      @click="
                        editor.chain().focus().setTextAlign('center').run()
                      "
                      :class="{
                        'bg-primary/20': editor.isActive({
                          textAlign: 'center',
                        }),
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
                      @click="
                        editor.chain().focus().setTextAlign('right').run()
                      "
                      :class="{
                        'bg-primary/20': editor.isActive({
                          textAlign: 'right',
                        }),
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
          <NoteHeader
            :initial-title="noteTitle"
            :initial-tags="noteTags"
            @update:title="updateNoteTitle"
            @update:tags="updateNoteTags"
            @enter-pressed="handleHeaderEnter"
            class="px-4 pt-4"
          />
          <editor-content class="p-4" :editor="editor" />
        </ScrollArea>
      </div>
    </div>
  </div>

  <!-- Image Modal -->
  <!-- Image Modal -->
  <Dialog :open="showImageModal" @update:open="closeImageModal">
    <DialogContent class="sm:max-w-[425px]">
      <DialogHeader>
        <DialogTitle>Insert Image</DialogTitle>
      </DialogHeader>
      <div class="grid gap-4 py-4">
        <!-- File Upload Section -->
        <div class="grid grid-cols-4 items-center gap-4">
          <label class="col-span-4 font-medium">Upload Image</label>
          <div class="col-span-4">
            <input
              ref="fileInputRef"
              type="file"
              accept="image/*"
              class="block w-full text-sm file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary hover:file:bg-primary-100"
            />
            <Button
              class="mt-2 w-full bg-green-600 hover:bg-green-700 text-white"
              @click="handleFileSelected"
            >
              <UploadIcon class="h-4 w-4 mr-2" />Upload
            </Button>
          </div>
        </div>

        <!-- Simple Camera Button -->
        <div class="grid grid-cols-4 items-center gap-4">
          <label class="col-span-4 font-medium">Take a Photo</label>
          <div class="col-span-4">
            <input
              ref="cameraInputRef"
              type="file"
              accept="image/*"
              capture="user"
              class="hidden"
              @change="handleCameraCapture"
            />
            <Button
              class="w-full bg-blue-600 hover:bg-blue-700 text-white"
              @click="triggerCamera"
            >
              <Camera class="h-4 w-4 mr-2" />Take Photo
            </Button>
          </div>
        </div>

        <!-- Image URL Section -->
        <div class="flex flex-col gap-2 mt-4">
          <label class="font-medium">Or insert image URL</label>
          <input
            v-model="imageUrlInput"
            type="text"
            placeholder="https://example.com/image.jpg"
            class="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
          />
          <Button class="mt-2" @click="handleUrlSubmit"
            >Insert Image URL</Button
          >
        </div>
      </div>
    </DialogContent>
  </Dialog>
</template>

<style lang="scss">
.hypermultimedia {
  iframe,
  audio,
  video {
    background-color: #cfcfcf;
  }

  &__resize-gripper {
    position: absolute;
    margin: 0;
    display: none;
    z-index: 1;

    .media-resize-clamp {
      width: 10px;
      height: 10px;
      background-color: #1a73e8;
      border: 1px solid #fff;
      display: none;
      z-index: 4;

      &--rotate {
        border-radius: 50%;
        position: absolute;
        top: -28px;
        left: 50%;
        transform: translateX(-50%);
        cursor: crosshair;

        &::after {
          content: "";
          position: absolute;
          left: 50%;
          transform: translateX(-50%);
          width: 1.5px;
          height: 30px;
          background-color: #1a73e8;
        }
      }

      &--left {
        position: absolute;
        top: 50%;
        left: -5px;
        transform: translateY(-50%);
        cursor: ew-resize;
        z-index: 2;
      }

      &--right {
        position: absolute;
        top: 50%;
        right: -5px;
        transform: translateY(-50%);
        cursor: ew-resize;
        z-index: 2;
      }

      &--top {
        position: absolute;
        top: -5px;
        left: 50%;
        transform: translateX(-50%);
        cursor: ns-resize;
        z-index: 2;
      }

      &--bottom {
        position: absolute;
        bottom: -5px;
        left: 50%;
        transform: translateX(-50%);
        cursor: ns-resize;
        z-index: 2;
      }

      &--top-left {
        position: absolute;
        top: -5px;
        left: -5px;
        cursor: nwse-resize;
      }

      &--top-right {
        position: absolute;
        top: -5px;
        right: -5px;
        cursor: nesw-resize;
      }

      &--bottom-left {
        position: absolute;
        bottom: -5px;
        left: -5px;
        cursor: nesw-resize;
      }

      &--bottom-right {
        position: absolute;
        bottom: -5px;
        right: -5px;
        cursor: nwse-resize;
      }
    }

    &--active {
      border: 1.5px solid #1a73e8;
      display: block;
      .media-resize-clamp {
        display: block;
      }
    }
  }

  &__modal {
    padding: 8px 8px;
    background-color: #fff;
    border-radius: 6px;
    display: flex;
    align-items: center;
    box-shadow:
      0 4px 6px -1px rgba(0, 0, 0, 0.1),
      0 2px 4px -1px rgba(0, 0, 0, 0.06);
    border: 1px solid rgba(0, 0, 0, 0.1);
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;

    &__divider {
      border-left: 2px solid #e5e7eb;
      height: 5px;
      margin: 6px 10px;
    }

    select {
      @apply border-gray-300 py-2 px-2 rounded-md;
      &:hover {
        background-color: #eee;
      }
    }

    button {
      border-color: #d1d5db;
      padding: 8px;
      border-radius: 0.375rem;
      &:hover {
        background-color: #eee;
      }
    }

    &__btn--resize {
      svg {
      }
    }

    &--active {
      background-color: #1a73e8;
      fill: #fff;
      &:hover {
        svg {
          fill: black;
        }
      }
      svg {
        fill: #fff;
      }
    }
  }
}

.editor-image {
  display: block;
  max-width: 100%;
  height: auto;
  margin: 1rem 0;
  border-radius: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s ease;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  &.ProseMirror-selectednode {
    outline: 3px solid #6a00f5;
  }
}

/* Style for uploading state */
.uploading-image {
  position: relative;
  display: inline-block;
  background-color: #f0f0f0;
  border-radius: 0.5rem;
  margin: 1rem 0;
  min-height: 100px;
  min-width: 200px;

  &::after {
    content: "Uploading...";
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 0.9rem;
    color: #666;
  }
}

math-inline {
  font-family: "KaTeX_Main", serif;
  min-width: 1em;
  min-height: 1em;
  font-size: 1em;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  // @apply bg-purple-600;
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
// .katex-html {
//   display: none;
// }
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
  .math-node {
  min-width: 1em;
  min-height: 1em;
  font-family: KaTeX_Main, 'Times New Roman', serif;
  cursor: pointer;
  display: inline-block;
}

/* Override any display:none that might be hiding the rendered output */
.katex, 
.katex-html, 
.katex-mathml {
  display: block !important;
}

.Tiptap-mathematics-editor {
  background: #202020;
  color: #fff;
  font-family: monospace;
  padding: 0.2rem 0.5rem;
  border-radius: 0.25rem;
}

.Tiptap-mathematics-render {
  display: inline-block !important;
  cursor: pointer;
  border-radius: 0.25rem;
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
  div[data-youtube-video] {
    cursor: move;
    // // padding-right: 1.5rem;
    height: auto;
    overflow: hidden;
    margin: 2.5rem 0;
    // max-width: 40%;
    border-radius: 0.25rem;

    iframe {
      // border: 0.5rem solid var(--black-contrast);
      display: block;
      // min-height: 200px;
      // min-width: 200px;
      outline: 0px solid transparent;
    }

    &.ProseMirror-selectednode {
      outline: 3px solid #6a00f5;
      border-radius: 0.25rem;
      display: inline-block; /* Prevent selection from extending - might break later so watch */
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

.tippy-svg-arrow {
  svg {
    bottom: 6px;
    background: #fff;
    fill: #aaa;
  }
}

.hyperlinkLinkModal {
  // background-color: #fff;
  border-radius: 10px;
  border: 1px solid;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 6px;
  box-shadow: 0 1px 3px 1px rgba(60, 64, 67, 0.15);
  @apply bg-secondary rounded-md px-4 border-secondary;

  .metadata {
    width: 200px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    flex-direction: row-reverse;
    a {
      font-size: 0.9rem;
      margin-right: 6px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    img {
      width: 18px;
      height: 18px;
      border-radius: 50%;
      margin-right: 8px;
    }
  }

  .copy {
    margin-left: auto;
  }

  form {
    display: flex;
    align-items: flex-end;
    width: 100%;
    input {
      border: 1px solid;
      border-radius: 6px;
      padding: 0.4rem 0.8rem;
      margin-bottom: 0.2rem;
      width: 100%;
      @apply border border-gray-600 bg-slate-100 dark:bg-slate-700;
      &:last-of-type {
        margin-bottom: 0;
      }
    }
    .buttonsWrapper {
      margin-left: 8px;
      button {
        border-radius: 6px;
        padding: 4px 14px;
        width: 70px;
        margin-bottom: 0.2rem;
        // color: #1a73e8;
        @apply bg-primary-foreground;
        &:hover {
          background: rgba(26, 115, 232, 0.04);
          // color: #174ea6;
        }
      }
    }
  }

  button {
    width: 30px;
    height: 30px;
    border-radius: 50%;
    margin: 0 0.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background-color 0.1s ease-in-out;
    &:hover {
      background-color: #eee;
    }

    > svg {
      width: 16px;
      height: 16px;
    }
  }
}
.link {
  @apply text-blue-700 dark:text-blue-400;
  cursor: pointer;
}
.link:hover {
  cursor: pointer;
  @apply text-blue-500 dark:text-blue-200;
}

.ProseMirror .mention {
  cursor: pointer;
}
</style>
