<template>
  <node-view-wrapper class="chemistry-component">
    <div id="location" class="border rounded-2xl shadow-md p-4 "></div>
  </node-view-wrapper>
</template>

<script setup>
import { onMounted, ref, watch } from "vue";
import { nodeViewProps, NodeViewWrapper } from "@tiptap/vue-3";
import { useUserStore } from "@/stores/useUserStore";
// import { Kekule } from "kekule";
// import "kekule/theme/default"; // if Kekule widgets is used in browser, the theme CSS should be imported as well
// console.error(Kekule.VERSION);

// for adding colour to 2d 

// var viewer = Kekule.Widget.getWidgetById('chemViewer2D');
// viewer.getRenderConfigs().getColorConfigs().setUseAtomSpecifiedColor(true);
// // ......
// viewer.setChemObj(mol);


const theme = ref(useUserStore().theme);
onMounted(() => {
  fetch("/6-meo-thh__.mol")
    .then((res) => res.text())
    .then((data) => {
      const mol = Kekule.IO.loadFormatData(data, "mol");
      var viewer = new Kekule.ChemWidget.Viewer3D(
        document.getElementById("location")
      );
      viewer.setEnableToolbar(false);
      viewer.setChemObj(mol);
      // viewer.setRenderType(Kekule.Render.RendererType.WEBGL);
      viewer.setEnableTouchInteraction(true);
      viewer.setDimension("500px", "250px");
      viewer.setAutofit(true);
      viewer.getRenderConfigs().getEnvironmentConfigs().setGraphicQuality(Kekule.Render.Render3DGraphicQuality.EXTREME_HIGH); 

    
   
        viewer.setBackgroundColor("transparent");
   
  
    });
  // chemViewer.setMoleculeDisplayType(Kekule.Render.Molecule2DDisplayType.SKELETAL/CONDENSED);
});

// var chemViewer = new Kekule.ChemWidget.Viewer(document);
// chemViewer.setDimension('500px', '400px');
// chemViewer.appendToElem(document.getElementById('location')).setChemObj(mol);
</script>

<style scoped>
/* Optional: tweak canvas background etc. */
</style>
