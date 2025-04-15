<!-- filepath: /Users/Henry/Desktop/EPQ/Frontend/src/components/Whiteboard.vue -->
<script setup>
import Loading from "@/components/Loading.vue";
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
} from "lucide-vue-next";
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
import { Button } from "@/components/ui/Button";
import { Switch } from "@/components/ui/switch";
import { Slider } from "@/components/ui/slider";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from "vue";
import { useToast } from "@/components/ui/toast/use-toast";
import * as fabric from "fabric";
import Hammer from "hammerjs";
import axios from "../axios.js";
import { useGraphStore } from "@/stores/useGraphStore";

// Props for the component
const props = defineProps({
  noteId: Number || 0,
  tabId: Number || 0,
});

const emit = defineEmits(["note-closed"]);
const { toast } = useToast();

// Drawing state
const currentMode = ref("draw"); // draw, type, select, etc.
const penColor = ref("#000000");
const penWidth = ref(3);
const backgroundColor = ref("#ffffff");
const isErasing = ref(false);
const noteName = ref("Untitled Whiteboard");
const isLoading = ref(true);

// Canvas references
const canvas = ref(null);
const gridCanvas = ref(null);
const gridContext = ref(null);

// Grid settings
const gridSize = ref(20);
const gridType = ref("blank"); // blank, s__grid, m_grid, l_grid, line

// History management
const undoStack = ref([]);
const redoStack = ref([]);

// Methods to control the whiteboard
const setMode = (mode) => {
  currentMode.value = mode;

  if (!canvas.value) return;

  // Set drawing mode based on selection
  if (mode === "draw") {
    canvas.value.isDrawingMode = true;
    isErasing.value = false;
  } else if (mode === "eraser") {
    canvas.value.isDrawingMode = true;
    isErasing.value = true;
    // Store the original brush color
    const originalColor = canvas.value.freeDrawingBrush.color;
    // Set brush color to background
    canvas.value.freeDrawingBrush.color = backgroundColor.value;
  } else {
    // For text or other modes
    canvas.value.isDrawingMode = false;
    isErasing.value = false;
  }
};

const setPenColor = (color) => {
  penColor.value = color;
  if (canvas.value && !isErasing.value) {
    canvas.value.freeDrawingBrush.color = color;
  }
};

const setPenWidth = (width) => {
  penWidth.value = width;
  if (canvas.value) {
    canvas.value.freeDrawingBrush.width = width;
  }
};

const setBackgroundColor = (color) => {
  backgroundColor.value = color;

  // If we have a canvas container, set its background
  const containerEl = document.querySelector(".canvas-container");
  if (containerEl) {
    containerEl.style.backgroundColor = color;
  }
};

const setGridType = (type) => {
  gridType.value = type;

  // Update grid size based on type
  if (type === "blank") {
    // No grid
  } else if (type === "s__grid") {
    gridSize.value = 20;
  } else if (type === "m_grid") {
    gridSize.value = 40;
  } else if (type === "l_grid") {
    gridSize.value = 60;
  } else if (type === "line") {
    gridSize.value = 40;
  }

  // Redraw the grid
  drawGrid();
};

// Shape handling
const addShape = (shapeType) => {
  if (!canvas.value) return;

  let shape;
  switch (shapeType) {
    case "rectangle":
      shape = new fabric.Rect({
        left: 100,
        top: 100,
        width: 100,
        height: 60,
        fill: penColor.value,
        strokeWidth: 1,
        stroke: "#000000",
      });
      break;
    case "circle":
      shape = new fabric.Circle({
        left: 100,
        top: 100,
        radius: 50,
        fill: penColor.value,
        strokeWidth: 1,
        stroke: "#000000",
      });
      break;
    case "triangle":
      shape = new fabric.Triangle({
        left: 100,
        top: 100,
        width: 100,
        height: 100,
        fill: penColor.value,
        strokeWidth: 1,
        stroke: "#000000",
      });
      break;
    case "line":
      shape = new fabric.Line([50, 50, 200, 50], {
        left: 100,
        top: 100,
        stroke: penColor.value,
        strokeWidth: penWidth.value,
      });
      break;
  }

  if (shape) {
    // Save canvas state before adding shape
    saveCanvasState();
    canvas.value.add(shape);
    canvas.value.setActiveObject(shape);
    canvas.value.requestRenderAll();
  }
};

