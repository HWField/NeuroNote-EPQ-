<script setup>
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";
import { Separator } from "@/components/ui/separator";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

import { Button } from "@/components/ui/button";
import { Input } from "./ui/input";
import { onMounted, onBeforeUnmount, onUnmounted, ref, watch } from "vue";

import { useGraphStore } from "@/stores/useGraphStore";
import {
  Settings,
  Bell,
  ChevronsUpDown,
  GalleryVerticalEnd,
  LogOut,
  MoreHorizontal,
  Plus,
  Sparkles,
  Search,
  Lock,
  Home,
  MessagesSquare,
  ChevronsDown,
  Shuffle,
  Tag,
  FileText,
  LayoutGrid,
  House,
  SeparatorVertical,
  Eye,
  Ellipsis,
} from "lucide-vue-next";
import { useTabStore } from "@/stores/useTabStore";
import axios from "../axios";
const tabStore = useTabStore();
const graphStore = useGraphStore();
let cy = null; // Reference for Cytoscape instance

const props = defineProps({
  tabId: Number,
  hasControls: {
    type: Boolean,
    default: true,
  },
  // tabType: String, // New property to identify the component type (e.g., 'cytoscape')
});

const emit = defineEmits(["note-selected"]);

const loadState = () => {
  const tab = tabStore.getTab(props.tabId);
  return tab?.state || {};
};

const saveState = () => {
  if (cy) {
    console.log("saving state");
    tabStore.updateTabState(props.tabId, cy.json());
  }
};

