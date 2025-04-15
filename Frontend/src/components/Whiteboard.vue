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

              <!-- Edit Mode -->
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="ghost"
                    size="sm"
                    class="flex gap-1 items-center"
                  >
                    <TextIcon v-if="mode === 'type'" class="h-4 w-4" />
                    <Pencil v-else-if="mode === 'draw'" class="h-4 w-4" />
                    <Eraser v-else-if="mode === 'eraser'" class="h-4 w-4" />
                    <span>Mode: {{ mode }}</span>
                    <ChevronDownIcon class="h-3 w-3 opacity-50" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuItem @click="mode = 'draw'">
                    <Pencil class="h-4 w-4 mr-2" />
                    <span>Draw</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="mode = 'type'">
                    <Type class="h-4 w-4 mr-2" />
                    <span>Type</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="mode = 'pan'">
                    <Move class="h-4 w-4 mr-2" />
                    <span>Move</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="mode = 'eraser'">
                    <Eraser class="h-4 w-4 mr-2" />
                    <span>Erase</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>

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
                    <Palette class="h-4 w-4" />
                    <span>Colour</span>
                    <ChevronDownIcon class="h-3 w-3 opacity-50" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuItem @click="penColour = 'black'">
                    <Circle class="h-4 w-4 mr-2" fill="black" />
                    <span>Black</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="penColour = 'white'">
                    <Circle class="h-4 w-4 mr-2" fill="white" />
                    <span>White</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="penColour = 'red'">
                    <Circle class="h-4 w-4 mr-2" fill="red" />
                    <span>Red</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="penColour = 'blue'">
                    <Circle class="h-4 w-4 mr-2" fill="blue" />
                    <span>Blue</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="penColour = 'green'">
                    <Circle class="h-4 w-4 mr-2" fill="green" />
                    <span>Green</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>

              <Separator orientation="vertical" class="h-6 mx-1" />

              <!-- Pen Width -->
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
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="penWidth = 3">
                    <Minus class="h-4 w-4 mr-2" :stroke-width="1" />
                    <span>Medium</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="penWidth = 8">
                    <Minus class="h-4 w-4 mr-2" :stroke-width="3" />
                    <span>Bold</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="penWidth = 16">
                    <Minus class="h-4 w-4 mr-2" :stroke-width="5" />
                    <span>Thick</span>
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
                  </DropdownMenuItem>
                  <Separator />
                  <DropdownMenuItem @click="background = 'sGrid'">
                    <Grid class="h-4 w-4 mr-2" />
                    <span>Small Grid</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="background = 'mGrid'">
                    <Grid class="h-4 w-4 mr-2" />
                    <span>Medium Grid</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="background = 'lGrid'">
                    <Grid class="h-4 w-4 mr-2" />
                    <span>Large Grid</span>
                  </DropdownMenuItem>
                  <Separator />
                  <DropdownMenuItem @click="background = 'empty'">
                    <Square class="h-4 w-4 mr-2" />
                    <span>Blank</span>
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
                      <Eraser class="h-4 w-4" />
                    </Button>
                  </TooltipTrigger>
                  <TooltipContent>Delete Selected</TooltipContent>
                </Tooltip>
              </TooltipProvider>
            </div>
          </div>
        </div>
      </div>

      <div class="flex justify-center flex-1">
        <div
          id="canvas-container"
          class="canvas-container w-full max-w-[2000px] h-[calc(100vh-12rem)] overflow-hidden bg-primary-foreground rounded-lg border border-input m-4 relative"
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

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from "vue";
import * as fabric from "fabric";
import Hammer from "hammerjs";
import axios, { getBaseUrl } from "../axios.js";
import { useTabStore } from "@/stores/useTabStore";
import { useGraphStore } from "@/stores/useGraphStore";
import { useUserStore } from "@/stores/useUserStore";
import Loading from "@/components/Loading.vue";
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
} from "lucide-vue-next";
import { useToast } from "@/components/ui/toast/use-toast";

const props = defineProps({
  noteId: Number || 0,
  tabId: Number || 0,
});
const emit = defineEmits(["note-closed"]);
const saveInterval = ref(null);
const noteTitle = ref("Untitled Note");
const noteTags = ref([]);
const { toast } = useToast();
const isLoading = ref(false);
const viewport = ref({ x: 0, y: 0, zoom: 1 });
const background = ref("Lgrid");
const mode = ref("draw");
const penColour = ref("");

if (useUserStore.theme == "dark") {
  penColour.value = "white";
} else {
  penColour.value = "black";
}
const penWidth = ref(5);

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
  console.error("Canvas initialized:", canvas);
  //might need changing in future but prevents blurry edges for now
  // Disable object caching for better performance
  fabric.Object.prototype.objectCaching = false;

  // IMPORTANT: Create a drawing brush first
  canvas.freeDrawingBrush = new fabric.PencilBrush(canvas);
  canvas.freeDrawingBrush.width = penWidth.value;
  canvas.freeDrawingBrush.color = penColour.value;

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
    // initaliseCanvas();
    // console.error("Editor loaded successfully", isLoading.value);
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

watch(penColour, (newColor) => {
  canvas.freeDrawingBrush.color = newColor;
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
  let shape;
  if (shapeType === "rectangle") {
    shape = new fabric.Rect({
      left: 100,
      top: 100,
      width: 100,
      height: 60,
      fill: "blue",
    });
  } else if (shapeType === "circle") {
    shape = new fabric.Circle({
      left: 100,
      top: 100,
      radius: 50,
      fill: "green",
    });
  } else if (shapeType === "triangle") {
    shape = new fabric.Triangle({
      left: 100,
      top: 100,
      width: 100,
      height: 100,
      fill: "yellow",
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
