import { defineStore } from "pinia";
import { markRaw, ref } from "vue";
import Cytoscape from "@/components/Cytoscape.vue";
import Dashboard from "@/components/Dashboard.vue";
// import TipTap from "@/components/Document editor/TipTap.vue";
import Chat from "@/components/Chat.vue";
// import Note from "@/components/Note.vue";
import { cloneDeep } from "lodash"; // Install lodash first
import GenericTab from "@/components/GenericTab.vue";
import axios from "../axios"; // Import the Axios instance
import { useUserStore } from "@/stores/useUserStore";

export const useTabStore = defineStore("tabStore", () => {
  const activeTab = ref(1); // Set first tab as active by default

  const defaultTabs = [
    {
      id: 1,
      title: "Dashboard",
      component: markRaw(Dashboard),
      type: "locked", // Special type tab that stores multiple components and states
      state: {},
    },
    {
      id: 2,
      title: "Chat",
      component: markRaw(Chat),
      type: "locked", // Special type for Chat tab
      state: {
        messages: [],
        userData: {},
      },
    },
    {
      id: 3,
      title: "DemoTab",
      component: markRaw(GenericTab),
      type: "generic", // Regular tab type
      state: {view: "graph", noteId: null},
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
      case "note": 
        tabs.value.push({
          id,
          title,
          component: markRaw(GenericTab),
          type: "generic",
          state: state || { view: "graph", noteId: null }
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
  }
  // 🚀 Get a tab by id and type (to handle different component types)
  function getTab(id) {
    return tabs.value.find((tab) => tab.id === id);
  }

  function updateTabState(id, newState) {
    console.error("backend Updating tab:", id ); // Debugging
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
      activeTab.value = tabs.value.length ? tabs.value[0].id : null;
    }
  }

  // Set active tab
  function setActiveTab(id) {
    activeTab.value = id;
  }

  // function FetchTabs(){
  //   tabs.value = newTabs;
  // }

  async function FetchTabs() {
    if (useUserStore().isAuthenticated) {
      try {
        const response = await axios.post("/load", {
          operation: "tabs",
        });
        console.log("tab data:", response.data);

        if (response.data.length > 0) {
          tabs.value = response.data;
        }
        else 
        {
          tabs.value = cloneDeep(defaultTabs);
        }
 
      } catch (error) {
        console.error("Error fetching graph data:", error);
      }
    }
  }

  async function SendTabs() {
    try {
      console.error("📤 SENDING TABS! tabs:");
      console.error(...tabs.value);
      const response = await axios.post("/update", {
        operation: "tabs",
        data: tabs.value,
      });
      console.error("Response:", response.data);
    } catch (error) {
      console.error("Error sending tabs:", error);
    }
    
  }

  function GetActiveTabID() {
    return activeTab.value;
  }

  function clearStore() {
  
    console.error("🧹 CLEARING TAB STORE!");
    console.error(...defaultTabs);
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
    FetchTabs,
    SendTabs,
    RenameTab
  };
});
