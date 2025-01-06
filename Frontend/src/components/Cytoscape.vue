<script setup>
import { onMounted } from 'vue';
import cytoscape from 'cytoscape';

function initializeCytoscape() {
  onMounted(() => {
    const cy = cytoscape({
      container: document.getElementById('cy'), // Reference to the div with id="cy"

      elements: [
        // List of nodes and edges
        { data: { id: 'a' } },
        { data: { id: 'b' } },
        { data: { id: 'c' } },
        { data: { id: 'd' } },
        { data: { id: 'e' } },
        { data: { source: 'a', target: 'b' } },
        { data: { source: 'a', target: 'c' } },
        { data: { source: 'c', target: 'd' } },
        { data: { source: 'd', target: 'e' } },
      ],

      style: [
        {
          selector: 'node',
          style: {
            'background-color': '#0074D9',
            label: 'data(id)',
            'text-valign': 'center',
            'text-halign': 'center',
            color: '#ffffff',
            'font-size': '10px',
          },
        },
        {
          selector: 'edge',
          style: {
            width: 2,
            'line-color': '#B10DC9',
            'target-arrow-color': '#B10DC9',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
          },
        },
      ],

      layout: {
        name: 'grid',
        rows: 2,
      },
    });

    // Add additional interactions or event listeners
    cy.on('tap', 'node', function (event) {
      const nodeId = event.target.id();
      console.log('Tapped on node:', nodeId);
    });
  });
}

initializeCytoscape();
</script>

<template>
  <h1>Second Brain Graph Views</h1>
  <div id="cy" style="height: 500px; width: 100%; border: 1px solid #ddd;"></div>
</template>