const addText = () => {
  if (!canvas.value) return;

  const textbox = new fabric.Textbox("Type here...", {
    left: 100,
    top: 100,
    width: 300,
    fontSize: 30,
    fill: "gray",
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
      textbox.set({ text: "" }); // Clear placeholder text
      textbox.set({ fill: "black" }); // Set text color to black
      canvas.value.renderAll(); // Re-render the canvas to reflect the changes
    }
  });

  // Save canvas state before adding text
  saveCanvasState();
  canvas.value.add(textbox);
  canvas.value.setActiveObject(textbox);
  canvas.value.requestRenderAll();
};

const deleteSelected = () => {
  if (!canvas.value) return;

  const activeObjects = canvas.value.getActiveObjects();
  if (activeObjects.length > 0) {
    // Save canvas state before deleting
    saveCanvasState();

    activeObjects.forEach((obj) => canvas.value.remove(obj));
    canvas.value.discardActiveObject().renderAll();

    toast({
      title: "Objects deleted",
      description: `Deleted ${activeObjects.length} object(s)`,
      duration: 2000,
    });
  }
};

const clearCanvas = () => {
  if (
    confirm(
      "Are you sure you want to clear the canvas? This action cannot be undone."
    )
  ) {
    if (!canvas.value) return;

    // Save canvas state before clearing
    saveCanvasState();

    // Clear all objects
    canvas.value.clear();
    canvas.value.backgroundColor = backgroundColor.value;
    canvas.value.renderAll();

    toast({
      title: "Canvas cleared",
      description: "All content has been removed",
    });
  }
};

// History management (undo/redo)
const saveCanvasState = () => {
  if (!canvas.value) return;

  const json = JSON.stringify(canvas.value.toJSON());
  undoStack.value.push(json);
  // Clear redo stack when new action is performed
  redoStack.value = [];

  // Limit undo stack size to prevent memory issues
  if (undoStack.value.length > 30) {
    undoStack.value.shift();
  }
};

const undo = () => {
  if (!canvas.value || undoStack.value.length === 0) return;

  // Save current state to redo stack
  const currentState = JSON.stringify(canvas.value.toJSON());
  redoStack.value.push(currentState);

  // Apply the previous state
  const prevState = undoStack.value.pop();
  canvas.value.loadFromJSON(
    prevState,
    canvas.value.renderAll.bind(canvas.value)
  );
};

const redo = () => {
  if (!canvas.value || redoStack.value.length === 0) return;

  // Save current state to undo stack
  const currentState = JSON.stringify(canvas.value.toJSON());
  undoStack.value.push(currentState);

  // Apply the next state
  const nextState = redoStack.value.pop();
  canvas.value.loadFromJSON(
    nextState,
    canvas.value.renderAll.bind(canvas.value)
  );
};

const downloadCanvas = () => {
  if (!canvas.value) return;

  // Temporarily show the grid for the download
  const showGrid = gridType.value !== "blank";

  // Create a composite canvas for download
  const downloadCanvas = document.createElement("canvas");
  const ctx = downloadCanvas.getContext("2d");

  // Set the download canvas size
  downloadCanvas.width = canvas.value.width;
  downloadCanvas.height = canvas.value.height;

  // Fill with background color
  ctx.fillStyle = backgroundColor.value;
  ctx.fillRect(0, 0, downloadCanvas.width, downloadCanvas.height);

  // If grid is enabled, draw it on the download canvas
  if (showGrid) {
    const tempCanvas = document.createElement("canvas");
    tempCanvas.width = downloadCanvas.width;
    tempCanvas.height = downloadCanvas.height;
    const tempCtx = tempCanvas.getContext("2d");

    // Draw grid on temp canvas
    tempCtx.strokeStyle = "#ccc";
    tempCtx.lineWidth = 0.5;

    const drawVertical = gridType.value !== "line";
    const drawHorizontal = gridType.value !== "blank";

    if (drawVertical) {
      for (let x = 0; x < downloadCanvas.width; x += gridSize.value) {
        tempCtx.beginPath();
        tempCtx.moveTo(x, 0);
        tempCtx.lineTo(x, downloadCanvas.height);
        tempCtx.stroke();
      }
    }

    if (drawHorizontal) {
      for (let y = 0; y < downloadCanvas.height; y += gridSize.value) {
        tempCtx.beginPath();
        tempCtx.moveTo(0, y);
        tempCtx.lineTo(downloadCanvas.width, y);
        tempCtx.stroke();
      }
    }

    // Copy the grid to the download canvas
    ctx.drawImage(tempCanvas, 0, 0);
  }

  // Draw Fabric.js canvas content on top
  ctx.drawImage(canvas.value.lowerCanvasEl, 0, 0);

  // Convert to data URL and create download link
  const dataURL = downloadCanvas.toDataURL("image/png");
  const link = document.createElement("a");
  link.download = `${noteName.value || "whiteboard"}.png`;
  link.href = dataURL;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  toast({
    title: "Image downloaded",
    description: "Whiteboard saved as PNG image",
    duration: 3000,
  });
};

