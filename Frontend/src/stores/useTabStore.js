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
import axios from "../axios"; // Import the Axios instance
import { useUserStore } from "@/stores/useUserStore";

export const useTabStore = defineStore("tabStore", () => {
  const activeTab = ref(1); // Set first tab as active by default
  const componentMapping = {
    Loading: markRaw(Loading),
    Dashboard: markRaw(Dashboard),
    Chat: markRaw(Chat),
    GenericTab: markRaw(GenericTab),
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
    // {
    //   id: 3,
    //   title: "DemoTab",
    //   component: markRaw(GenericTab),
    //   type: "generic", // Regular tab type
    //   state: {view: "graph", noteId: null},
    // },
  ];

  const tabs = ref(cloneDeep(defaultTabs)); // Initialize tabs with default tabs

  // Add a new tab
  function addTab(title, type, state = null) {
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

    const id = Date.now();
    // const component = type === "cytoscape" ? markRaw(Cytoscape) : null; // Add other components as needed
    let component;
    switch (type) {
      case "generic":
      case "note":
        tabs.value.push({
          id,
          title,
          ccomponentName: "GenericTab", // Store name for serialization
          component: componentMapping.GenericTab,
          type: "generic",
          state: state || { view: "graph", noteId: null },
        });
        break;
      // case "settings":
      // component = markRaw(Settings);
      // break;

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
  function removeTab(id) {
    tabs.value = tabs.value.filter((tab) => tab.id !== id);
    if (activeTab.value === id) {
      activeTab.value = tabs.value.length ? tabs.value[1].id : null; // Set to first tab if available if not set to dashbaord
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
  };
});
