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

    try {
      const response = await axios.post("/load", {
        operation: "graph",
      });
 
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
  function RenameNode(nodeId, newName) {
    // Parse the nodeId to determine type and actual ID
    const [type, id] = nodeId.split('_');
    const numericId = parseInt(id);
    
    // Find the element in the store
    const element = elements.value.find(
      (el) => el.type === type && el.id === numericId
    );
    
    if (element) {
      // Update the name in the local store
      element.name = newName;
      
      // Send update to backend
      return axios.post('/update', {
        operation: 'rename',
        id: nodeId,
        name: newName
      })
      .then(response => {
      
        return response.data;
      })
      .catch(error => {
        console.error(`Error renaming node ${nodeId}:`, error);
        throw error;
      });
    } else {
      return Promise.reject(new Error(`Node ${nodeId} not found in store`));
    }
  }


  async function DeleteNode(nodeId) {
  
    
    const edgeDeletions = []; // Array to hold all deletion promises
    
    if (nodeId.startsWith("tag_")) {
      // Find tag-to-tag relationships (as source)
      const tagNode = elements.value.find(el => el.id === parseInt(nodeId.split("_")[1]) && el.type === "tag");
      if (tagNode && tagNode.children) {
        tagNode.children.forEach(childId => {
          edgeDeletions.push(DeleteEdge(nodeId, `tag_${childId}`));
        });
      }
      
      // Find tag-to-note relationships
      const tagNodeId = parseInt(nodeId.split("_")[1]);
      elements.value.filter(el => el.type === "note").forEach(note => {
        if (note.tags && note.tags.includes(tagNodeId)) {
          edgeDeletions.push(DeleteEdge(nodeId, `note_${note.id}`));
        }
      });
      
      // Find tag-to-tag relationships (as target)
      elements.value.filter(el => el.type === "tag").forEach(tag => {
        if (tag.children && tag.children.includes(tagNodeId)) {
          edgeDeletions.push(DeleteEdge(`tag_${tag.id}`, nodeId));
        }
      });
    } 
    
    else if (nodeId.startsWith("note_")) {
      // Find all tags connected to this note
      const noteNode = elements.value.find(el => el.id === parseInt(nodeId.split("_")[1]) && el.type === "note");
      if (noteNode && noteNode.tags) {
        noteNode.tags.forEach(tagId => {
          edgeDeletions.push(DeleteEdge(`tag_${tagId}`, nodeId));
        });
      }
    }
    
    // Wait for ALL edge deletions to complete before deleting the node
    try {
      await Promise.all(edgeDeletions);
      // Now that edges are deleted, delete the node
      return axios.post("/delete", {
        type: "node",
        id: nodeId
      })
      .then(response => {

        const nodeTypeId = nodeId.split('_');
      const nodeType = nodeTypeId[0];
      const nodeIdNumber = parseInt(nodeTypeId[1]);
      
      // Find and remove the node from elements array
      const nodeIndex = elements.value.findIndex(el => 
        el.type === nodeType && el.id === nodeIdNumber
      );
      
      if (nodeIndex !== -1) {
        elements.value.splice(nodeIndex, 1);
      }
      
        return response.data;
      })
      .catch(error => {
        console.error("Error deleting node:", error.response?.data || error.message);
        throw error;
      });
    } catch (error) {
      console.error("Error during edge deletion:", error);
      throw error;
    }
  }
  function CreateEdge(source, target) {
    

    // Update the relationships in the frontend data model
    if (source.startsWith("tag_") && target.startsWith("tag_")) {
      // For tag-to-tag relationships (parent-child)
      const sourceNode = elements.value.find(
        (el) => el.id === parseInt(source.split("_")[1])
      );
      if (sourceNode) {
        // Ensure children array exists
        if (!sourceNode.children) sourceNode.children = [];
        // Add target to children if not already there
        const targetId = parseInt(target.split("_")[1]);
        if (!sourceNode.children.includes(targetId)) {
          sourceNode.children.push(targetId);
        }
      }
    } else if (source.startsWith("tag_") && target.startsWith("note_")) {
      // For tag-to-note relationships
      const sourceTag = elements.value.find(
        (el) => el.id === parseInt(source.split("_")[1]));
      const targetNode = elements.value.find(
        (el) => el.id === parseInt(target.split("_")[1])
      );
      if (targetNode) {
        // Ensure tags array exists
        if (!targetNode.tags) targetNode.tags = [];
        // Add source to tags if not already there
        const sourceId = parseInt(source.split("_")[1]);
        if (!targetNode.tags.includes(sourceId)) {
          targetNode.tags.push(sourceId);
      
        }
      }
      // Update the tag with its note
      if (sourceTag) {
        if (!sourceTag.notes) sourceTag.notes = [];
        const targetId = parseInt(target.split("_")[1]);
        if (!sourceTag.notes.includes(targetId)) {
          sourceTag.notes.push(targetId);
     
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

  function DeleteEdge(source, target) {
   
  
    // Update the relationships in the frontend data model
    if (source.startsWith("tag_") && target.startsWith("tag_")) {
      // For tag-to-tag relationships (parent-child)
      const sourceNode = elements.value.find(
        (el) => el.id === parseInt(source.split("_")[1])
      );
      if (sourceNode && sourceNode.children) {
        // Remove target from children if it exists
        const targetId = parseInt(target.split("_")[1]);
        sourceNode.children = sourceNode.children.filter(id => id !== targetId);
    
      }
    } else if (source.startsWith("tag_") && target.startsWith("note_")) {
      // For tag-to-note relationships
      const sourceTag = elements.value.find(
        (el) => el.id === parseInt(source.split("_")[1])
      );
      const targetNode = elements.value.find(
        (el) => el.id === parseInt(target.split("_")[1])
      );
  
      // Remove tag from note
      if (targetNode && targetNode.tags) {
        const sourceId = parseInt(source.split("_")[1]);
        targetNode.tags = targetNode.tags.filter(id => id !== sourceId);
   
      }
  
      // Remove note from tag
      if (sourceTag && sourceTag.notes) {
        const targetId = parseInt(target.split("_")[1]);
        sourceTag.notes = sourceTag.notes.filter(id => id !== targetId);
      
      }
    }
  
    // Find and remove the actual edge element if it exists
    const edgeId = `e_${source}_${target}`;
    const edgeIndex = elements.value.findIndex(el => el.id === edgeId);
    if (edgeIndex !== -1) {
      elements.value.splice(edgeIndex, 1);
    }
  
    // Send to backend
    return axios.post("/delete", {
      type: "edge",
      source: source,
      target: target,
    })
    .then(response => {
    
      return response.data;
    })
    .catch(error => {
      console.error("Error deleting edge:", error);
      throw error; // Re-throw so it can be caught in DeleteNode
    });
  }

  function updateNoteName(noteId, newName) {
    const note = this.elements.find((el) => el.id === parseInt(noteId));
    if (note) {
      note.name = newName;
    }
  }
// Add this new function to the returned object in useGraphStore
function replaceNoteTags(noteId, tagIds) {
  const noteKey = `note_${noteId}`;
  const existingNote = elements.value.find(el => el.id === parseInt(noteId) && el.type === 'note');
  
  if (!existingNote) {
    console.error(`Note with id ${noteId} not found`);
    return;
  }
  
  // Step 1: Get existing tags for this note
  const existingTags = existingNote.tags || [];
  
  // Step 2: Remove all existing tag edges
  existingTags.forEach(tagId => {
    DeleteEdge(`tag_${tagId}`, noteKey);
  });
  
  // Step 3: Create new edges for each tag
  tagIds.forEach(tagId => {
    CreateEdge(`tag_${tagId}`, noteKey);
  });
  
  // Step 4: Update the in-memory note's tags
  // updateNoteTags(noteId, tagIds);
  
  // Step 5: Send the updated tags to the backend
  // axios.post("/update", {
  //   operation: "tags",
  //   id: noteId,
  //   tags: tagIds
  // }).catch(error => {
  //   console.error("Error updating note tags:", error);
  // });
}
  // Update the tags of a note in the store
  // function updateNoteTags(noteId, tagIds) {
  //   const note = this.elements.find((el) => el.id === parseInt(noteId));
  //   if (note) {
  //     note.tags = tagIds;
  //   }
  // }

  return {
    elements,
    fetchGraph,
    setGraph,
    updatePositions,
    resetGraph,
    updateNoteName,
    replaceNoteTags,
    addNode,
    RenameNode,
    DeleteNode,
    CreateEdge,
    DeleteEdge,
  };
});
