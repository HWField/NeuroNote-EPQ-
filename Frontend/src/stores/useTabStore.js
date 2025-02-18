import { defineStore } from "pinia";
import { markRaw, ref } from "vue";
import Cytoscape from "@/components/Cytoscape.vue";
import Dashboard from "@/components/Dashboard.vue";
import Chat from "@/components/Chat.vue";
export const useTabStore = defineStore("tabStore", () => {
  

  const activeTab = ref(1); // Set first tab as active by default

  const defaultTabs = [ {
    id: 1,
    title: "Dashboard",
    component: markRaw(Dashboard),
    type: "dashboard", // Component type
   
  },
  {
    id: 2,
    title: "Chat",
    component: markRaw(Chat),
    type: "chat", // Component type
    state: { },
  },
  {
    id: 3,
    title: "Note1",
    component: markRaw(Cytoscape),
    type: "cytoscape", // Component type
    state: { },
  },];

  
  const tabs = ref([...defaultTabs]); // Initialize tabs with default tabs
  // Add a new tab
  function addTab(title, type) {
    const id = Date.now();
    const component = type === "cytoscape" ? markRaw(Cytoscape) : null; // Add other components as needed
    tabs.value.push({
      id,
      title,
      component,
      type,
      state: {  },
    });
    activeTab.value = id;
  }
  // 🚀 Get a tab by id and type (to handle different component types)
  function getTab(id, type) {
    return tabs.value.find((tab) => tab.id === id && tab.type === type);
  }

  function updateTabState(id, type, newState) {
    const tab = tabs.value.find((tab) => tab.id === id && tab.type === type);
    if (tab) {
      tab.state = { ...newState };
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

  function clearStore() {
    console.error("🧹 CLEARING TAB STORE!");
    tabs.value.forEach((tab) => {
      console.log("before state" + tab.state);
      tab.state = {}; // Reset state manually
      console.log("after state" + tab.state);
    });
    // Reset tabs with brand new objects (deep reset)
    tabs.value = [ {
      id: 1,
      title: "Dashboard",
      component: markRaw(Dashboard),
      type: "dashboard", // Component type
     
    },
    {
      id: 2,
      title: "Chat",
      component: markRaw(Chat),
      type: "chat", // Component type
      state: { },
    },
    {
      id: 3,
      title: "Note1",
      component: markRaw(Cytoscape),
      type: "cytoscape", // Component type
      state: { },
    },];
  
    activeTab.value = 1; // Reset active tab
  
    console.log("After Clear:", JSON.stringify(tabs.value, null, 2));
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
  };
});
