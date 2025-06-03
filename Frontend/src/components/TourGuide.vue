<!-- TourGuide.vue -->
<template>
  <!-- Tour will be handled by Shepherd.js directly, no template needed -->
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from "vue";
import Shepherd from "shepherd.js";
import { useGraphStore } from "@/stores/useGraphStore";
import { useTabStore } from "@/stores/useTabStore";
import { useUserStore } from "@/stores/useUserStore";

// Props
const props = defineProps<{
  shouldStart?: boolean;
  triggerTour?: boolean;
}>();

// Emits
const emit = defineEmits<{
  tourComplete: [];
  tourCancel: [];
}>();

// Stores
const graphStore = useGraphStore();
const tabStore = useTabStore();
const userStore = useUserStore();

// Reactive state
const tour = ref<Shepherd.Tour | null>(null);
const isActive = ref(false);

// Check if user is new (no graph elements)
// const isNewUser = computed(() => {
//   return graphStore.elements.length === 0
// })
const isNewUser = true;

function createTour() {
  if (tour.value) {
    tour.value.complete();
  }

  tour.value = new Shepherd.Tour({
    useModalOverlay: true,
    defaultStepOptions: {
      classes: "shepherd-theme-custom",
      scrollTo: true,
      cancelIcon: {
        enabled: true,
      },
      when: {
        show() {
          // Add any global show logic here
        },
        hide() {
          // Add any global hide logic here
        },
      },
    },
  });

  // Step 1: Welcome
  tour.value.addStep({
    title: "🎉 Welcome to NeuroNote!",
    text: "Let's take a quick tour to get you started with your knowledge management system. This will only take a minute!",
    buttons: [
      {
        text: "Skip Tour",
        classes: "shepherd-button-secondary",
        action() {
          return this.cancel();
        },
      },
      {
        text: "Start Tour",
        classes: "shepherd-button-primary",
        action() {
          return this.next();
        },
      },
    ],
  });

  // Step 2: Sidebar
  tour.value.addStep({
    title: "Navigation Sidebar",
    text: "This is your main navigation sidebar. You can collapse it, search through your content, and manage all your tabs from here.",
    attachTo: {
      element: '[data-sidebar="sidebar"]',
      on: "right",
    },
    beforeShowPromise() {
      return new Promise((resolve) => {
        const isMobile = window.innerWidth < 768;
        
        if (isMobile) {
          const sidebarTrigger = document.querySelector('[data-tour="sidebar-trigger"]');
          
          if (sidebarTrigger) {
            console.log("Opening sidebar for mobile tour");
            sidebarTrigger.click();
            
            // Wait longer and check for the element repeatedly
            let attempts = 0;
            const maxAttempts = 100; // 1 second total
            
            const checkForSidebar = () => {
              const sidebar = document.querySelector('[data-sidebar="sidebar"]');
              if (sidebar && sidebar.offsetWidth > 0) {
                console.error("Sidebar is now visible");
                resolve();
              } else if (attempts < maxAttempts) {
                attempts++;
                setTimeout(checkForSidebar, 50);
              } else {
                console.error("Timeout waiting for sidebar, continuing anyway");
                resolve();
              }
            };
            
            checkForSidebar();
          } else {
            resolve();
          }
        } else {
          resolve();
        }
      });
    },
    buttons: [
      {
        text: "Back",
        classes: "shepherd-button-secondary",
        action() {
          return this.back();
        },
      },
      {
        text: "Next",
        classes: "shepherd-button-primary",
        action() {
          return this.next();
        },
      },
    ],
  });

  // Step 3: Search
  tour.value.addStep({
    title: "⚡ Quick Search",
    text: "Here you can find some quick tab shortcuts you can also use <kbd>Cmd/Ctrl + J</kbd> to instantly search through all your notes and tags, or click here to open the search dialog.",
    attachTo: {
      element: '[data-tour="sidebar-links"]',
      on: "right",
    },
    buttons: [
      {
        text: "Back",
        classes: "shepherd-button-secondary",
        action() {
          return this.back();
        },
      },
      {
        text: "Next",
        classes: "shepherd-button-primary",
        action() {
          return this.next();
        },
      },
    ],
  });

  // Step 4: Dashboard
  tour.value.addStep({
    title: "📊 Your Dashboard",
    text: "Your dashboard provides an overview of your knowledge graph, recent activity, and quick access to your most important content.",
    attachTo: {
      element: '[data-tour="dashboard-tab"]',
      on: "right",
    },
    beforeShowPromise() {
      tabStore.setActiveTab(1);
      return new Promise((resolve) => setTimeout(resolve, 300));
    },
    buttons: [
      {
        text: "Back",
        classes: "shepherd-button-secondary",
        action() {
          return this.back();
        },
      },
      {
        text: "Next",
        classes: "shepherd-button-primary",
        action() {
          return this.next();
        },
      },
    ],
  });

  // Step 5: Add New Tab
  tour.value.addStep({
    title: "➕ Create New Content",
    text: "Click this plus button to create new tabs with graphs, open settings, or access other features. This is where you'll start building your knowledge base.",
    attachTo: {
      element: '[data-tour="add-tab"]',
      on: "right",
    },
    buttons: [
      {
        text: "Back",
        classes: "shepherd-button-secondary",
        action() {
          return this.back();
        },
      },
      {
        text: "Create Graph",
        classes: "shepherd-button-primary",
        action() {
          tabStore.addTab("My First Graph", "graph");
          return this.next();
        },
      },
    ],
  });

  // Step 6: Graph Interface
  tour.value.addStep({
    title: "🕸️ Knowledge Graph",
    text: "This is where the magic happens! Your knowledge graph visualizes connections between notes, tags, and ideas. As you create content, you'll see your knowledge network grow here.",
    attachTo: {
      element: '[data-tour="main-content"]',
      on: "top",
    },
    beforeShowPromise() {
      return new Promise((resolve) => setTimeout(resolve, 500));
    },
    buttons: [
      {
        text: "Back",
        classes: "shepherd-button-secondary",
        action() {
          return this.back();
        },
      },
      {
        text: "Next",
        classes: "shepherd-button-primary",
        action() {
          return this.next();
        },
      },
    ],
  });

  // Step 7: Tab Management
  tour.value.addStep({
    title: "📑 Tab Management",
    text: "Each tab represents different views or content. You can drag to reorder them, close with the X button, and easily switch between different contexts.",
    attachTo: {
      element: '[data-tour="tabs-section"]',
      on: "right",
    },
    buttons: [
      {
        text: "Back",
        classes: "shepherd-button-secondary",
        action() {
          return this.back();
        },
      },
      {
        text: "Next",
        classes: "shepherd-button-primary",
        action() {
          return this.next();
        },
      },
    ],
  });

  // Step 8: Profile Menu
  tour.value.addStep({
    title: "⚙️ Your Profile & More",
    text: "Access your profile settings, sync your data, get help, and manage your account from this dropdown menu.",
    attachTo: {
      element: '[data-tour="profile-menu"]',
      on: "top",
    },
    buttons: [
      {
        text: "Back",
        classes: "shepherd-button-secondary",
        action() {
          return this.back();
        },
      },
      {
        text: "Finish Tour",
        classes: "shepherd-button-primary",
        action() {
          return this.complete();
        },
      },
    ],
  });

  // Step 9: Completion
  tour.value.addStep({
    title: "🚀 You're All Set!",
    text: "Congratulations! You now know the basics of Vault. Start by creating some notes and tags to build your knowledge graph. You can always access this tour again from your profile menu.",
    buttons: [
      {
        text: "Start Building!",
        classes: "shepherd-button-primary",
        action() {
          return this.complete();
        },
      },
    ],
  });

  // Tour event handlers
  tour.value.on("complete", () => {
    isActive.value = false;
    localStorage.setItem("vault-tour-completed", "true");
    emit("tourComplete");
  });

  tour.value.on("cancel", () => {
    isActive.value = false;
    localStorage.setItem("vault-tour-completed", "true");
    emit("tourCancel");
  });

  return tour.value;
}