const closeNote = async () => {
  if (isLoading.value) return;

  try {
    await saveToBackend();
    emit("note-closed");
  } catch (error) {
    console.error("Error saving note before close:", error);
    toast({
      title: "Save error",
      description: "Failed to save your whiteboard. Please try again.",
      variant: "destructive",
    });
  }
};

// Drawing the grid
const drawGrid = () => {
  if (!gridCanvas.value || !gridContext.value) return;

  // Clear the grid canvas
  gridContext.value.clearRect(
    0,
    0,
    gridCanvas.value.width,
    gridCanvas.value.height
  );

  if (gridType.value === "blank") return;

  const drawVertical = gridType.value !== "line";
  const drawHorizontal = gridType.value !== "blank";

  gridContext.value.strokeStyle = "#ccc";
  gridContext.value.lineWidth = 0.5;

  let vpt = [1, 0, 0, 1, 0, 0]; // Default transform
  let zoom = 1;

  if (canvas.value) {
    vpt = canvas.value.viewportTransform;
    zoom = canvas.value.getZoom();
  }

  const scaledGridSize = gridSize.value * zoom;
  const offsetX = vpt[4] || 0;
  const offsetY = vpt[5] || 0;

  // Calculate starting points based on offset
  const startX = ((offsetX % scaledGridSize) + scaledGridSize) % scaledGridSize;
  const startY = ((offsetY % scaledGridSize) + scaledGridSize) % scaledGridSize;

  // Draw vertical lines
  if (drawVertical) {
    for (let x = startX; x < gridCanvas.value.width; x += scaledGridSize) {
      gridContext.value.beginPath();
      gridContext.value.moveTo(x, 0);
      gridContext.value.lineTo(x, gridCanvas.value.height);
      gridContext.value.stroke();
    }
  }

  // Draw horizontal lines
  if (drawHorizontal) {
    for (let y = startY; y < gridCanvas.value.height; y += scaledGridSize) {
      gridContext.value.beginPath();
      gridContext.value.moveTo(0, y);
      gridContext.value.lineTo(gridCanvas.value.width, y);
      gridContext.value.stroke();
    }
  }
};

// Loading and saving whiteboard content
const loadFromBackend = async () => {
  try {
    isLoading.value = true;
    console.log("Loading whiteboard content with note id:", props.noteId);
    
    const response = await axios.post("/load", {
      id: props.noteId,
      operation: "content",
    });

    noteName.value = response.data.name || "Untitled Whiteboard";
    
    // Only set loading to false once, after everything is complete
    isLoading.value = false;
    // Use nextTick to ensure the DOM has updated before initializing
    await nextTick();
    
    // Initialize canvas first
    initializeCanvas();
    
    // Only continue if canvas initialization was successful
    if (canvas.value) {
      // Load the content if available
      if (response.data.content) {
        canvas.value.loadFromJSON(
          response.data.content,
          canvas.value.renderAll.bind(canvas.value)
        );
      }
  
      // Set viewport transform if available
      if (response.data.viewport) {
        const viewport = JSON.parse(response.data.viewport);
        canvas.value.setViewportTransform(viewport);
      }
  
      // Set background/grid settings
      if (response.data.background) {
        gridType.value = response.data.background;
        setGridType(gridType.value);
      }
    }
    
    // Now set loading to false ONCE at the end of the function
    isLoading.value = false;
    return true;
  } catch (error) {
    console.error("Error loading whiteboard:", error);
    toast({
      title: "Error loading whiteboard",
      description: "The whiteboard could not be loaded.",
      variant: "destructive",
    });
    
    isLoading.value = false;
    return false;
  }
};

const saveToBackend = async () => {
  if (isLoading.value || !canvas.value) {
    console.error("Canvas is still loading or not initialized, skipping save.");
    return false;
  }

  try {
    // Convert canvas to JSON string
    const json = JSON.stringify(canvas.value.toJSON());
    const viewport = JSON.stringify(canvas.value.viewportTransform);
    const name = noteName.value || "Untitled Whiteboard";

    // Update graph store with the name
    const graphStore = useGraphStore();
    graphStore.updateNoteName(props.noteId, name);

    await axios.post("/update", {
      operation: "content",
      id: props.noteId,
      content: json,
      viewport: viewport,
      background: gridType.value,
      name: name,
    });

    return true;
  } catch (error) {
    console.error("Error saving whiteboard:", error);
    return false;
  }
};

