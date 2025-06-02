<template>
  <NodeViewWrapper class="h-full whiteboard-embed">
    <div class="whiteboard-container h-full">
      <Button size="sm" class="edit-button" @click="openFullWhiteboard">
        <Pencil class="h-4 w-4 mr-1" /> Edit
      </Button>
      <div class="whiteboard-wrapper">
        <Whiteboard
          :noteId="node.attrs.id"
          :viewOnly="true"
          :embedded="true"
          :parentTab="useTabStore().activeTab.value"
          class="w-full max-h-full"
        />
        <!-- :parentTab="node.attrs.parentTab" -->
      </div>
    </div>
  </NodeViewWrapper>
</template>

<script setup>
import { NodeViewWrapper } from "@tiptap/vue-3";
import { Button } from "@/components/ui/button";
import { Pencil } from "lucide-vue-next";
import { useTabStore } from "@/stores/useTabStore";
import { useToast } from "@/components/ui/toast/use-toast";
import Whiteboard from "@/components/Whiteboard.vue";

const props = defineProps({
  editor: Object,
  node: Object,
  getPos: Function,
  updateAttributes: Function,
});

const { toast } = useToast();

// Function to open the full whiteboard editor
function openFullWhiteboard() {
  if (props.node.attrs.id) {
    useTabStore().addTab("note", "note", {
      noteId: props.node.attrs.id,
      creationTabId: useTabStore().activeTab,
    });
  } else {
    toast({
      title: "Error",
      description: "Could not open whiteboard: Missing ID",
      variant: "destructive",
    });
  }
}
</script>

<style>
.whiteboard-embed {
  margin: 0rem 0;
  position: relative;
}
.whiteboard-embed.ProseMirror-selectednode {
  outline: 3px solid #6a00f5;
  border-radius: 0.5rem;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1); /* Subtle glow */
}



.whiteboard-container {
  height: 300px;
  width: 100%;
  border: 0px solid #e2e8f0;
  border-radius: 0.5rem;
  overflow: hidden;
  position: relative;
  max-height: 300px;
  min-height: 300px;
}
.whiteboard-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

.edit-button {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 10;
  background-color: hsl(222.2 47.4% 11.2%);
  color: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
</style>
