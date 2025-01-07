<script setup>
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";

import { Button } from "@/components/ui/button";
import { Input } from "./ui/input";
import { onMounted, onBeforeUnmount, ref, watch } from "vue";
import cytoscape from "cytoscape";

const cyRef = ref(null); // Reference for Cytoscape instance
let cyInstance = null;

function initializeCytoscape() {
  const container = document.getElementById("cy");

  if (!container) {
    console.warn("Cytoscape container not found");
    return;
  }

  // Initialize Cytoscape
  cyInstance = cytoscape({
    container,
    elements: [
      // List of nodes and edges
      { data: { id: "a" } },
      { data: { id: "b" } },
      { data: { id: "c" } },
      { data: { id: "d" } },
      { data: { id: "e" } },
      { data: { source: "a", target: "b" } },
      { data: { source: "a", target: "c" } },
      { data: { source: "c", target: "d" } },
      { data: { source: "d", target: "e" } },
    ],

    style: [
      {
        selector: "node",
        style: {
          "background-color": "#0074D9",
          label: "data(id)",
          "text-valign": "center",
          "text-halign": "center",
          color: "#ffffff",
          "font-size": "10px",
        },
      },
      {
        selector: "edge",
        style: {
          width: 2,
          "line-color": "#B10DC9",
          "target-arrow-color": "#B10DC9",
          "target-arrow-shape": "triangle",
          "curve-style": "bezier",
        },
      },
    ],

    layout: {
      name: "grid",
      rows: 2,
    },
  });

  // Trigger layout recalculation after initialization
  cyInstance.layout({ name: "grid", rows: 2 }).run();
}

function destroyCytoscape() {
  if (cyInstance) {
    cyInstance.destroy();
    cyInstance = null;
  }
}

onMounted(() => {
  initializeCytoscape();

  // Listen for tab changes or size changes
  const resizeObserver = new ResizeObserver(() => {
    if (cyInstance) {
      cyInstance.resize();
      cyInstance.layout({ name: "grid", rows: 2 }).run();
    }
  });

  resizeObserver.observe(document.getElementById("cy"));
  cyRef.value = resizeObserver;
});

onBeforeUnmount(() => {
  destroyCytoscape();

  if (cyRef.value) {
    cyRef.value.disconnect();
    cyRef.value = null;
  }
});
</script>

<template>
  <ResizablePanelGroup direction="vertical">
    <ResizablePanel :default-size="80">
      <div id="cy" class="h-full w-full border-solid"></div>
    </ResizablePanel>

    <ResizableHandle with-handle="" />

    <ResizablePanel :default-size="20">
      <form id="searchForm">
        <Input
          type="text"
          id="searchInput"
          name="query"
          placeholder="Search..."
        />
        <Button type="submit">Search</Button>
      </form>
      <Button id="unlockAllButton">Unlock All</Button>
      <Button id="newNote">New Note</Button>
      <Button id="newTag">New Tag</Button>
      <Button id="logout">Logout</Button>

      <div class="form__field">
    <div class="form__label">
      <strong>Please choose a color:</strong>
    </div>
    <div class="form__input">
      <VSwatches v-model="color" popover-x="left"></VSwatches>
    </div>
  </div>
    </ResizablePanel>
  </ResizablePanelGroup>

</template>
