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
            <div class="flex items-center gap-1 flex-wrap">
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

              <!-- Edit Mode -->
              <Button
                :variant="mode === 'draw' ? 'default' : 'ghost'"
                size="sm"
                class="flex items-center gap-2 px-3"
                @click="mode = mode === 'draw' ? 'type' : 'draw'"
              >
                <Pencil class="h-4 w-4" />
                <span>{{
                  mode === "draw" ? "Drawing: On" : "Drawing: Off"
                }}</span>
              </Button>

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
                </DropdownMenuContent>
              </DropdownMenu>

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
      <Circle class="h-4 w-4 mr-2" fill="white" stroke="#e5e5e5" />
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
                    <span>Type</span>
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
                    <Check v-if="background == 'line'" class="h-4 w-4 ml-auto" />
                  </DropdownMenuItem>
                  <Separator />
                  <DropdownMenuItem @click="background = 'sGrid'">
                    <Grid class="h-4 w-4 mr-2" />
                    <span>Small Grid</span>
                    <Check v-if="background == 'sGrid'" class="h-4 w-4 ml-auto" />
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="background = 'mGrid'">
                    <Grid class="h-4 w-4 mr-2" />
                    <span>Medium Grid</span>
                    <Check v-if="background == 'mGrid'" class="h-4 w-4 ml-auto" />
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="background = 'lGrid'">
                    <Grid class="h-4 w-4 mr-2" />
                    <span>Large Grid</span>
                    <Check v-if="background == 'lGrid'" class="h-4 w-4 ml-auto" />
                  </DropdownMenuItem>
                  <Separator />
                  <DropdownMenuItem @click="background = 'empty'">
                    <Square class="h-4 w-4 mr-2" />
                    <span>Blank</span>
                    <Check v-if="background == 'empty'" class="h-4 w-4 ml-auto" />
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
            class="bg-primary-foreground shadow-lg rounded-lg p-4 max-w-[2000px] w-full mx-auto"
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

      <div class="flex justify-center flex-1">
        <div
          id="canvas-container"
          class="canvas-container w-full  overflow-hidden bg-primary-foreground rounded-lg border border-input m-4 relative"
          :class="showNoteHeader ? 'h-[calc(100vh-24rem)]' : 'h-[calc(100vh-12rem)]'"
        >
          <!-- Grid canvas (bottom layer) -->
          <canvas
            id="grid-canvas"
            class="absolute top-0 left-0 w-full h-full"
          ></canvas>
          <!-- Main canvas (top layer) -->
          <canvas
            id="fabricCanvas"
            class="absolute top-0 left-0 w-full h-full"
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
import { ref, onMounted, onBeforeUnmount, watch } from "vue";
import * as fabric from "fabric";
import Hammer from "hammerjs";
import axios, { getBaseUrl } from "../axios.js";
import { useTabStore } from "@/stores/useTabStore";
import { useGraphStore } from "@/stores/useGraphStore";
import { useUserStore } from "@/stores/useUserStore";
import Loading from "@/components/Loading.vue";
import NoteHeader from "@/components/Document Editor/NoteHeader.vue";
import { FileText, Info } from "lucide-vue-next";
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
  Check
} from "lucide-vue-next";
import { useToast } from "@/components/ui/toast/use-toast";

