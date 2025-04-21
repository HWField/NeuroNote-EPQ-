<template>
    <NodeViewWrapper class="whiteboard-embed">
      <div class="whiteboard-header">
        <h3>{{ node.attrs.name || 'Untitled Whiteboard' }}</h3>
        <Button variant="outline" size="sm" @click="openFullWhiteboard">
          <Pencil class="h-4 w-4 mr-1" /> Edit
        </Button>
      </div>
      <div 
        ref="canvasContainer" 
        class="canvas-container"
      >
        <!-- Grid canvas (bottom layer) -->
        <canvas
          ref="gridCanvas"
          class="absolute top-0 left-0 w-full h-full"
        ></canvas>
        <!-- Main canvas (top layer) -->
        <canvas
          ref="fabricCanvas"
          class="absolute top-0 left-0 w-full h-full"
        ></canvas>
      </div>
    </NodeViewWrapper>
  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  import { NodeViewWrapper } from '@tiptap/vue-3';
  import { useRouter } from 'vue-router';
  import * as fabric from 'fabric';
  import { Button } from '@/components/ui/button';
  import { Pencil } from 'lucide-vue-next';
  import axios from '@/axios.js';
  import { useToast } from '@/components/ui/toast/use-toast';
  
  const props = defineProps({
    editor: Object,
    node: Object,
    getPos: Function,
    updateAttributes: Function
  });
  
  const router = useRouter();
  const { toast } = useToast();
  const canvasContainer = ref(null);
  const fabricCanvas = ref(null);
  const gridCanvas = ref(null);
  let canvas = null;
  
  // Function to open the full whiteboard editor
  function openFullWhiteboard() {
    if (props.node.attrs.id) {
      const tabParams = {
        id: props.node.attrs.id,
        name: props.node.attrs.name || 'Untitled Whiteboard',
        type: 'whiteboard'
      };
      
      // You can adjust this to match your application's routing pattern
      router.push({
        name: 'whiteboard',
        params: { id: props.node.attrs.id },
        query: { tab: JSON.stringify(tabParams) }
      });
    } else {
      toast({
        title: "Error",
        description: "Could not open whiteboard: Missing ID",
        variant: "destructive"
      });
    }
  }
  
  // Initialize the view-only canvas
  function initializeViewCanvas() {
    if (!canvasContainer.value) return;
    
    const containerWidth = canvasContainer.value.clientWidth;
    const containerHeight = 500; // Fixed height
    
    // Initialize fabric canvas
    canvas = new fabric.Canvas(fabricCanvas.value, {
      width: containerWidth,
      height: containerHeight,
      selection: false,
      interactive: false
    });
    
    // Initialize grid canvas
    const gridCtx = gridCanvas.value.getContext('2d');
    gridCanvas.value.width = containerWidth;
    gridCanvas.value.height = containerHeight;
    
    // Set up pan functionality
    let isPanning = false;
    let lastPosX = 0;
    let lastPosY = 0;
    
    canvas.on('mouse:down', function(opt) {
      const evt = opt.e;
      isPanning = true;
      lastPosX = evt.clientX;
      lastPosY = evt.clientY;
      canvas.setCursor('grabbing');
    });
    
    canvas.on('mouse:move', function(opt) {
      if (isPanning) {
        const evt = opt.e;
        const deltaX = evt.clientX - lastPosX;
        const deltaY = evt.clientY - lastPosY;
        const vpt = canvas.viewportTransform;
        vpt[4] += deltaX;
        vpt[5] += deltaY;
        drawGrid(vpt[4], vpt[5], canvas.getZoom());
        lastPosX = evt.clientX;
        lastPosY = evt.clientY;
        canvas.requestRenderAll();
      }
    });
    
    canvas.on('mouse:up', function() {
      isPanning = false;
      canvas.setCursor('default');
    });
    
    canvas.on('mouse:wheel', function(opt) {
      const evt = opt.e;
      let zoom = canvas.getZoom();
      zoom *= 0.999 ** evt.deltaY;
      zoom = Math.min(Math.max(zoom, 0.1), 20);
      canvas.zoomToPoint({ x: evt.offsetX, y: evt.offsetY }, zoom);
      drawGrid(canvas.viewportTransform[4], canvas.viewportTransform[5], zoom);
      evt.preventDefault();
      canvas.requestRenderAll();
    });
    
    // Function to draw grid
    function drawGrid(offsetX = 0, offsetY = 0, zoom = 1) {
      if (!gridCtx) return;
      
      let gridSize = 20;
      let background = props.node.attrs.background || 'sGrid';
      let vertical = true;
      let horizontal = true;
      
      if (background === 'empty') {
        vertical = false;
        horizontal = false;
      } else if (background === 'sGrid') {
        gridSize = 20;
      } else if (background === 'mGrid') {
        gridSize = 40;
      } else if (background === 'lGrid') {
        gridSize = 60;
      } else if (background === 'line') {
        vertical = false;
        gridSize = 40;
      }
      
      gridCtx.clearRect(0, 0, gridCanvas.value.width, gridCanvas.value.height);
      gridCtx.strokeStyle = '#ccc';
      gridCtx.lineWidth = 0.5;
      
      const scaledGridSize = gridSize * zoom;
      const startX = ((offsetX % scaledGridSize) + scaledGridSize) % scaledGridSize;
      const startY = ((offsetY % scaledGridSize) + scaledGridSize) % scaledGridSize;
      
      if (vertical) {
        for (let x = startX; x < gridCanvas.value.width; x += scaledGridSize) {
          gridCtx.beginPath();
          gridCtx.moveTo(x, 0);
          gridCtx.lineTo(x, gridCanvas.value.height);
          gridCtx.stroke();
        }
      }
      
      if (horizontal) {
        for (let y = startY; y < gridCanvas.value.height; y += scaledGridSize) {
          gridCtx.beginPath();
          gridCtx.moveTo(0, y);
          gridCtx.lineTo(gridCanvas.value.width, y);
          gridCtx.stroke();
        }
      }
    }
    
    // Load whiteboard content
    loadWhiteboardContent();
  }
  
  // Load content from backend
  async function loadWhiteboardContent() {
    if (!props.node.attrs.id) return;
    
    try {
      const response = await axios.post('/load', {
        id: props.node.attrs.id,
        operation: 'content',
      });
      
      if (response.data.content) {
        // Disable all canvas interactions for objects (view-only mode)
        fabric.Object.prototype.selectable = false;
        fabric.Object.prototype.evented = false;
        
        canvas.loadFromJSON(response.data.content, function() {
          // Set viewport transform if available
          if (response.data.viewport) {
            try {
              const viewport = JSON.parse(response.data.viewport);
              canvas.setViewportTransform(viewport);
            } catch (e) {
              console.error('Error parsing viewport:', e);
            }
          }
          
          // Apply styling to paths for consistent appearance
          canvas.getObjects().forEach(obj => {
            if (obj.type === 'path' || obj.type === 'line' || obj.path) {
              obj.objectCaching = false;
              if (obj.strokeLineCap !== undefined) {
                obj.strokeLineCap = 'round';
                obj.strokeLineJoin = 'round';
              }
            }
          });
          
          // Update grid with current viewport state
          const vpt = canvas.viewportTransform;
          drawGrid(vpt[4], vpt[5], canvas.getZoom());
          
          canvas.requestRenderAll();
        });
      }
    } catch (error) {
      console.error('Error loading whiteboard:', error);
    }
  }
  
  // Clean up resources when component is destroyed
  onBeforeUnmount(() => {
    if (canvas) {
      canvas.dispose();
    }
  });
  
  // Initialize canvas when component is mounted
  onMounted(() => {
    // Wait for DOM to be ready
    setTimeout(() => {
      initializeViewCanvas();
    }, 0);
    
    // Update canvas size when window resizes
    const handleResize = () => {
      if (canvas && canvasContainer.value) {
        const width = canvasContainer.value.clientWidth;
        canvas.setWidth(width);
        gridCanvas.value.width = width;
        canvas.requestRenderAll();
        const vpt = canvas.viewportTransform;
        drawGrid(vpt[4], vpt[5], canvas.getZoom());
      }
    };
    
    window.addEventListener('resize', handleResize);
    
    onBeforeUnmount(() => {
      window.removeEventListener('resize', handleResize);
    });
  });
  </script>
  
  <style>
  .whiteboard-embed {
    margin: 1.5rem 0;
    border-radius: 0.5rem;
    overflow: hidden;
    border: 1px solid #e2e8f0;
  }
  
  .whiteboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem 1rem;
    background-color: rgba(106, 0, 245, 0.05);
    border-bottom: 1px solid #e2e8f0;
  }
  
  .whiteboard-header h3 {
    margin: 0;
    font-size: 1rem;
    color: #6a00f5;
  }
  
  .canvas-container {
    position: relative;
    width: 100%;
    height: 500px;
    cursor: grab;
    background-color: white;
  }
  
  .canvas-container:active {
    cursor: grabbing;
  }
  
  .canvas-container canvas {
    position: absolute;
    top: 0;
    left: 0;
  }
  </style>