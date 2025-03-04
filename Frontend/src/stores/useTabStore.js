import { defineStore } from "pinia";
import { markRaw, ref } from "vue";
import Cytoscape from "@/components/Cytoscape.vue";
import Dashboard from "@/components/Dashboard.vue";
// import TipTap from "@/components/Document editor/TipTap.vue";
import Chat from "@/components/Chat.vue";
// import Note from "@/components/Note.vue";
import GenericTab from "@/components/GenericTab.vue";

export const useTabStore = defineStore("tabStore", () => {
  const activeTab = ref(1); // Set first tab as active by default

  const defaultTabs = [
    {
      id: 1,
      title: "Dashboard",
      component: markRaw(Dashboard),
      type: "locked", // Special type tab that stores multiple components and states
      state: {
        someState: {}, // Put your special state here for Dashboard
      },
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
      type: "normal", // Regular tab type
      state: {},
    },
  ];

  const tabs = ref([...defaultTabs]); // Initialize tabs with default tabs

  // Add a new tab
  function addTab(title, type, state = null) {
    const id = Date.now();
    // const component = type === "cytoscape" ? markRaw(Cytoscape) : null; // Add other components as needed
    let component;
    switch (type) {
      case "generic":
        component = markRaw(GenericTab);
        break;

      // case "settings":
      // component = markRaw(Settings);
      // break;

      // case "Help":
      // component = markRaw(Help);
      // break;

      //add other tab types here
      default:
        component = markRaw(GenericTab);
    }
    tabs.value.push({
      id,
      title,
      component,
      type: "generic",
      state: state || {},
    });
    setActiveTab(id);
  }
  // 🚀 Get a tab by id and type (to handle different component types)
  function getTab(id) {
    return tabs.value.find((tab) => tab.id === id);
  }

  function updateTabState(id, newState) {
    const tab = tabs.value.find((tab) => tab.id === id);
    if (tab) {
      tab.state = { ...newState };
    }
  }

  // function navigate(id, breadcrumb) {
  //   const tab = tabs.value.find((tab) => tab.id === id);
  //   if (tab) {
  //     tab.breadcrumb = breadcrumb
  // }
  // }

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
    tabs.value = [...defaultTabs]; // Reset tabs to default state
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
  };
});