function initializeCytoscape() {
  // Initialize Cytoscape

  console.log("Initializing Cytoscape...");
  let state = loadState();
  console.log(state);

  if (cy) {
    console.log(
      "Destroying previous Cytoscape instance before reinitializing..."
    );
    cy.destroy();
    cy = null;
  }

  cy = cytoscape({
    boxSelectionEnabled: true,
    container: document.getElementById("cy"),
    elements: [],

    style: [
      {
        selector: "node",
        style: {
          "text-valign": "center",
          "text-halign": "center",
          // color: "#f44336",
          "text-outline-color": "#b3aae2",
          "text-outline-width": 2,
          "font-size": "5px",
          // label: "data(label)",
          "border-width": "2px",
          "border-opacity": 0.4,
          "transition-property":
            "border-color background-color border-width opacity width height", // Enable smooth transition for multiple properties
          "transition-duration": "0.3s", // Different transition durations for each property
          "transition-timing-function": "ease", // Different easing functions for each property
        },
      },
      {
        selector: 'node[type="tag"]',
        style: {
          "background-color": "data(colour)",
          width: "data(width)",
          height: "data(height)",
          label: "data(label)",
          "text-halign": "center",
          "text-valign": "center",
          color: "#fff",
          "font-size": "10px",
        },
      },
      {
        selector: 'node[type="note"]',
        style: {
          "background-color": "data(colour)",
          label: "data(label)",
          "text-halign": "center",
          "text-valign": "center",
          color: "#fff",
          "font-size": "8px",
          width: "data(width)",
          height: "data(height)",
        },
      },
      {
        selector: 'node[format="whiteboard"]',
        style: {
          shape: "triangle",
        },
      },
      {
        selector: 'node[format="document"]',
        style: {
          shape: "round-rectangle",
        },
      },
      {
        selector: "edge",
        style: {
          width: 2,
          "line-color": "#aaa",
          opacity: 0.1,
          "curve-style": "bezier",
          "target-arrow-shape": "triangle",
          "target-arrow-color": "#aaa",
          "arrow-scale": 1,
          "z-index": 0,
          "transition-property":
            "line-color target-arrow-color opacity arrow-scale", // Enable smooth transition for multiple properties
          "transition-duration": "0.3s", // Different transition durations for each property
          "transition-timing-function": "ease", // Different easing functions for each property
        },
      },
      {
        selector: "node:selected",
        style: {
          "border-color": "#f00",
        },
      },
      {
        selector: "node.static",
        style: {
          "border-color": "#FF69B4", // Faint pink color
        },
      },
      {
        selector: "node.highlighted",
        style: {
          "background-color": "#FFC300" /* Yellow background */,
          "border-color": "#FF5733", // Light red color
          "border-width": "10px",
          "z-index": 9999,
          "transition-property": "border-color background-color border-width", // Enable smooth transition for multiple properties
          "transition-duration": "0.3s", // Different transition durations for each property
          "transition-timing-function": "ease", // Different easing functions for each property
        },
      },
      {
        selector: "edge.highlighted",
        style: {
          "line-color": "#FF5733",
          "target-arrow-color": "#FF5733",
          "arrow-scale": 1.5,
          opacity: 0.8,
          "transition-property":
            "line-color target-arrow-color opacity arrow-scale", // Enable smooth transition for multiple properties
          "transition-duration": "0.3s", // Different transition durations for each property
          "transition-timing-function": "ease", // Different easing functions for each property
        },
      },

      {
        selector: ".eh-handle",
        style: {
          "background-color": "red",
          opacity: 1.0,
          width: 12,
          height: 12,
          shape: "ellipse",
          "overlay-opacity": 0,
          "border-width": 12, // makes the handle easier to hit
          "border-opacity": 0,
        },
      },

      {
        selector: ".eh-hover",
        style: {
          "background-color": "red",
        },
      },

      {
        selector: ".eh-source",
        style: {
          "border-width": 2,
          "border-color": "red",
        },
      },

      {
        selector: ".eh-target",
        style: {
          "border-width": 20,
          "border-color": "red",
        },
      },

      {
        selector: ".eh-preview, .eh-ghost-edge",
        style: {
          // 'background-color': 'red',
          "line-color": "red",
          "target-arrow-color": "red",
          "source-arrow-color": "red",
          opacity: 1.0,
        },
      },

      {
        selector: ".eh-ghost-edge.eh-preview-active",
        style: {
          opacity: 0,
        },
      },

      {
        selector: ".greyed-out",
        style: {
          "background-color": "#d3d3d3",
          opacity: 0.5,
        },
      },
    ],
    layout: {
      name: "preset",
    },
  });

  let popperEnabled = true;

  // example code for making your own handles -- customise events and presentation where fitting
  // var popper;
  var popperNode;
  var popper;
  var popperDiv;
  var started = false;

  function start() {
    eh.start(popperNode);
  }

  function stop() {
    eh.stop();
  }

  function setHandleOn(node) {
    if (started) {
      return;
    }

    removeHandle(); // rm old handle

    popperNode = node;

    popperDiv = document.createElement("div");
    popperDiv.classList.add("popper-handle");

    // Better event handling for both mouse and touch
    popperDiv.addEventListener("mousedown", function (e) {
      e.preventDefault();
      e.stopPropagation();
      start(e);
    });

    // Improved touch handling
    popperDiv.addEventListener(
      "touchstart",
      function (e) {
        e.preventDefault();
        e.stopPropagation();
        document.body.classList.add("eh-operation-in-progress");
        eh.start(popperNode);
      },
      { passive: false }
    );

    document.body.appendChild(popperDiv);

    popper = node.popper({
      content: popperDiv,
      popper: {
        placement: "top",
        modifiers: [
          {
            name: "offset",
            options: {
              offset: [0, -10],
            },
          },
        ],
      },
    });
    // Update the popper position on each frame
    const updatePopperPosition = () => {
      if (popper && !started) {
        popper.update();
        requestAnimationFrame(updatePopperPosition);
      }
    };

    requestAnimationFrame(updatePopperPosition);
  }

  function removeHandle() {
    if (popper) {
      popper.destroy();
      popper = null;
    }

    if (popperDiv) {
      document.body.removeChild(popperDiv);
      popperDiv = null;
    }

    popperNode = null;
  }
  window.removeHandle = removeHandle;

  cy.on("mouseover", "node[type='tag']", function (e) {
    setHandleOn(e.target);
  });
  cy.on("mouseout", "node", function (e) {
    removeHandle();
  });

  cy.on("grab", "node", function () {
    removeHandle();
  });

  cy.on("tap", function (e) {
    if (e.target === cy) {
      removeHandle();
      cy.elements().removeClass("greyed-out");
    } else if (e.target.isNode()) {
      setHandleOn(e.target);
    }
  });

  cy.on("zoom pan", function () {
    removeHandle();
  });

  window.addEventListener("mouseup", function (e) {
    stop();
  });

  cy.on("ehstart", function () {
    started = true;
  });

  cy.on("ehstop", function () {
    started = false;
  });

  // Prevent default behavior for touch events on the popper handle
  function start(e) {
    e.preventDefault();
    e.stopPropagation();
    eh.start(popperNode);
  }
  // function to control links between nodes if possible when trying to create edges
  function canConnectNodes(sourceNode, targetNode) {
    // Disallow loops
    if (sourceNode.same(targetNode)) {
      return false;
    }
    // Disallow edges if an edge already exists between the nodes in any direction
    if (sourceNode.edgesWith(targetNode).length > 0) {
      return false;
    }
    // If source is type 'note', target must be type 'note'
    if (sourceNode.data("type") === "note") {
      return false;
    }
    return true;
  }

  var eh = cy.edgehandles({
    canConnect: canConnectNodes,
    snap: true,
    snapThreshold: 5,
    snapFrequency: 15,
  });

  // Event listener for when edge handle is activated
  cy.on("ehstart", function (event, sourceNode) {
    cy.nodes().forEach(function (node) {
      // Exclude the source node itself
      if (!node.same(sourceNode) && !canConnectNodes(sourceNode, node)) {
        node.addClass("greyed-out");
      }
    });
  });

  // Event listener for when edge handle is completed
  cy.on("ehstop", function () {
    cy.nodes().removeClass("greyed-out");
  });

  cy.on("ehcomplete", function (event, sourceNode, targetNode, addedEdge) {
    useGraphStore().CreateEdge(sourceNode.id(), targetNode.id());
    UpdateNodes();
    // Remove the edge handle
    removeHandle();
  });

  cy.on("tap", "node", (event) => {
    const node = event.target.data();
    if (node.type === "note") {
      console.log("Note node selected:", node.id);
      removeHandle();
      emit("note-selected", node.id);
      // tabStore.openTab(node.id);
      // additional note-specific logic here, e.g., open a modal or display details
    }
  });

  cy.on("unselect", "node", function (event) {
    cy.nodes().removeClass("highlighted");
    cy.edges().removeClass("highlighted");
  });

  cy.on("select", 'node[type="tag"]', function (event) {
    const selectedNodes = cy.$("node:selected").map((node) => node);
    selectedNodes.forEach((node) => {
      if (node.data("type") === "tag") {
        const selectedNode = node; // The selected node
        const nodeId = selectedNode.id(); // ID of the selected node

        // Find child nodes and edges
        const childEdges = cy.edges(`[source = "${nodeId}"]`);
        const childNodes = childEdges.targets(); // Get the target nodes of those edges
        const selectedNodes = new Set();
        const selectedEdges = new Set();
        // Store original styles and animate in the new highlights
        childEdges.forEach((edge) => {
          selectedEdges.add(edge.id());
          edge.addClass("highlighted");
        });

        childNodes.forEach((node) => {
          selectedNodes.add(node.id());
          node.addClass("highlighted");
          // node.select();
        });
      }
    });
  });
  // cy.layout({
  //   name: "cola",
  //   infinite: true, // Infinite animation
  //   animate: true,
  //   randomize: false, // Preserve fcose positions
  //   fit: false, // Do not fit the graph after layout
  //   refresh: 0, // number of ticks per frame; higher is faster but more jerky
  //   centerGraph: false,
  //   eles: null,
  // }).run();

  // cy.zoom(state.zoom);
  // cy.pan(state.pan);

  document.addEventListener("keydown", HandlecyClick);
  // Step 2: Start cola layout with infinite animation after fcose completes
}