// Canvas initialization
const initializeCanvas = () => {
  const containerEl = document.getElementById("canvas-container");
  const fabricCanvasEl = document.getElementById("drawing-canvas");
  const gridCanvasEl = document.getElementById("grid-canvas");

  if (!fabricCanvasEl || !gridCanvasEl || !containerEl) {
    console.error("Canvas elements not found");
    return;
  }

  // Set container background
  containerEl.style.backgroundColor = backgroundColor.value;

  // Initialize grid canvas
  gridCanvas.value = gridCanvasEl;
  gridContext.value = gridCanvasEl.getContext("2d");

  // Check if we already have a canvas instance
  if (canvas.value) {
    console.warn("Canvas already initialized, disposing old instance");
    canvas.value.dispose();
    canvas.value = null;
  }

  try {
    // Initialize fabric.js canvas
    canvas.value = new fabric.Canvas(fabricCanvasEl, {
      width: containerEl.offsetWidth,
      height: containerEl.offsetHeight,
      backgroundColor: "transparent",
      selection: true,
    });

    // Disable object caching for better performance
    fabric.Object.prototype.objectCaching = false;

    // Make sure canvas is fully initialized before accessing freeDrawingBrush
    if (canvas.value && canvas.value.freeDrawingBrush) {
      // Set initial brush settings
      canvas.value.freeDrawingBrush.width = penWidth.value;
      canvas.value.freeDrawingBrush.color = penColor.value;
      canvas.value.isDrawingMode = currentMode.value === "draw";
    } else {
      console.warn("freeDrawingBrush not available, setting default pencil brush");
      canvas.value.isDrawingMode = true; // Enable drawing mode to initialize the brush
      // Now the brush should be created
      if (canvas.value.freeDrawingBrush) {
        canvas.value.freeDrawingBrush.width = penWidth.value;
        canvas.value.freeDrawingBrush.color = penColor.value;
      }
      canvas.value.isDrawingMode = currentMode.value === "draw";
    }

    // Set canvas dimensions
    resizeCanvas();

    // Draw the initial grid
    drawGrid();

    // Setup event listeners
    setupEventListeners();

    // Set up object selected event for quick access to colors
    canvas.value.on("selection:created", (opt) => {
      const obj = opt.selected[0];
      if (obj && obj.fill && obj.fill !== "transparent") {
        penColor.value = obj.fill;
      } else if (obj && obj.stroke) {
        penColor.value = obj.stroke;
      }
    });

    // Set up observers for canvas changes
    canvas.value.on("object:added", saveCanvasState);
    canvas.value.on("object:modified", saveCanvasState);
    canvas.value.on("object:removed", saveCanvasState);

    // Create initial save point
    saveCanvasState();
  } catch (error) {
    console.error("Error initializing canvas:", error);
    canvas.value = null; // Reset the canvas reference on error
  }
};

// Handle canvas resize
const resizeCanvas = () => {
  const containerEl = document.getElementById("canvas-container");
  if (!canvas.value || !containerEl || !gridCanvas.value) return;

  // Get dimensions from container
  const width = containerEl.offsetWidth;
  const height = containerEl.offsetHeight;

  // Update canvas dimensions
  canvas.value.setWidth(width);
  canvas.value.setHeight(height);

  // Update grid canvas dimensions
  gridCanvas.value.width = width;
  gridCanvas.value.height = height;

  // Redraw grid
  drawGrid();
};

