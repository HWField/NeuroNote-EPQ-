<template>
  <div class="flex w-full h-full flex-col">
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

    <!-- Version History Modal -->
    <Dialog
      :open="showVersionHistoryModal"
      @update:open="closeVersionHistoryModal"
    >
      <DialogContent class="sm:max-w-[800px]">
        <DialogHeader>
          <DialogTitle>
            <div class="flex items-center">
              <History class="h-5 w-5 mr-2" />
              Version History
            </div>
          </DialogTitle>
        </DialogHeader>
        <div class="mb-4 mt-2">
          <Button variant="default" class="w-full" @click="createManualVersion">
            <Clock class="h-4 w-4 mr-2" />
            Create New Restore Point
          </Button>
        </div>
        <div class="py-4 flex flex-col sm:flex-row gap-4 h-[500px]">
          <!-- Versions List on the left -->
          <div class="w-full sm:w-1/3 border-r pr-4">
            <h3 class="font-medium mb-2">Versions</h3>

            <div v-if="loadingVersions" class="flex justify-center py-8">
              <div
                class="animate-spin h-8 w-8 border-4 border-primary/20 border-t-primary rounded-full"
              ></div>
            </div>

            <div
              v-else-if="versionHistory.length === 0"
              class="text-center py-8 text-muted-foreground"
            >
              No version history available
            </div>

            <div v-else class="flex overflow- max-h-[420px] pr-2">
              <ScrollArea class="flex-1 min-h-0 overflow-y-auto pr-2">
                <div
                  v-for="(version, index) in versionHistory"
                  :key="index"
                  @click="selectedVersion = version"
                  class="p-3 border rounded-md hover:bg-muted/50 mb-2 transition-colors cursor-pointer"
                  :class="{
                    'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800':
                      selectedVersion === version,
                  }"
                >
                  <div class="font-medium">
                    {{ version.version_name || `Version ${index + 1}` }}

                    <!-- Badge for manual versions -->
                    <span
                      v-if="version.version_type === 'manual'"
                      class="ml-2 px-2 py-0.5 text-xs rounded-full bg-blue-100 text-blue-800 dark:bg-blue-900/40 dark:text-blue-300"
                    >
                      Manual
                    </span>

                    <!-- Badge for auto versions -->
                    <span
                      v-else-if="version.version_type === 'auto'"
                      class="ml-2 px-2 py-0.5 text-xs rounded-full bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-300"
                    >
                      Auto
                    </span>

                    <!-- Badge for restored versions -->
                    <span
                      v-else-if="version.version_type === 'restored'"
                      class="ml-2 px-2 py-0.5 text-xs rounded-full bg-purple-100 text-purple-800 dark:bg-purple-900/40 dark:text-purple-300"
                    >
                      Restored
                    </span>
                  </div>
                  <div class="text-sm text-muted-foreground mt-1">
                    {{ version.friendly_time || " " }}
                  </div>
                </div>
              </ScrollArea>
            </div>
          </div>

          <!-- Content Display on the right -->
          <div class="w-full sm:w-2/3">
            <div class="flex justify-between items-center mb-2">
              <h3 class="font-medium">Content</h3>
              <Button
                v-if="selectedVersion"
                variant="default"
                size="sm"
                @click="restoreVersion(selectedVersion)"
              >
                <RotateCcw class="h-3 w-3 mr-1" />
                Restore This Version
              </Button>
            </div>

            <div
              v-if="!selectedVersion"
              class="flex items-center justify-center h-[420px] text-muted-foreground border rounded-md p-4"
            >
              Select a version to view its content
            </div>

            <div v-else class="border rounded-md p-2 h-[420px]">
              <ScrollArea class="h-full w-full" orientation="both">
                <pre
                  class="text-xs font-mono p-2 whitespace-pre-wrap break-all"
                  >{{ selectedVersion.content || "No content available" }}</pre
                >
              </ScrollArea>
            </div>
          </div>
        </div>

        <DialogFooter>
          <Button variant="outline" @click="closeVersionHistoryModal"
            >Close</Button
          >
        </DialogFooter>
      </DialogContent>
    </Dialog>

    <!-- Floating Toolbar -->
    <Loading v-if="isLoading" />

    <div v-else>
      <div v-if="!viewOnly" class="h-24 w-full mb-0 relative">
        <div   class="absolute top-6 w-full z-50 px-4 flex justify-center">
          <div
          data-tour="whiteboardToolbar" class="bg-primary-foreground shadow-lg rounded-lg p-3 max-w-[90%] mx-auto"
          >
            <div  class="flex items-center gap-1 flex-wrap">
              <!-- Close button -->
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant="ghost"
                      size="icon"
                      @click="closeNote()"
                      class="mr-2 bg-red-100 dark:bg-red-900/20 hover:bg-red-200 dark:hover:bg-red-800/30"
                    >
                      <X class="h-4 w-4 text-red-500 dark:text-red-400" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>Close Whiteboard</TooltipContent>
                </Tooltip>
              </TooltipProvider>

              <Separator orientation="vertical" class="h-6 mx-1" />

              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      :variant="showNoteHeader ? 'default' : 'ghost'"
                      size="icon"
                      @click="showNoteHeader = !showNoteHeader"
                    >
                      <Info class="h-4 w-4" />
                      <span class="sr-only">Toggle Note Header</span>
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent
                    >{{ showNoteHeader ? "Hide" : "Show" }} Note
                    Details</TooltipContent
                  >
                </Tooltip>
              </TooltipProvider>

              <Separator orientation="vertical" class="h-6 mx-1" />
              <div
                class="inline-flex rounded-md shadow-sm border overflow-hidden"
              >
                <!-- Auto Button -->
                <Button
                  :variant="mode === 'auto' ? 'default' : 'ghost'"
                  size="sm"
                  class="rounded-none border-r px-3"
                  @click="mode = mode === 'auto' ? 'type' : 'auto'"
                >
                  <Bot class="h-4 w-4 mr-1" />
                  Auto
                </Button>

                <!-- Manual Draw Button -->
                <Button
                  :variant="mode === 'draw' ? 'default' : 'ghost'"
                  :class="{ 'opacity-50 ': mode === 'auto' }"
                  size="sm"
                  class="rounded-none px-3"
                  @click="mode = mode === 'draw' ? 'type' : 'draw'"
                >
                  <Pencil class="h-4 w-4 mr-1" />
                  Draw
                </Button>
              </div>

              <Separator orientation="vertical" class="h-6 mx-1" />

              <!-- Add Shape -->
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="ghost"
                    size="sm"
                    class="flex gap-1 items-center"
                  >
                    <PlusIcon class="h-4 w-4" />
                    <span>Add</span>
                    <ChevronDownIcon class="h-3 w-3 opacity-50" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuItem @click="addShape('rectangle')">
                    <Square class="h-4 w-4 mr-2" />
                    <span>Rectangle</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="addShape('circle')">
                    <Circle class="h-4 w-4 mr-2" />
                    <span>Circle</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="addShape('triangle')">
                    <Triangle class="h-4 w-4 mr-2" />
                    <span>Triangle</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="addShape('line')">
                    <Minus class="h-4 w-4 mr-2" />
                    <span>Line</span>
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem @click="addText()">
                    <Type class="h-4 w-4 mr-2" />
                    <span>Text</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="openImageModal()">
                    <ImagePlus class="h-4 w-4 mr-2" />
                    <span>Image</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>

              <Separator orientation="vertical" class="h-6 mx-1" />

              <Button @click="centerWhiteboard()" variant="ghost" class="">
                <Home class="h-4 w-4" /> Home</Button
              >

              <Separator orientation="vertical" class="h-6 mx-1" />

              <!-- Pen Color -->
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="ghost"
                    size="sm"
                    class="flex gap-1 items-center"
                  >
                    <Palette class="h-4 w-4" :color="colour" />
                    <span>Colour</span>
                    <ChevronDownIcon class="h-3 w-3 opacity-50" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuItem @click="colour = 'black'">
                    <Circle class="h-4 w-4 mr-2" fill="black" />
                    <span>Black</span>
                    <Check v-if="colour === 'black'" class="h-4 w-4 ml-auto" />
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="colour = 'white'">
                    <Circle
                      class="h-4 w-4 mr-2"
                      fill="white"
                      stroke="#e5e5e5"
                    />
                    <span>White</span>
                    <Check v-if="colour === 'white'" class="h-4 w-4 ml-auto" />
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="colour = 'red'">
                    <Circle class="h-4 w-4 mr-2" fill="red" />
                    <span>Red</span>
                    <Check v-if="colour === 'red'" class="h-4 w-4 ml-auto" />
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="colour = 'blue'">
                    <Circle class="h-4 w-4 mr-2" fill="blue" />
                    <span>Blue</span>
                    <Check v-if="colour === 'blue'" class="h-4 w-4 ml-auto" />
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="colour = 'green'">
                    <Circle class="h-4 w-4 mr-2" fill="green" />
                    <span>Green</span>
                    <Check v-if="colour === 'green'" class="h-4 w-4 ml-auto" />
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>

              <Separator orientation="vertical" class="h-6 mx-1" />

              <!-- Pen type -->
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="ghost"
                    size="sm"
                    class="flex gap-1 items-center"
                  >
                    <Pencil class="h-4 w-4" />
                    <span>Width</span>
                    <ChevronDownIcon class="h-3 w-3 opacity-50" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuItem @click="penWidth = 1">
                    <Minus class="h-4 w-4 mr-2" :stroke-width="0.5" />
                    <span>Fine</span>
                    <Check v-if="penWidth == 1" class="h-4 w-4 ml-auto" />
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="penWidth = 3">
                    <Minus class="h-4 w-4 mr-2" :stroke-width="1" />
                    <span>Medium</span>
                    <Check v-if="penWidth == 3" class="h-4 w-4 ml-auto" />
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="penWidth = 8">
                    <Minus class="h-4 w-4 mr-2" :stroke-width="3" />
                    <span>Bold</span>
                    <Check v-if="penWidth == 8" class="h-4 w-4 ml-auto" />
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="penWidth = 16">
                    <Minus class="h-4 w-4 mr-2" :stroke-width="5" />
                    <span>Thick</span>
                    <Check v-if="penWidth == 16" class="h-4 w-4 ml-auto" />
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>

              <Separator orientation="vertical" class="h-6 mx-1" />

              <!-- Background/Grid -->
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="ghost"
                    size="sm"
                    class="flex gap-1 items-center"
                  >
                    <Grid class="h-4 w-4" />
                    <span>Background</span>
                    <ChevronDownIcon class="h-3 w-3 opacity-50" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuItem @click="background = 'line'">
                    <Rows3Icon class="h-4 w-4 mr-2" />
                    <span>Line</span>
                    <Check
                      v-if="background == 'line'"
                      class="h-4 w-4 ml-auto"
                    />
                  </DropdownMenuItem>
                  <Separator />
                  <DropdownMenuItem @click="background = 'sGrid'">
                    <Grid class="h-4 w-4 mr-2" />
                    <span>Small Grid</span>
                    <Check
                      v-if="background == 'sGrid'"
                      class="h-4 w-4 ml-auto"
                    />
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="background = 'mGrid'">
                    <Grid class="h-4 w-4 mr-2" />
                    <span>Medium Grid</span>
                    <Check
                      v-if="background == 'mGrid'"
                      class="h-4 w-4 ml-auto"
                    />
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="background = 'lGrid'">
                    <Grid class="h-4 w-4 mr-2" />
                    <span>Large Grid</span>
                    <Check
                      v-if="background == 'lGrid'"
                      class="h-4 w-4 ml-auto"
                    />
                  </DropdownMenuItem>
                  <Separator />
                  <DropdownMenuItem @click="background = 'empty'">
                    <Square class="h-4 w-4 mr-2" />
                    <span>Blank</span>
                    <Check
                      v-if="background == 'empty'"
                      class="h-4 w-4 ml-auto"
                    />
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>

              <Separator orientation="vertical" class="h-6 mx-1" />

              <!-- Delete Selected -->
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant="ghost"
                      size="icon"
                      class="text-orange-600"
                      @click="deleteSelected"
                    >
                      <Trash2 class="h-4 w-4" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>Delete Selected</TooltipContent>
                </Tooltip>
              </TooltipProvider>

              <Separator orientation="vertical" class="h-6 mx-1" />

              <!-- Version History Button -->
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <Button
                      variant="ghost"
                      size="sm"
                      @click="openVersionHistoryModal"
                      class="flex gap-1 items-center"
                    >
                      <History class="h-4 w-4 mr-1" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>Version History</TooltipContent>
                </Tooltip>
              </TooltipProvider>
            </div>
          </div>
        </div>
      </div>
      <Transition name="slide-down">
        <div
          v-if="showNoteHeader"
          class="relative m-4 z-40 flex justify-center"
        >
          <div
            class="bg-primary-foreground shadow-lg rounded-lg shadow-md p-4 max-w-[2000px] w-full mx-auto"
          >
            <NoteHeader
              :initial-title="noteTitle"
              :initial-tags="noteTags"
              @update:title="updateNoteTitle($event)"
              @update:tags="noteTags = $event"
            />
          </div>
        </div>
      </Transition>

      <div class="flex justify-center h-full flex-1">
        <div
        data-tour="whiteboardCanvas"
          :id="canvasContainerId"
          class="canvas-container w-full overflow-hidden bg-none m-4 relative"
          :class="[
            !embedded
              ? showNoteHeader
                ? 'h-[calc(100vh-24rem)]'
                : 'h-[calc(100vh-12rem)]'
              : 'h-full',
            !embedded ? 'shadow-md' : '',
          ]"
        >
          <!-- Grid canvas (bottom layer) -->
          <canvas
            :id="gridCanvasId"
            class="absolute top-0 left-0 w-full rounded-lg h-full bg-white"
          ></canvas>
          <!-- Main canvas (top layer) -->
          <canvas
            :id="fabricCanvasId"
            class="absolute top-0 left-0 w-full rounded-lg h-full"
          ></canvas>
        </div>
      </div>
    </div>
  </div>