function AddNodes(data) {
  const cyElements = [];
  const elements = data.elements; // Get the array from the elements property

  const addedEdges = new Set(); // Track added edges to avoid duplicates
  let staticNodes = [];

  // Add nodes and edges
  elements.forEach((item) => {
    if (item.name && item.id) {
      const nodeId = `${item.type}_${item.id}`;
      let style = {};
      let position = undefined;

      if (item.data?.x !== null && item.data?.y !== null) {
        position = { x: item.data.x, y: item.data.y };
        staticNodes.push({ nodeId, position });
      }

      let nodeDefinition;
      if (item.type === "tag") {
        nodeDefinition = {
          data: {
            id: nodeId,
            label: item.name,
            type: item.type,
            colour: "red",
            width: 5, // Adjust size based on depth
            height: 5,
            x: position ? position.x : undefined,
            y: position ? position.y : undefined,
          },
          classes: position ? "static" : "", // Add 'static' class if position is set
        };
      } else if (item.type === "note") {
        nodeDefinition = {
          data: {
            id: nodeId,
            label: item.name,
            type: item.type,
            format: item.format,
            colour: "#1aed2c",
            width: 20, // Adjust size based on depth
            height: 20,
            x: position ? position.x : undefined,
            y: position ? position.y : undefined,
          },
          classes: position ? "static" : "", // Add 'static' class if position is set
        };
      } else {
        console.error("Unknown node type:", item.type);
        return;
      }

      cyElements.push(nodeDefinition);
    }

    // Add edges for children
    if (item.children && Array.isArray(item.children)) {
      item.children.forEach((childId) => {
        const edgeId = `${item.type}_${item.id}->tag_${childId}`;
        if (!addedEdges.has(edgeId)) {
          cyElements.push({
            data: {
              source: `${item.type}_${item.id}`, // Match node ID format
              target: `tag_${childId}`, // Since children are tags, use "tag_" + childId
            },
          });
          addedEdges.add(edgeId);
        }
      });
    }

    // Add edges for notes
    if (item.notes && Array.isArray(item.notes)) {
      item.notes.forEach((noteId) => {
        const edgeId = `${item.type}_${item.id}->note_${noteId}`;
        if (!addedEdges.has(edgeId)) {
          cyElements.push({
            data: {
              source: `${item.type}_${item.id}`, // Source is the tag
              target: `note_${noteId}`, // Target is the note
            },
          });
          addedEdges.add(edgeId);
        }
      });
    }
  });

  const fixedNodeConstraints = staticNodes.map((node) => ({
    nodeId: node.nodeId,
    position: node.position,
  }));

  cy.add(cyElements);
}
function UpdateNodes() {
  function getColorByDepth(depth) {
    const colors = [
      "#b3aae2", // Red for depth 0
      "#7cafd1", // Orange for depth 1
      "#bfd1e2", // Yellow for depth 2
      "#008000", // Green for depth 3
      "#0000FF", // Blue for depth 4
      "#4B0082", // Indigo for depth 5
      "#EE82EE", // Violet for depth 6
    ];
    // Return a color for the depth or a fallback if depth exceeds predefined colors
    return colors[depth] || "#808080"; // Grey for depths beyond the defined range
  }

  function getSizeByDepth(depth) {
    const size = [5, 4, 3, 2, 1];
    // Return a color for the depth or a fallback if depth exceeds predefined colors
    return size[depth] || 1; // Grey for depths beyond the defined range
  }

  function calculateDepth() {
    const nodes = cy.nodes();
    const edges = cy.edges();
    const depthMap = {}; // Stores the depth of each node
    const parentMap = {}; // Maps child nodes to their parents

    // Build a parent map from edges
    edges.forEach((edge) => {
      const sourceId = edge.data("source"); // Parent node
      const targetId = edge.data("target"); // Child node
      if (!parentMap[targetId]) {
        parentMap[targetId] = [];
      }
      parentMap[targetId].push(sourceId);
    });

    // Identify root nodes (nodes without parents)
    const roots = nodes
      .filter((node) => !parentMap[node.id()]) // Nodes not found in parentMap
      .map((node) => node.id());

    // Calculate depth using BFS starting from root nodes
    const queue = [];
    roots.forEach((root) => {
      queue.push({ id: root, depth: 0 });
      depthMap[root] = 0;
    });

    while (queue.length > 0) {
      const { id, depth } = queue.shift();

      // Find children of the current node from edges
      const children = edges
        .filter((edge) => edge.data("source") === id)
        .map((edge) => edge.data("target"));

      children.forEach((childId) => {
        // If depth is not yet calculated or this path is shorter, update it
        if (depthMap[childId] === undefined || depth + 1 < depthMap[childId]) {
          depthMap[childId] = depth + 1;
          queue.push({ id: childId, depth: depth + 1 });
        }
      });
    }

    return depthMap;
  }
  const depthMap = calculateDepth();
  cy.nodes().forEach((node) => {
    if (node.data("type") === "tag") {
      node.data({
        colour: getColorByDepth(depthMap[node.id()]),
        width: getSizeByDepth(depthMap[node.id()]) * 10,
        height: getSizeByDepth(depthMap[node.id()]) * 10,
      });
    }
  });
}
function RunLayout(effectors) {
  cy.stop(); // Stop any ongoing layouts
  cy.off("layoutstop");
  console.log("Running layout on nodes:", effectors);
  let fixedNodeConstraints = [];
  // this function will run the layout on only the nodes specified, all others will remain statitionary

  if (effectors == "all") {
    fixedNodeConstraints = cy
      .nodes()
      .map((node) => {
        const data = node.data();
        if (data.x !== undefined && data.y !== undefined) {
          return {
            nodeId: node.id(),
            position: { x: data.x, y: data.y },
          };
        }
      })
      .filter(Boolean);
  } else if (effectors == "none") {
    //all nodes are layed out
    fixedNodeConstraints = [];
  } else {
    //all nodes except those specified are layed out
    effectors = Array.isArray(effectors) ? effectors : [effectors];
    cy.nodes().forEach((node) => {
      fixedNodeConstraints.push({
        nodeId: node.id(),
        position: node.position(),
      });
    });

    fixedNodeConstraints = fixedNodeConstraints.filter(
      (constraint) =>
        !effectors.some((effector) => effector === constraint.nodeId)
    );
    //remove wanted nodes from fixedNodeConstraints
  }
  // Step 1: Run fcose to organize orphan nodes
  cy.layout({
    name: "fcose",
    animate: true,
    randomize: false,
    nodeDimensionsIncludeLabels: true,
    fixedNodeConstraint: fixedNodeConstraints, // Cluster orphan nodes
    fit: true,
  }).run();

  // Step 2: Start cola layout with infinite animation after fcose completes
  cy.on("layoutstop", runCola);

  function runCola() {
    const colaLayout = cy.layout({
      name: "cola",
      infinite: true, // Infinite animation
      nodeSpacing: function (node) {
        return 10;
      }, // extra spacing around nodes
      animate: true,

      randomize: false, // Preserve fcose positions
      fit: false, // Do not fit the graph after layout
      refresh: 0, // number of ticks per frame; higher is faster but more jerky
      centerGraph: false,
      eles: null,
    });
    colaLayout.run();
  }
  // startSavingNodePositions();
}