// Setup event listeners for canvas interaction
const setupEventListeners = () => {
  if (!canvas.value) return;
  const canvasWrapper = canvas.value.wrapperEl;
  // Keyboard event handlers
  const handleKeyDown = (e) => {
    // Don't process keyboard events when editing text
    const activeObj = canvas.value.getActiveObject();
    if (activeObj && activeObj.type === "textbox" && activeObj.isEditing) {
      return;
    }

    if (e.key === "Delete" || e.key === "Backspace") {
      const activeObj = canvas.value.getActiveObject();
      if (activeObj) {
        e.preventDefault();
        deleteSelected();
      }
    } else if (e.key === "Escape") {
      e.preventDefault();
      closeNote();
    } else if (e.key === "Tab") {
      e.preventDefault();
      // Toggle between draw and text modes
      currentMode.value = currentMode.value === "draw" ? "type" : "draw";
      setMode(currentMode.value);
    } else if (e.key === "z" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      if (e.shiftKey) {
        redo();
      } else {
        undo();
      }
    } else if (e.key === "y" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      redo();
    } else if (e.key === "d") {
      canvas.value.discardActiveObject().renderAll();
    }
  };

  window.addEventListener("keydown", handleKeyDown);

  // Store reference for cleanup
  canvas.value.__keydownHandler = handleKeyDown;

  // Mouse events for panning
  let isPanning = false;
  let lastPosX = 0;
  let lastPosY = 0;

  canvas.value.on("mouse:down", function (opt) {
    const evt = opt.e;
    if (evt.button === 1) {
      // Middle mouse button
      isPanning = true;
      lastPosX = evt.clientX;
      lastPosY = evt.clientY;
      canvas.value.selection = false;
    }
  });

  canvas.value.on("mouse:move", function (opt) {
    if (isPanning) {
      const evt = opt.e;
      const deltaX = evt.clientX - lastPosX;
      const deltaY = evt.clientY - lastPosY;
      const vpt = canvas.value.viewportTransform;
      vpt[4] += deltaX;
      vpt[5] += deltaY;
      canvas.value.requestRenderAll();
      drawGrid();
      lastPosX = evt.clientX;
      lastPosY = evt.clientY;
    }
  });

  canvas.value.on("mouse:up", function () {
    isPanning = false;
    canvas.value.selection = true;
  });

  // Mouse wheel for zoom
  canvas.value.on("mouse:wheel", function (opt) {
    const evt = opt.e;

    // Check for Ctrl key for zooming
    if (evt.ctrlKey || evt.metaKey) {
      evt.preventDefault();
      const delta = evt.deltaY;
      let zoom = canvas.value.getZoom();
      zoom *= 0.999 ** delta;
      zoom = Math.min(Math.max(zoom, 0.1), 20);

      // Zoom relative to mouse position
      canvas.value.zoomToPoint({ x: evt.offsetX, y: evt.offsetY }, zoom);

      // Update grid
      drawGrid();
    } else {
      // Pan with wheel when not zooming
      const vpt = canvas.value.viewportTransform;
      vpt[4] -= evt.deltaX;
      vpt[5] -= evt.deltaY;
      canvas.value.requestRenderAll();
      drawGrid();
    }
    evt.preventDefault();
  });

  // Touch gestures with Hammer.js
  if (typeof Hammer !== "undefined") {
    const canvasWrapper = canvas.value.wrapperEl;
    const hammer = new Hammer(canvasWrapper);

    // Configure recognizers
    hammer.get("pan").set({ direction: Hammer.DIRECTION_ALL, pointers: 2 });
    hammer.get("pinch").set({ enable: true });
    hammer.get("press").set({ time: 0 });
    hammer.get("pinch").recognizeWith(hammer.get("pan"));

    // Variables for tracking pinch/zoom
    let lastScale = 1;
    let lastDeltaX = 0;
    let lastDeltaY = 0;

    // Pinch start handler
    hammer.on("pinchstart", function (e) {
      canvas.value._zoomStartScale = canvas.value.getZoom();
      lastScale = 1;

      // Disable drawing mode during gesture
      canvas.value.__tempDrawingMode = canvas.value.isDrawingMode;
      canvas.value.isDrawingMode = false;
    });

    // Pinch move handler
    hammer.on("pinchmove", function (e) {
      const scaleChange = e.scale / lastScale;
      lastScale = e.scale;

      let newZoom = canvas.value.getZoom() * scaleChange;
      newZoom = Math.min(Math.max(newZoom, 0.1), 20);

      const center = { x: e.center.x, y: e.center.y };
      canvas.value.zoomToPoint(center, newZoom);

      drawGrid();
      canvas.value.requestRenderAll();
    });

    // Pinch end handler
    hammer.on("pinchend", function () {
      lastScale = 1;

      // Restore drawing mode
      if (canvas.value.__tempDrawingMode !== undefined) {
        canvas.value.isDrawingMode = canvas.value.__tempDrawingMode;
        delete canvas.value.__tempDrawingMode;
      }
    });

    // Pan with two fingers
    hammer.on("panstart", function () {
      lastDeltaX = 0;
      lastDeltaY = 0;

      // Disable drawing mode during gesture
      canvas.value.__tempDrawingMode = canvas.value.isDrawingMode;
      canvas.value.isDrawingMode = false;
    });

    hammer.on("panmove", function (e) {
      const deltaX = e.deltaX - lastDeltaX;
      const deltaY = e.deltaY - lastDeltaY;

      lastDeltaX = e.deltaX;
      lastDeltaY = e.deltaY;

      const vpt = canvas.value.viewportTransform;
      vpt[4] += deltaX;
      vpt[5] += deltaY;

      canvas.value.requestRenderAll();
      drawGrid();
    });

    hammer.on("panend", function () {
      lastDeltaX = 0;
      lastDeltaY = 0;

      // Restore drawing mode
      if (canvas.value.__tempDrawingMode !== undefined) {
        canvas.value.isDrawingMode = canvas.value.__tempDrawingMode;
        delete canvas.value.__tempDrawingMode;
      }
    });

    // Store reference for cleanup
    canvas.value.__hammer = hammer;
  }

  // Prevent context menu on right-click
  canvasWrapper.addEventListener("contextmenu", function (e) {
    e.preventDefault();
  });

  // Handle window resize
  window.addEventListener("resize", resizeCanvas);

  // Store reference for cleanup
  canvas.value.__resizeHandler = resizeCanvas;

  // Sync grid with canvas changes
  canvas.value.on("after:render", function () {
    drawGrid();
  });
};

