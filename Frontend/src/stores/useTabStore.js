import { defineStore } from "pinia";
import { markRaw, ref } from "vue";
import Cytoscape from "@/components/Cytoscape.vue";
export const useTabStore = defineStore("tabStore", () => {
  const tabs = ref([
    {
      id: 1,
      title: "Tets",
      component: markRaw(Cytoscape),
      type: "cytoscape", // Component type
      state: { elements: [], zoom: 1, pan: { x: 0, y: 0 } },
    },
    {
      id: 2,
      title: "numbewr3",
      component: markRaw(Cytoscape),
      type: "cytoscape", // Component type
      state: { elements: [], zoom: 1, pan: { x: 0, y: 0 } },
    },
  ]);

  const activeTab = ref(1); // Set first tab as active by default

  // Add a new tab
  function addTab(title, type) {
    const id = Date.now();
    const component = type === 'cytoscape' ? markRaw(Cytoscape) : null; // Add other components as needed
    tabs.value.push({
      id,
      title,
      component,
      type,
      state: { elements: [], zoom: 1, pan: { x: 0, y: 0 } }
    });
    activeTab.value = id;
  }
  // 🚀 Get a tab by id and type (to handle different component types)
  function getTab(id, type) {
    return tabs.value.find(tab => tab.id === id && tab.type === type);
  }

  function updateTabState(id, type, newState) {
    const tab = tabs.value.find(tab => tab.id === id && tab.type === type);
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

  return {
    tabs,
    activeTab,
    addTab,
    setActiveTab,
    updateTabState,
    getTab,
    removeTab,
  };
});