const props = defineProps({
  noteId: Number || 0,
  tabId: Number || 0,
});
const showNoteHeader = ref(false);
const emit = defineEmits(["note-closed"]);
const saveInterval = ref(null);
const noteTitle = ref("Untitled Note");
const noteTags = ref([]);
const { toast } = useToast();
const isLoading = ref(false);
const viewport = ref({ x: 0, y: 0, zoom: 1 });
const background = ref("lGrid");
const mode = ref("draw");
const colour = ref("");

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
  try {
    // isLoading.value = true;

    const response = await axios.post("/load", {
      id: props.noteId,
      operation: "content",
    });
    console.error("Note loaded successfully:", response.data);
    // Set the title in our ref
    noteTitle.value = response.data.name || "Untitled Note";
    // Set the viewport

    // Extract tags if they exist in the response
    if (response.data.tags) {
      noteTags.value = response.data.tags;
    }

    if (response.data.viewport) {
      viewport.value = JSON.parse(response.data.viewport);
      canvas.setViewportTransform(viewport.value);
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
            canvas.getObjects().forEach(obj => {
              // Check if it's a path or path-like object
              if (obj.type === 'path' || obj.type === 'line' || obj.path) {
                obj.objectCaching = false;
                if (obj.strokeLineCap !== undefined) {
                  obj.strokeLineCap = 'round';
                  obj.strokeLineJoin = 'round';
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
  // Guard against accessing canvas before it's initialized
  if (!canvas || !gridCanvas || !modalContent) return;
  
  // Get the new container dimensions
  const newWidth = modalContent.offsetWidth;
  const newHeight = modalContent.offsetHeight;
  
  // Update both canvas sizes
  canvas.setWidth(newWidth);
  canvas.setHeight(newHeight);
  gridCanvas.width = newWidth;
  gridCanvas.height = newHeight;
  
  // Redraw the grid with current viewport
  const vpt = canvas.viewportTransform;
  drawGrid(vpt[4], vpt[5], canvas.getZoom());
  
  // Force canvas to render
  canvas.requestRenderAll();
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
  modalContent = document.getElementById("canvas-container");
  fabricCanvasEl = document.getElementById("fabricCanvas");
  gridCanvas = document.getElementById("grid-canvas");
  gridContext = gridCanvas.getContext("2d");

  canvas = new fabric.Canvas(fabricCanvasEl, {
    width: modalContent.offsetWidth,
    height: modalContent.offsetHeight,
    backgroundColor: "transparent", // Ensure background is transparent
  });
  
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

  canvas.setWidth(width);
  canvas.setHeight(height);

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
      drawGrid(canvas.viewportTransform[4], canvas.viewportTransform[5], zoom); // Redraw grid on zoom
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
  window.addEventListener(
    "touchstart",
    function (e) {
      const touches = e.touches;
      if (touches.length === 2) {
        console.log("ultimate two fingers detected");
        console.log(touches);
        canvas.discardActiveObject().renderAll();
        // const activ=eObject = canvas.getActiveObject();

        e.preventDefault();
        canvas.isDrawingMode = false;
        canvas.selection = false;
        canvas.forEachObject(function (o) {
          o.lockMovementX = true;
          o.lockMovementY = true;
          o.selectable = false;
        });
      } else if (touches.length === 1) {
        console.log("only one finger detected");

        canvas.selection = true;
        canvas.forEachObject(function (o) {
          o.lockMovementX = false;
          o.lockMovementY = false;
          o.selectable = true;
        });
        if (mode.value === "draw") {
          canvas.isDrawingMode = true;
        }
      }

      if (touches.length > 0) {
        const touch = touches[0];

        if ("force" in touch) {
          console.log("Touch pressure (force):", touch.force);
        }
        if (touch.force > 0) {
          console.log("Apple Pencil detected");
          if (mode.value === "draw") {
            canvas.isDrawingMode = true;
          }
        } else {
          console.log("Finger detected");
          canvas.isDrawingMode = false;
        }
      }
    },
    true
  );
  const hammer = new Hammer(canvas.wrapperEl);
  hammer.get("pan").set({ direction: Hammer.DIRECTION_ALL, pointers: 2 });
  hammer.get("pinch").set({ enable: true });
  hammer.get("press").set({ time: 0 });
  hammer.get("pinch").recognizeWith(hammer.get("pan"));

  let lastScale = 1;

  hammer.on("pinchstart", function (e) {
    canvas._zoomStartScale = canvas.getZoom(); // Record the initial zoom level
    lastScale = 1; // Reset the last scale for the new gesture
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
  });
  let lastDeltaX = 0;
  let lastDeltaY = 0;

  hammer.on("panmove", function (e) {
    console.log("Pan move detected:", e); // Debugging log

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
  });
}


function HandleWhiteboardClick(event) {
    // Check if the active element is an input, textarea, or contenteditable element
    const activeElement = document.activeElement;
  const isEditableElement = 
    activeElement.tagName === 'INPUT' || 
    activeElement.tagName === 'TEXTAREA' || 
    activeElement.getAttribute('contenteditable') === 'true' ||
    activeElement.classList.contains('tiptap-editor') ||
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
  }  else if (event.key === "Tab") {
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
  // Wait for content to load before proceeding
  initaliseCanvas();
  const loaded = await LoadFromBackend();

  // Only proceed with the rest if loading was successful
  if (loaded) {
    useUserStore().addToRecentNotes(props.noteId);
    

    // Full save every minute
    saveInterval.value = setInterval(async () => {
      await SaveToBackend();
    }, 60000);
    window.addEventListener("keydown", HandleWhiteboardClick);
    // initaliseCanvas();
    // console.error("Editor loaded successfully", isLoading.value);
  }
});

onBeforeUnmount(async () => {
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
});

function drawGrid(offsetX = 0, offsetY = 0, zoom = 1) {
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
  } else {
    canvas.isDrawingMode = false;
  }
});



watch(colour, (newColor) => {
  canvas.freeDrawingBrush.color = newColor;
  const activeObjects = canvas.getActiveObjects();
  activeObjects.forEach((obj) => {
    console.error("Updating color of object:", obj);
    
    if (obj.type === "path") {
      obj.set("stroke", newColor);
    } else {
      obj.set("fill", newColor);
    }
    canvas.renderAll();
  });
});
watch(penWidth, (newWidth) => {
  canvas.freeDrawingBrush.width = newWidth;
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

function addShape(shapeType) {

    // Calculate the center of the current viewport in canvas coordinates
    const vpt = canvas.viewportTransform;
  const zoom = canvas.getZoom();
  
  // Get the visible area dimensions
  const visibleWidth = modalContent.offsetWidth;
  const visibleHeight = modalContent.offsetHeight;
  
  // Calculate the center position in canvas coordinates
  const centerX = (-vpt[4] / zoom) + (visibleWidth / (2 * zoom));
  const centerY = (-vpt[5] / zoom) + (visibleHeight / (2 * zoom));
  let shape;
  if (shapeType === "rectangle") {
    shape = new fabric.Rect({
      left: centerX - 50, // Center by offsetting half width
      top: centerY - 30,  // Center by offsetting half height
      width: 100,
      height: 60,
      fill: colour.value,
      objectCaching: false,
    });
  } else if (shapeType === "circle") {
    shape = new fabric.Circle({
      left: centerX - 50, 
      top: centerY - 30,
      radius: 50,
      fill: colour.value,
      objectCaching: false, // prevent cachnig to improve sharpnes on zoom
    });
  } else if (shapeType === "triangle") {
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
  }
}

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
</script>