// Cleanup
const cleanup = () => {
  if (canvas.value) {
    // Remove event listeners
    if (canvas.value.__keydownHandler) {
      window.removeEventListener("keydown", canvas.value.__keydownHandler);
    }

    if (canvas.value.__resizeHandler) {
      window.removeEventListener("resize", canvas.value.__resizeHandler);
    }

    // Clean up Hammer instance
    if (canvas.value.__hammer) {
      canvas.value.__hammer.destroy();
    }

    // Dispose of canvas
    canvas.value.dispose();
    canvas.value = null;
  }
};

// Auto-save interval
const autoSaveInterval = ref(null);

// Lifecycle hooks
onMounted(async () => {
  await loadFromBackend();

  // Set up auto-save
  autoSaveInterval.value = setInterval(async () => {
    await saveToBackend();
  }, 60000); // Auto-save every minute
});

onBeforeUnmount(async () => {
  // Clear auto-save interval
  if (autoSaveInterval.value) {
    clearInterval(autoSaveInterval.value);
    autoSaveInterval.value = null;
  }

  // Save before unmounting
  if (!isLoading.value) {
    await saveToBackend();
  }

  // Clean up resources
  cleanup();
});

// Predefined colors
const colorOptions = [
  { name: "Black", value: "#000000" },
  { name: "Red", value: "#ff0000" },
  { name: "Blue", value: "#0000ff" },
  { name: "Green", value: "#00ff00" },
  { name: "Yellow", value: "#ffff00" },
  { name: "Purple", value: "#800080" },
  { name: "Orange", value: "#ffa500" },
  { name: "White", value: "#ffffff" },
];

// Background options
const backgroundOptions = [
  { name: "Blank", value: "blank" },
  { name: "Small Grid", value: "s__grid" },
  { name: "Medium Grid", value: "m_grid" },
  { name: "Large Grid", value: "l_grid" },
  { name: "Lines", value: "line" },
];

// Handle name changes
const updateNoteName = (name) => {
  noteName.value = name;
};

const handleEscapeKey = (event) => {
  if (event.key === "Escape") {
    closeNote();
  }
};

// Watch for mode changes
watch(currentMode, (newMode) => {
  setMode(newMode);
});

