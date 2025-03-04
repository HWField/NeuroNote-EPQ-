import { defineStore } from "pinia";
import { ref } from "vue";
import axios from "../axios"; // Import the Axios instance
import { useUserStore } from "@/stores/useUserStore";

export const useGraphStore = defineStore("graphStore", () => {
  // **State: Holds global truth of the graph**
  const elements = ref([]); // All notes & tags as nodes

  // **Actions**
  async function fetchGraph() {
    if (useUserStore().isAuthenticated) {
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

  return { elements, fetchGraph, setGraph, updatePositions, resetGraph };
});
