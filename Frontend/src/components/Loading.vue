<template>
  <div v-if="isLoading" class="loading-overlay">
    <div class="loading-spinner">
      <svg viewBox="25 25 50 50">
        <circle cx="50" cy="50" r="20" fill="none" stroke-width="3" stroke-miterlimit="10"></circle>
      </svg>
      <div class="spinner-shadow"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

const isLoading = ref(false);

onMounted(() => {
  isLoading.value = true; // Show the loader when the component is mounted
  console.log("Loading component mounted");
});

onUnmounted(() => {
  isLoading.value = false; // Hide the loader when the component is unmounted
  console.log("Loading component unmounted");
});
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* background-color: rgba(20, 15, 30, 0.8); Darker background with purple tint */
  @apply bg-[rgba(245,240,255,0.85)] dark:bg-[rgba(20,15,30,0.8)];
  /* bg-[rgba(245,240,255,0.85)] */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* Ensure it appears above other elements */
}

.loading-spinner {
  position: relative;
  width: 150px; /* Larger spinner */
  height: 150px;
  filter: drop-shadow(0 0 15px rgba(128, 90, 213, 0.6)); /* Purple glow effect */
}

.loading-spinner svg {
  animation: spin 2s linear infinite;
  filter: drop-shadow(0 0 8px rgba(138, 73, 226, 0.5));
}

.spinner-shadow {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(149, 76, 233, 0.3) 0%, transparent 70%);
  transform: translate(-50%, -50%);
  animation: pulse 2s ease-in-out infinite alternate;
}

.loading-spinner circle {
  stroke: #9c5cff; /* Purple color */
  stroke-dasharray: 150, 200;
  stroke-dashoffset: -10;
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

@keyframes pulse {
  0% {
    opacity: 0.4;
    transform: translate(-50%, -50%) scale(0.8);
  }
  100% {
    opacity: 0.8;
    transform: translate(-50%, -50%) scale(1.2);
  }
}

@keyframes dash {
  0% {
    stroke-dasharray: 1, 200;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 89, 200;
    stroke-dashoffset: -35;
  }
  100% {
    stroke-dasharray: 89, 200;
    stroke-dashoffset: -124;
  }
}
</style>