// Add global escape key handler
window.addEventListener("keydown", handleEscapeKey);
onBeforeUnmount(() => {
  window.removeEventListener("keydown", handleEscapeKey);
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

              <!-- Whiteboard name -->
              <input
                v-model="noteName"
                class="bg-transparent border-b border-gray-300 dark:border-gray-700 px-2 py-1 text-sm focus:outline-none focus:border-primary"
                placeholder="Untitled Whiteboard"
              />

              <Separator orientation="vertical" class="h-6 mx-1" />

              <!-- Drawing Mode -->
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="ghost"
                    size="sm"
                    class="flex gap-1 items-center"
                  >
                    <TextIcon v-if="currentMode === 'type'" class="h-4 w-4" />
                    <Pencil
                      v-else-if="currentMode === 'draw'"
                      class="h-4 w-4"
                    />
                    <Eraser
                      v-else-if="currentMode === 'eraser'"
                      class="h-4 w-4"
                    />
                    <span>Mode: {{ currentMode }}</span>
                    <ChevronDownIcon class="h-3 w-3 opacity-50" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuItem @click="setMode('draw')">
                    <Pencil class="h-4 w-4 mr-2" />
                    <span>Draw</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="setMode('type')">
                    <Type class="h-4 w-4 mr-2" />
                    <span>Type</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem @click="setMode('eraser')">
                    <Eraser class="h-4 w-4 mr-2" />
                    <span>Eraser</span>
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
                    <span>Add Shape</span>
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
                    <span>Add Text</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>

              <Separator orientation="vertical" class="h-6 mx-1" />

              <!-- Pen Color -->
              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    variant="ghost"
                    size="sm"
                    class="flex gap-1 items-center"
                  >
                    <div
                      class="w-4 h-4 rounded-full mr-1 border border-gray-300"
                      :style="{ backgroundColor: penColor }"
                    ></div>
                    <span>Color</span>
                    <ChevronDownIcon class="h-3 w-3 opacity-50" />
                  </Button>
                </PopoverTrigger>
                <PopoverContent class="w-64">
                  <div class="grid grid-cols-4 gap-2">
                    <Button
                      v-for="color in colorOptions"
                      :key="color.value"
                      variant="outline"
                      class="w-full h-8 p-0"
                      :class="{
                        'ring-2 ring-primary ring-offset-2':
                          penColor === color.value,
                      }"
                      :style="{ backgroundColor: color.value }"
                      @click="setPenColor(color.value)"
                    >
                      <span class="sr-only">{{ color.name }}</span>
                    </Button>
                  </div>
                  <div class="flex items-center gap-2 mt-2">
                    <label for="custom-color">Custom:</label>
                    <input
                      id="custom-color"
                      type="color"
                      v-model="penColor"
                      class="w-8 h-8 border-none p-0 bg-transparent"
                      @change="setPenColor(penColor)"
                    />
                    <span class="ml-2">{{ penColor }}</span>
                  </div>
                </PopoverContent>
              </Popover>

              <Separator orientation="vertical" class="h-6 mx-1" />

              <!-- Pen Width -->
              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    variant="ghost"
                    size="sm"
                    class="flex gap-1 items-center"
                  >
                    <Pencil class="h-4 w-4" />
                    <span>Width: {{ penWidth }}px</span>
                    <ChevronDownIcon class="h-3 w-3 opacity-50" />
                  </Button>
                </PopoverTrigger>
                <PopoverContent class="w-80">
                  <div class="grid gap-4">
                    <div class="flex items-center justify-between">
                      <label for="pen-width">Pen Width: {{ penWidth }}px</label>
                    </div>
                    <Slider
                      :model-value="penWidth"
                      :min="1"
                      :max="20"
                      :step="1"
                      class="w-full"
                      @update:model-value="setPenWidth"
                    />
                    <div class="flex gap-2 justify-between">
                      <Button
                        variant="outline"
                        size="sm"
                        @click="setPenWidth(1)"
                        :class="{ 'bg-primary/10': penWidth === 1 }"
                      >
                        Fine
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        @click="setPenWidth(3)"
                        :class="{ 'bg-primary/10': penWidth === 3 }"
                      >
                        Medium
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        @click="setPenWidth(8)"
                        :class="{ 'bg-primary/10': penWidth === 8 }"
                      >
                        Bold
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        @click="setPenWidth(16)"
                        :class="{ 'bg-primary/10': penWidth === 16 }"
                      >
                        Thick
                      </Button>
                    </div>
                  </div>
                </PopoverContent>
              </Popover>

              <Separator orientation="vertical" class="h-6 mx-1" />

              <!-- Background/Grid -->
              <Popover>
                <PopoverTrigger asChild>
                  <Button
                    variant="ghost"
                    size="sm"
                    class="flex gap-1 items-center"
                  >
                    <Grid class="h-4 w-4" />
                    <span>Grid</span>
                    <ChevronDownIcon class="h-3 w-3 opacity-50" />
                  </Button>
                </PopoverTrigger>
                <PopoverContent class="w-64">
                  <div class="grid gap-2">
                    <h4 class="font-medium">Grid Type</h4>
                    <div class="grid gap-2">
                      <Button
                        v-for="option in backgroundOptions"
                        :key="option.value"
                        variant="outline"
                        size="sm"
                        :class="{ 'bg-primary/10': gridType === option.value }"
                        @click="setGridType(option.value)"
                      >
                        {{ option.name }}
                      </Button>
                    </div>

                    <h4 class="font-medium mt-4">Background Color</h4>
                    <div class="grid grid-cols-4 gap-2">
                      <Button
                        v-for="color in colorOptions"
                        :key="color.value"
                        variant="outline"
                        class="w-full h-8 p-0"
                        :class="{
                          'ring-2 ring-primary ring-offset-2':
                            backgroundColor === color.value,
                        }"
                        :style="{ backgroundColor: color.value }"
                        @click="setBackgroundColor(color.value)"
                      >
                        <span class="sr-only">{{ color.name }}</span>
                      </Button>
                    </div>
                    <div class="flex items-center gap-2 mt-2">
                      <label for="bg-color">Custom:</label>
                      <input
                        id="bg-color"
                        type="color"
                        v-model="backgroundColor"
                        class="w-8 h-8 border-none p-0 bg-transparent"
                        @change="setBackgroundColor(backgroundColor)"
                      />
                      <span class="ml-2">{{ backgroundColor }}</span>
                    </div>
                  </div>
                </PopoverContent>
              </Popover>

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

              <Separator orientation="vertical" class="h-6 mx-1" />

              <!-- History Controls -->
              <div class="flex items-center gap-1">
                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        variant="ghost"
                        size="icon"
                        @click="undo"
                        :disabled="undoStack.length === 0"
                      >
                        <Undo class="h-4 w-4" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>Undo</TooltipContent>
                  </Tooltip>
                </TooltipProvider>

                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        variant="ghost"
                        size="icon"
                        @click="redo"
                        :disabled="redoStack.length === 0"
                      >
                        <Redo class="h-4 w-4" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>Redo</TooltipContent>
                  </Tooltip>
                </TooltipProvider>

                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        variant="ghost"
                        size="icon"
                        @click="downloadCanvas"
                      >
                        <Download class="h-4 w-4" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>Download as Image</TooltipContent>
                  </Tooltip>
                </TooltipProvider>

                <TooltipProvider>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <Button
                        variant="ghost"
                        size="icon"
                        class="text-red-600"
                        @click="clearCanvas"
                      >
                        <Trash2 class="h-4 w-4" />
                      </Button>
                    </TooltipTrigger>
                    <TooltipContent>Clear Canvas</TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="flex justify-center flex-1">
        <div
          id="canvas-container"
          class="canvas-container w-full max-w-[2000px] h-[calc(100vh-12rem)] overflow-hidden bg-primary-foreground rounded-lg border border-input m-4 relative"
          :style="{ backgroundColor: backgroundColor }"
        >
          <!-- Grid canvas (bottom layer) -->
          <canvas
            id="grid-canvas"
            class="absolute top-0 left-0 w-full h-full"
          ></canvas>
          <!-- Main canvas (top layer) -->
          <canvas
            id="drawing-canvas"
            class="absolute top-0 left-0 w-full h-full"
          ></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss">
