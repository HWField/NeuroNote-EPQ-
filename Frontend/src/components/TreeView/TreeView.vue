<template>
    <div class="tree-view">
      <h3 class="tree-view-title">Knowledge Tree</h3>
      <div class="tree-search">
        <input 
          type="text" 
          v-model="searchTerm" 
          placeholder="Search..." 
          class="search-input" 
          @input="filterTree"
        />
      </div>
      
      <div class="tree-container">
        <!-- Root level tags -->
        <div v-if="rootTags.length === 0" class="empty-state">
          <p>No tags available. Create a tag to organize your knowledge.</p>
        </div>
        
        <ul class="tree-root">
          <li v-for="tag in rootTags" :key="`root-tag-${tag.id}`">
            <tag-node :tag="tag" :depth="0" />
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted, watch } from 'vue';
  import { useGraphStore } from '@/stores/useGraphStore';
  import TagNode from '@/components/TreeView/TagNode.vue';
  
  
  const graphStore = useGraphStore();
  const searchTerm = ref('');
  const filteredElements = ref([]);
  
  // Get all tags from the graph store
  const tags = computed(() => {
    return graphStore.elements.filter(el => el.type === 'tag');
  });
  
  // Find tags that don't have parents (root level)
  const rootTags = computed(() => {
    // A tag is considered a root tag if no other tag has it in its children array
    const childTagIds = new Set();
    
    tags.value.forEach(tag => {
      if (tag.children && tag.children.length > 0) {
        tag.children.forEach(childId => childTagIds.add(childId));
      }
    });
    
    // If search term exists, filter all tags
    if (searchTerm.value) {
      return filteredElements.value.filter(tag => 
        tag.type === 'tag' && !childTagIds.has(tag.id)
      );
    }
    
    // Otherwise, just return the root tags
    return tags.value.filter(tag => !childTagIds.has(tag.id));
  });
  
  function filterTree() {
    if (!searchTerm.value.trim()) {
      filteredElements.value = [];
      return;
    }
    
    const term = searchTerm.value.toLowerCase();
    
    // Filter elements that match the search term
    filteredElements.value = graphStore.elements.filter(el => 
      el.name && el.name.toLowerCase().includes(term)
    );
  }
  
  // Fetch graph data when component is mounted
  onMounted(() => {
    if (graphStore.elements.length === 0) {
      graphStore.fetchGraph();
    }
  });
  
  // Watch for changes in the graph store elements
  watch(() => graphStore.elements, () => {
    if (searchTerm.value) {
      filterTree();
    }
  }, { deep: true });
  </script>
  
  <style scoped>
  .tree-view {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    color: #333;
    background-color: #f8f9fa;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    overflow: hidden;
  }
  
  .tree-view-title {
    padding: 16px 20px;
    margin: 0;
    font-size: 1.25rem;
    font-weight: 600;
    border-bottom: 1px solid #eaeaea;
    background-color: #fff;
  }
  
  .tree-search {
    padding: 12px 16px;
    background-color: #fff;
    border-bottom: 1px solid #eaeaea;
  }
  
  .search-input {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 0.9rem;
    transition: border-color 0.2s;
  }
  
  .search-input:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
  }
  
  .tree-container {
    flex: 1;
    overflow-y: auto;
    padding: 12px 0;
  }
  
  .tree-root {
    list-style-type: none;
    padding: 0 16px;
    margin: 0;
  }
  
  .empty-state {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 32px;
    color: #666;
    text-align: center;
    font-style: italic;
  }
  
  @media (max-width: 768px) {
    .tree-view-title {
      font-size: 1.1rem;
      padding: 12px 16px;
    }
    
    .tree-search {
      padding: 8px 12px;
    }
  }
  </style>