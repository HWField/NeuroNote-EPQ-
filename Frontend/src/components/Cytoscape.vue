<script setup>
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";

import { Button } from "@/components/ui/button";
import { Input } from "./ui/input";
import { onMounted, onBeforeUnmount, ref, watch } from "vue";

import axios from '../axios';

const cyRef = ref(null); // Reference for Cytoscape instance
let cy = null;

function initializeCytoscape() {
  // Initialize Cytoscape
  const cyElements = [];
  cy = cytoscape({
    boxSelectionEnabled: true,
    container: document.getElementById("cy"),
    elements: cyElements,
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
          shape: "round-rectangle",
        },
      },
      {
        selector: "edge",
        style: {
          width: 2,
          "line-color": "#aaa",
          "curve-style": "bezier",
          "target-arrow-shape": "triangle",
          "target-arrow-color": "#aaa",
          "arrow-scale": 1,

          "transition-property": "line-color target-arrow-color arrow-scale", // Enable smooth transition for multiple properties
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

          "transition-property": "line-color target-arrow-color arrow-scale", // Enable smooth transition for multiple properties
          "transition-duration": "0.3s", // Different transition durations for each property
          "transition-timing-function": "ease", // Different easing functions for each property
        },
      },

      {
        selector: ".eh-handle",
        style: {
          "background-color": "red",
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

    popperDiv.addEventListener("mousedown", start);
    popperDiv.addEventListener("touchstart", start);
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

  cy.on("mouseover", "node", function (e) {
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
    if (
      sourceNode.data("type") === "note" &&
      targetNode.data("type") !== "note"
    ) {
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
    // Send POST request to the backend
    fetch("/create", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        type: "edge",
        source: sourceNode.id(),
        target: targetNode.id(),
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          UpdateNodes();
          //later make space to update node colours
        } else {
          console.error("Failed to create edge:", data.message);
          // Optionally, remove the edge if creation failed
          addedEdge.remove();
        }
      })
      .catch((error) => {
        console.error("Error creating edge:", error);
        // Optionally, remove the edge if there was an error
        addedEdge.remove();
      });
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
    atMouse: false, // draw menu at mouse position
    outsideMenuCancel: 50, // if set to a number, this will cancel the command if the pointer is released outside of the spotlight, padded by the number given
  };

  cy.cxtmenu({
    ...sharedMenuConfig,
    selector: "node", // Apply to all nodes
    commands: [
      {
        content: "Edit",
        select: function (ele) {
          const noteNode = ele;
          const noteId = noteNode.id();
          const noteContent = noteNode.data("label");
        },
      },
      {
        content: "Drill Down",
        select: function (ele) {
          fetch("http://127.0.0.1:8000/load", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              operation: "search",
              query: ele.data("label"),
            }),
          })
            .then((response) => response.json())
            .then((data) => {
              cy.elements().remove(); // Remove existing nodes
              AddNodes(data); // Call the updateGraph function with the new data
              UpdateNodes();
              RunLayout("all");
            })
            .catch((error) => {
              console.error("Error fetching data:", error);
            });
        },
      },
      {
        content: "Unlock",
        select: function (ele) {
          fetch("/update", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ operation: "unlock", id: ele.id() }),
          });
          ele.removeClass("static");
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
          const edgeData = {
            id: ele.id(), // Edge ID
            source: ele.data("source"), // Source node ID
            target: ele.data("target"), // Target node ID
          };

          // Send DELETE request to the backend
          fetch("/delete", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              type: "edge",
              source: ele.data("source"),
              target: ele.data("target"),
            }), // Pass edge details in the body
          })
            .then((response) => {
              if (response.ok) {
                ele.remove(); // Remove edge from the Cytoscape graph
                UpdateNodes();
              } else {
                return response.json().then((err) => {
                  console.error(`Failed to delete edge: ${err.message}`);
                  alert(`Error: ${err.message}`);
                });
              }
            })
            .catch((error) => {
              console.error("Error deleting edge:", error);
              alert("An error occurred while deleting the edge.");
            });
        },
      },
    ],
    activeFillColor: "rgba(255, 0, 0, 0.75)", // Nice red color
    outsideMenuCancel: 0,
  });

  const selectedNodes = new Set();
  const selectedEdges = new Set();
  // cy.on("select", 'node[type="tag"]', function (event) {
  //   const selectedNode = event.target; // The selected node
  //   const nodeId = selectedNode.id(); // ID of the selected node

  //   // Find child nodes and edges
  //   const childEdges = cy.edges(`[source = "${nodeId}"]`);
  //   const childNodes = childEdges.targets(); // Get the target nodes of those edges

  //   // Store original styles and animate in the new highlights
  //   childEdges.forEach((edge) => {
  //     selectedEdges.add(edge.id());
  //     edge.addClass("highlighted");
  //   });

  //   childNodes.forEach((node) => {
  //     selectedNodes.add(node.id());
  //     node.addClass("highlighted");
  //   });
  // });

  cy.on("unselect", 'node[type="tag"]', function (event) {
    cy.nodes().removeClass("highlighted");
    cy.edges().removeClass("highlighted");
  });

  cy.on("select", 'node[type="note"]', function (event) {
    if (cy.$("node:selected").length > 1) {
      return;
    } else {
      showFabricModal(event.target.id(), event.target.data("label"));
    }
  });

  cy.on("dragfree", "node", function (event) {
    const node = event.target; // The moved node
    const nodeId = node.id(); // Node ID
    const position = node.position(); // Updated position {x, y}

    // Send the data to the backend
    sendNodePositionToBackend(node);
    if (event.target.data("type") === "tag") {
      event.target.select();
    }
  });
  document.addEventListener("keydown", HandlecyClick);
  console.log("cytoscape click event listener addded");
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
      CreateNote("child");
    } else {
      CreateNote("none");
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
    const searchTerm = prompt("Enter a search term:");
    const lowerCaseSearchTerm = searchTerm.toLowerCase();
    cy.elements().forEach((ele) => {
      if (
        ele.isNode() &&
        !ele.data("label").toLowerCase().includes(lowerCaseSearchTerm)
      ) {
        ele.addClass("greyed-out");
      } else {
        ele.removeClass("greyed-out");
        if (ele.isNode()) {
          ele.select();
        }
      }
    });
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
function CreateTag(type) {
  if (type == "child") {
    const selectedTag = cy.$('node[type="tag"]:selected');
    let newTagId = "";
    if (selectedTag.length > 0) {
      const tagName = prompt("Enter the name for the new Tag:");
      if (tagName) {
        fetch("http://127.0.0.1:8000/create", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ type: "tag", name: tagName }),
        })
          .then((response) => response.json())
          .then((data) => {
            newTagId = data.elements[0].id;

            console.log("new tag id:", newTagId);
            AddNodes(data); // Call the updateGraph function with the new data
            // UpdateNodes();
            // Get the id from the single element in the array
            // RunLayout("note_" + newNoteId); // Pass the id property of the single node
            const tagId = selectedTag.id(); // Get the id of the selected tag
            console.log(
              "creating edge with source:",
              tagId,
              "target",
              "tag_" + newTagId
            );
            // Create an edge between the selected tag and the new note
            fetch("http://127.0.0.1:8000 /create", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                type: "edge",
                source: tagId,
                target: "tag_" + newTagId,
              }),
            })
              .then((response) => response.json())
              .then((data) => {
                if (data.status === "success") {
                  cy.add({
                    group: "edges",
                    data: {
                      source: tagId,
                      target: "tag_" + newTagId,
                    },
                  });
                  UpdateNodes();
                  RunLayout("tag_" + newTagId); // Run layout for the new note
                } else {
                  console.error("Failed to create edge:", data.message);
                }
              })
              .catch((error) => {
                console.error("Error creating edge:", error);
              });
          })
          .catch((error) => {
            console.error("Error fetching data:", error);
          });
      }
    }
  } else {
    const tagName = prompt("Enter the name for the new tag:");
    if (tagName) {
      fetch("/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ type: "tag", name: tagName }),
      })
        .then((response) => response.json())
        .then((data) => {
          AddNodes(data); // Call the updateGraph function with the new data
          UpdateNodes();
          RunLayout("tag_" + data.elements[0].id); // Pass the id property of the single node
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    }
  }
}
function CreateNote(type) {
  if (type == "child") {
    const selectedTag = cy.$('node[type="tag"]:selected');
    let newNoteId = "";
    if (selectedTag.length > 0) {
      const noteName = prompt("Enter the name for the new Note:");
      if (noteName) {
        fetch("/create", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ type: "note", name: noteName }),
        })
          .then((response) => response.json())
          .then((data) => {
            newNoteId = data.elements[0].id;

            console.log("new note id:", newNoteId);
            AddNodes(data); // Call the updateGraph function with the new data
            // UpdateNodes();
            // Get the id from the single element in the array
            // RunLayout("note_" + newNoteId); // Pass the id property of the single node
            const tagId = selectedTag.id(); // Get the id of the selected tag

            // Create an edge between the selected tag and the new note
            fetch("http://127.0.0.1:8000/create", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({
                type: "edge",
                source: tagId,
                target: "note_" + newNoteId,
              }),
            })
              .then((response) => response.json())
              .then((data) => {
                if (data.status === "success") {
                  cy.add({
                    group: "edges",
                    data: {
                      source: tagId,
                      target: "note_" + newNoteId,
                    },
                  });
                  UpdateNodes();
                  RunLayout("note_" + newNoteId); // Run layout for the new note
                } else {
                  console.error("Failed to create edge:", data.message);
                }
              })
              .catch((error) => {
                console.error("Error creating edge:", error);
              });
          })
          .catch((error) => {
            console.error("Error fetching data:", error);
          });
      }
    }
  } else {
    const noteName = prompt("Enter the name for the new note:");
    if (noteName) {
      fetch("http://127.0.0.1:8000/create", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ type: "note", name: noteName }),
      })
        .then((response) => response.json())
        .then((data) => {
          AddNodes(data); // Call the updateGraph function with the new data
          UpdateNodes();
          RunLayout("note_" + data.elements[0].id); // Pass the id property of the single node
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    }
  }
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

    console.log("fixed constraints:", fixedNodeConstraints);
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
  cy.on("layoutstop", runCola);

  function runCola() {
    const colaLayout = cy.layout({
      name: "cola",
      infinite: true, // Infinite animation
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

function showFabricModal(noteId, noteContent) {
  // Hide the popper handle
  window.removeHandle();
  // remove event listeners
  document.removeEventListener("keydown", HandlecyClick);

  var modal = document.getElementById("myModal");
  modal.style.display = "flex";

  // Access the modal content dimensions
  const modalContent = document.querySelector(".modal-content");
  const fabricCanvasEl = document.getElementById("fabricCanvas");
  const gridCanvas = document.getElementById("grid-canvas");
  const gridContext = gridCanvas.getContext("2d");

  // Initialize Fabric.js canvas
  const canvas = new fabric.Canvas(fabricCanvasEl, {
    width: modalContent.offsetWidth,
    height: modalContent.offsetHeight,
    backgroundColor: "transparent", // Ensure background is transparent
  });
  //might need changing in future but prevents blurry edges for now
  fabric.Object.prototype.objectCaching = false; // Disable object caching for better performance

  canvas.freeDrawingBrush.width = 5; // Set default pen width

  const width = modalContent.offsetWidth;
  const height = modalContent.offsetWidth;

  canvas.setWidth(width);
  canvas.setHeight(height);

  gridCanvas.width = width;
  gridCanvas.height = height;

  // Grid settings
  let gridSize = 20;
  let vertical = true;
  let horizontal = true;
  function drawGrid(offsetX = 0, offsetY = 0, zoom = 1) {
    const backgroundSelect = document.getElementById("Background");
    const selectedBackground = backgroundSelect.value;

    if (selectedBackground === "blank") {
      vertical = false;
      horizontal = false;
    } else if (selectedBackground === "s__grid") {
      vertical = true;
      horizontal = true;
      gridSize = 20;
    } else if (selectedBackground === "m_grid") {
      vertical = true;
      horizontal = true;
      gridSize = 40;
    } else if (selectedBackground === "l_grid") {
      vertical = true;
      horizontal = true;
      gridSize = 60;
    } else if (selectedBackground === "line") {
      vertical = false;
      horizontal = true;
      gridSize = 40;
    }
    gridContext.clearRect(0, 0, gridCanvas.width, gridCanvas.height); // Clear the grid canvas

    gridContext.strokeStyle = "#ccc";
    gridContext.lineWidth = 0.5;

    const scaledGridSize = gridSize * zoom;

    // Calculate starting points based on offset
    const startX =
      ((offsetX % scaledGridSize) + scaledGridSize) % scaledGridSize;
    const startY =
      ((offsetY % scaledGridSize) + scaledGridSize) % scaledGridSize;

    // Draw vertical lines
    if (vertical) {
      for (let x = startX; x < gridCanvas.width; x += scaledGridSize) {
        gridContext.beginPath();
        gridContext.moveTo(x, 0);
        gridContext.lineTo(x, gridCanvas.height);
        gridContext.stroke();
      }
    }

    // Draw horizontal lines
    if (horizontal) {
      for (let y = startY; y < gridCanvas.height; y += scaledGridSize) {
        gridContext.beginPath();
        gridContext.moveTo(0, y);
        gridContext.lineTo(gridCanvas.width, y);
        gridContext.stroke();
      }
    }
  }

  function switchMode(mode) {
    canvas.isDrawingMode = mode === "draw";
    document.getElementById("modeToggle").value = mode;
  }

  // if in draw mode, enable drawing
  if (document.getElementById("modeToggle").value === "draw") {
    canvas.isDrawingMode = true;
  }

  document.getElementById("modeToggle").addEventListener("change", (e) => {
    switchMode(e.target.value);
  });

  document.getElementById("addShapeButton").addEventListener("click", () => {
    const shapeType = document.getElementById("addShape").value;
    let shape;
    if (shapeType === "rectangle") {
      shape = new fabric.Rect({
        left: 100,
        top: 100,
        width: 100,
        height: 60,
        fill: "blue",
      });
    } else if (shapeType === "circle") {
      shape = new fabric.Circle({
        left: 100,
        top: 100,
        radius: 50,
        fill: "green",
      });
    } else if (shapeType === "triangle") {
      shape = new fabric.Triangle({
        left: 100,
        top: 100,
        width: 100,
        height: 100,
        fill: "yellow",
      });
    }
    if (shape) {
      canvas.add(shape);
    }
  });

  // Pen Color and Width
  document.getElementById("penColor").addEventListener("input", (e) => {
    canvas.freeDrawingBrush.color = e.target.value;
  });
  document.getElementById("penWidth").addEventListener("input", (e) => {
    canvas.freeDrawingBrush.width = parseInt(e.target.value, 10) || 1;
  });

  const backgroundSelect = document.getElementById("Background");
  backgroundSelect.addEventListener("change", (e) => {
    const vpt = canvas.viewportTransform;

    drawGrid(vpt[4], vpt[5], canvas.getZoom());
  });

  document.getElementById("addTextButton").addEventListener("click", () => {
    const textbox = new fabric.Textbox("Type here...", {
      left: 20,
      top: 20,
      width: 300,
      fontSize: 30,
      fill: "gray", // Set placeholder text color
      editable: true,
      borderColor: "#ccc",
      cornerColor: "#ccc",
      hasBorders: true,
      hasControls: true,
    });

    // Event listener for when the text box is clicked and edited
    textbox.on("editing:entered", function () {
      // Only clear the text if it is still the placeholder text
      if (textbox.text.trim() === "Type here...") {
        textbox.set({ text: "" }); // Clear the placeholder text
        textbox.set({ fill: "black" }); // Set text color to black
        canvas.renderAll(); // Re-render the canvas to reflect the changes
      }
    });

    canvas.add(textbox);
  });

  // delete button
  document.getElementById("deleteButton").addEventListener("click", () => {
    const activeObjects = canvas.getActiveObjects();
    activeObjects.forEach((obj) => canvas.remove(obj));
    canvas.discardActiveObject().renderAll();
  });

  document.addEventListener("keydown", HandleNoteClick);
  // Check if the canvas is initialized
  function HandleNoteClick(event) {
    console.log("key pressed", event.key);
    if (!canvas) return;

    // Check if the key pressed is "Delete" or "Backspace"
    if (event.key === "Delete" || event.key === "Backspace") {
      const activeObject = canvas.getActiveObject(); // Get the selected object

      // Check if we are in a textbox and actively editing
      if (
        activeObject &&
        activeObject.type === "textbox" &&
        activeObject.isEditing
      ) {
        // Allow backspace and delete to behave normally inside the textbox
        // This will automatically allow the normal text editing behavior
        if (event.key === "Backspace" || event.key === "Delete") {
          return; // Let the default behavior happen
        }
      }

      if (activeObject) {
        // Prevent default behavior (e.g., Backspace from navigating back in browsers)
        event.preventDefault();

        // Get all selected objects
        const activeObjects = canvas.getActiveObjects();

        // Remove each selected object
        activeObjects.forEach((obj) => canvas.remove(obj));

        // Clear selection
        canvas.discardActiveObject();
        canvas.renderAll(); // Re-render the canvas
      }
    } else if (event.key === "Escape") {
      event.preventDefault();
      ExitNoteModal();
    } else if (event.key === "Tab") {
      event.preventDefault();
      const currentMode = document.getElementById("modeToggle").value;

      // Toggle between "draw" and "text" modes
      if (currentMode === "draw") {
        switchMode("text");
      } else {
        switchMode("draw");
      }
    } else if (event.key === "d") {
      console.log("d pressed");
      canvas.discardActiveObject().renderAll();
    }
  }

  fetch("http://127.0.0.1:8000/load", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ operation: "content", id: noteId }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        // parse the data into the canvas
        console.log("loading id:", noteId, "data: ", data.content);
        canvas.loadFromJSON(data.content);
        // re-render the canvas
        canvas.renderAll();

        if (data.viewport) {
          const viewport = JSON.parse(data.viewport);
          canvas.setViewportTransform(viewport);
          drawGrid(
            canvas.viewportTransform[4],
            canvas.viewportTransform[5],
            canvas.getZoom()
          );
        }
        if (data.background) {
          backgroundSelect.value = data.background;
          drawGrid(
            canvas.viewportTransform[4],
            canvas.viewportTransform[5],
            canvas.getZoom()
          );
        }
        document.getElementById("nameInput").value = data.name;
      } else {
        console.error(
          "Failed to fetch note content:",
          data.message,
          "new canvas created"
        );
      }
    })
    .catch((error) => {
      console.error("critical Error fetching note content:", error);
    });

  let isPanning = false;
  let lastPosX = 0;
  let lastPosY = 0;

  // Mouse down to start panning
  canvas.on("mouse:down", function (opt) {
    const evt = opt.e;
    if (evt.button === 1) {
      // Middle mouse button pressed
      isPanning = true;
      // canvas.isDrawingMode = false; // Temporarily disable drawing
      lastPosX = evt.clientX;
      lastPosY = evt.clientY;
    }
  });

  // Mouse move to pan
  canvas.on("mouse:move", function (opt) {
    if (isPanning) {
      const evt = opt.e;
      const deltaX = evt.clientX - lastPosX;
      const deltaY = evt.clientY - lastPosY;
      const vpt = canvas.viewportTransform;
      vpt[4] += deltaX; // Update x-axis pan
      vpt[5] += deltaY; // Update y-axis pan
      drawGrid(vpt[4], vpt[5], canvas.getZoom());
      lastPosX = evt.clientX;
      lastPosY = evt.clientY;
    }
  });

  // Mouse up to stop panning
  canvas.on("mouse:up", function () {
    isPanning = false;
    // canvas.isDrawingMode = true; // Re-enable drawing mode
  });

  // Two-finger swipe (trackpad) for panning
  canvas.on("mouse:wheel", function (opt) {
    const evt = opt.e;

    // Check for Ctrl key or pinch-to-zoom gesture
    if (evt.ctrlKey) {
      // Zoom behavior
      let zoom = canvas.getZoom();
      zoom *= 0.99 ** evt.deltaY; // Adjust zoom level
      zoom = Math.min(Math.max(zoom, 0.1), 50); // Limit zoom levels
      canvas.zoomToPoint({ x: evt.offsetX, y: evt.offsetY }, zoom);
      drawGrid(canvas.viewportTransform[4], canvas.viewportTransform[5], zoom); // Redraw grid on zoom
    } else {
      // Panning behavior
      const deltaX = evt.deltaX;
      const deltaY = evt.deltaY;
      const vpt = canvas.viewportTransform;

      vpt[4] -= deltaX; // Horizontal panning
      vpt[5] -= deltaY; // Vertical panning
      drawGrid(vpt[4], vpt[5], canvas.getZoom()); // Redraw grid during panning
      canvas.requestRenderAll();
    }

    evt.preventDefault(); // Prevent default scrolling behavior
  });

  window.addEventListener(
    "touchstart",
    function (e) {
      const touches = e.touches;
      if (touches.length === 2) {
        console.log("ultimate two fingers detected");
        console.log(touches);
        canvas.discardActiveObject().renderAll();
        // const activ=eObject = canvas.getActiveObject();

        e.preventDefault();
        canvas.isDrawingMode = false;
        canvas.selection = false;
        canvas.forEachObject(function (o) {
          o.lockMovementX = true;
          o.lockMovementY = true;
          o.selectable = false;
        });
      } else if (touches.length === 1) {
        console.log("only one finger detected");

        canvas.selection = true;
        canvas.forEachObject(function (o) {
          o.lockMovementX = false;
          o.lockMovementY = false;
          o.selectable = true;
        });
        if (document.getElementById("modeToggle").value === "draw") {
          canvas.isDrawingMode = true;
        }
      }

      if (touches.length > 0) {
        const touch = touches[0];

        if ("force" in touch) {
          console.log("Touch pressure (force):", touch.force);
        }
        if (touch.force > 0) {
          console.log("Apple Pencil detected");
          if (document.getElementById("modeToggle").value === "draw") {
            canvas.isDrawingMode = true;
          }
        } else {
          console.log("Finger detected");
          canvas.isDrawingMode = false;
        }
      }
    },
    true
  );
  // Create a Hammer.js instance
  const hammer = new Hammer(canvas.wrapperEl);
  hammer.get("pan").set({ direction: Hammer.DIRECTION_ALL, pointers: 2 });
  hammer.get("pinch").set({ enable: true });
  hammer.get("press").set({ time: 0 });
  hammer.get("pinch").recognizeWith(hammer.get("pan"));

  // hammer.on("press", function (e) {
  //   const inputType = e.pointerType; // "touch", "pen", or "mouse"
  //   if (inputType === "touch") {
  //     canvas.isDrawingMode = false;

  //     // canvas.selection = false;
  //     // canvas.forEachObject(function (o) {
  //     //   o.selectable = false;
  //     // });
  //     e.preventDefault();
  //   } else if (inputType === "pen") {
  //     if (document.getElementById("modeToggle").value === "draw") {
  //       canvas.isDrawingMode = true;
  //     }
  //     // canvas.selection = false;
  //     // canvas.forEachObject(function (o) {
  //     //   o.selectable = false;
  //     // });
  //   }
  //   // e.preventDefault();
  //   // canvas.isDrawingMode = false;
  //   // canvas.selection = false;
  //   // canvas.forEachObject(function (o) {
  //   //   o.selectable = false;
  //   // });
  // });

  // Pinch to zoom functionality

  let lastScale = 1;

  hammer.on("pinchstart", function (e) {
    canvas._zoomStartScale = canvas.getZoom(); // Record the initial zoom level
    lastScale = 1; // Reset the last scale for the new gesture
  });

  hammer.on("pinchmove", function (e) {
    const scaleChange = e.scale / lastScale; // Calculate incremental scale change
    lastScale = e.scale; // Update last scale for the next move event

    const newZoom = canvas.getZoom() * scaleChange; // Apply incremental zoom
    const boundedZoom = Math.min(Math.max(newZoom, 0.1), 50); // Clamp zoom level

    const center = { x: e.center.x, y: e.center.y }; // Zoom relative to touch center
    canvas.zoomToPoint(center, boundedZoom); // Apply zoom at the given point

    // Redraw grid and canvas
    drawGrid(
      canvas.viewportTransform[4],
      canvas.viewportTransform[5],
      boundedZoom
    );
    canvas.requestRenderAll();
  });

  hammer.on("pinchend", function () {
    lastScale = 1; // Reset scale tracking after the pinch gesture ends
  });

  // hammer.on("pinchend", function (e) {
  //   if (document.getElementById("modeToggle").value === "draw") {
  //     canvas.isDrawingMode = true;
  //   }
  //   canvas.selection = true;
  //   canvas.forEachObject(function (o) {
  //     o.selectable = true;
  //   });
  // });

  // Two-finger pan start
  // hammer.on("panstart", function (e) {
  //   canvas.discardActiveObject().renderAll();
  //   const activeObject = canvas.getActiveObject();
  //   activeObject.lockMovementY = true;
  //   activeObject.lockMovementX = true;
  //   e.preventDefault();
  //   canvas.isDrawingMode = false;
  //   canvas.selection = false;
  //   canvas.forEachObject(function (o) {
  //     o.selectable = false;
  //   });
  // });

  // Pan with two fingers functionality
  let lastDeltaX = 0;
  let lastDeltaY = 0;

  hammer.on("panmove", function (e) {
    console.log("Pan move detected:", e); // Debugging log

    const vpt = canvas.viewportTransform;

    // Calculate the incremental delta values
    const deltaX = e.deltaX - lastDeltaX;
    const deltaY = e.deltaY - lastDeltaY;

    // Update last delta values
    lastDeltaX = e.deltaX;
    lastDeltaY = e.deltaY;

    // Adjust the movement scale (optional for smoothing)
    const movementScale = 1;

    // Apply panning movement incrementally
    vpt[4] += deltaX * movementScale;
    vpt[5] += deltaY * movementScale;

    // Re-render the canvas with the new viewport transform
    canvas.requestRenderAll();
    drawGrid(vpt[4], vpt[5], canvas.getZoom()); // Redraw grid during panning
  });

  hammer.on("panend", function () {
    // Reset last delta values when the pan gesture ends
    lastDeltaX = 0;
    lastDeltaY = 0;
  });

  // hammer.on("panend", function (e) {
  //   if (document.getElementById("modeToggle").value === "draw") {
  //     canvas.isDrawingMode = true;
  //   }
  //   canvas.selection = true;
  //   canvas.forEachObject(function (o) {
  //     o.selectable = true;
  //   });
  // });

  // Ensure single-finger gestures are handled by Fabric.js
  // canvas.wrapperEl.addEventListener("touchstart", function (e) {
  //   if (e.touches.length === 1) {
  //     // Allow Fabric.js to handle one-finger gestures
  //     return;
  //   } else {
  //     console.log("blocking fabricjs");
  //     e.preventDefault(); // Prevent Fabric.js from handling multi-touch gestures
  //   }
  // });
  // Prevent context menu from appearing on right-click
  document
    .getElementById("fabricCanvas")
    .addEventListener("contextmenu", function (e) {
      e.preventDefault();
    });
  window.addEventListener("resize", handleNoteResize);

  function handleNoteResize() {
    const width = modalContent.offsetWidth;
    const height = modalContent.offsetWidth;

    canvas.setWidth(width);
    canvas.setHeight(height);

    gridCanvas.width = width;
    gridCanvas.height = height;

    const transform = canvas.viewportTransform;
    drawGrid(transform[4], transform[5], canvas.getZoom());
  }

  // Sync grid with Fabric.js canvas transformations
  function syncGridWithCanvas() {
    const vpt = canvas.viewportTransform;
    drawGrid(vpt[4], vpt[5], canvas.getZoom()); // Redraw grid
  }

  // Sync after every render
  canvas.on("after:render", syncGridWithCanvas);

  window.onclick = function (event) {
    if (event.target == modal) {
      ExitNoteModal();
    }
  };
  const closeModal = document.getElementById("closeModal");
  closeModal.onclick = function () {
    ExitNoteModal();
  };
  function ExitNoteModal() {
    saveCanvas(); // Save the canvas content
    canvas.dispose(); // Clear the Fabric.js canvas
    modal.style.display = "none"; // Hide the modal
    document.removeEventListener("keydown", HandleNoteClick);
    window.removeEventListener("resize", handleNoteResize);
    document.addEventListener("keydown", HandlecyClick);
    cy.elements().unselect(); //enables repeat clicks
  }
  function saveCanvas() {
    // convert canvas to a json string

    var json = JSON.stringify(canvas.toJSON());
    var viewport = JSON.stringify(canvas.viewportTransform);
    var background = backgroundSelect.value;
    var name = document.getElementById("nameInput").value;
    // Update the node label with the new name
    const node = cy.getElementById(noteId);
    if (node) {
      node.data("label", name);
    }

    console.log("saving id:", noteId, "data: ", json);
    fetch("/update", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        operation: "content",
        id: noteId,
        content: json,
        viewport: viewport,
        background: background,
        name: name,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.status === "success") {
          console.log("Canvas saved successfully");
        } else {
          console.error("Failed to save canvas:", data.message);
        }
      })
      .catch((error) => {
        console.error("critical Error saving canvas:", error);
      });
  }
}