function startTour() {
  console.log("Starting tour...");
  const newTour = createTour();
  isActive.value = true;
  newTour.start();
}

function checkAndStartTourForNewUser() {
  if (isNewUser) {
    console.error("New user detected, starting tour...");
    setTimeout(() => {
      startTour();
    }, 1500); // Give UI time to load
  }
}

// Watch for trigger prop changes
watch(
  () => props.triggerTour,
  (shouldTrigger) => {
    if (shouldTrigger) {
      startTour();
    }
  }
);

// Auto-start for new users
onMounted(() => {
  console.error("Mounted TourGuide component");

  if (props.shouldStart) {
    checkAndStartTourForNewUser();
  }
});

onUnmounted(() => {
  if (tour.value) {
    tour.value.complete();
  }
});

// Expose methods for parent component
defineExpose({
  startTour,
});
</script>

<style>
/* Import Shepherd CSS */
@import "shepherd.js/dist/css/shepherd.css";


/* Custom Shepherd Styles */
.shepherd-theme-custom {
  max-width: 400px;
  border-radius: 0.5rem;
  box-shadow:
    0 20px 25px -5px rgb(0 0 0 / 0.1),
    0 10px 10px -5px rgb(0 0 0 / 0.04);
}

.shepherd-element {
  z-index: 9999 !important;
}

.shepherd-modal-overlay-container {
  z-index: 9998 !important;
}

.shepherd-header {
  background: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
  padding: 1rem;
  border-radius: 0.5rem 0.5rem 0 0;
  font-weight: 600;
}

.shepherd-text {
  padding: 1.25rem;
  font-size: 0.875rem;
  line-height: 1.6;
  color: hsl(var(--foreground));
}

.shepherd-text kbd {
  background: hsl(var(--muted));
  color: hsl(var(--muted-foreground));
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  border: 1px solid hsl(var(--border));
}

.shepherd-footer {
  padding: 0.75rem 1.25rem;
  border-top: 1px solid hsl(var(--border));
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  background: hsl(var(--background));
  border-radius: 0 0 0.5rem 0.5rem;
}

.shepherd-button {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 2.25rem;
}

.shepherd-button-primary {
  background: hsl(var(--primary));
  color: hsl(var(--primary-foreground));
}

.shepherd-button-primary:hover {
  background: hsl(var(--primary) / 0.9);
}

.shepherd-button-secondary {
  background: hsl(var(--secondary));
  color: hsl(var(--secondary-foreground));
  border: 1px solid hsl(var(--border));
}

.shepherd-button-secondary:hover {
  background: hsl(var(--secondary) / 0.8);
}

.shepherd-cancel-icon {
  color: hsl(var(--muted-foreground));
  transition: color 0.2s ease;
}

.shepherd-cancel-icon:hover {
  color: hsl(var(--foreground));
}

/* Dark mode adjustments */
@media (prefers-color-scheme: dark) {
  .shepherd-element {
    background: hsl(var(--background));
    border: 1px solid hsl(var(--border));
  }
}
</style>
