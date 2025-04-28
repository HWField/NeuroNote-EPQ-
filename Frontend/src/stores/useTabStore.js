import { defineStore } from "pinia";
import { markRaw, ref } from "vue";
import Cytoscape from "@/components/Cytoscape.vue";
import Dashboard from "@/components/Dashboard.vue";
import Loading from "@/components/Loading.vue";
// import TipTap from "@/components/Document editor/TipTap.vue";
import Chat from "@/components/Chat.vue";
// import Note from "@/components/Note.vue";
import { cloneDeep } from "lodash"; // Install lodash first
import GenericTab from "@/components/GenericTab.vue";
import Settings from "@/components/Settings.vue";
import Feedback from "@/components/Feedback.vue";
import NoteTab from "@/components/NoteTab.vue";
import axios from "../axios"; // Import the Axios instance
import GraphTab from "@/components/GraphTab.vue"; // Import the GraphTab component
import LegalTab from "@/components/LegalTab.vue"; // Import the LegalTab component
import { useUserStore } from "@/stores/useUserStore";
import chemicalstructure from "@/components/Document Editor/ChemicalStructure.vue"; // Import the ChemicalStructure component

export const useTabStore = defineStore("tabStore", () => {
  const activeTab = ref(1); // Set first tab as active by default
  const componentMapping = {
    Loading: markRaw(Loading),
    Dashboard: markRaw(Dashboard),
    Chat: markRaw(Chat),
    GenericTab: markRaw(GenericTab),
    Settings: markRaw(Settings),
    Feedback: markRaw(Feedback),
    NoteTab: markRaw(NoteTab),
    GraphTab: markRaw(GraphTab),
    LegalTab: markRaw(LegalTab),
  };

  const defaultTabs = [
    {
      id: 0,
      title: "Loading",
      componentName: "Loading", // Store component name instead of reference
      component: componentMapping.Loading,
      type: "loading", // Special type tab that stores multiple components and states
      state: {},
    },
    {
      id: 1,
      title: "Dashboard",
      componentName: "Dashboard",
      component: componentMapping.Dashboard,
      type: "locked", // Special type tab that stores multiple components and states
      state: {},
    },
    {
      id: 2,
      title: "Chat",
      componentName: "Chat",
      component: componentMapping.Chat,
      type: "locked", // Special type for Chat tab
      state: {
        messages: [],
        userData: {},
      },
    },
  ];

  const tabs = ref(cloneDeep(defaultTabs)); // Initialize tabs with default tabs

  // Add a new tab
  function addTab(title, type, state = null) {
    const id = Date.now();
    // const component = type === "cytoscape" ? markRaw(Cytoscape) : null; // Add other components as needed
    let component;
    switch (type) {
      case "generic":
      
        if (state && state.noteId) {
          // Find any existing tab that has this noteId
          const existingTab = tabs.value.find(
            (tab) => tab.state && tab.state.noteId === state.noteId
          );

          // If found, just activate that tab instead of creating a new one
          if (existingTab) {
            console.log(
              `Note ${state.noteId} already open in tab ${existingTab.id} - switching to it`
            );

            setActiveTab(existingTab.id);
            return; // Exit early - no need to create a new tab
          }
        }
        tabs.value.push({
          id,
          title,
          componentName: "GenericTab", // Store name for serialization
          component: componentMapping.GenericTab,
          type: "generic",
          state: state || { view: "graph", noteId: null },
        });
        break;

      case "note":
        if (state && state.noteId) {
          // Find any existing tab that has this noteId
          const existingTab = tabs.value.find(
            (tab) => tab.state && tab.state.noteId === state.noteId
          );

          // If found, just activate that tab instead of creating a new one
          if (existingTab) {
            console.log(
              `Note ${state.noteId} already open in tab ${existingTab.id} - switching to it`
            );
            updateTabState(existingTab.id, state); // Update the creation id to be the current tab id need to be carreful this doesnt overwrite other elements but should be fine
            setActiveTab(existingTab.id);
            return; // Exit early - no need to create a new tab
          }
        }

        tabs.value.push({
          id,
          title,
          componentName: "NoteTab", // Store name for serialization
          component: componentMapping.NoteTab,
          type: "note",
          state: state || {noteId: null, creationTabId: null},
        });
        break;


      case "graph":
        tabs.value.push({
          id,
          title,
          componentName: "GraphTab", // Store name for serialization
          component: componentMapping.GraphTab,
          type: "graph",
          state: state || {},
        });
        break;

        case "legal":
          tabs.value.push({
            id,
            title,
            componentName: "LegalTab", // Store name for serialization
            component: componentMapping.LegalTab,
            type: "legal",
            state: state || {},
          });
          break;


      case "settings":
        // Find any existing tab that is of type settings
        const existingSettingsTab = tabs.value.find(
          (tab) => tab.type === "settings"
        );

        if (existingSettingsTab) {
          console.log(
            `Settings already open in tab ${existingSettingsTab.id} - switching to it`
          );
          setActiveTab(existingSettingsTab.id);
          return; // Exit early - no need to create a new tab
        }

        component = markRaw(Settings);
        tabs.value.push({
          id,
          title,
          componentName: "Settings", // Store name for serialization
          component: componentMapping.Settings,
          type: "settings",
          state: state || {},
        });
        break;

      case "feedback":
        component = markRaw(Settings);
        tabs.value.push({
          id,
          title,
          componentName: "Feedback", // Store name for serialization
          component: componentMapping.Feedback,
          type: "feedback",
          state: state || {},
        });
        break;

      // case "Help":
      // component = markRaw(Help);
      // break;

      //add other tab types here
    }

    setActiveTab(id);
    useUserStore().saveUser({ tabs: Array.from(tabs.value) });
  }
  // 🚀 Get a tab by id and type (to handle different component types)
  function getTab(id) {
    return tabs.value.find((tab) => tab.id === id);
  }

  function loadTabsFromPreferences(preferenceTabs) {
    if (
      !preferenceTabs ||
      !Array.isArray(preferenceTabs) ||
      preferenceTabs.length === 0
    ) {
      tabs.value = cloneDeep(defaultTabs);
      return;
    }

    // Restore components in the loaded tabs
    const loadedTabs = preferenceTabs.map((tab) => {
      // Create a copy of the tab
      const newTab = { ...tab };

      // Restore the component reference from the componentName
      if (tab.componentName && componentMapping[tab.componentName]) {
        newTab.component = componentMapping[tab.componentName];
      } else {
        // Fallback to GenericTab if component not found
        newTab.component = componentMapping.GenericTab;
        newTab.componentName = "GenericTab";
      }

      return newTab;
    });

    // Replace tabs with loaded tabs
    tabs.value = loadedTabs;
  }

  function updateTabState(id, newState) {
    const tab = tabs.value.find((tab) => tab.id === id);
    if (tab) {
      // Merge with existing state instead of replacing
      // tab.state = { ...tab.state, ...newState };
      // tab.state = { ...newState };]
      Object.assign(tab.state, newState);
    }
  }

  function RenameTab(id, newTitle) {
    const tab = tabs.value.find((tab) => tab.id === id);
    if (tab) {
      tab.title = newTitle;
    }
  }
  // Remove a tab
  function removeTab(id, newTab = null) {
    tabs.value = tabs.value.filter((tab) => tab.id !== id);
    if (activeTab.value === id) {
      if (newTab) {
        activeTab.value = newTab;
      }
      else {
      activeTab.value = tabs.value.length ? tabs.value[1].id : null; // Set to first tab if available if not set to dashbaord
      }
    }
    useUserStore().saveUser({ tabs: Array.from(tabs.value) });
  }

  // Set active tab
  function setActiveTab(id) {
    activeTab.value = id;
    useUserStore().saveUser({ tabs: Array.from(tabs.value) });
  }

  // async function SendTabs() {
  //   try {

  //     const response = await axios.post("/update", {
  //       operation: "tabs",
  //       data: tabs.value,
  //     });

  //   } catch (error) {
  //     console.error("Error sending tabs:", error);
  //   }

  // }

  function GetActiveTabID() {
    return activeTab.value;
  }

  function clearStore() {
    // tabs.value = [...defaultTabs]; // Reset tabs to default state
    tabs.value = cloneDeep(defaultTabs);
    activeTab.value = 1;
  }

  function reorderTabs(newOrder) {
    // Create a map of the existing tabs by id for easy lookup
    const tabMap = tabs.value.reduce((acc, tab) => {
      acc[tab.id] = tab;
      return acc;
    }, {});

    // Get the locked tabs (0, 1, 2) which should remain at the start
    const lockedTabs = tabs.value.filter(
      (tab) => tab.id === 0 || tab.id === 1 || tab.id === 2
    );

    // Ensure all filtered tabs (non-locked ones) are in the new order
    const reorderedTabs = newOrder.map((tab) => tabMap[tab.id]);

    // Combine the locked tabs with the reordered ones
    tabs.value = [...lockedTabs, ...reorderedTabs];

    // Save the new order
    useUserStore().saveUser({ tabs: Array.from(tabs.value) });
  }
  return {
    tabs,
    activeTab,
    addTab,
    setActiveTab,
    updateTabState,
    getTab,
    removeTab,
    clearStore,
    GetActiveTabID,
    // SendTabs,
    RenameTab,
    loadTabsFromPreferences,
    reorderTabs,
  };
});
