<script setup>
// Wait for Three.js to load
function waitForThree() {
  return new Promise((resolve) => {
    const check = () => {
      if (typeof THREE !== "undefined") {
        resolve();
      } else {
        setTimeout(check, 50);
      }
    };
    check();
  });
}

waitForThree().then(() => {
  // Three.js setup
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  const renderer = new THREE.WebGLRenderer({
    canvas: document.getElementById("bg"),
    alpha: true,
  });
  renderer.setSize(window.innerWidth, window.innerHeight);

  const group = new THREE.Group();
  scene.add(group);

  // Create nodes
  const nodeCount = 1000;
  const nodes = Array.from({ length: nodeCount }, (_, i) => ({
    id: i,
    x: (Math.random() - 0.5) * 20,
    y: (Math.random() - 0.5) * 20,
    z: (Math.random() - 0.5) * 20,
    vx: 0,
    vy: 0,
    vz: 0,
    connections: [],
  }));

  const links = [];
  const linkLines = [];

  // Create Three.js meshes for nodes
  const sphereGeo = new THREE.SphereGeometry(0.1, 8, 8);
  const sphereMat = new THREE.MeshBasicMaterial({ color: 0xa855f7 });
  const lineMat = new THREE.LineBasicMaterial({
    color: 0xc084fc,
    transparent: true,
    opacity: 0.4,
  });

  nodes.forEach((node) => {
    const mesh = new THREE.Mesh(sphereGeo, sphereMat);
    mesh.position.set(node.x, node.y, node.z);
    group.add(mesh);
    node.mesh = mesh;
  });

  // Simple force-directed layout simulation
  function applyForces() {
    const damping = 0.9;
    const repulsion = 0.5;
    const attraction = 0.002;
    const linkDistance = 2;

    // Reset forces
    nodes.forEach((node) => {
      node.fx = 0;
      node.fy = 0;
      node.fz = 0;
    });

    // Repulsion between all nodes
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dx = nodes[i].x - nodes[j].x;
        const dy = nodes[i].y - nodes[j].y;
        const dz = nodes[i].z - nodes[j].z;
        const distance = Math.sqrt(dx * dx + dy * dy + dz * dz) + 0.1;

        const force = repulsion / (distance * distance);

        nodes[i].fx += (dx / distance) * force;
        nodes[i].fy += (dy / distance) * force;
        nodes[i].fz += (dz / distance) * force;

        nodes[j].fx -= (dx / distance) * force;
        nodes[j].fy -= (dy / distance) * force;
        nodes[j].fz -= (dz / distance) * force;
      }
    }

    // Attraction for connected nodes
    links.forEach((link) => {
      const dx = link.target.x - link.source.x;
      const dy = link.target.y - link.source.y;
      const dz = link.target.z - link.source.z;
      const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);
      const force = (distance - linkDistance) * attraction;

      link.source.fx += (dx / distance) * force;
      link.source.fy += (dy / distance) * force;
      link.source.fz += (dz / distance) * force;

      link.target.fx -= (dx / distance) * force;
      link.target.fy -= (dy / distance) * force;
      link.target.fz -= (dz / distance) * force;
    });

    // Apply forces and update positions
    nodes.forEach((node) => {
      node.vx = (node.vx + node.fx) * damping;
      node.vy = (node.vy + node.fy) * damping;
      node.vz = (node.vz + node.fz) * damping;

      node.x += node.vx;
      node.y += node.vy;
      node.z += node.vz;

      // Update mesh position
      node.mesh.position.set(node.x, node.y, node.z);
    });

    // Update link lines
    links.forEach((link, i) => {
      if (linkLines[i]) {
        const points = [
          new THREE.Vector3(link.source.x, link.source.y, link.source.z),
          new THREE.Vector3(link.target.x, link.target.y, link.target.z),
        ];
        linkLines[i].geometry.dispose();
        linkLines[i].geometry = new THREE.BufferGeometry().setFromPoints(
          points
        );
      }
    });
  }

  // Function to add a new link
  function addRandomLink() {
    if (links.length >= 100000) return;

    const a = Math.floor(Math.random() * nodes.length);
    const b = Math.floor(Math.random() * nodes.length);

    if (a === b) return;

    // Check if link already exists
    const exists = links.some(
      (link) =>
        (link.source === nodes[a] && link.target === nodes[b]) ||
        (link.source === nodes[b] && link.target === nodes[a])
    );

    if (exists) return;

    // Add new link
    const newLink = { source: nodes[a], target: nodes[b] };
    links.push(newLink);

    // Update node connections
    nodes[a].connections.push(nodes[b]);
    nodes[b].connections.push(nodes[a]);

    // Create Three.js line
    const geometry = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(nodes[a].x, nodes[a].y, nodes[a].z),
      new THREE.Vector3(nodes[b].x, nodes[b].y, nodes[b].z),
    ]);
    const line = new THREE.Line(geometry, lineMat);
    group.add(line);
    linkLines.push(line);
  }

  // Gradually add links
  setTimeout(() => {
    const linkInterval = setInterval(addRandomLink, 60);
    setTimeout(() => clearInterval(linkInterval), 240000);
  }, 1000);

  camera.position.z = 15;

  function animate() {
    requestAnimationFrame(animate);

    // Apply physics simulation
    applyForces();

    // Gentle rotation
    group.rotation.y += 0.003;
    group.rotation.x += 0.001;

    renderer.render(scene, camera);
  }

  animate();

  // Handle window resize
  window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
});
</script>

<style lang="scss">
html {
  scroll-behavior: smooth;
}

::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(147, 51, 234, 0.3);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(147, 51, 234, 0.5);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}


#hero {

  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 0;
  height: 100%;
  font-family:
    "Inter",
    -apple-system,
    BlinkMacSystemFont,
    sans-serif;
  background: linear-gradient(135deg, #0a0a0a 0%, #1a0a2e 30%, #16213e 100%);
  color: white;
  overflow-x: hidden;
}

canvas {
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: block;
}

.content-wrapper {

}




</style>



<template>
  <!-- Fixed background simulation -->
  <section id="hero">
    <canvas id="bg"></canvas>
  </section>
</template>