function sendNodePositionToBackend(node) {
  // Prepare data to send
  nodeId = node.id();
  position = node.position();
  // Send POST request to backend
  fetch("/update", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      operation: "location",
      id: nodeId,
      x: position.x,
      y: position.y,
    }),
  })
    .then((response) => {
      if (response.ok) {
        // Update node data with new position

        node.data("x", Math.round(position.x));
        node.data("y", Math.round(position.y));
        node.addClass("static");
      } else {
        console.error(`Failed to send position for node ${nodeId}.`);
      }
    })
    .catch((error) => {
      console.error(`Error sending position for node ${nodeId}:`, error);
    });
}
function destroyCytoscape() {
  if (cy) {
    cy.destroy();
    cy = null;
  }
}

onMounted(() => {
  initializeCytoscape();

  const loadData = async () => {
    try {
      const response = await axios.post('/load', {
        operation: 'all'
      });
      AddNodes(response.data); // Call the updateGraph function with the new data
      UpdateNodes();
      RunLayout("all");
    } catch (error) {
      console.error('Error fetching data:', error.response ? error.response.data : error);
    }
  };

  loadData();





  // Handle search form submission
  document
    .getElementById("searchForm")
    .addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent the default form submission

      const query = document.getElementById("searchInput").value; // if the search query is blank call
      if (query.trim() === "") {
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
      } else {
        fetch("http://127.0.0.1:8000/load", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ operation: "search", query: query }),
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
    });

  document.getElementById("newNote").addEventListener("click", CreateNote);

  document.getElementById("newTag").addEventListener("click", CreateTag);

  document
    .getElementById("unlockAllButton")
    .addEventListener("click", function () {
      // Send a POST request to the backend
      fetch("/update", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ operation: "unlock", id: "all" }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.status === "success") {
            // Remove the 'static' class from all nodes
            cy.nodes(".static").removeClass("static");
          } else {
            console.error("Failed to unlock nodes:", data.message);
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });

  document.getElementById("logout").addEventListener("click", function () {
    window.location.href = "/logout"; // Navigate to /logout
  });
  // Listen for tab changes or size changes
  const resizeObserver = new ResizeObserver(() => {
    if (cy) {
      cy.resize();

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
          <!-- <VSwatches v-model="color" popover-x="left"></VSwatches> -->
        </div>
      </div>
    </ResizablePanel>
  </ResizablePanelGroup>
</template>
