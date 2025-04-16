
<template>
 <node-view-wrapper class="chemistry-component">
  
  <div id="location" class="border rounded-2xl h-full shadow-md p-4 bg-white">
  
  </div>
</node-view-wrapper>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { nodeViewProps, NodeViewWrapper } from '@tiptap/vue-3'
import { Kekule } from 'kekule';
import 'kekule/theme/default';       // if Kekule widgets is used in browser, the theme CSS should be imported as well
console.error(Kekule.VERSION);

var mol = new Kekule.Molecule();

// add atoms to molecule
mol.appendNode(new Kekule.Atom().setSymbol('B').setExplicitHydrogenCount(2).setCoord2D({x: -1, y: 0}));
mol.appendNode(new Kekule.Atom().setSymbol('B').setExplicitHydrogenCount(2).setCoord2D({x: 1, y: 0}));
mol.appendNode(new Kekule.Atom().setSymbol('H').setCoord2D({x: 0, y: 1}));
mol.appendNode(new Kekule.Atom().setSymbol('H').setCoord2D({x: 0, y: -1}));
// add two multicenter bond: B-H-B
mol.appendBond([0, 2, 1], 1);
mol.appendBond([0, 3, 1], 1);

onMounted(() => {
// create a viewer and set its dimension
// the viewer will be appended to the element with id 'location'
// the viewer will display the molecule created above

//VIEWER ALLOWS FOR CHANGING BETWEEN 2D AND 3D BUT LOSES IPAD INTERACTIVITY SO USE Viewer3D and VIEWER 2D BELOW
//   var chemViewer = new Kekule.ChemWidget.Viewer(document);

//   chemViewer.setDimension('100%', '100%');
//   chemViewer.appendToElem(document.getElementById('location')).setChemObj(mol);
//   // display 3D molecule in space fill model
// chemViewer.setRenderType(Kekule.Render.RendererType.R3D);
// chemViewer.setEnableToolbar(true);



// var viewer = new Kekule.ChemWidget.Viewer3D(document.getElementById('location'));
// viewer.setEnableToolbar(false);
// viewer.setChemObj(mol);
// // viewer.setRenderType(Kekule.Render.RendererType.WEBGL);
// viewer.setEnableTouchInteraction(true);
// viewer.setDimension('100%', '100%');


fetch('/6-meo-thh__.mol')
.then(res => res.text())
.then(data => {
const mol = Kekule.IO.loadFormatData(data, 'mol');
var viewer = new Kekule.ChemWidget.Viewer3D(document.getElementById('location'));
viewer.setEnableToolbar(false);
viewer.setChemObj(mol);
// viewer.setRenderType(Kekule.Render.RendererType.WEBGL);
viewer.setEnableTouchInteraction(true);
viewer.setDimension('100%', '250px');

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