</template>
<style>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
  max-height: 500px;
  opacity: 1;
  transform: translateY(0);
}

.slide-down-enter-from,
.slide-down-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-20px);
}
</style>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, computed } from "vue";
import * as fabric from "fabric";
import Hammer from "hammerjs";
import axios, { getBaseUrl } from "../axios.js";
import { useTabStore } from "@/stores/useTabStore";
import { useGraphStore } from "@/stores/useGraphStore";
import { useUserStore } from "@/stores/useUserStore";
import Loading from "@/components/Loading.vue";
import NoteHeader from "@/components/Document Editor/NoteHeader.vue";
import { Bot, FileText, Home, ImagePlus, Info } from "lucide-vue-next";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { Separator } from "@/components/ui/separator";
import { Button } from "@/components/ui/button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import {
  X,
  Pencil,
  Type,
  Square,
  Triangle,
  PlusIcon,
  Eraser,
  Circle,
  ChevronDown as ChevronDownIcon,
  TextIcon,
  Palette,
  Minus,
  Undo,
  Redo,
  Download,
  Trash2,
  Image,
  Grid,
  LucideFileLineChart,
  Rows3Icon,
  Move,
  Check,
  History,
  RotateCcw,
  Clock,
} from "lucide-vue-next";
import { useToast } from "@/components/ui/toast/use-toast";
import rough from 'roughjs/bundled/rough.esm';
const props = defineProps({
  noteId: Number || 0,
  tabId: Number || 0,
  viewOnly: {
    type: Boolean,
    default: false,
  },
  embedded: {
    type: Boolean,
    default: false,
  },
  instanceKey: {
    type: String,
    default: null,
  },
  initialViewport: {
    type: [String, Array],
    default: null,
  },
});