/* Add custom styles for the color picker and canvas */
input[type="color"] {
  -webkit-appearance: none;
  border: none;
  width: 32px;
  height: 32px;
  cursor: pointer;
}
input[type="color"]::-webkit-color-swatch-wrapper {
  padding: 0;
}
input[type="color"]::-webkit-color-swatch {
  border: none;
  border-radius: 4px;
}

/* Canvas styling */
.canvas-container {
  position: relative;
  user-select: none;
}

/* Drawing canvas cursor styles */
canvas {
  cursor: crosshair;
}

.canvas-container.eraser canvas {
  cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="%23000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m7 21-4.3-4.3c-1-1-1-2.5 0-3.4l9.6-9.6c1-1 2.5-1 3.4 0l5.6 5.6c1 1 1 2.5 0 3.4L13 21"></path><path d="M22 21H7"></path><path d="m5 11 9 9"></path></svg>'),
    auto;
}

.canvas-container.text canvas {
  cursor: text;
}

/* Touch UI handling */
@media (pointer: coarse) {
  .canvas-container {
    touch-action: none; /* Prevent browser handling of touch gestures */
  }
}

/* Fabric.js specific styling */
.canvas-container .upper-canvas {
  position: absolute !important;
}

.canvas-container .lower-canvas {
  position: absolute !important;
}

/* Override a Fabric.js style that makes canvas margins weird */
.canvas-container canvas {
  margin: 0 !important;
  left: 0 !important;
  top: 0 !important;
}
</style>
