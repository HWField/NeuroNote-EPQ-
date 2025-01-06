<script setup>
import { onMounted } from 'vue';


</script>

<template>
  <div id="toolbar" class="">
          <!-- Mode Toggle -->
          <label for="nameInput">Name:</label>
          <input type="text" id="nameInput" placeholder="note name" />

          <label for="modeToggle">Mode:</label>
          <select id="modeToggle">
            <option value="draw">Draw</option>
            <option value="text" selected>Text</option>
          </select>

          <!-- Add Shape -->

          <label for="addShape">Add Shape:</label>
          <select id="addShape">
            <option value="none">Select Shape</option>
            <option value="rectangle">Rectangle</option>
            <option value="circle">Circle</option>
            <option value="triangle">Triangle</option>
          </select>
          <button id="addShapeButton">Add</button>

          <button id="addTextButton">Add Text</button>

          <!-- Pen Settings -->
          <label for="penColor">Pen Color:</label>
          <input type="color" id="penColor" value="#000000" />
          <label for="penWidth">Pen Width:</label>

          <input type="number" id="penWidth" min="1" max="50" value="5" />

          <select id="Background">
            <option value="blank" selected>Blank</option>
            <option value="s__grid">Small Grid</option>
            <option value="m_grid">Medium Grid</option>
            <option value="l_grid">Large Grid</option>
            <option value="line">Lines</option>
          </select>

          <!-- Eraser -->
          <button id="deleteButton">Delete</button>

          <button id="deleteNoteButton">Delete Note</button>

          <!-- Close Button -->
          <button id="closeModal" class="close-button">Close</button>
        </div>

        <!-- Canvas -->
        <div id="canvas-container">
          <!-- Bottom grid canvas -->
          <canvas id="grid-canvas"></canvas>
          <!-- Top Fabric.js canvas for drawing -->
          <canvas id="fabricCanvas"></canvas>
        </div>
     
</template>