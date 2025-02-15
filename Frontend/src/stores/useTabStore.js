import { defineStore } from 'pinia';
import { markRaw, ref } from 'vue';
import Cytoscape from "@/components/Cytoscape.vue";
export const useTabStore = defineStore('tabStore', () => {
  const tabs = ref([
    { id: 1, title: 'Tets', component: markRaw(Cytoscape), active: true },
    { id: 2, title: 'fdfdfgssdfs', component: markRaw(Cytoscape), active: true },
   
  ]);
  
  const activeTab = ref(tabs.value[0].id); // Set first tab as active by default

  // Add a new tab
  function addTab(title, component) {
    const id = Date.now();
    tabs.value.push({ id, title, component, active: false });
    setActiveTab(id);
  }

  // Remove a tab
  function removeTab(id) {
    tabs.value = tabs.value.filter(tab => tab.id !== id);
    if (activeTab.value === id) {
      activeTab.value = tabs.value.length ? tabs.value[0].id : null;
    }
  }

  // Set active tab
  function setActiveTab(id) {
    activeTab.value = id;
    tabs.value.forEach(tab => {
      tab.active = tab.id === id;
    });
  }

  return { tabs, activeTab, addTab, removeTab, setActiveTab };
});