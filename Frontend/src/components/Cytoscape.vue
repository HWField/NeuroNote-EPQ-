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

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

import { Button } from "@/components/ui/button";
import { Input } from "./ui/input";
import {
  onMounted,
  onBeforeUnmount,
  onUnmounted,
  ref,
  watch,
  computed,
} from "vue";

import { useGraphStore } from "@/stores/useGraphStore";
import {
  Settings,
  CaseSensitive,
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
  Filter,
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
  externalFilters: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(["note-selected", "filters-changed"]);
const activeFilters = ref([]);

const loadState = () => {
  const tab = tabStore.getTab(props.tabId);
  const state = tab?.state || {};

  // Load filters from tab state if they exist
  if (state.filters && state.filters.length > 0) {
    activeFilters.value = state.filters;
  } else if (props.externalFilters && props.externalFilters.length > 0) {
    // Load from props if available
    activeFilters.value = [...props.externalFilters];
  }
  return state;
};

const dialogueOpen = ref(false);
const dialogueType = ref("");
const dialogueData = ref({});
let dialogueResolve = null;
let dialogueReject = null;
function openDialogue(type, options = {}) {
  // Reset data object for fresh input
  dialogueData.value = { ...options }; // insert any provided default values
  // Set dialog properties
  dialogueType.value = type;
  dialogueOpen.value = true;

  if (type === "newNote") {
    setTimeout(() => {
      const inputElement = document.querySelector("#name");
      if (inputElement) inputElement.focus();
    }, 50);
  }

  if (type === "filter") {
    setTimeout(() => {
      const inputElement = document.querySelector("#type");
      if (inputElement) inputElement.focus();
    }, 50);
  }

  if (type === "filter") {
    setTimeout(() => {
      const inputElement = document.querySelector("#value");
      if (inputElement) inputElement.focus();
    }, 50);
  }

  // Return a promise that will resolve when dialog is submitted
  return new Promise((resolve, reject) => {
    dialogueResolve = resolve;
    dialogueReject = reject;
  });
}
function submitDialogue() {
  if (dialogueType.value === "newNote") {
    // Set default name if empty
    if (!dialogueData.value.name || dialogueData.value.name.trim() === "") {
      dialogueData.value.name = "Untitled note";
    }

    // Set default type if not selected
    if (!dialogueData.value.type) {
      dialogueData.value.type = "document"; //later make a preference user can set
    }
  }

  // Resolve the promise with the current dialogueData
  if (dialogueResolve) {
    dialogueResolve(dialogueData.value);
  }
  closeDialogue();
}

function cancelDialogue() {
  // Reject the promise
  if (dialogueReject) {
    dialogueReject("Dialog cancelled");
  }
  closeDialogue();
}

function closeDialogue() {
  dialogueOpen.value = false;
  dialogueResolve = null;
  dialogueReject = null;
}
// Make sure your saveState function emits the filter changes
const saveState = () => {
  // Save filters to tab store
  tabStore.updateTabState(props.tabId, {
    filters: activeFilters.value,
  });

  // Emit to parent component
  emit("filters-changed", activeFilters.value);
};

function initializeCytoscape() {
  // Initialize Cytoscape
  let state = loadState();
  if (cy) {
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
          "overlay-opacity": 0, // Makes the overlay transparent
          ghost: "yes", // Disables ghost effect during drag

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
        selector: "node:selected",
        style: {
          "border-width": "8px",
        },
      },
      {
        selector: "node:active",
        style: {
          "border-width": "8px",
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
      cy.nodes().removeClass("highlighted");
      cy.edges().removeClass("highlighted");
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

  const sharedMenuConfig = {
    fillColor: "rgba(0, 0, 0, 0.75)", // the background colour of the menu
    activeFillColor: "rgba(1, 105, 217, 0.75)", // the colour used to indicate the selected command
    activePadding: 0, // additional size in pixels for the active command
    indicatorSize: 24, // the size in pixels of the pointer to the active command, will default to the node size if the node size is smaller than the indicator size,
    separatorWidth: 3, // the empty spacing in pixels between successive commands
    spotlightPadding: 4, // extra spacing in pixels between the element and the spotlight
    adaptativeNodeSpotlightRadius: true, // specify whether the spotlight radius should adapt to the node size
    minSpotlightRadius: 24, // the minimum radius in pixels of the spotlight (ignored for the node if adaptativeNodeSpotlightRadius is enabled but still used for the edge & background)
    maxSpotlightRadius: 38, // the maximum radius in pixels of the spotlight (ignored for the node if adaptativeNodeSpotlightRadius is enabled but still used for the edge & background)
    openMenuEvents: "cxttapstart taphold", // space-separated cytoscape events that will open the menu; only `cxttapstart` and/or `taphold` work here
    itemColor: "white", // the colour of text in the command's content
    itemTextShadowColor: "transparent", // the text shadow colour of the command's content
    zIndex: 9999, // the z-index of the ui div
    snapToCenter: true, // Add this option to keep menu centered
    atMouse: false, // draw menu at mouse position
    outsideMenuCancel: 50, // if set to a number, this will cancel the command if the pointer is released outside of the spotlight, padded by the number given
  };

  cy.cxtmenu({
    ...sharedMenuConfig,
    selector: 'node[type="tag"]',

    commands: [
      {
        content: "Rename",
        select: function (ele) {
          const node = ele;
          RenameNode(node);
        },
      },
      {
        content: "Add Filter",
        select: function (ele) {
          // searchByTag(ele.data("label"));
          addFilter(
            "tag",
            true,
            "tag",
            ele.data("label").toLowerCase(),
            ele.data("label")
   
          );
          //           async function addFilter(
          //   type,
          //   prefilledValue = false,
          //   preType,
          //   preValue,
          //   preLabel
          // )
        },
      },
      {
        content: "Delete",
        select: function (ele) {
          if (confirm("Are you sure you want to delete this node?")) {
            // Show loading indicator
            const loadingNode = ele;
            loadingNode.data(
              "originalColor",
              loadingNode.style("background-color")
            );
            loadingNode.style("background-color", "#ff8080"); // Light red to indicate deletion in progress

            graphStore
              .DeleteNode(ele.id())
              .then(() => {
                ele.remove();
                UpdateNodes();
              })
              .catch((error) => {
                console.error("Failed to delete node:", error);
                // Reset color on error
                loadingNode.style(
                  "background-color",
                  loadingNode.data("originalColor")
                );
                alert("Error deleting node. Please try again.");
              });
          }
        },
      },
    ],
  });

  cy.cxtmenu({
    ...sharedMenuConfig,
    selector: 'node[type="note"]',

    commands: [
      {
        content: "Rename",
        select: function (ele) {
          const node = ele;
          RenameNode(node);
        },
      },

      {
        content: "Delete",
        select: function (ele) {
          if (confirm("Are you sure you want to delete this node?")) {
            // Show loading indicator
            const loadingNode = ele;
            loadingNode.data(
              "originalColor",
              loadingNode.style("background-color")
            );
            loadingNode.style("background-color", "#ff8080"); // Light red to indicate deletion in progress

            graphStore
              .DeleteNode(ele.id())
              .then(() => {
                ele.remove();
                UpdateNodes();
              })
              .catch((error) => {
                console.error("Failed to delete node:", error);
                // Reset color on error
                loadingNode.style(
                  "background-color",
                  loadingNode.data("originalColor")
                );
                alert("Error deleting node. Please try again.");
              });
          }
        },
      },
    ],
  });

  // Add context menu for edges
  cy.cxtmenu({
    ...sharedMenuConfig,
    selector: "edge", // Apply to all edges
    commands: [
      {
        content: "Delete",
        select: function (ele) {
          useGraphStore().DeleteEdge(ele.data("source"), ele.data("target"));
          ele.remove();
          UpdateNodes();
        },
      },
    ],
    activeFillColor: "rgba(255, 0, 0, 0.75)", // Nice red color
    outsideMenuCancel: 0,
  });

  cy.on("tap", "node", (event) => {
    const node = event.target.data();
    if (node.type === "note") {
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

  document.addEventListener("keydown", HandlecyClick);
}

// function deleteNode(node) {
//   // Show loading indicator
//   node.data("originalColor", node.style("background-color"));
//   node.style("background-color", "#ff8080"); // Light red to indicate deletion in progress

//   graphStore
//     .DeleteNode(node.id())
//     .then(() => {
//       node.remove();
//       UpdateNodes();
//     })
//     .catch((error) => {
//       console.error("Failed to delete node:", error);
//       // Reset color on error
//       node.style("background-color", node.data("originalColor"));
//       alert("Error deleting node. Please try again.");
//     });
// }

function AddNodes(data) {
  const cyElements = [];
  const elements = data.elements; // Get the array from the elements property

  const addedNodes = new Set(); // Track added nodes
  const addedEdges = new Set(); // Track added edges to avoid duplicates
  let staticNodes = [];

  // First pass: Add all nodes
  elements.forEach((item) => {
    if (item.name && item.id) {
      const nodeId = `${item.type}_${item.id}`;

      // Skip if we've already added this node
      if (addedNodes.has(nodeId)) return;
      addedNodes.add(nodeId);

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
            width: 5,
            height: 5,
            x: position ? position.x : undefined,
            y: position ? position.y : undefined,
          },
          classes: position ? "static" : "",
        };
      } else if (item.type === "note") {
        nodeDefinition = {
          data: {
            id: nodeId,
            label: item.name,
            type: item.type,
            format: item.format,
            colour: "#1aed2c",
            width: 20,
            height: 20,
            x: position ? position.x : undefined,
            y: position ? position.y : undefined,
          },
          classes: position ? "static" : "",
        };
      } else {
        console.error("Unknown node type:", item.type);
        return;
      }

      cyElements.push(nodeDefinition);
    }
  });

  // Second pass: Add edges, but only if both source and target nodes exist
  elements.forEach((item) => {
    const sourceId = `${item.type}_${item.id}`;

    // Skip if the source node wasn't added
    if (!addedNodes.has(sourceId)) return;

    // Add edges for children (tag-to-tag)
    if (item.children && Array.isArray(item.children)) {
      item.children.forEach((childId) => {
        const targetId = `tag_${childId}`;
        const edgeId = `${sourceId}->${targetId}`;

        // Only add the edge if the target node exists and we haven't added this edge yet
        if (addedNodes.has(targetId) && !addedEdges.has(edgeId)) {
          cyElements.push({
            data: {
              id: edgeId,
              source: sourceId,
              target: targetId,
            },
          });
          addedEdges.add(edgeId);
        }
      });
    }

    // Add edges for notes (tag-to-note)
    if (item.notes && Array.isArray(item.notes)) {
      item.notes.forEach((noteId) => {
        const targetId = `note_${noteId}`;
        const edgeId = `${sourceId}->${targetId}`;

        // Only add the edge if the target node exists and we haven't added this edge yet
        if (addedNodes.has(targetId) && !addedEdges.has(edgeId)) {
          cyElements.push({
            data: {
              id: edgeId,
              source: sourceId,
              target: targetId,
            },
          });
          addedEdges.add(edgeId);
        }
      });
    }
  });

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
  console.log("running layout on:", effectors);
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
    randomize: true,
    nodeDimensionsIncludeLabels: true,
    fixedNodeConstraint: fixedNodeConstraints, // Cluster orphan nodes
    fit: true,
  }).run();

  // Step 2: Start cola layout with infinite animation after fcose completes
  setTimeout(() => {
    cy.one("layoutstop", runCola); // Use 'one' instead of 'on'
  }, 50);

  function runCola() {
    const currentColaLayout = cy.layout({
      name: "cola",
      infinite: true, // Infinite animation
      nodeSpacing: function (node) {
        return 5;
      }, // extra spacing around nodes
      animate: true,
      // Add these properties to handle label dimensions in physics
      nodeDimensionsIncludeLabels: true, // Important: include label dimensions
      avoidOverlap: true, // Force nodes not to overlap
      randomize: false, // Preserve fcose positions
      fit: false, // Do not fit the graph after layout
      refresh: 0, // number of ticks per frame; higher is faster but more jerky
      centerGraph: false,
      eles: null,
    });
    currentColaLayout.run();
  }
  // startSavingNodePositions();
}

function HandlecyClick(event) {
  if (
    //chcek if in a typing scenario (e.g. search bar)
    event.target.tagName === "INPUT" ||
    event.target.tagName === "TEXTAREA" ||

    dialogueOpen.value || // Don't trigger shortcuts when any dialog is open
    
    // If the SelectContent is open (search dropdown)
    document.querySelector('.select-content-open')
    
  ) {
    return;
  }

  if (event.key === "Delete" || event.key === "Backspace") {
    const selectedElements = cy.$("node:selected");
    const nodeCount = selectedElements.length;

    // No nodes selected - nothing to do
    if (nodeCount === 0) return;

    if (nodeCount === 1) {
      const node = selectedElements[0];
      if (confirm(`Are you sure you want to delete "${node.data("label")}"?`)) {
        const loadingNode = node;
        loadingNode.data(
          "originalColor",
          loadingNode.style("background-color")
        );
        loadingNode.style("background-color", "#ff8080"); // Light red to indicate deletion in progress

        graphStore
          .DeleteNode(node.id())
          .then(() => {
            node.remove();
            UpdateNodes();
          })
          .catch((error) => {
            console.error("Failed to delete node:", error);
            // Reset color on error
            loadingNode.style(
              "background-color",
              loadingNode.data("originalColor")
            );
            alert("Error deleting node. Please try again.");
          });
      }
    } else {
      if (confirm(`Delete ${nodeCount} selected nodes?`)) {
        if (
          confirm(
            `Are you REALLY sure you want to delete ${nodeCount} nodes? This cannot be undone.`
          )
        ) {
          // Process nodes in sequence to avoid backend conflicts
          selectedElements.forEach((ele) => {
            if (ele.isNode()) {
              // Show loading indicator
              const loadingNode = ele;
              loadingNode.data(
                "originalColor",
                loadingNode.style("background-color")
              );
              loadingNode.style("background-color", "#ff8080"); // Light red to indicate deletion in progress

              graphStore
                .DeleteNode(ele.id())
                .then(() => {
                  ele.remove();
                  UpdateNodes();
                })
                .catch((error) => {
                  console.error("Failed to delete node:", error);
                  // Reset color on error
                  loadingNode.style(
                    "background-color",
                    loadingNode.data("originalColor")
                  );
                  alert("Error deleting node. Please try again.");
                });
            }
          });
        }
      }
    }
  } else if (event.key === "n") {
    const selectedTag = cy.$('node[type="tag"]:selected');
    if (selectedTag.length > 0) {
      CreateNote("document");
    } else {
      CreateNote();
    }
  } else if (event.key === "t") {
    event.preventDefault();
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
    event.preventDefault(); // Stop default action
    const selectedNode = cy.$("node:selected");
    if (selectedNode.length === 1) {
      const currentName = selectedNode.data("label");
      let ele = selectedNode[0];
      const node = ele;
      RenameNode(selectedNode);
      // const newName = prompt("Enter new name for the node:", currentName);
      // if (newName !== null && newName.trim() !== "") {
      //   fetch("/update", {
      //     method: "POST",
      //     headers: {
      //       "Content-Type": "application/json",
      //     },
      //     body: JSON.stringify({
      //       operation: "rename",
      //       id: selectedNode.id(),
      //       name: newName,
      //       type: selectedNode.data("type"),
      //     }),
      //   })
      //     .then((response) => response.json())
      //     .then((data) => {
      //       if (data.status === "success") {
      //         selectedNode.data("label", newName);
      //       }
      //     })
      //     .catch((error) => {
      //       console.error("Error renaming node:", error);
      //     });
      // }
    }
  } else if (event.key === "i") {
    event.preventDefault();
    Spotlight();
  }
  else if (event.key === "f") {
    // stackableSearch();
    event.preventDefault();
    addFilter();
  } 
  // else if (event.key === "t") {
  //   searchByTag();
  // } else if (event.key === "g") {
  //   filterByNodeType();
  // }
  else if (event.key === "d") {
    const selectedNodes = cy.$("node:selected");
    searchByTag(selectedNodes.data("label"));
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
async function RenameNode(Node) {
  // Remove the handle if it's currently set
  removeHandle();
  const currentName = Node.data("label");
  const newName = (
    await openDialogue("rename", {
      name: currentName,
    })
  ).name;
  if (newName !== null && newName.trim() !== "") {
    graphStore
      .RenameNode(Node.id(), newName)
      .then((data) => {
        if (data.status === "success") {
          // Update the node name in Cytoscape
          Node.data("label", newName);
        } else {
          console.error("Failed to rename node:", data.message);
        }
      })
      .catch((error) => {
        console.error("Error renaming node:", error);
      });
  }
}

async function CreateNote(format) {
  let noteName = "";
  let noteFormat;
  let response;
  if (!format) {
    console.error("No format provided for CreateNote");
    response = (await openDialogue("newNote"));
  } else {
    console.error(" format provided for CreateNote");
    response = (await openDialogue("newNote", { type: format }));
  }
  noteName = response.name;
  noteFormat = response.type;
  console.errror
  console.error("noteName is", noteName);
  console.error("noteFormat is", noteFormat);
  if (!noteName || noteName.trim() === "") return;

  // Get all currently selected tags before creating the note
  const selectedTags = cy.$('node[type="tag"]:selected');

  axios
    .post("/create", {
      type: "note",
      name: noteName,
      format: noteFormat,
    })
    .then((response) => {
      AddNodes(response.data); // Call the updateGraph function with the new data
      useGraphStore().addNode(response.data);
      UpdateNodes();

      // Get the new note ID
      const newNoteId = "note_" + response.data.elements[0].id;

      // Create edges between all selected tags and the new note
      if (selectedTags.length > 0) {
        console.log(
          `Creating connections from ${selectedTags.length} selected tags to new note: ${newNoteId}`
        );

        // Process each selected tag
        let edgePromises = [];
        selectedTags.forEach((tagNode) => {
          const tagId = tagNode.id();

          // Create an edge between this tag and the new note
          const edgePromise = useGraphStore().CreateEdge(tagId, newNoteId);
          edgePromises.push(edgePromise);

          // Also add the edge to the Cytoscape instance immediately for visual feedback
          cy.add({
            group: "edges",
            data: {
              source: tagId,
              target: newNoteId,
            },
          });
        });

        // After all edge creation requests are complete
        Promise.all(edgePromises)
          .then(() => {
            UpdateNodes(); // Update the appearance of nodes
          })
          .catch((error) => {
            console.error(
              "Error creating one or more tag-note connections:",
              error
            );
          });
      }

      // Run layout focusing on the new note
      RunLayout(newNoteId);
    })
    .catch((error) => {
      console.error("Error creating note:", error);
    });
}

async function CreateTag() {
  const tagName = (await openDialogue("newTag")).name;

  if (!tagName || tagName.trim() === "") return;

  // Get all currently selected tags before creating the new tag
  const selectedTags = cy.$('node[type="tag"]:selected');

  axios
    .post("/create", {
      type: "tag",
      name: tagName,
    })
    .then((response) => {
      AddNodes(response.data); // Call the updateGraph function with the new data
      useGraphStore().addNode(response.data);
      UpdateNodes();

      // Get the new tag ID
      const newTagId = "tag_" + response.data.elements[0].id;

      // Create edges between all selected tags and the new tag (selected tags become parents)
      if (selectedTags.length > 0) {
        // Process each selected tag
        let edgePromises = [];
        selectedTags.forEach((parentTagNode) => {
          const parentTagId = parentTagNode.id();

          // Create an edge from parent tag to new tag
          const edgePromise = useGraphStore().CreateEdge(parentTagId, newTagId);
          edgePromises.push(edgePromise);

          // Also add the edge to the Cytoscape instance immediately for visual feedback
          cy.add({
            group: "edges",
            data: {
              source: parentTagId,
              target: newTagId,
            },
          });
        });

        // After all edge creation requests are complete
        Promise.all(edgePromises)
          .then(() => {
            UpdateNodes(); // Update the appearance of nodes
          })
          .catch((error) => {
            console.error(
              "Error creating one or more parent-child connections:",
              error
            );
          });
      }

      const newNode = cy.getElementById(newTagId);

      if (newNode) {
        newNode.select();
      }
      // Run layout focusing on the new tag
      RunLayout(newTagId);
    })
    .catch((error) => {
      console.error("Error creating tag:", error);
    });
}
const tags = computed(() => {
  return graphStore.elements
    .filter((item) => item.type === "tag")
    .map((tag) => ({
      id: tag.id,
      name: tag.name,
      value: `tag_${tag.id}`,
    }))
    .sort((a, b) => a.name.localeCompare(b.name));
});

const tagSearchQuery = ref("");

const filteredTags = computed(() => {
  if (!tagSearchQuery.value) return tags.value;
  const query = tagSearchQuery.value.toLowerCase();
  return tags.value.filter((tag) => tag.name.toLowerCase().includes(query));
});

async function addFilter(
  type,
  prefilledValue = false,
  preType,
  preValue,
  preLabel
) {
  let newFilter = {};

  if (prefilledValue) {
    console.error("prefilledValue is true", preType, preValue, preLabel);
    newFilter = {
      id: Date.now().toString(),
      type: preType, // Fix: use standard property names
      value: preValue,
      label: preLabel,
    };
  } else {
    const result = await openDialogue("filter", { type: type || null });
    if (result.type === "tag" && result.value) {
      // Extract the tag name from the selected value
      const tagname = result.value;
      console.error("detected tagname is", tagname);

        newFilter = {
          id: Date.now().toString(),
          type: "tag",
          value: tagname.toLowerCase(),
          label: `Tag: ${tagname}`,
        };
      
    } else if (result.type === "text" && result.value) {
      // Handle text filter
      newFilter = {
        id: Date.now().toString(),
        type: "text",
        value: result.value.toLowerCase(),
        label: `Contains: "${result.value}"`,
      };
    } else if (result.type === "type" && result.value) {
      // Handle node type filter
      newFilter = {
        id: Date.now().toString(),
        type: "nodeType",
        value: result.value.toLowerCase(),
        label: `Type: ${result.value}`,
      };
    }
  }

  activeFilters.value.push(newFilter);
  applyFilters();
  saveState();
}

function removeFilter(filterId) {
  activeFilters.value = activeFilters.value.filter((f) => f.id !== filterId);
  applyFilters(); // Reapply remaining filters
  saveState(); // Save to tab state
}

function clearAllFilters() {
  activeFilters.value = [];
  loadData(); // Reset to full graph
  saveState(); // Save to tab state
  RunLayout("all");
}

// Enhanced search that supports stacking
// function stackableSearch() {
//   const searchQuery = prompt("Enter search term:");
//   if (!searchQuery || searchQuery.trim() === "") return;

//   // Add as a text filter
//   addFilter("text", searchQuery.toLowerCase(), `Contains "${searchQuery}"`);
// }

// // Search by tag
// function searchByTag(tagName = null) {
//   if (tagName == null) {
//     tagName = prompt("Enter tag name to filter by:");
//   }
//   if (!tagName || tagName.trim() === "") return;

//   // Add as a tag filter
//   addFilter("tag", tagName.toLowerCase(), `Tag: ${tagName}`);
// }

// // Filter by node type
// function filterByNodeType() {
//   const nodeType = prompt("Enter node type (note/tag):");
//   if (!nodeType || !["note", "tag"].includes(nodeType.toLowerCase())) return;

//   // Add as a node type filter
//   addFilter("nodeType", nodeType.toLowerCase(), `Type: ${nodeType}`);
// }

function applyFilters() {
  // If no filters, show all data
  if (activeFilters.value.length === 0) {
    loadData();
    RunLayout("all");
    return;
  }

  // Get all elements from graph store
  const allElements = graphStore.elements;
  const processedNodeIds = new Set(); // Track which nodes we've already processed
  const processedEdgeIds = new Set(); // Track which edges we've already processed
  const resultElements = [];
  const highlightedNodeIds = new Set();

  // Helper function to get descendants
  function getDescendants(tag) {
    const descendants = [];
    if (tag.children && tag.children.length > 0) {
      tag.children.forEach((childId) => {
        const childTag = allElements.find(
          (el) => el.type === "tag" && el.id === childId
        );  
        if (childTag) {
          descendants.push(childTag);
          descendants.push(...getDescendants(childTag));
        }
      });
    }
    return descendants;
  }

  // Start with all elements
  let filteredElements = [...allElements];

  // Apply each filter sequentially, narrowing down results
  activeFilters.value.forEach((filter) => {
    if (filter.type === "text") {
      // Text search filter
      filteredElements = filteredElements.filter(
        (element) =>
          element.name && element.name.toLowerCase().includes(filter.value)
      );

      // Highlight matches for text search
      filteredElements.forEach((element) => {
        if (element.name && element.name.toLowerCase().includes(filter.value)) {
          highlightedNodeIds.add(`${element.type}_${element.id}`);
        }
      });
    } else if (filter.type === "tag") {
      // Find tags matching the filter
      const matchingTags = filteredElements.filter(
        (element) =>
          element.type === "tag" &&
          element.name &&
          element.name.toLowerCase().includes(filter.value)
      );

      // Highlight matching tags
      matchingTags.forEach((tag) => {
        highlightedNodeIds.add(`tag_${tag.id}`);
      });

      // Get all tag IDs that match
      const matchingTagIds = new Set(matchingTags.map((tag) => tag.id));

      // Include notes that have these tags
      const relatedNotes = allElements.filter(
        (element) =>
          element.type === "note" &&
          element.tags &&
          element.tags.some((tagId) => matchingTagIds.has(tagId))
      );

      // Helper function to get parent tags
      function getParents(tagId, allTags) {
        const parents = [];
        allTags.forEach((potentialParent) => {
          if (
            potentialParent.type === "tag" &&
            potentialParent.children &&
            potentialParent.children.includes(tagId)
          ) {
            parents.push(potentialParent);
            // Recursively get parents of parents
            const grandparents = getParents(potentialParent.id, allTags);
            parents.push(...grandparents);
          }
        });
        return parents;
      }

      // Include the matching tags, their ancestors, descendants, and related notes
      const includedTags = new Set();
      matchingTags.forEach((tag) => {
        includedTags.add(tag.id);

        // Add all descendants
        getDescendants(tag).forEach((descendant) => {
          includedTags.add(descendant.id);
        });

        // Add all parents/ancestors
        // const parents = getParents(tag.id, allElements);
        // parents.forEach(parent => {
        //   includedTags.add(parent.id);
        // });
      });

      // Get all notes connected to any tag in the hierarchy
      const allHierarchyNotes = allElements.filter(
        (element) =>
          element.type === "note" &&
          element.tags &&
          element.tags.some((tagId) => includedTags.has(tagId))
      );

      // Create new filtered set with matching tags, their ancestors, descendants, and related notes
      filteredElements = [
        ...allElements.filter(
          (element) => element.type === "tag" && includedTags.has(element.id)
        ),
        ...allHierarchyNotes,
      ];
    }else if (filter.type === "nodeType") {
      // Node type filter - only show nodes of the specified type
      filteredElements = filteredElements.filter(
        (element) => element.type === filter.value
      );
      
      // Highlight all nodes that match this type
      filteredElements.forEach((element) => {
        highlightedNodeIds.add(`${element.type}_${element.id}`);
      });
    }
  });

  // Now prepare elements for Cytoscape, ensuring all nodes needed for edges are included
  const nodesToAdd = new Map(); // Map of nodeId -> node

  // First, add all filtered nodes to our map
  filteredElements.forEach((element) => {
    const nodeId = `${element.type}_${element.id}`;
    nodesToAdd.set(nodeId, element);
  });

  // Convert to array for Cytoscape
  const cyElements = {
    elements: Array.from(nodesToAdd.values()),
  };

  // Display the filtered elements
  cy.elements().remove();
  AddNodes(cyElements);
  UpdateNodes();
  saveState();
  RunLayout("all");

  // Highlight nodes that match search queries
  // cy.ready(() => {
  //   highlightedNodeIds.forEach(nodeId => {
  //     const node = cy.getElementById(nodeId);
  //     if (node) {
  //       node.addClass("highlighted");
  //     }
  //   });

  // Center on highlighted nodes if any
  // if (highlightedNodeIds.size > 0) {
  //   cy.animate({
  //     fit: { eles: cy.$(".highlighted"), padding: 50 },
  //     duration: 500
  //   });
  // }
  // });

  // Save the updated filter state
}
function advancedSearch() {
  const searchQuery = prompt("Enter search term:");
  if (!searchQuery || searchQuery.trim() === "") return;

  const lowerCaseQuery = searchQuery.toLowerCase();

  // Get all elements from the graph store
  const storeElements = graphStore.elements;

  // Sets to track processed elements
  const processedTags = new Set();
  const processedNotes = new Set();
  const resultElements = [];
  const highlightedNodeIds = new Set(); // Track nodes that directly match the search query

  // Helper function to get all descendants of a tag
  function getDescendants(tag) {
    const descendants = [];
    if (tag.children && tag.children.length > 0) {
      tag.children.forEach((childId) => {
        const childTag = storeElements.find(
          (el) => el.type === "tag" && el.id === childId
        );
        if (childTag) {
          descendants.push(childTag);
          descendants.push(...getDescendants(childTag));
        }
      });
    }
    return descendants;
  }

  // Find tags matching the query
  const matchedTags = storeElements.filter(
    (element) =>
      element.type === "tag" &&
      element.name &&
      element.name.toLowerCase().includes(lowerCaseQuery)
  );

  // Process each matched tag and its descendants
  matchedTags.forEach((tag) => {
    // Mark this tag as directly matching the search query
    highlightedNodeIds.add(`tag_${tag.id}`);

    // Get all descendants of this tag
    const allRelatedTags = [tag, ...getDescendants(tag)];

    // Add each tag to the result set
    allRelatedTags.forEach((currentTag) => {
      if (!processedTags.has(currentTag.id)) {
        resultElements.push(currentTag);
        processedTags.add(currentTag.id);

        // Find and add all notes associated with this tag
        if (currentTag.notes && currentTag.notes.length > 0) {
          currentTag.notes.forEach((noteId) => {
            const note = storeElements.find(
              (el) => el.type === "note" && el.id === noteId
            );
            if (note && !processedNotes.has(note.id)) {
              resultElements.push(note);
              processedNotes.add(note.id);
            }
          });
        }
      }
    });
  });

  // Find notes matching the query
  const matchedNotes = storeElements.filter(
    (element) =>
      element.type === "note" &&
      element.name &&
      element.name.toLowerCase().includes(lowerCaseQuery)
  );

  // Add matching notes to the result set and highlight them
  matchedNotes.forEach((note) => {
    if (!processedNotes.has(note.id)) {
      resultElements.push(note);
      processedNotes.add(note.id);
      highlightedNodeIds.add(`note_${note.id}`);
    }
  });

  // If there are results, display them
  if (resultElements.length > 0) {
    cy.elements().remove(); // Clear the current graph
    AddNodes({ elements: resultElements }); // Add the filtered elements
    UpdateNodes();
    RunLayout("all");

    // Highlight the nodes that directly matched the search query
    // cy.ready(() => {
    //   highlightedNodeIds.forEach((nodeId) => {
    //     const node = cy.getElementById(nodeId);
    //     if (node) {
    //       node.addClass("highlighted");
    //     }
    //   });

    // Center the view on the highlighted nodes
    // const highlightedNodes = cy.$(".highlighted");
    // if (highlightedNodes.length > 0) {
    //   cy.animate({
    //     fit: { eles: highlightedNodes, padding: 500 },
    //     duration: 500
    //   });
    // }
    // });
  } else {
    alert("No matches found for: " + searchQuery);
  }
}

async function Spotlight() {
  const searchTerm = (await openDialogue("spotlight")).value;
  console.error("Spotlight search term:", searchTerm);
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
        padding: 10,
      },
      duration: 500,
    });
  }
}

