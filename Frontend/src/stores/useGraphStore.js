import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "../axios"; // Import the Axios instance
import { useUserStore } from "@/stores/useUserStore";

export const useGraphStore = defineStore("graphStore", () => {
  // **State: Holds global truth of the graph**
  const elements = ref([]); // All notes & tags as nodes

  // **Actions**
  async function fetchGraph() {
    // if (useUserStore().isAuthenticated) {
    console.error("Fetching graph data...");
    try {
      const response = await axios.post("/load", {
        operation: "graph",
      });
      console.log("Graph data:", response.data);
      setGraph(response.data);
    } catch (error) {
      console.error("Error fetching graph data:", error);
    }
  }

  function setGraph(data) {
    elements.value = data.elements;
  }

  function updatePositions(newPositions) {
    positions.value = { ...positions.value, ...newPositions };
  }

  function resetGraph() {
    elements.value = [];
  }

  function addNode(response) {
    console.error("---Adding node:", response);
    // Check if response has elements array
    if (response.elements && Array.isArray(response.elements)) {
      // Add each element from the response to the store
      response.elements.forEach((element) => {
        elements.value.push(element);
      });
    } else {
      console.error("Invalid node format:", response);
    }
  }
  function CreateEdge(source, target) {
    console.error("Creating edge between:", source, target);
    // const newEdge = {
    //   id: `e${elements.value.length + 1}`,
    //   source: source,
    //   target: target,
    // };
    // elements.value.push(newEdge);
  
    // Update the relationships in the frontend data model
    if (source.startsWith('tag_') && target.startsWith('tag_')) {
      // For tag-to-tag relationships (parent-child)
      const sourceNode = elements.value.find(el => el.id === parseInt(source.split('_')[1]));
      if (sourceNode) {
        // Ensure children array exists
        if (!sourceNode.children) sourceNode.children = [];
        // Add target to children if not already there
        const targetId = parseInt(target.split('_')[1]);
        if (!sourceNode.children.includes(targetId)) {
          sourceNode.children.push(targetId);
        }
      }
    } else if (source.startsWith('tag_') && target.startsWith('note_')) {
      // For tag-to-note relationships
      const targetNode = elements.value.find(el => el.id === parseInt(target.split('_')[1]));
      if (targetNode) {
        // Ensure tags array exists
        if (!targetNode.tags) targetNode.tags = [];
        // Add source to tags if not already there
        const sourceId = parseInt(source.split('_')[1]);
        if (!targetNode.tags.includes(sourceId)) {
          targetNode.tags.push(sourceId);
        }
      }
    }
  
    // Send to backend
    axios.post("/create", {
      type: "edge",
      source: source,
      target: target,
    });
  }

  function updateNoteName(noteId, newName) {
    const note = this.elements.find((el) => el.id === parseInt(noteId));
    if (note) {
      note.name = newName;
    }
  }

  // Update the tags of a note in the store
  function updateNoteTags(noteId, tagIds) {
    const note = this.elements.find((el) => el.id === parseInt(noteId));
    if (note) {
      note.tags = tagIds;
    }
  }

  return {
    elements,
    fetchGraph,
    setGraph,
    updatePositions,
    resetGraph,
    updateNoteName,
    updateNoteTags,
    addNode,
    CreateEdge,
  };
});