function HandlecyClick(event) {
  if (
    //chcek if in a typing scenario (e.g. search bar)
    event.target.tagName === "INPUT" ||
    event.target.tagName === "TEXTAREA"
  ) {
    return;
  }
  console.log("cytoscope key pressed", event.key);
  if (event.key === "Delete" || event.key === "Backspace") {
    const selectedElements = cy.$(":selected");
    selectedElements.forEach((ele) => {
      if (ele.isNode()) {
        fetch("/delete", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ type: "node", id: ele.id() }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "success") {
              ele.unselect();
              removeHandle();
              ele.remove();
              console.log("element deleted, updating");
              UpdateNodes();
            } else {
              console.error("Failed to delete node:", data.message);
            }
          })
          .catch((error) => {
            console.error("Error deleting node:", error);
          });
      } else if (ele.isEdge()) {
        fetch("/delete", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            type: "edge",
            source: ele.data("source"),
            target: ele.data("target"),
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "success") {
              ele.unselect();
              removeHandle();
              ele.remove();
              console.log("element deleted, updating");
              UpdateNodes();
            } else {
              console.error("Failed to delete edge:", data.message);
            }
          })
          .catch((error) => {
            console.error("Error deleting edge:", error);
          });
      }
    });
  } else if (event.key === "n") {
    const selectedTag = cy.$('node[type="tag"]:selected');
    if (selectedTag.length > 0) {
      CreateNote("document");
    } else {
      CreateNote("document");
    }
  } else if (event.key === "t") {
    const selectedTag = cy.$('node[type="tag"]:selected');
    if (selectedTag.length > 0) {
      CreateTag("child");
    } else {
      CreateTag("none");
    }
  } else if (event.key === "Enter") {
    // CreateTag('child');
  } else if ((event.ctrlKey || event.metaKey) && event.key === "s") {
    event.preventDefault();
    cy.nodes().forEach((node) => {
      sendNodePositionToBackend(node);
    });
  } else if (event.key === "s") {
    const selectedNodes = cy.$("node:selected").map((node) => node.id());
    if (selectedNodes.length > 0) {
      RunLayout(selectedNodes);
    } else {
      // RunLayout("all");
      RunLayout("none");
    }
  } else if (event.key === "h") {
    const selectedNodes = cy.$("node:selected").map((node) => node);
    selectedNodes.forEach((node) => {
      if (node.data("type") === "tag") {
        const selectedNode = node; // The selected node
        const nodeId = selectedNode.id(); // ID of the selected node

        // Find child nodes and edges
        const childEdges = cy.edges(`[source = "${nodeId}"]`);
        const childNodes = childEdges.targets(); // Get the target nodes of those edges
        const selectedNodes = new Set();
        const selectedEdges = new Set();
        // Store original styles and animate in the new highlights
        childEdges.forEach((edge) => {
          selectedEdges.add(edge.id());
          edge.addClass("highlighted");
        });

        childNodes.forEach((node) => {
          selectedNodes.add(node.id());
          node.addClass("highlighted");
          node.select();
        });
      }
    });
  } else if (event.key === "c") {
    centerGraph();
  } else if (event.key === "l") {
    const selectedNodes = cy.$("node:selected").map((node) => node);
    selectedNodes.forEach((node) => {
      sendNodePositionToBackend(node);
    });
  } else if (event.key === "u") {
    const selectedNodes = cy.$("node:selected");
    const selectedNodeIds = selectedNodes.map((node) => node);

    selectedNodeIds.forEach((node) => {
      fetch("/update", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ operation: "unlock", id: node.id() }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            // Remove the 'static' class from the node
            node.removeClass("static");
          } else {
            console.error(`Failed to unlock node ${node.id()}:`, data.message);
          }
        })
        .catch((error) => {
          console.error(`Error unlocking node ${node.id()}:`, error);
        });
    });
  } else if ((event.ctrlKey || event.metaKey) && event.key === "a") {
    event.preventDefault();
    cy.elements().select();
  } else if (event.key === "Escape") {
    event.preventDefault();

    cy.elements().unselect();
    cy.elements().forEach((ele) => {
      ele.removeClass("greyed-out");
    });
  } else if (event.key === "r") {
    const selectedNode = cy.$("node:selected");
    if (selectedNode.length === 1) {
      const currentName = selectedNode.data("label");
      const newName = prompt("Enter new name for the node:", currentName);
      if (newName !== null && newName.trim() !== "") {
        fetch("/update", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            operation: "rename",
            id: selectedNode.id(),
            name: newName,
            type: selectedNode.data("type"),
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === "success") {
              selectedNode.data("label", newName);
            }
          })
          .catch((error) => {
            console.error("Error renaming node:", error);
          });
      }
    }
  } else if (event.key === "f") {
    Spotlight();
  } else if (event.key === "d") {
    const selectedNodes = cy.$("node:selected");
    if (selectedNodes.length > 0) {
      const combinedLabels = selectedNodes
        .map((node) => node.data("label"))
        .join(", ");
      console.log("Combined Labels:", combinedLabels);
      fetch("http://127.0.0.1:8000/load", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          operation: "search",
          query: combinedLabels,
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          cy.elements().remove(); // Clear the graph
          AddNodes(data); // Call the updateGraph function with the new data
          UpdateNodes();
          RunLayout("all");
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    } else {
      fetch("http://127.0.0.1:8000/load", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ operation: "all" }),
      })
        .then((response) => response.json())
        .then((data) => {
          cy.elements().remove(); // Clear the graph
          AddNodes(data); // Call the updateGraph function with the new data
          UpdateNodes();
          RunLayout("all");
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    }
  }
}