function loadData() {
  let elements = graphStore.elements;
  AddNodes({ elements });
  UpdateNodes();
  // RunLayout("all");
}

onMounted(() => {
  console.log("Cytoscape mounted");
  initializeCytoscape();
  let state = loadState();
  loadData();
  applyFilters();
});

onUnmounted(() => {
  removeHandle();
  console.log("Cytoscape unmounted");
  if (cy) {
    cy.stop(); // Stop any ongoing layouts
    cy.off("layoutstop"); // Clean up listeners
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
  <Dialog :open="dialogueOpen" @update:open="(val) => !val && cancelDialogue()">
    <DialogContent>


      <!-- Rename dialog -->
      <div v-if="dialogueType === 'rename'">
        <DialogHeader>
          <DialogTitle>Rename Node</DialogTitle>
          <DialogDescription>Enter a new name for this node</DialogDescription>
        </DialogHeader>

        <div class="grid gap-4 py-4">
          <div class="flex flex-col space-y-2">
            <label for="name" class="text-sm font-medium"
              >Name:</label
            >
            <Input
              id="name"
              v-model="dialogueData.name"
              autofocus
              @keyup.enter="submitDialogue"
            />
          </div>
        </div>
      </div>

      <div v-if="dialogueType === 'newTag'">
        <DialogHeader>
          <DialogTitle>New Tag</DialogTitle>
          <DialogDescription>Enter a name for the Tag</DialogDescription>
        </DialogHeader>

        <div class="grid gap-4 py-4">
          <div class="flex flex-col space-y-2">
            <label for="name" class=" text-sm font-medium"
              >Name:</label
            >
            <Input
              id="name"
              v-model="dialogueData.name"

              autofocus
              @keyup.enter="submitDialogue"
            />
          </div>
        </div>
      </div>

      <div v-if="dialogueType === 'spotlight'">
        <DialogHeader>
          <DialogTitle>Spotlight</DialogTitle>
          <DialogDescription>Enter a search term</DialogDescription>
        </DialogHeader>

        <div class="grid gap-4 py-4">
          <div class="flex flex-col space-y-2">
            <label for="name" class=" text-sm font-medium"
              >Keyword:</label
            >
            <Input
              id="value"
              v-model="dialogueData.value"
              class="col-span-3"
              autofocus
              @keyup.enter="submitDialogue"
            />
          </div>
        </div>
      </div>

      <div v-if="dialogueType === 'newNote'">
        <DialogHeader>
          <DialogTitle>Name Note</DialogTitle>
          <DialogDescription>Enter a name for the note</DialogDescription>
        </DialogHeader>

        <div class="grid gap-4 py-4">
          <div class="flex flex-col space-y-2">
            <label for="name" class=" text-sm font-medium"
              >Name:</label
            >
            <Input
              id="name"
              v-model="dialogueData.name"
              class="col-span-3"
              autofocus
              placeholder="Untitled note"
              @keyup.enter="submitDialogue"
            />
            <label for="type" class=" text-sm font-medium"
              >Type:</label
            >
            <Select id="type" v-model="dialogueData.type">
              <SelectTrigger class="col-span-3">
                <SelectValue placeholder="Default" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectItem value="document"> Document </SelectItem>
                  <SelectItem value="whiteboard"> Whiteboard </SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>

      <div v-if="dialogueType === 'filter'">
        <DialogHeader>
          <DialogTitle>New Filter</DialogTitle>
          <DialogDescription>Select Filter type</DialogDescription>
        </DialogHeader>

        <div class="grid gap-4 py-4">
          <!-- Row 1: Filter Type Selection -->
          <div class="flex flex-col space-y-2">
            <label for="type" class=" text-sm font-medium"
              >Type:</label
            >
            <Select id="type" v-model="dialogueData.type" >
              <SelectTrigger class="col-span-3">
                <SelectValue placeholder="Choose filter type" />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <SelectItem value="text">Text Filter</SelectItem>
                  <SelectItem value="tag">Tag Filter</SelectItem>
                  <SelectItem value="type">Type Filter</SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
          </div>

          <!-- Row 2: Text Filter Input (conditional) -->
          <div
            v-if="dialogueData.type === 'text'"
            class="flex flex-col space-y-2"
          >
            <label for="textValue" class=" text-sm font-medium"
              >Keyword:</label
            >
            <Input
              id="textValue"
              v-model="dialogueData.value"
              class="col-span-3"
              autofocus
              @keyup.enter="submitDialogue"
            />
          </div>

          <!-- Row 3: Type Filter Input (conditional) -->
          <div
            v-if="dialogueData.type === 'type'"
            class="flex flex-col space-y-2"
          >
            <label for="value" class=" text-sm font-medium"
              >Type:</label
            >
            <Select id="value" v-model="dialogueData.value">
              <SelectTrigger class="col-span-3">
                <SelectValue placeholder="..." />
              </SelectTrigger>
              <SelectContent>
                <SelectGroup>
                  <!-- <SelectLabel>Fruits</SelectLabel> -->
                  <SelectItem value="tag"> Tag </SelectItem>
                  <SelectItem value="note"> Note </SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
          </div>

          <!-- Row 4: Tag Filter Selector (conditional) -->
          <div
            v-if="dialogueData.type === 'tag'"
            class="flex flex-col space-y-2"
          >
            <label for="tagSelector" class="text-sm font-medium"
              >Tag:</label
            >
            <div class="col-span-3">
              <Select id="tagSelector" v-model="dialogueData.value">
                <SelectTrigger>
                  <SelectValue placeholder="Select a tag" />
                </SelectTrigger>
                <SelectContent>
                  <div class="p-2">
                    <Input
                      v-model="tagSearchQuery"
                      placeholder="Search tags..."
                      class="mb-2 w-full"
                      @keydown.stop
                    />
                  </div>
                  <SelectGroup>
                    <SelectItem
                      v-for="tag in filteredTags"
                      :key="tag.id"
                      :value="tag.name"
                    >
                      {{ tag.name }}
                    </SelectItem>
                  </SelectGroup>
                </SelectContent>
              </Select>
            </div>
          </div>
        </div>
      </div>

      <DialogFooter>
        <Button variant="outline" @click="cancelDialogue">Cancel</Button>
        <Button type="submit" @click="submitDialogue">Submit</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>

  <!-- <div class="w-full h-full p-6"> -->
  <div class="editor w-full h-full overflow-y-auto">
    <div ref="navbarContainer" class="h-full w-full relative">
      <!-- Large toolbar -->

      <div  v-if="hasControls && isLargeNavbarVisible" class="flex justify-center absolute top-6 left-1/2 transform -translate-x-1/2 z-50 bg-primary-foreground p-3 shadow-lg rounded-lg space-x-2 max-w-max"
      >
        <DropdownMenu>
          <DropdownMenuTrigger as-child>
            <Button class="flex items-center">
              <Filter class="" />
              <span>Filter</span>
            </Button>
          </DropdownMenuTrigger>

          <DropdownMenuContent class="w-48 mt-2 shadow-lg rounded-lg">
            <DropdownMenuItem
              class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
              @click="addFilter((type = 'text'))"
            >
              <CaseSensitive class="w-5 h-5 text-gray-600" />
              <span>Filter by Name</span>
            </DropdownMenuItem>

            <DropdownMenuItem
              class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
              @click="addFilter((type = 'tag'))"
            >
              <Tag class="w-5 h-5 text-gray-600" />
              <span>Filter by Tag</span>
            </DropdownMenuItem>
            <DropdownMenuItem
              class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
              @click="addFilter((type = 'type'))"
            >
              <FileText class="w-5 h-5 text-gray-600" />
              <span>Filter by Type</span>
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem
              class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
              @click="clearAllFilters()"
            >
              <Eye class="w-5 h-5 text-gray-600" />
              <span>Show All</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        <Button @click="Spotlight()" class="flex items-center">
          <Search class="" />
          <span>Spotlight</span>
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
        <Filter></Filter>
        <span>Filter</span>
      </Button>
    </DropdownMenuTrigger>

    <DropdownMenuContent class="w-48 mt-2 shadow-lg rounded-lg">
      <DropdownMenuItem
        class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
        @click="addFilter('text')"
      >
        <CaseSensitive class="w-5 h-5 text-gray-600" />
        <span>Filter by Name</span>
      </DropdownMenuItem>

      <DropdownMenuItem
        class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
        @click="addFilter('tag')"
      >
        <Tag class="w-5 h-5 text-gray-600" />
        <span>Filter by Tag</span>
      </DropdownMenuItem>
      <DropdownMenuItem
        class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
        @click="addFilter('type')"
      >
        <FileText class="w-5 h-5 text-gray-600" />
        <span>Filter by Type</span>
      </DropdownMenuItem>
      <DropdownMenuSeparator />
      <DropdownMenuItem
        class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
        @click="clearAllFilters()"
      >
        <Eye class="w-5 h-5 text-gray-600" />
        <span>Show All</span>
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

  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button class="">
        <Ellipsis></Ellipsis>
        <span>More</span>
      </Button>
    </DropdownMenuTrigger>

    <DropdownMenuContent class="w-48 mt-2 shadow-lg rounded-lg">
      <DropdownMenuItem
        class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
        @click="Spotlight()"
      >
        <Search class="w-5 h-5 text-gray-600" />
        <span>Spotlight</span>
      </DropdownMenuItem>
      <DropdownMenuItem
        class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
        @click="centerGraph()"
      >
        <House class="w-5 h-5 text-gray-600" />
        <span>Center</span>
      </DropdownMenuItem>
      <DropdownMenuItem
        class="flex items-center space-x-2 p-2 hover:bg-gray-100 cursor-pointer"
        @click="ShuffleGraph()"
      >
        <Shuffle class="w-5 h-5 text-gray-600" />
        <span>Shuffle</span>
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</div>

      <!-- tagbar -->
      <div
        v-if="activeFilters.length > 0"
        class="flex flex-wrap gap-2 absolute top-20 left-1/2 transform -translate-x-1/2 z-50 bg-primary-foreground/80 backdrop-blur-sm p-3 shadow-lg rounded-lg max-w-max"
      >
        <div
          v-for="filter in activeFilters"
          :key="filter.id"
          class="flex items-center gap-1 px-2 py-1 rounded-md text-sm"
          :class="
            filter.type === 'tag'
              ? 'bg-blue-100 text-blue-800'
              : filter.type === 'text'
                ? 'bg-green-100 text-green-800'
                : filter.type === 'nodeType'
                  ? 'bg-purple-100 text-purple-800'
                  : 'bg-gray-100'
          "
        >
          <span v-if="filter.type === 'tag'">🏷️</span>
          <span v-else-if="filter.type === 'text'">🔍</span>
          <span v-else-if="filter.type === 'nodeType'">📌</span>
          <span>{{ filter.label }}</span>
          <button
            @click="removeFilter(filter.id)"
            class="ml-1 text-gray-500 hover:text-gray-700"
          >
            ×
          </button>
        </div>
        <button
          @click="clearAllFilters"
          class="text-xs text-gray-600 hover:text-gray-800 flex items-center"
        >
          Clear all
        </button>
      </div>

      <div id="cy" class="w-full h-full absolute"></div>
    </div>
  </div>
  <!-- </div> -->
</template>
