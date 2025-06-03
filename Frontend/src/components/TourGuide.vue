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
    text: "This is your main navigation sidebar. You can collapse it, add new views, and manage all your tabs from here.",
    attachTo: {
      element: '[data-sidebar="sidebar"]',
      on: "right",
    },
    beforeShowPromise() {
      return new Promise((resolve) => {
        const isMobile = window.innerWidth < 768;

        // if (isMobile) {
        //   useUserStore().tourState = "sidebar";
        //   const sidebarTrigger = document.querySelector(
        //     '[data-tour="sidebar-trigger"]'
        //   );

        //   if (sidebarTrigger) {
        //     console.log("Opening sidebar for mobile tour");
        //     sidebarTrigger.click();

        //     // Wait longer and check for the element repeatedly
        //     let attempts = 0;
        //     const maxAttempts = 100; // 1 second total

        //     const checkForSidebar = () => {
        //       const sidebar = document.querySelector(
        //         '[data-sidebar="sidebar"]'
        //       );
        //       if (sidebar && sidebar.offsetWidth > 0) {
        //         console.error("Sidebar is now visible");
        //         resolve();
        //       } else if (attempts < maxAttempts) {
        //         attempts++;
        //         setTimeout(checkForSidebar, 50);
        //       } else {
        //         console.error("Timeout waiting for sidebar, continuing anyway");
        //         resolve();
        //       }
        //     };

        //     checkForSidebar();
        //   } else {
        //     resolve();
        //   }
        // } else {
        //   resolve();
        // }

        userStore.tourState = "expanded";
        resolve();
      });
    },
  });

  // Step 3: tab shortcuts
  tour.value.addStep({
    title: "⚡ Tab Shortcuts",
    text: "Here you can find some quick tab shortcuts you can also use <kbd>Cmd/Ctrl + J</kbd> to instantly search through all your notes and tags, or click here to open the search dialog.",
    attachTo: {
      element: '[data-tour="sidebar-links"]',
      on: "right",
    },
  });

  // Step 4: profile dropdown
  tour.value.addStep({
    title: "Profile",
    text: "This dropdown gives you access to your profile, settings, other tab types and quick actions. You can also access this tour again from here.",
    attachTo: {
      element: '[data-tour="sidebar-profile"]',
      on: "auto",
    },
    beforeShowPromise() {
      return new Promise((resolve) => {
        // Find and click the dropdown menu button
        const menuButton = document.querySelector(
          '[data-tour="sidebar-profile"]'
        );

        // code to open the dropdown but this messes with focus so not used for now
        // if (menuButton) {
        //   menuButton.click();

        //   // Wait for the dropdown to open
        //     setTimeout(() => {
        //     setTimeout(() => {
        //       const shepherdElement = document.querySelector('.shepherd-element');
        //       if (shepherdElement) {
        //       shepherdElement.focus();
        //       }
        //     }, 1000);

        //     resolve();
        //   }, 200);
        // } else {
        //   console.warn("Menu button not found");
        //   resolve();
        // }
        resolve();
      });
    },
  });

  tour.value.addStep({
    title: "Active Tab",
    text: "This is where the magic happens! when you open a tab, it will show up here. showing you exactly what you are working on. Right now we're on the dashboard tab, lets take a look ->",
    attachTo: {
      element: '[data-tour="tabContent"]',
      on: "left",
    },
    beforeShowPromise() {
      return new Promise((resolve) => {
        // Find and click the dropdown menu button
        // userStore.tourState = "";
        // const background = document.querySelector(
        //   '[data-tour="sidebar-profile"]'
        // );
        if (tabStore.activeTab.id !== 1) {
          console.error("Active tab is not dashboard, switching to it");
          tabStore.setActiveTab(1); // Set to dashboard tab
          //short delay
          setTimeout(resolve, 300);
        }

        userStore.tourState = "collapsed";

        resolve();
      });
    },
  });

  tour.value.addStep({
    title: "Recent Notes",
    text: "This section shows your most recent notes. You can click on any of these to open them directly in a new tab.",
    attachTo: {
      element: '[data-tour="dashboardRecentNotes"]',
      on: "auto",
    },
  });

  tour.value.addStep({
    title: "Shortcuts",
    text: "Here you can configure some shortcut buttons for quick access to your most used notes and tags. You can add, remove, or rearrange them as you like. To start just click the pencil icon to edit your shortcuts.",
    attachTo: {
      element: '[data-tour="dashboardShortcuts"]',
      on: "auto",
    },
  });

  tour.value.addStep({
    title: "Note Graph",
    text: "This is where the magic happens! Your note graph visualizes connections between notes, tags, and ideas. As you create content, you'll see your knowledge network grow here. It might look empty now, but lets add some structure to it!",
    attachTo: {
      element: '[data-tour="dashboardGraph"]',
      on: "auto",
    },
  });

  tour.value.addStep({
    title: "Create a Tag",
    text: "To make a tag, click the new button in the toolbar. This will open a dropdown in which you can select tag and give it a name. You can also use <kbd>T</kbd> to quickly create a new tag. The tour will automatically continue once you create a tag!",
    attachTo: {
      element: '[data-tour="dashboardGraph"]',
      on: "right",
    },
    when: {
      show() {
        // Record current count when step shows
        const initialCount = graphStore.elements.length;
        console.log(`Initial element count: ${initialCount}`);

        // Set up interval to check for increases
        const checkInterval = setInterval(() => {
          const currentCount = graphStore.elements.length;
          if (currentCount > initialCount) {
            console.log(
              `Elements increased from ${initialCount} to ${currentCount}. Auto-progressing...`
            );
            clearInterval(checkInterval);

            // Auto-progress after short delay to show the new element
            setTimeout(() => {
              if (tour.value && tour.value.getCurrentStep()) {
                tour.value.next();
              }
            }, 1500);
          }
        }, 500); // Check every 500ms

        // Store interval ID on the step for cleanup
        this.elementCheckInterval = checkInterval;
      },
      hide() {
        // Clean up interval when step is hidden
        if (this.elementCheckInterval) {
          clearInterval(this.elementCheckInterval);
          this.elementCheckInterval = null;
        }
      },
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
        text: "Skip / Tag Created!",
        classes: "shepherd-button-primary",
        action() {
          return this.next();
        },
      },
    ],
  });


  tour.value.addStep({
    title: "Great Job!",
    text: "You've created your first tag! Now you can start connecting it to notes and other tags. This will help you build a rich knowledge graph over time, with the tag selected we can now create a note and they will magically be connected!, to make a note, click the new button in the toolbar and select Document for now, alternatively you can use <kbd>N</kbd> to quickly create a new note.",
    attachTo: {
      element: '[data-tour="dashboardGraph"]',
      on: "right",
    },
    when: {
      show() {
        // Record current count when step shows
        const initialCount = graphStore.elements.length;
        console.log(`Initial element count: ${initialCount}`);

        // Set up interval to check for increases
        const checkInterval = setInterval(() => {
          const currentCount = graphStore.elements.length;
          if (currentCount > initialCount) {
            console.log(
              `Elements increased from ${initialCount} to ${currentCount}. Auto-progressing...`
            );
            clearInterval(checkInterval);

            // Auto-progress after short delay to show the new element
            setTimeout(() => {
              if (tour.value && tour.value.getCurrentStep()) {
                tour.value.next();
              }
            }, 1500);
          }
        }, 500); // Check every 500ms

        // Store interval ID on the step for cleanup
        this.elementCheckInterval = checkInterval;
      },
      hide() {
        // Clean up interval when step is hidden
        if (this.elementCheckInterval) {
          clearInterval(this.elementCheckInterval);
          this.elementCheckInterval = null;
        }
      },
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
        text: "Skip / Note Created!",
        classes: "shepherd-button-primary",
        action() {
          return this.next();
        },
      },
    ],
  });

  tour.value.addStep({
    title: "Great Job!",
    text: "With a note created you can see how it connects to the graph - if you want to make more connections later you can drag the red dot from a note to a tag or select from the dropdown in the note editor, deleting a connection is just as easy - simply hold down on the connecting line and drag to delete. Lets take a look at the note you just created! simply click on it in the graph to open it in a new tab.",
    attachTo: {
      element: '[data-tour="dashboardGraph"]',
      on: "auto",
    },
    when: {
    show() {
      // Record current active tab ID when step shows
      const initialTabId = tabStore.activeTab;
      console.error(`Initial active tab ID: ${initialTabId}`);
      
      // Set up interval to check for tab changes
      const checkInterval = setInterval(() => {
        const currentTabId = tabStore.activeTab;
        if (currentTabId !== initialTabId) {
          console.log(`Active tab changed from ${initialTabId} to ${currentTabId}. Auto-progressing...`);
          clearInterval(checkInterval);
          
          // Auto-progress after short delay to show the new tab
          setTimeout(() => {
            if (tour.value && tour.value.getCurrentStep()) {
              tour.value.next();
            }
          }, 1000);
        }
      }, 500); // Check every 500ms
      
      // Store interval ID on the step for cleanup
      this.tabCheckInterval = checkInterval;
    },
    hide() {
      // Clean up interval when step is hidden
      if (this.tabCheckInterval) {
        clearInterval(this.tabCheckInterval);
        this.tabCheckInterval = null;
      }
    }
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
      text: "Skip / Note Opened!",
      classes: "shepherd-button-primary",
      action() {
        return this.next();
      },
    },
  ],
  });

  tour.value.addStep({
    title: "Document Editor",
    text: "Welcome to the Document Editor! This is where you can write and format your notes. You can use Markdown for formatting, and all your changes will be saved automatically. Lets explore the editor a bit!",
    attachTo: {
      element: '',
      on: "auto",
    },
  });


  tour.value.addStep({
    title: "Toolbar",
    text: "The toolbar provides quick access to formatting options and note history",
    attachTo: {
      element: '[data-tour="tiptapToolbar"]',
      on: "auto",
    },
  });

  tour.value.addStep({
    title: "Main Content Area",
    text: "This is your main content area. Here you can see the note you just created. You can get typing write away,  use  <kbd>-</kbd>tabs,  <kbd>1. </kbd> numbered lists and many other common markdown shortcuts or even use the  <kbd>/</kbd> command whilst typing to select from a wide range of options.",
    attachTo: {
      element: '[data-tour="tiptapContent"]',
      on: "auto",
    },
  });

  tour.value.addStep({
    title: "Party Trick",
    text: "Earlier on you may have noticed the option to create a whiteboard rather than a docuement. Whilst docuemts are great for formatting beautiful typed notes, whiteboard excel at letting your creativity flourish and are perfect for brainstorming, mind mapping and sketching out ideas. whilst you can't draw in an editor you can easily attach a whiteboard preview, making it easy to integrate the two. To get started type the <kbd>/</kbd> command and start typing whiteboard, once it appears simply click the option.",
    attachTo: {
      element: '[data-tour="tiptapContent"]',
      on: "auto",
    },
    when: {
    show() {
      // Set up interval to check for whiteboard select popup
      const checkInterval = setInterval(() => {
        const whiteboardSelect = document.querySelector('[role="dialog"]');
        if (whiteboardSelect) {
          console.log('Whiteboard select popup appeared. Auto-progressing...');
          clearInterval(checkInterval);
          
          // Auto-progress after short delay to show the popup
          setTimeout(() => {
            if (tour.value && tour.value.getCurrentStep()) {
              tour.value.next();
            }
          }, 1000);
        }
      }, 500); // Check every 500ms
      
      // Store interval ID on the step for cleanup
      this.whiteboardCheckInterval = checkInterval;
    },
    hide() {
      // Clean up interval when step is hidden
      if (this.whiteboardCheckInterval) {
        clearInterval(this.whiteboardCheckInterval);
        this.whiteboardCheckInterval = null;
      }
    }
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
      text: "Skip / Popup Opened!",
      classes: "shepherd-button-primary",
      action() {
        return this.next();
      },
    },
  ],
  });


  tour.value.addStep({
    title: "Select whiteboard",
    text: "In this popup you can select an existing whiteboard or create a new one. As we haven't made one yet, lets create a new one. Simply type a name and click the create button and a new whiteboard will be created and attached to this note - dont worry this will automatically be added to your knowledge graph as well.",
    attachTo: {
      element: '[role="dialog"]',
      on: "auto",
    },
    when: {
    show() {
      // Set up interval to check for when whiteboard select popup disappears
      const checkInterval = setInterval(() => {
        const whiteboardSelect = document.querySelector('[role="dialog"]');
        if (!whiteboardSelect) {
          console.log('Whiteboard select popup disappeared. Auto-progressing...');
          clearInterval(checkInterval);
          
          // Auto-progress after short delay
          setTimeout(() => {
            if (tour.value && tour.value.getCurrentStep()) {
              tour.value.next();
            }
          }, 500);
        }
      }, 500); // Check every 500ms
      
      // Store interval ID on the step for cleanup
      this.whiteboardCheckInterval = checkInterval;
    },
    hide() {
      // Clean up interval when step is hidden
      if (this.whiteboardCheckInterval) {
        clearInterval(this.whiteboardCheckInterval);
        this.whiteboardCheckInterval = null;
      }
    }
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
      text: "Skip / Whiteboard Created!",
      classes: "shepherd-button-primary",
      action() {
        return this.next();
      },
    },
  ],
  });

  tour.value.addStep({
    title: "Whiteboard Preview",
    text: "Great! You now have a whiteboard attached to your note.You may however notice it is looking a little blank! to solve this lets click on the edit button in the top right to open it in a new tab and start sketching out your ideas. This is a powerful way to visualize your thoughts and connect them to your notes.",
    attachTo: {
      element: '.whiteboard-embed',
      on: "auto",
    },
    when: {
    show() {
      // Record current active tab ID when step shows
      const initialTabId = tabStore.activeTab;
      console.log(`Initial active tab ID: ${initialTabId}`);
      
      // Set up interval to check for tab changes (when edit button is clicked)
      const checkInterval = setInterval(() => {
        const currentTabId = tabStore.activeTab;
        if (currentTabId !== initialTabId) {
          console.log(`Active tab changed from ${initialTabId} to ${currentTabId}. Auto-progressing...`);
          clearInterval(checkInterval);
          
          // Auto-progress after short delay to show the new tab
          setTimeout(() => {
            if (tour.value && tour.value.getCurrentStep()) {
              tour.value.next();
            }
          }, 200);
        }
      }, 500); // Check every 500ms
      
      // Store interval ID on the step for cleanup
      this.tabCheckInterval = checkInterval;
    },
    hide() {
      // Clean up interval when step is hidden
      if (this.tabCheckInterval) {
        clearInterval(this.tabCheckInterval);
        this.tabCheckInterval = null;
      }
    }
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
      text: "Skip / Whiteboard Opened!",
      classes: "shepherd-button-primary",
      action() {
        return this.next();
      },
    },
  ],
  });

  tour.value.addStep({
    title: "Whiteboard Editor",
    text: "Welcome to the Whiteboard Editor! This is where you can draw, sketch, and brainstorm your ideas. You can use various tools to create shapes, draw freehand, and even add images. All your changes will be saved automatically. Lets explore the editor a bit!",
    attachTo: {
      element: '',
      on: "auto",
    },
  });


  tour.value.addStep({
    title: "Toolbar",
    text: "The toolbar provides quick access to input modes (auto to switch based on if a stylus/finger is used or a mouse, draw or select), pen controls, other tools and note history",
    attachTo: {
      element: '[data-tour="whiteboardToolbar"]',
      on: "auto",
    },
    scrollTo: false,
  });

  tour.value.addStep({
    title: "Main Content Area",
    text: "This is your main content area. Here you can see the whiteboard you just created. You can get drawing right away, use the pen tool to draw freehand, or select shapes and images from the toolbar.",
    attachTo: {
      element: '[data-tour="whiteboardCanvas"]',
      on: "auto",
    },
    scrollTo: false,
    buttons: [
    {
      text: "Back",
      classes: "shepherd-button-secondary",
      action() {
        return this.back();
      },
    },
    {
      text: "Back to the Dashboard",
      classes: "shepherd-button-primary",
      action() {
        // Switch back to the dashboard tab
        tabStore.setActiveTab(1); // Assuming 1 is the dashboard tab ID
        setTimeout(() => {
          return this.next();
        }, 500);
        // return this.next();
      },
    },
  ],
  });

  tour.value.addStep({
    title: "Wrapping up",
    text: "That's it for the tour! You've learned the basics of NeuroNote, including how to create notes, tags, and whiteboards. You can always access this tour again from your profile menu if you need a refresher. We hope you enjoy using NeuroNote to manage your knowledge and ideas!, if you ever need help, you can find more resources in the help section of your profile menu and if you have any feedback or suggestions, please fill out the feedback form in the profile dropdown",
    attachTo: {
      element: '',
      on: "auto",
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

  

  // Tour event handlers
  tour.value.on("complete", () => {
    useUserStore().tourState = "";
    isActive.value = false;
    localStorage.setItem("vault-tour-completed", "true");
    emit("tourComplete");
  });

  tour.value.on("cancel", () => {
    useUserStore().tourState = "";
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

body.shepherd-active * {
  pointer-events: none !important;
}

body.shepherd-active .shepherd-element,
body.shepherd-active .shepherd-element *,
body.shepherd-active .shepherd-modal-overlay-container,
body.shepherd-active .shepherd-modal-overlay-container * {
  pointer-events: auto !important;
}
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