function centerGraph() {
  cy.animate({ fit: { eles: cy.elements(), padding: 50 }, duration: 600 });
}

function ShuffleGraph() {
  {
    const selectedNodes = cy.$("node:selected").map((node) => node.id());
    if (selectedNodes.length > 0) {
      RunLayout(selectedNodes);
    } else {
      RunLayout("none");
    }
  }
}

function CreateNote(format) {
  //   const selectedTag = cy.$('node[type="tag"]:selected');
  //   let newNoteId = "";
  //   if (selectedTag.length > 0) {
  //     const noteName = prompt("Enter the name for the new Note:");
  //     if (noteName) {
  //       fetch("/create", {
  //         method: "POST",
  //         headers: {
  //           "Content-Type": "application/json",
  //         },
  //         body: JSON.stringify({ type: "note", name: noteName }),
  //       })
  //         .then((response) => response.json())
  //         .then((data) => {
  //           newNoteId = data.elements[0].id;

  //           console.log("new note id:", newNoteId);
  //           AddNodes(data); // Call the updateGraph function with the new data
  //           // UpdateNodes();
  //           // Get the id from the single element in the array
  //           // RunLayout("note_" + newNoteId); // Pass the id property of the single node
  //           const tagId = selectedTag.id(); // Get the id of the selected tag

  //           // Create an edge between the selected tag and the new note
  //           fetch("/create", {
  //             method: "POST",
  //             headers: {
  //               "Content-Type": "application/json",
  //             },
  //             body: JSON.stringify({
  //               type: "edge",
  //               source: tagId,
  //               target: "note_" + newNoteId,
  //             }),
  //           })
  //             .then((response) => response.json())
  //             .then((data) => {
  //               if (data.status === "success") {
  //                 cy.add({
  //                   group: "edges",
  //                   data: {
  //                     source: tagId,
  //                     target: "note_" + newNoteId,
  //                   },
  //                 });
  //                 UpdateNodes();
  //                 RunLayout("note_" + newNoteId); // Run layout for the new note
  //               } else {
  //                 console.error("Failed to create edge:", data.message);
  //               }
  //             })
  //             .catch((error) => {
  //               console.error("Error creating edge:", error);
  //             });
  //         })
  //         .catch((error) => {
  //           console.error("Error fetching data:", error);
  //         });
  //     }
  //   }
  // } else {
  // const noteName = prompt("Enter the name for the new note:");

  const noteName = prompt("Enter the name for the new Note:");
  axios
    .post("/create", {
      type: "note",
      name: noteName,
      format: format,
    })
    .then((response) => {
      AddNodes(response.data); // Call the updateGraph function with the new data
      useGraphStore().addNode(response.data);
      UpdateNodes();
      RunLayout("note_" + response.data.elements[0].id); // Pass the id property of the single node
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

function CreateTag() {
  const tagName = prompt("Enter the name for the new Tag:");
  axios
    .post("/create", {
      type: "tag",
      name: tagName,
    })
    .then((response) => {
      AddNodes(response.data); // Call the updateGraph function with the new data
      useGraphStore().addNode(response.data);
      UpdateNodes();
      RunLayout("tag_" + response.data.elements[0].id); // Pass the id property of the single node
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

function drillDown(ele) {
  axios
    .post("/load", {
      operation: "search",
      query: ele.data("label"),
    })
    .then((response) => {
      cy.elements().remove(); // Remove existing nodes
      AddNodes(response.data); // Update graph with new data
      UpdateNodes();
      RunLayout("all");
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

function Spotlight() {
  const searchTerm = prompt("Enter a search term:");
  if (!searchTerm || searchTerm.trim() === "") return;

  const lowerCaseSearchTerm = searchTerm.toLowerCase();

  // Reset any previous search state
  cy.elements().removeClass("greyed-out");
  cy.elements().unselect();

  // Track if we found any matches
  let foundMatches = false;

  // Search through nodes in the graph
  cy.nodes().forEach((node) => {
    if (
      node.data("label") &&
      node.data("label").toLowerCase().includes(lowerCaseSearchTerm)
    ) {
      node.select();
      foundMatches = true;
    } else {
      node.addClass("greyed-out");
    }
  });

  if (!foundMatches) {
    // If no matches in visible graph, search the entire store
    const storeElements = graphStore.elements;
    const storeMatches = storeElements.filter(
      (element) =>
        element.name && element.name.toLowerCase().includes(lowerCaseSearchTerm)
    );

    if (storeMatches.length > 0) {
      // Found matches in store but not in current view, offer to load them
      if (
        confirm(
          `Found ${storeMatches.length} matches in other parts of the graph. Load them?`
        )
      ) {
        // Clear current graph and load matches
        cy.elements().remove();

        // Create a data structure similar to what AddNodes expects
        const matchData = {
          elements: storeMatches,
        };

        AddNodes(matchData);
        UpdateNodes();
        RunLayout("all");
        return;
      }
    } else {
      alert("No matches found for: " + searchTerm);
      cy.elements().removeClass("greyed-out");
      return;
    }
  }

  // Center the view on the selected nodes
  const selectedNodes = cy.$("node:selected");
  if (selectedNodes.length > 0) {
    cy.animate({
      fit: {
        eles: selectedNodes,
        padding: 50,
      },
      duration: 500,
    });
  }
}

function loadData() {
  let elements = graphStore.elements;
  AddNodes({ elements });
  UpdateNodes();
  RunLayout("all");
}

onMounted(() => {
  console.log("Cytoscape mounted");

  initializeCytoscape();
  let state = loadState();
  //log to track changes in state that should be applied after loading data

  loadData();
});

onUnmounted(() => {
  removeHandle();
  console.log("Cytoscape unmounted");
  // if (cy && cy.elements().length > 0) {
  //   saveState();
  // }
  if (cy) {
    console.log("Destroying Cytoscape instance...");
    cy.stop(); // Stop any ongoing layouts
    cy.remove("*"); // Remove all elements from the graph
    cy.destroy(); // Completely destroy the instance
    cy = null; // Nullify reference to prevent memory leaks
  }

  document.removeEventListener("keydown", HandlecyClick);
});

const navbarContainer = ref(null);
const isLargeNavbarVisible = ref(true); // Controls visibility of the large navbar

// Resize observer
const handleResize = () => {
  if (navbarContainer.value) {
    const containerWidth = navbarContainer.value.offsetWidth;
    // Toggle navbar visibility based on container width
    isLargeNavbarVisible.value = containerWidth >= 600; // Adjust threshold as needed
  }
};

// Setup ResizeObserver
onMounted(() => {
  const observer = new ResizeObserver(handleResize);
  observer.observe(navbarContainer.value); // Observe the navbar container
  // Initial check
  handleResize();
});

// Cleanup observer on component unmount
onBeforeUnmount(() => {
  const observer = new ResizeObserver(handleResize);
  observer.disconnect();
});
</script>

<style>
.popper-handle {
  background-color: red;
  border-radius: 50%;
  width: 16px;
  height: 16px;
  text-align: center;
  color: white;
  cursor: pointer;
  position: absolute;
  z-index: 9999;
}

.eh-operation-in-progress {
  user-select: none !important;
  -webkit-user-select: none !important;
  -webkit-touch-callout: none !important;
  cursor: grabbing !important;
}
</style>
<template>
  <div ref="navbarContainer" class="h-full w-full relative">
    <!-- Large toolbar -->

    <div
      v-if="hasControls && isLargeNavbarVisible"
      class="flex justify-center absolute top-6 left-1/2 transform -translate-x-1/2 z-50 bg-primary-foreground p-3 shadow-lg rounded-lg space-x-2 max-w-max"
    >
      <Button class="flex items-center" @click="Spotlight()">
        <Search class="" />
        <span>Search</span>
      </Button>

      <Button class="flex items-center">
        <Lock class="" />
        <span>Lock</span>
      </Button>
      <!-- <Separator orientation="vertical"></Separator> -->
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <Button class="">
            <Plus></Plus>
            <span>New</span>
          </Button>
        </DropdownMenuTrigger>

        <DropdownMenuContent class="w-48 mt-2 shadow-lg rounded-lg">
          <DropdownMenuItem
            class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
            @click="CreateTag()"
          >
            <Tag class="w-5 h-5 text-gray-600" />
            <span>Tag</span>
          </DropdownMenuItem>
          <DropdownMenuItem
            class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
            @click="CreateNote('document')"
          >
            <FileText class="w-5 h-5 text-gray-600" />
            <span>Document</span>
          </DropdownMenuItem>
          <DropdownMenuItem
            class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
            @click="CreateNote('whiteboard')"
          >
            <LayoutGrid class="w-5 h-5 text-gray-600" />
            <span>Whiteboard</span>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      <!-- <Separator orientation="vertical"></Separator> -->

      <Button @click="centerGraph()"> <House></House> Center </Button>

      <Button @click="drillDown(cy.$('node:selected')[0])">
        <ChevronsDown></ChevronsDown> Drill
      </Button>

      <Button variant="destructive" @click="ShuffleGraph()">
        <Shuffle></Shuffle> Shuffle
      </Button>
    </div>

    <!-- Small toolbar -->
    <div
      v-else
      v-if="hasControls"
      class="flex justify-center absolute top-6 left-1/2 transform -translate-x-1/2 z-50 bg-primary-foreground p-3 shadow-lg rounded-lg space-x-2 max-w-max"
    >
      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <Button class="">
            <Eye></Eye>
            <span>View</span>
          </Button>
        </DropdownMenuTrigger>

        <DropdownMenuContent class="w-48 mt-2 shadow-lg rounded-lg">
          <DropdownMenuItem
            class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
          >
            <Shuffle class="w-5 h-5 text-gray-600" />
            <span>Shuffle</span>
          </DropdownMenuItem>
          <DropdownMenuItem
            class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
          >
            <ChevronsDown class="w-5 h-5 text-gray-600" />
            <span>Drill</span>
          </DropdownMenuItem>
          <DropdownMenuItem
            class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
          >
            <Home class="w-5 h-5 text-gray-600" />
            <span>Centre</span>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <Button class="">
            <Plus></Plus>
            <span>New</span>
          </Button>
        </DropdownMenuTrigger>

        <DropdownMenuContent class="w-48 mt-2 shadow-lg rounded-lg">
          <DropdownMenuItem
            class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
          >
            <Tag class="w-5 h-5 text-gray-600" />
            <span>Tag</span>
          </DropdownMenuItem>
          <DropdownMenuItem
            class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
          >
            <FileText class="w-5 h-5 text-gray-600" />
            <span>Docuement</span>
          </DropdownMenuItem>
          <DropdownMenuItem
            class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
          >
            <LayoutGrid class="w-5 h-5 text-gray-600" />
            <span>Whiteboard</span>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>

      <DropdownMenu>
        <DropdownMenuTrigger as-child>
          <Button class="">
            <Ellipsis></Ellipsis>
            <span>Options</span>
          </Button>
        </DropdownMenuTrigger>

        <DropdownMenuContent class="w-48 mt-2 shadow-lg rounded-lg">
          <DropdownMenuItem
            class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
          >
            <Lock class="w-5 h-5 text-gray-600" />
            <span>Lock</span>
          </DropdownMenuItem>

          <DropdownMenuItem
            class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
          >
            <Search class="w-5 h-5 text-gray-600" />
            <span>Search</span>
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>

    <div id="cy" class="w-full h-full absolute"></div>
  </div>
</template>
