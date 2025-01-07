<script setup>
import { onMounted } from "vue";
import { Input } from "./ui/input";
import { Button } from "./ui/button";

import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from '@/components/ui/resizable'

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
</script>

<template>
  <ResizablePanelGroup direction="vertical">
    
    <ResizablePanel :default-size="80">
      <div id="canvas-container">
        <!-- Bottom grid canvas -->
        <canvas id="grid-canvas"></canvas>
        <!-- Top Fabric.js canvas for drawing -->
        <canvas id="fabricCanvas"></canvas>
      </div>
    </ResizablePanel>

    <ResizableHandle with-handle="" />

    <ResizablePanel :default-size="20">
      <div id="toolbar" style="display: flex; flex-direction: row; flex-wrap: wrap;">
        <!-- Mode Toggle -->
        <label for="nameInput">Name:</label>
        <Input type="text" id="nameInput" placeholder="note name" />

        <label for="modeToggle">Mode:</label>

        <Select id="modeToggle">
          <SelectTrigger>
        <SelectValue placeholder="Mode:" />
          </SelectTrigger>
          <SelectContent>
        <SelectGroup>
          <SelectLabel>Mode</SelectLabel>
          <SelectItem value="draw"> Draw </SelectItem>
          <SelectItem value="text"> Text </SelectItem>
        </SelectGroup>
          </SelectContent>
        </Select>

        <!-- Add Shape -->

        <label for="addShape">Add Shape:</label>

        <Select id="addShape">
          <SelectTrigger>
        <SelectValue placeholder="Add Shape:" />
          </SelectTrigger>
          <SelectContent>
        <SelectGroup>
          <SelectLabel>Shape</SelectLabel>
          <SelectItem value="none"> None </SelectItem>
          <SelectItem value="rectangle"> Rectangle </SelectItem>
          <SelectItem value="circle"> Circle </SelectItem>
          <SelectItem value="triangle"> Triangle </SelectItem>
        </SelectGroup>
          </SelectContent>
        </Select>

        <Button id="addShapeButton">Add</Button>

        <Button id="addTextButton">Add Text</Button>

        <!-- Pen Settings -->
        <label for="penColor">Pen Color:</label>
        <Input type="color" id="penColor" value="#000000" />
        <label for="penWidth">Pen Width:</label>

        <Input type="number" id="penWidth" min="1" max="50" />

        <Select id="Background">
          <SelectTrigger>
        <SelectValue placeholder="Background:" />
          </SelectTrigger>
          <SelectContent>
        <SelectGroup>
          <SelectLabel>Shape</SelectLabel>
          <SelectItem value="s__grid"> Small Grid </SelectItem>
          <SelectItem value="m_grid"> Medium Grid </SelectItem>
          <SelectItem value="l_grid"> Large Grid </SelectItem>
          <SelectItem value="line"> Lines </SelectItem>
        </SelectGroup>
          </SelectContent>
        </Select>

        <!-- Eraser -->
        <Button id="deleteButton">Delete</Button>

        <Button id="deleteNoteButton">Delete Note</Button>
      </div>
    </ResizablePanel>
  </ResizablePanelGroup>

</template>