const instanceId = ref(
  props.instanceKey ||
    `${props.noteId}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
);

const canvasContainerId = computed(() =>
  props.embedded ? `canvas-container-${instanceId.value}` : `canvas-container`
);

const fabricCanvasId = computed(() =>
  props.embedded ? `fabricCanvas-${instanceId.value}` : `fabricCanvas`
);

const gridCanvasId = computed(() =>
  props.embedded ? `grid-canvas-${instanceId.value}` : `grid-canvas`
);

const showNoteHeader = ref(false);
const emit = defineEmits(["note-closed", "viewport-changed"]);
const saveInterval = ref(null);
const noteTitle = ref("Untitled Note");
const noteTags = ref([]);
const { toast } = useToast();
const isLoading = ref(false);
const viewport = ref({ x: 0, y: 0, zoom: 1 });
const background = ref("Lgrid");
const mode = ref("auto");
const colour = ref("red");

if (useUserStore.theme == "dark") {
  colour.value = "white";
} else {
  colour.value = "black";
}
const penWidth = ref(3);

let modalContent = null;
let fabricCanvasEl = null;
let gridCanvas = null;
let gridContext = null;
let canvas = null;
let gridSize = 20;
let vertical = true;
let horizontal = true;

let isPanning = false;
let lastPosX = 0;
let lastPosY = 0;
let width = 0;
let height = 0;

async function SaveToBackend() {
  if (isLoading.value) {
    console.error("Editor is still loading, skipping save.");
    return false;
  }

  try {
    if (!canvas) {
      console.error("Canvas not initialized");
      return false;
    }

    // Get the data directly
    const noteContent = canvas.toJSON();
    const title = noteTitle.value || "Untitled Note";
    const tags = noteTags.value;

    // Update graph store
    const graphStore = useGraphStore();
    graphStore.updateNoteName(props.noteId, title);
    graphStore.replaceNoteTags(props.noteId, tags);

    // Make the request
    await axios.post("/update", {
      operation: "content",
      name: title,
      content: noteContent, // Already serialized by toJSON()
      tags: tags, // Use the local constant
      id: props.noteId,
      viewport: JSON.stringify(canvas.viewportTransform),
      background: background.value,
    });
    console.error("Note saved  successfully:", props.noteId);
    return true;
  } catch (error) {
    console.error("Error saving note:", error);
    return false;
  }
}
async function LoadFromBackend() {
  console.error("Loading note:", props.noteId);
  console.log("Initial viewport prop:", props.initialViewport);
  try {
    const response = await axios.post("/load", {
      id: props.noteId,
      operation: "content",
    });
    console.error("Note loaded successfully:", response.data);
    Loading.value = false;
    // Set the title in our ref
    noteTitle.value = response.data.name || "Untitled Note";
    // Set the viewport

    // Extract tags if they exist in the response
    if (response.data.tags) {
      noteTags.value = response.data.tags;
    }
    if (!canvas || !gridCanvas || !modalContent) {
      console.error("Canvas elements loading not found, retrying in 50ms");
      // Try again after a short delay to allow DOM to render
      setTimeout(LoadFromBackend, 50);
      return;
    }

    // Handle viewport with priority: initialViewport > backend viewport
    let viewportToUse = null;

    //makes remembering preview work

    // makes opening note behaviour work

    if (props.embedded) {
      if (props.initialViewport) {
        // Priority 1: Use initialViewport prop (from preview)
        if (typeof props.initialViewport === "string") {
          viewportToUse = JSON.parse(props.initialViewport);
        } else if (Array.isArray(props.initialViewport)) {
          viewportToUse = props.initialViewport;
        }
      }
    } else {
      if (useTabStore().getTab(useTabStore().activeTab).state.initialViewport) {
        // Priority 1: Use initialViewport prop (from preview)
        if (
          typeof useTabStore().getTab(useTabStore().activeTab).state
            .initialViewport === "string"
        ) {
          console.error("aaaaaaaa is a string");
          viewportToUse = JSON.parse(
            useTabStore().getTab(useTabStore().activeTab).state.initialViewport
          );
        } else if (
          Array.isArray(
            useTabStore().getTab(useTabStore().activeTab).state.initialViewport
          )
        ) {
          console.error("aaaaaaaa is an array");
          viewportToUse = useTabStore().getTab(useTabStore().activeTab).state
            .initialViewport;
        }
        console.error(
          "!!!!!!!!Using custom preview sent viewport:",
          useTabStore().getTab(useTabStore().activeTab).state.initialViewport
        );

        const previewHeight = 265;
        const fullEditorHeight = modalContent.offsetHeight;
        const heightDifference = (fullEditorHeight - previewHeight) / 2;

        // Adjust the Y translation (index 5) to center the content
        // Move the viewport down by half the height difference
        viewportToUse[5] += heightDifference;

        console.error("Adjusted viewport for full editor:", viewportToUse);
        console.error("Height difference compensation:", heightDifference);
      } else if (response.data.viewport) {
        console.error(
          "!!!!!!!!Using loaded viewport:",
          useTabStore().getTab(useTabStore().activeTab).state.initialViewport
        );
        // Priority 2: Use backend viewport (for full editor only)
        viewportToUse = JSON.parse(response.data.viewport);
        console.log("Using backend viewport:", viewportToUse);
      }
    }

    if (viewportToUse) {
      canvas.setViewportTransform(viewportToUse);
    }

    if (response.data.background) {
      background.value = response.data.background;
    }
    drawGrid(
      canvas.viewportTransform[4],
      canvas.viewportTransform[5],
      canvas.getZoom()
    );

    if (response.data.content) {
      return new Promise((resolve) => {
        try {
          canvas.loadFromJSON(response.data.content, function () {
            // Force multiple render calls to ensure everything appears
            setTimeout(() => {
              canvas.renderAll();
              // Apply sharpness settings to all paths after loading
              canvas.getObjects().forEach((obj) => {
                // Check if it's a path or path-like object
                if (obj.type === "path" || obj.type === "line" || obj.path) {
                  obj.objectCaching = false;
                  if (obj.strokeLineCap !== undefined) {
                    obj.strokeLineCap = "round";
                    obj.strokeLineJoin = "round";
                  }
                }
              });

              // Force a second render after a brief delay
              setTimeout(() => {
                canvas.renderAll();

                isLoading.value = false;
                resolve(true);
              }, 50);
            }, 50);
          });
        } catch (err) {
          console.error("Error loading canvas JSON:", err);
          isLoading.value = false;
          resolve(false);
        }
      });
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
function resizeCanvasToContainer() {
  console.error("Resizing canvas to container dimensions");

  // Guard against accessing canvas before it's initialized
  if (!canvas || !gridCanvas || !modalContent) return;

  // Get current dimensions for comparison
  const currentFabricWidth = canvas.getWidth();
  const currentFabricHeight = canvas.getHeight();
  const currentGridWidth = gridCanvas.width;
  const currentGridHeight = gridCanvas.height;

  // Calculate new dimensions based on mode
  let newWidth, newHeight;
  if (props.embedded) {
    // For embedded mode, get actual container dimensions
    // newWidth = modalContent.offsetWidth;
    newWidth = modalContent.offsetWidth;
    newHeight = 265;
  } else {
    newWidth = modalContent.offsetWidth;
    newHeight = modalContent.offsetHeight;
  }

  // console.error(`Current sizes - Fabric: ${currentFabricWidth}x${currentFabricHeight}, Grid: ${currentGridWidth}x${currentGridHeight}, Container: ${modalContent.offsetWidth}x${modalContent.offsetHeight}`);
  // console.error(`Target sizes: ${newWidth}x${newHeight}`);

  // Store current viewport transform
  const currentTransform = [...canvas.viewportTransform];

  // Update fabric canvas size
  canvas.setWidth(newWidth);
  canvas.setHeight(newHeight);

  // Update grid canvas dimensions - CRITICAL: Set both properties
  gridCanvas.width = newWidth;
  gridCanvas.height = newHeight;

  // Also set CSS dimensions to ensure they match exactly
  gridCanvas.style.width = newWidth + "px";
  gridCanvas.style.height = newHeight + "px";
  canvas.getElement().style.width = newWidth + "px";
  canvas.getElement().style.height = newHeight + "px";

  // Restore viewport transform
  canvas.setViewportTransform(currentTransform);

  // Redraw grid and canvas
  const vpt = canvas.viewportTransform;
  drawGrid(vpt[4], vpt[5], canvas.getZoom());
  canvas.requestRenderAll();

  // console.error(`After resize - Fabric: ${canvas.getWidth()}x${canvas.getHeight()}, Grid: ${gridCanvas.width}x${gridCanvas.height}`);
}
let viewportChangeTimeout = null;
function emitViewportChange() {
  if (!props.embedded || !canvas) return;

  // Throttle viewport change emissions to avoid performance issues
  clearTimeout(viewportChangeTimeout);
  viewportChangeTimeout = setTimeout(() => {
    const currentViewport = canvas.viewportTransform;
    emit("viewport-changed", [...currentViewport]); // Clone the array
  }, 500); // Emit after 500ms of no changes
}
// Add a watcher for showNoteHeader
watch(showNoteHeader, () => {
  // Use setTimeout to ensure the DOM has updated before measuring
  setTimeout(() => {
    resizeCanvasToContainer();
  }, 50); // Small delay to ensure DOM has updated
});

function updateNoteTitle(newTitle) {
  console.error("Updating note title:", newTitle, "tab is", props.tabId);
  noteTitle.value = newTitle;
  useTabStore().RenameTab(props.tabId, newTitle); //update tab live
}

function initaliseCanvas() {
  return new Promise((resolve, reject) => {
    // Get DOM elements with proper null checks
    modalContent = document.getElementById(canvasContainerId.value);
    fabricCanvasEl = document.getElementById(fabricCanvasId.value);
    gridCanvas = document.getElementById(gridCanvasId.value);

    // Check if elements exist before proceeding
    if (!modalContent || !fabricCanvasEl || !gridCanvas) {
      console.error("Canvas elements not found, retrying in 50ms");
      // Try again after a short delay to allow DOM to render
      setTimeout(() => {
        initaliseCanvas().then(resolve).catch(reject);
      }, 50);
      return;
    }

    try {
      // Now we can safely get the context
      gridContext = gridCanvas.getContext("2d");

      // Continue with canvas initialization
      canvas = new fabric.Canvas(fabricCanvasEl, {
        width: modalContent.offsetWidth,
        height: modalContent.offsetHeight,
        backgroundColor: "transparent",
      });

      // Add ResizeObserver to watch for container size changes

      // Add ResizeObserver to watch for container size changes
      const resizeObserver = new ResizeObserver((entries) => {
        for (let entry of entries) {
          // Debounce the resize to avoid too many calls
          clearTimeout(canvas.__resizeTimeout);
          canvas.__resizeTimeout = setTimeout(() => {
            resizeCanvasToContainer();
          }, 100);
        }
      });

      // Store observer reference for cleanup
      canvas.__resizeObserver = resizeObserver;

      // Start observing the container
      resizeObserver.observe(modalContent);

      //   function onObjectSelected(e) {
      //     object = e.selected[0]
      //     console.error("Object selected:", object).type;
      //     canvas.bringObjectToFront(object);
      //     object.bringObjectToFront();
      //     object.bringToFront();
      //     canvas.renderAll();

      // }
      // canvas.on('selection:created', onObjectSelected);

      console.error("Canvas initialized:", canvas);
      //might need changing in future but prevents blurry edges for now
      // Disable object caching for better performance
      fabric.Object.prototype.objectCaching = false;

      // IMPORTANT: Create a drawing brush first
      canvas.freeDrawingBrush = new fabric.PencilBrush(canvas);
      canvas.freeDrawingBrush.width = penWidth.value;
      canvas.freeDrawingBrush.color = colour.value;

      // Override the createPath method to disable caching
      const originalCreatePath = canvas.freeDrawingBrush.createPath;
      canvas.freeDrawingBrush.createPath = function (pathData) {
        const path = originalCreatePath.call(this, pathData);
        path.objectCaching = false;
        path.strokeLineCap = "round";
        path.strokeLineJoin = "round";
        return path;
      };

      // Set drawing mode based on your current mode
      canvas.isDrawingMode = mode.value === "draw";

      width = modalContent.offsetWidth;
      height = modalContent.offsetHeight;

      // canvas.setWidth(width);
      // canvas.setHeight(height);

      canvas.width = width;
      canvas.height = height;

      gridCanvas.width = width;
      gridCanvas.height = height;

      //drawgrid function here???
      gridSize = 20;
      vertical = true;
      horizontal = true;

      isPanning = false;
      lastPosX = 0;
      lastPosY = 0;
      // Sync grid with canvas after every render
      function syncGridWithCanvas() {
        const vpt = canvas.viewportTransform;
        drawGrid(vpt[4], vpt[5], canvas.getZoom());

        // Only emit viewport changes for embedded previews
        if (props.embedded) {
          emitViewportChange();
        }
      }

      // Attach the sync function to the after:render event
      canvas.on("after:render", syncGridWithCanvas);

      canvas.on("mouse:down", function (opt) {
        const evt = opt.e;
        if (evt.button === 1) {
          // Middle mouse button pressed
          isPanning = true;
          // canvas.isDrawingMode = false; // Temporarily disable drawing
          lastPosX = evt.clientX;
          lastPosY = evt.clientY;
        }
      });
      canvas.on("mouse:move", function (opt) {
        if (isPanning) {
          const evt = opt.e;
          const deltaX = evt.clientX - lastPosX;
          const deltaY = evt.clientY - lastPosY;
          const vpt = canvas.viewportTransform;
          vpt[4] += deltaX; // Update x-axis pan
          vpt[5] += deltaY; // Update y-axis pan
          drawGrid(vpt[4], vpt[5], canvas.getZoom());
          lastPosX = evt.clientX;
          lastPosY = evt.clientY;
        }
      });
      canvas.on("mouse:up", function () {
        isPanning = false;
      });
      canvas.on("mouse:wheel", function (opt) {
        const evt = opt.e;

        // Check for Ctrl key or pinch-to-zoom gesture
        if (evt.ctrlKey) {
          // Zoom behavior
          let zoom = canvas.getZoom();
          zoom *= 0.99 ** evt.deltaY; // Adjust zoom level
          zoom = Math.min(Math.max(zoom, 0.1), 50); // Limit zoom levels
          canvas.zoomToPoint({ x: evt.offsetX, y: evt.offsetY }, zoom);
          drawGrid(
            canvas.viewportTransform[4],
            canvas.viewportTransform[5],
            zoom
          ); // Redraw grid on zoom
        } else {
          // Panning behavior
          const deltaX = evt.deltaX;
          const deltaY = evt.deltaY;
          const vpt = canvas.viewportTransform;

          vpt[4] -= deltaX; // Horizontal panning
          vpt[5] -= deltaY; // Vertical panning
          drawGrid(vpt[4], vpt[5], canvas.getZoom()); // Redraw grid during panning
          canvas.requestRenderAll();
        }

        evt.preventDefault(); // Prevent default scrolling behavior
      });

      //mode switching if auto
      canvas.wrapperEl.addEventListener("pointerdown", (e) => {
        if (mode.value == "auto") {
          if (e.pointerType === "pen") {
            canvas.isDrawingMode = true;
            canvas.selection = false;
          } else if (e.pointerType === "touch" || e.pointerType === "mouse") {
            canvas.isDrawingMode = false;
            canvas.selection = true;
          }
        }
      });

      const hammer = new Hammer(canvas.wrapperEl);
      hammer
        .get("pan")
        .set({ direction: Hammer.DIRECTION_ALL, pointers: 2, threshold: 10 }); //threshod 10 to minimise accidental pans
      hammer.get("pinch").set({ enable: true });
      hammer.get("press").set({ time: 0 });
      hammer.get("pinch").recognizeWith(hammer.get("pan"));

      let lastScale = 1;

      hammer.on("pinchstart", function (e) {
        canvas._zoomStartScale = canvas.getZoom(); // Record the initial zoom level
        lastScale = 1; // Reset the last scale for the new gesture

        e.preventDefault();
        canvas.isDrawingMode = false;
        canvas.selection = false;
        canvas.forEachObject(function (o) {
          o.lockMovementX = true;
          o.lockMovementY = true;
          o.selectable = false;
        });
      });

      hammer.on("pinchmove", function (e) {
        const scaleChange = e.scale / lastScale; // Calculate incremental scale change
        lastScale = e.scale; // Update last scale for the next move event

        const newZoom = canvas.getZoom() * scaleChange; // Apply incremental zoom
        const boundedZoom = Math.min(Math.max(newZoom, 0.1), 50); // Clamp zoom level

        const center = { x: e.center.x, y: e.center.y }; // Zoom relative to touch center
        canvas.zoomToPoint(center, boundedZoom); // Apply zoom at the given point

        // Redraw grid and canvas
        drawGrid(
          canvas.viewportTransform[4],
          canvas.viewportTransform[5],
          boundedZoom
        );
        canvas.requestRenderAll();
      });

      hammer.on("pinchend", function () {
        lastScale = 1; // Reset scale tracking after the pinch gesture ends
        //restore canvas interaction
        if (mode.value == "draw") {
          canvas.isDrawingMode = true;
        }
        canvas.selection = true;
        canvas.forEachObject(function (o) {
          o.lockMovementX = false;
          o.lockMovementY = false;
          o.selectable = true;
        });
      });

      let lastDeltaX = 0;
      let lastDeltaY = 0;

      hammer.on("panstart", function (e) {
        e.preventDefault();
        canvas.isDrawingMode = false;
        canvas.selection = false;
        canvas.forEachObject(function (o) {
          o.lockMovementX = true;
          o.lockMovementY = true;
          o.selectable = false;
        });
      });

      hammer.on("panmove", function (e) {
        e.preventDefault();
        canvas.isDrawingMode = false;
        canvas.selection = false;
        canvas.forEachObject(function (o) {
          o.lockMovementX = true;
          o.lockMovementY = true;
          o.selectable = false;
        });

        const vpt = canvas.viewportTransform;

        // Calculate the incremental delta values
        const deltaX = e.deltaX - lastDeltaX;
        const deltaY = e.deltaY - lastDeltaY;

        // Update last delta values
        lastDeltaX = e.deltaX;
        lastDeltaY = e.deltaY;

        // Adjust the movement scale (optional for smoothing)
        const movementScale = 1;

        // Apply panning movement incrementally
        vpt[4] += deltaX * movementScale;
        vpt[5] += deltaY * movementScale;

        // Re-render the canvas with the new viewport transform
        canvas.requestRenderAll();
        drawGrid(vpt[4], vpt[5], canvas.getZoom()); // Redraw grid during panning
      });

      hammer.on("panend", function () {
        // Reset last delta values when the pan gesture ends
        lastDeltaX = 0;
        lastDeltaY = 0;
        //restore canvas interaction
        if (mode.value == "draw") {
          canvas.isDrawingMode = true;
        }
        canvas.selection = true;
        canvas.forEachObject(function (o) {
          o.lockMovementX = false;
          o.lockMovementY = false;
          o.selectable = true;
        });
      });
      resolve(canvas);
    } catch (error) {
      console.error("Error initializing canvas:", error);
      reject(error);
    }
  });
}

function HandleWhiteboardClick(event) {
  // Check if the active element is an input, textarea, or contenteditable element
  const activeElement = document.activeElement;
  const isEditableElement =
    activeElement.tagName === "INPUT" ||
    activeElement.tagName === "TEXTAREA" ||
    activeElement.getAttribute("contenteditable") === "true" ||
    activeElement.classList.contains("tiptap-editor") ||
    activeElement.isContentEditable;

  // If user is typing in an editable field, don't process keyboard shortcuts
  if (isEditableElement) {
    return;
  }
  if (event.key === "Escape") {
    event.preventDefault();
    closeNote();
  } else if (event.key === "Backspace" || event.key === "Delete") {
    deleteSelected();
  } else if (event.key === "Tab") {
    event.preventDefault(); // Prevent default tab behavior
    // Toggle between draw and type mode

    if (mode.value === "type") {
      mode.value = "draw";
    } else {
      mode.value = "type";
    }
  } else if (event.key === "Enter") {
    event.preventDefault(); // Prevent default enter behavior
    // Add a new text box
    addText();
  } else if (event.key === "r" || event.key === "R") {
    event.preventDefault(); // Prevent default R behavior
    // Add a rectangle shape
    addShape("rectangle");
  } else if (event.key === "c" || event.key === "C") {
    event.preventDefault(); // Prevent default C behavior
    // Add a circle shape
    addShape("circle");
  } else if (event.key === "t" || event.key === "T") {
    event.preventDefault(); // Prevent default T behavior
    // Add a triangle shape
    addShape("triangle");
  } else if (event.key === "i") {
    event.preventDefault(); // Prevent default I behavior
    // Add an image shape
    showNoteHeader.value = !showNoteHeader.value;
  } else if ((event.metaKey || event.ctrlKey) && event.key === "a") {
    event.preventDefault();
    canvas.discardActiveObject();
    var sel = new fabric.ActiveSelection(canvas.getObjects(), {
      canvas: canvas,
    });
    canvas.setActiveObject(sel);
    canvas.requestRenderAll();
  }
}

onMounted(async () => {
  await initaliseCanvas();
  console.error("Canvas initialization completed");
  const loaded = await LoadFromBackend();

  if (loaded) {
    // Only enable editing if not in view-only mode
    if (!props.viewOnly) {
      console.error("#########Edit mode enabled");
      useUserStore().addToRecentNotes(props.noteId);
      useTabStore().RenameTab(props.tabId, noteTitle);

      saveInterval.value = setInterval(async () => {
        await SaveToBackend();
      }, 15000);
      window.addEventListener("keydown", HandleWhiteboardClick);
    } else {
      // For view-only mode, disable all interactions except panning/zooming
      mode.value = "view";
      canvas.isDrawingMode = true;
      canvas.selection = false;
      canvas.forEachObject(function (e) {
        e.selectable = false;
        e.evented = false;
        e.target.lockSkewingY = true;
        e.target.lockSkewingX = true;
        e.target.lockMovementY = true;
        e.target.lockMovementX = true;
        e.target.hasControls = false;
      });
      let canvasElement = document.getElementsByClassName("fabricCanvas")[0];
      canvasElement.classList.add("locked");
    }
    // // Wait 50ms and then call the resize function
    // setTimeout(() => {
    //   resizeCanvasToContainer();
    // }, 500);
  }
});

onBeforeUnmount(async () => {
  // Clear viewport change timeout
  if (viewportChangeTimeout) {
    clearTimeout(viewportChangeTimeout);
    viewportChangeTimeout = null;
  }
  // Clean up ResizeObserver
  if (canvas && canvas.__resizeObserver) {
    canvas.__resizeObserver.disconnect();
    canvas.__resizeObserver = null;
  }

  if (canvas && canvas.__resizeTimeout) {
    clearTimeout(canvas.__resizeTimeout);
    canvas.__resizeTimeout = null;
  }
  if (!props.viewOnly) {
    // Wait for save to complete before destroying editor
    window.removeEventListener("keydown", HandleWhiteboardClick);
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
  }
});

function drawGrid(offsetX = 0, offsetY = 0, zoom = 1) {
  if (!gridContext || !gridCanvas) {
    console.error("Grid canvas not initialized");
    return;
  }
  if (background.value === "empty") {
    vertical = false;
    horizontal = false;
  } else if (background.value === "sGrid") {
    vertical = true;
    horizontal = true;
    gridSize = 20;
  } else if (background.value === "mGrid") {
    vertical = true;
    horizontal = true;
    gridSize = 40;
  } else if (background.value === "lGrid") {
    vertical = true;
    horizontal = true;
    gridSize = 60;
  } else if (background.value === "line") {
    vertical = false;
    horizontal = true;
    gridSize = 40;
  }
  gridContext.clearRect(0, 0, gridCanvas.width, gridCanvas.height); // Clear the grid canvas

  gridContext.strokeStyle = "#ccc";
  gridContext.lineWidth = 0.5;

  const scaledGridSize = gridSize * zoom;

  // Calculate starting points based on offset
  const startX = ((offsetX % scaledGridSize) + scaledGridSize) % scaledGridSize;
  const startY = ((offsetY % scaledGridSize) + scaledGridSize) % scaledGridSize;

  // Draw vertical lines
  if (vertical) {
    for (let x = startX; x < gridCanvas.width; x += scaledGridSize) {
      gridContext.beginPath();
      gridContext.moveTo(x, 0);
      gridContext.lineTo(x, gridCanvas.height);
      gridContext.stroke();
    }
  }

  // Draw horizontal lines
  if (horizontal) {
    for (let y = startY; y < gridCanvas.height; y += scaledGridSize) {
      gridContext.beginPath();
      gridContext.moveTo(0, y);
      gridContext.lineTo(gridCanvas.width, y);
      gridContext.stroke();
    }
  }
}

watch(mode, (newMode) => {
  //   canvas.isDrawingMode = newMode === "draw";
  if (newMode == "draw") {
    canvas.isDrawingMode = true;
    canvas.selection = false;
  } else if (newMode == "type") {
    canvas.isDrawingMode = false;
    canvas.selection = true;
  } else if (newMode == "view") {
    console.error("#########View-only mode enabled");
    canvas.isDrawingMode = false;
    canvas.selection = false;
    canvas.forEachObject(function (o) {
      o.selectable = false;
      o.evented = false;
    });
  }
});

watch(colour, (newColor) => {
  canvas.freeDrawingBrush.color = newColor;
  const activeObjects = canvas.getActiveObjects();
  activeObjects.forEach((obj) => {
    console.error("Updating color of object:", obj);

    if (obj.type === "path") {
      obj.set("stroke", newColor);
    } else if (obj.rough) {
      // Handle rough shapes - update properties and clear cache
      if (obj.type === "rect" || obj.type === "circle") {
        obj.set("stroke", newColor);
        obj.set("fill", newColor);
        // Clear the cached rough shape to force regeneration
        obj._roughShape = null;
      }
    } else {
      obj.set("fill", newColor);
    }
    canvas.renderAll();
  });
});

// Update the pen width watcher to handle rough shapes
watch(penWidth, (newWidth) => {
  canvas.freeDrawingBrush.width = newWidth;
  const activeObjects = canvas.getActiveObjects();
  activeObjects.forEach((obj) => {
    console.error("Updating stroke width of object:", obj);

    if (obj.type === "path") {
      obj.set("strokeWidth", newWidth);
    } else if (obj.rough) {
      // Handle rough shapes - update properties and clear cache
      obj.set("strokeWidth", newWidth);
      // Clear the cached rough shape to force regeneration
      obj._roughShape = null;
    }
    canvas.renderAll();
  });
});
watch(background, (newBackground) => {
  drawGrid(
    canvas.viewportTransform[4],
    canvas.viewportTransform[5],
    canvas.getZoom()
  );
});

// untested
// watch(background, (newBackground) => {
//   drawGrid(
//     canvas.viewportTransform[4],
//     canvas.viewportTransform[5],
//     canvas.getZoom()
//   );
// });
function centerWhiteboard() {
  if (!canvas) return;

  const zoom = canvas.getZoom();
  const visibleWidth = modalContent.offsetWidth;
  const visibleHeight = modalContent.offsetHeight;

  // Calculate the offsets to center (0, 0) in the visible area
  const offsetX = visibleWidth / 2 - 0 * zoom;
  const offsetY = visibleHeight / 2 - 0 * zoom;

  // Update the viewport transform
  canvas.viewportTransform = [zoom, 0, 0, zoom, offsetX, offsetY];

  // Redraw the grid and canvas
  drawGrid(offsetX, offsetY, zoom);
  canvas.requestRenderAll();
}
function addShape(shapeType) {
  const vpt = canvas.viewportTransform;
  const zoom = canvas.getZoom();
  const visibleWidth = modalContent.offsetWidth;
  const visibleHeight = modalContent.offsetHeight;
  const centerX = -vpt[4] / zoom + visibleWidth / (2 * zoom);
  const centerY = -vpt[5] / zoom + visibleHeight / (2 * zoom);
  
  let shape;
  
  if (shapeType === 'rectangle') {
    shape = createRoughShape('rectangle', {
      left: centerX - 50,
      top: centerY - 30,
      width: 100,
      height: 60,
      stroke: colour.value,
      strokeWidth: penWidth.value,
      // fill: colour.value,
      roughness: roughness.value,
      fillStyle: fillStyle.value,
    });
  } else if (shapeType === 'circle') {
    shape = createRoughShape('circle', {
      left: centerX - 50,
      top: centerY - 50,
      radius: 50,
      stroke: colour.value,
      strokeWidth: penWidth.value,
      fill: colour.value,
      roughness: roughness.value,
      fillStyle: fillStyle.value,
    });
  } else if (shapeType === 'triangle') {
    // For triangle, you might want to use regular Fabric or create a custom rough triangle
    shape = new fabric.Triangle({
      left: centerX - 50,
      top: centerY - 30,
      width: 100,
      height: 100,
      fill: colour.value,
      objectCaching: false,
    });
  }
  
  if (shape) {
    canvas.add(shape);
    canvas.setActiveObject(shape);
    canvas.renderAll();
  }
}

function createRoughShape(shapeType, options = {}) {
  let shape;
  
  if (shapeType === 'rectangle') {
    shape = new fabric.Rect({
      left: options.left || 100,
      top: options.top || 100,
      width: options.width || 100,
      height: options.height || 60,
      stroke: options.stroke || colour.value,
      strokeWidth: options.strokeWidth || penWidth.value,
      fill: options.fill || colour.value,
      objectCaching: false,
      // fillStyle: options.fillStyle || fillStyle.value,
      rough: true,
      roughness: options.roughness || roughness.value,
      bowing: options.bowing || 1,
      fillStyle: options.fillStyle || fillStyle.value,
    });
    
    const originalRender = shape._render;
    shape._render = function(ctx) {
      if (!this.rough) {
        originalRender.call(this, ctx);
        return;
      }
      
      const rc = rough.canvas(ctx.canvas);
      
      // Always check if we need to regenerate the shape
      // This happens when properties change or cache is cleared
      if (!this._roughShape || this._needsRegeneration) {
        this._roughShape = rc.rectangle(
          -this.width / 2,
          -this.height / 2,
          this.width,
          this.height,
          {
            stroke: this.stroke,
            strokeWidth: this.strokeWidth,
            fill: this.fill,
            roughness: this.roughness || 1,
            bowing: this.bowing || 1,
            fillStyle: this.fillStyle || 'solid',
          }
        );
        this._needsRegeneration = false;
      }
      
      rc.draw(this._roughShape);
    };
    
    // Override the set method to detect property changes
    const originalSet = shape.set;
    shape.set = function(key, value) {
      const result = originalSet.call(this, key, value);
      
      // Check if any property that affects rough rendering has changed
      if (typeof key === 'object') {
        const roughProps = ['stroke', 'strokeWidth', 'fill', 'roughness', 'bowing', 'fillStyle', 'width', 'height'];
        const hasRoughPropChange = roughProps.some(prop => key.hasOwnProperty(prop));
        if (hasRoughPropChange) {
          this._needsRegeneration = true;
        }
      } else if (['stroke', 'strokeWidth', 'fill', 'roughness', 'bowing', 'fillStyle', 'width', 'height'].includes(key)) {
        this._needsRegeneration = true;
      }
      
      return result;
    };
    
  } else if (shapeType === 'circle') {
    shape = new fabric.Circle({
      left: options.left || 100,
      top: options.top || 100,
      radius: options.radius || 50,
      stroke: options.stroke || colour.value,
      strokeWidth: options.strokeWidth || penWidth.value,
      fill: options.fill || colour.value,
      objectCaching: false,
      rough: true,
      roughness: options.roughness || roughness.value,
      bowing: options.bowing || 1,
      fillStyle: options.fillStyle || fillStyle.value,
    });
    
    const originalRender = shape._render;
    shape._render = function(ctx) {
      if (!this.rough) {
        originalRender.call(this, ctx);
        return;
      }
      
      const rc = rough.canvas(ctx.canvas);
      
      if (!this._roughShape || this._needsRegeneration) {
        this._roughShape = rc.circle(0, 0, this.radius * 2, {
          stroke: this.stroke,
          strokeWidth: this.strokeWidth,
          fill: this.fill,
          roughness: this.roughness || 1,
          bowing: this.bowing || 1,
          fillStyle: this.fillStyle || 'solid',
        });
        this._needsRegeneration = false;
      }
      
      rc.draw(this._roughShape);
    };
    
    // Override the set method for circles too
    const originalSet = shape.set;
    shape.set = function(key, value) {
      const result = originalSet.call(this, key, value);
      
      if (typeof key === 'object') {
        const roughProps = ['stroke', 'strokeWidth', 'fill', 'roughness', 'bowing', 'fillStyle', 'radius'];
        const hasRoughPropChange = roughProps.some(prop => key.hasOwnProperty(prop));
        if (hasRoughPropChange) {
          this._needsRegeneration = true;
        }
      } else if (['stroke', 'strokeWidth', 'fill', 'roughness', 'bowing', 'fillStyle', 'radius'].includes(key)) {
        this._needsRegeneration = true;
      }
      
      return result;
    };
  }
  
  return shape;
}

// Add roughness controls
const roughness = ref(1);
const fillStyle = ref('hachure');


function addText() {
  const textbox = new fabric.Textbox("Type here...", {
    left: 20,
    top: 20,
    width: 300,
    fontSize: 30,
    fill: "gray", // Set placeholder text color
    editable: true,
    borderColor: "#ccc",
    cornerColor: "#ccc",
    hasBorders: true,
    hasControls: true,
  });

  // Event listener for when the text box is clicked and edited
  textbox.on("editing:entered", function () {
    // Only clear the text if it is still the placeholder text
    if (textbox.text.trim() === "Type here...") {
      textbox.set({ text: "" }); // Clear the placeholder text
      textbox.set({ fill: "black" }); // Set text color to black
      canvas.renderAll(); // Re-render the canvas to reflect the changes
    }
  });

  canvas.add(textbox);
}
function deleteSelected() {
  const activeObjects = canvas.getActiveObjects();
  activeObjects.forEach((obj) => canvas.remove(obj));
  canvas.discardActiveObject().renderAll();
}

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

const uploadImageFile = (file) => {
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
        // Insert the image at at the middle of the fabric canvas and select it use src - src: getBaseUrl() + response.data.url
        const fullImageUrl = getBaseUrl() + response.data.url;
        console.error("Image URL:", fullImageUrl);
        addImageToCanvas(fullImageUrl);
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
    // add the selected url as an image to center of fabric src - src: getBaseUrl() + response.data.url
    addImageToCanvas(imageUrlInput.value);
    closeImageModal();
  }
};
const addImageToCanvas = (imageUrl) => {
  if (!canvas) return;

  // Calculate the center of the current viewport in canvas coordinates
  const vpt = canvas.viewportTransform;
  const zoom = canvas.getZoom();
  const visibleWidth = modalContent.offsetWidth;
  const visibleHeight = modalContent.offsetHeight;
  const centerX = -vpt[4] / zoom + visibleWidth / (2 * zoom);
  const centerY = -vpt[5] / zoom + visibleHeight / (2 * zoom);
  console.error("Adding image to canvas at:", centerX, centerY);
  // Create a fabric image object
  // fabric.Image.fromURL(imageUrl, (img) => {
  //   // Scale image if it's too large
  //   const maxSize = 300;
  //   if (img.width > maxSize || img.height > maxSize) {
  //     const scale = maxSize / Math.max(img.width, img.height);
  //     img.scale(scale);
  //   }

  // Position at center
  // img.set({
  //   left: centerX - (img.width * (img.scaleX || 1)) / 2,
  //   top: centerY - (img.height * (img.scaleY || 1)) / 2,
  //   objectCaching: false,
  // });

  // Add to canvas, select it and render
  // canvas.add(img);
  // canvas.setActiveObject(img);
  // canvas.requestRenderAll();
  // });

  fabric.Image.fromURL(imageUrl, function (img) {
    var oImg = img
      .set({ left: 0, top: 0, angle: 0, width: 100, height: 100 })
      .scale(1);
    canvas.add(oImg).renderAll();
    canvas.requestRenderAll();
    var a = canvas.setActiveObject(oImg);
    var dataURL = canvas.toDataURL({ format: "png", quality: 0.8 });
  });

  // image = new fabric.Rect({
  //   left: centerX - 50, // Center by offsetting half width
  //   top: centerY - 30, // Center by offsetting half height
  //   width: 100,
  //   height: 60,
  //   fill: colour.value,
  //   objectCaching: false,
  // });
};

// Version history methods
const openVersionHistoryModal = async () => {
  showVersionHistoryModal.value = true;
  await fetchVersionHistory();
};

const closeVersionHistoryModal = () => {
  showVersionHistoryModal.value = false;
  selectedVersion.value = null;
};

const fetchVersionHistory = async () => {
  loadingVersions.value = true;
  try {
    const response = await axios.post("/load", {
      operation: "versions",
      note_id: props.noteId,
    });
    versionHistory.value = response.data.versions || [];
  } catch (error) {
    console.error("Error fetching version history:", error);
    toast({
      title: "Error",
      description: "Failed to load version history",
      variant: "destructive",
    });
  } finally {
    loadingVersions.value = false;
  }
};
const restoreVersion = async (version) => {
  if (!confirm("Are you sure you want to restore this version?")) {
    return;
  }

  try {
    // await axios.post(`/restore-version/${props.noteId}/${version.id}`);

    const response = await axios.post("/update", {
      operation: "restore",
      note_id: props.noteId,
      version_index: version.index,
    });

    // Reload content
    await LoadFromBackend();

    toast({
      title: "Success",
      description: "Version restored successfully",
      variant: "success",
    });

    // Close the modal
    closeVersionHistoryModal();
  } catch (error) {
    console.error("Error restoring version:", error);
    toast({
      title: "Error",
      description: "Failed to restore version",
      variant: "destructive",
    });
  }
};
const createManualVersion = async () => {
  // Get a name for this version from the user
  const versionName = prompt(
    "Enter a name for this restore point:",
    `Manual save ${new Date().toLocaleString()}`
  );

  if (versionName === null) return; // User cancelled

  try {
    // Make the API call to create a manual version
    const response = await axios.post("/create", {
      type: "version",
      note_id: props.noteId,
      version_name: versionName,
    });

    // Show success message
    toast({
      title: "Restore Point Created",
      description: `Version "${versionName}" created successfully`,
      variant: "success",
    });

    // Refresh version history to show the new version
    await fetchVersionHistory();
  } catch (error) {
    console.error("Error creating manual version:", error);
    toast({
      title: "Error",
      description: "Failed to create restore point",
      variant: "destructive",
    });
  }
};
const showVersionHistoryModal = ref(false);
const selectedVersion = ref(null);
const versionHistory = ref([]);
const loadingVersions = ref(false);
</script>
