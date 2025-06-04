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

// const isNewUser = true;

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
      modalOverlayOpeningRadius: 10,
      modalOverlayOpeningPadding: 0,
      
      buttons: [
        {
          text: "← Back",
          classes: "shepherd-button-secondary",
          action() {
            return this.back();
          },
        },
        {
          text: "Next →",
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
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">Let's take a quick tour to get you started with your knowledge management system.</p>
    </div>
    
   
    
    <p style="margin: 16px 0 0 0; color: hsl(var(--muted-foreground)); font-size: 0.85em; text-align: center; font-style: italic;">
      Estimated time about 2 minutes
    </p>
  `,
    buttons: [
      {
        text: "Skip Tour",
        classes: "shepherd-button-secondary",
        action() {
          return this.cancel();
        },
      },
      {
        text: "Start Tour →",
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
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">This is your main navigation sidebar where you can manage all your tabs and navigate between different views.</p>
    </div>
    
    <div style="margin: 16px 0;">
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Collapse or expand the sidebar for more screen space</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Create new tabs and organize your workspace</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Switch between different types of content</p>
    </div>
    
    <div style="background: hsl(var(--accent) / 0.6); padding: 14px; border-radius: 8px; margin: 16px 0; border-left: 3px solid hsl(var(--accent-foreground));">
      <p style="margin: 0; font-size: 0.85em; color: hsl(var(--foreground) / 0.9);">
        <strong style="color: hsl(var(--accent-foreground));">💡 Quick tip:</strong> Use <kbd>Cmd/Ctrl + /</kbd> to quickly toggle the sidebar!
      </p>
    </div>
  `,
    attachTo: {
      element: '[data-sidebar="sidebar"]',
      on: "right",
    },
    beforeShowPromise() {
      return new Promise((resolve) => {
        const isMobile = window.innerWidth < 768;
        userStore.tourState = "expanded";
        resolve();
      });
    },
  });

  // Step 3: tab shortcuts
  tour.value.addStep({
    title: "Tab Shortcuts",
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">Here you can find some quick tab shortcuts for easy navigation around your workspace.</p>
    </div>
    
    <div style="margin: 16px 0;">
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Click any shortcut to quickly open that section</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Use the search button to find specific notes and tags</p>
    </div>
    
    <div style="background: hsl(var(--accent) / 0.6); padding: 14px; border-radius: 8px; margin: 16px 0; border-left: 3px solid hsl(var(--accent-foreground));">
      <p style="margin: 0; font-size: 0.85em; color: hsl(var(--foreground) / 0.9);">
        <strong style="color: hsl(var(--accent-foreground));">⚡ Power user tip:</strong> Use <kbd>Cmd/Ctrl + J</kbd> to instantly search through all your notes and tags!
      </p>
    </div>
  `,
    attachTo: {
      element: '[data-tour="sidebar-links"]',
      on: "right",
    },
  });

  // Step 4: profile dropdown
  tour.value.addStep({
    title: "Profile",
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">This dropdown gives you access to your profile, settings, and other important features.</p>
    </div>
    
    <div style="margin: 16px 0;">
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Access your profile and account settings</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Give feedback and access Legal documents</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Find quick actions and help resources</p>
    </div>
    
    <div style="background: hsl(var(--accent) / 0.6); padding: 14px; border-radius: 8px; margin: 16px 0; border-left: 3px solid hsl(var(--accent-foreground));">
      <p style="margin: 0; font-size: 0.85em; color: hsl(var(--foreground) / 0.9);">
        <strong style="color: hsl(var(--accent-foreground));">🔄 Come back anytime:</strong> You can restart this tour from the help section in this menu!
      </p>
    </div>
  `,
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
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">This is where the magic happens! When you open a tab, it will show up here, showing you exactly what you are working on.</p>
      <p style="margin: 8px 0; font-size: 0.9em;">Right now we're on the dashboard tab - let's explore what it offers!</p>
    </div>
    
    <div style="background: hsl(var(--accent) / 0.6); padding: 14px; border-radius: 8px; margin: 16px 0; border-left: 3px solid hsl(var(--accent-foreground));">
      <p style="margin: 0; font-size: 0.85em; color: hsl(var(--foreground) / 0.9);">
        <strong style="color: hsl(var(--accent-foreground));">💡 Navigation tip:</strong> You can switch between tabs using the sidebar
      </p>
    </div>
  `,
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
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">This section shows your most recent notes. You can click on any of these to open them directly in a new tab.</p>
    </div>`,
    attachTo: {
      element: '[data-tour="dashboardRecentNotes"]',
      on: "auto",
    },
  });

  tour.value.addStep({
    title: "Shortcuts",
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">Here you can configure some shortcut buttons for quick access to your most used notes and tags. You can add, remove, or rearrange them as you like.</p>
    </div>
    
    <div style="margin: 16px 0;">
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Click the pencil icon to edit your shortcuts</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Give them a fun, descriptive name</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Add your favorite notes and tags for instant access</p>
    </div>
    
    <div style="background: hsl(var(--accent) / 0.6); padding: 14px; border-radius: 8px; margin: 16px 0; border-left: 3px solid hsl(var(--accent-foreground));">
      <p style="margin: 0; font-size: 0.85em; color: hsl(var(--foreground) / 0.9);">
        <strong style="color: hsl(var(--accent-foreground));">⚡ Productivity boost:</strong> Create shortcuts for your most important content to save time!
      </p>
    </div>
  `,
    attachTo: {
      element: '[data-tour="dashboardShortcuts"]',
      on: "auto",
    },
  });

  tour.value.addStep({
    title: "Note Graph",
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">Ready to be amazed? Your note graph visualizes connections between notes, tags, and ideas. As you create content, you'll see your knowledge network grow here.</p>
      <p style="margin: 8px 0; font-size: 0.9em;">It might look empty now, but let's add some structure to it!</p>
    </div>
    
    <div style="margin: 16px 0;">
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Watch connections form as you link notes and tags</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Use filters to find exactly what you need, and spotlight to highlight the details </p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Click on any element to open it directly</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> If you fancy a change of scenery just press shuffly and watch the engine create beautiful layouts</p>
    </div>
    
    <div style="background: hsl(var(--accent) / 0.6); padding: 14px; border-radius: 8px; margin: 16px 0; border-left: 3px solid hsl(var(--accent-foreground));">
      <p style="margin: 0; font-size: 0.85em; color: hsl(var(--foreground) / 0.9);">
        <strong style="color: hsl(var(--accent-foreground));">🧠 Knowledge mapping:</strong> This visual representation helps you find your notes and discover unexpected connections between your ideas!
      </p>
    </div>
  `,
    attachTo: {
      element: '[data-tour="dashboardGraph"]',
      on: "auto",
    },
  });

  tour.value.addStep({
    title: "🏷️ Create Your First Tag",
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">1.</strong> Click the <kbd>+ New</kbd> button in the toolbar above the graph</p>
      <p style="margin: 8px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">2.</strong> Select <kbd>Tag</kbd> from the dropdown menu</p>
      <p style="margin: 8px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">3.</strong> Give your tag a name (e.g. "My First Tag")</p>
    </div>
    
    <div style="background: hsl(var(--accent) / 0.6); padding: 14px; border-radius: 8px; margin: 16px 0; border-left: 3px solid hsl(var(--accent-foreground));">
      <p style="margin: 0; font-size: 0.85em; color: hsl(var(--foreground) / 0.9);">
        <strong style="color: hsl(var(--accent-foreground));">💡 Quick tip:</strong> You can also press <kbd>T</kbd> as a shortcut!
      </p>
    </div>
    
    <p style="margin: 16px 0 0 0; color: hsl(var(--muted-foreground)); font-size: 0.85em; text-align: center; font-style: italic;">
      The tour will automatically continue once you create your tag
    </p>
  `,
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
            }, 300);
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
        text: "← Back",
        classes: "shepherd-button-secondary",
        action() {
          return this.back();
        },
      },
      {
        text: "Skip this step →",
        classes: "shepherd-button-primary",
        action() {
          return this.next();
        },
      },
    ],
  });

  tour.value.addStep({
    title: "📝 Create Your First Note",
    text: `
       <div style="margin-bottom: 20px;">
   <p>  You've created your first tag! Now you can start connecting it to notes and other tags. This will help you build a rich knowledge graph over time lets make a note </p>
     </div>
   <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">1.</strong> Click the <kbd>+ New</kbd> button again</p>
      <p style="margin: 8px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">2.</strong> Select  <kbd>Document</kbd> from the dropdown</p>
      <p style="margin: 8px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">3.</strong> Give your note a name</p>
    </div>
    
    <div style="background: hsl(var(--accent) / 0.6); padding: 14px; border-radius: 8px; margin: 16px 0; border-left: 3px solid hsl(var(--accent-foreground));">
      <p style="margin: 0; font-size: 0.85em; color: hsl(var(--foreground) / 0.9);">
        <strong style="color: hsl(var(--accent-foreground));">🔗 Magic moment:</strong> Since you have a tag selected, the note will automatically connect to it!
      </p>
    </div>
    
    <p style="margin: 16px 0 0 0; color: hsl(var(--muted-foreground)); font-size: 0.85em; text-align: center; font-style: italic;">
      The tour continues automatically when you create the note
    </p>
  `,
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
            }, 300);
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
        text: "← Back",
        classes: "shepherd-button-secondary",
        action() {
          return this.back();
        },
      },
      {
        text: "Skip this step →",
        classes: "shepherd-button-primary",
        action() {
          return this.next();
        },
      },
    ],
  });

  tour.value.addStep({
    title: "Great Job!",
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">With a note created you can see how it connects to the graph - if you want to make more connections later you can drag the red dot from a note to a tag or select from the dropdown in the note editor.</p>
      <p style="margin: 8px 0; font-size: 0.9em;">Deleting a connection is just as easy - simply hold down on the connecting line and drag to delete.</p>
    </div>
    
    <div style="margin: 16px 0;">
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">1.</strong> Click on your note in the graph to open it in a new tab</p>
    </div>
    
    <div style="background: hsl(var(--accent) / 0.6); padding: 14px; border-radius: 8px; margin: 16px 0; border-left: 3px solid hsl(var(--accent-foreground));">
      <p style="margin: 0; font-size: 0.85em; color: hsl(var(--foreground) / 0.9);">
        <strong style="color: hsl(var(--accent-foreground));">💡 Pro tip:</strong> You can also click & hold on any element for additional options!
      </p>
    </div>
    
    <p style="margin: 16px 0 0 0; color: hsl(var(--muted-foreground)); font-size: 0.85em; text-align: center; font-style: italic;">
      The tour continues automatically when you open the note
    </p>
  `,
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
            console.log(
              `Active tab changed from ${initialTabId} to ${currentTabId}. Auto-progressing...`
            );
            clearInterval(checkInterval);

            // Auto-progress after short delay to show the new tab
            setTimeout(() => {
              if (tour.value && tour.value.getCurrentStep()) {
                tour.value.next();
              }
            }, 100);
          }
        }, 100); // Check every 500ms

        // Store interval ID on the step for cleanup
        this.tabCheckInterval = checkInterval;
      },
      hide() {
        // Clean up interval when step is hidden
        if (this.tabCheckInterval) {
          clearInterval(this.tabCheckInterval);
          this.tabCheckInterval = null;
        }
      },
    },
    buttons: [
      {
        text: "← Back",
        classes: "shepherd-button-secondary",
        action() {
          return this.back();
        },
      },
      {
        text: "Skip this step →",
        classes: "shepherd-button-primary",
        action() {
          return this.next();
        },
      },
    ],
  });

  tour.value.addStep({
    title: "Document Editor",
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">Welcome to the Document Editor! This is where you can write and format your notes using rich text formatting.</p>
      <p style="margin: 8px 0; font-size: 0.9em;">Let's explore what makes this editor so powerful!</p>
    </div>`,

    attachTo: {
      element: "",
      on: "auto",
    },
  });

  tour.value.addStep({
    title: "Toolbar",
    text: 

    `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">The toolbar provides quick access to formatting options and note history</p>
    </div>`,
    attachTo: {
      element: '[data-tour="tiptapToolbar"]',
      on: "auto",
    },
  });

  tour.value.addStep({
    title: "Main Content Area",
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">This is your main content area where you can write and format your note. You can start typing right away and use many helpful shortcuts:</p>
    </div>
    
    <div style="margin: 16px 0;">
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Use <kbd>-</kbd> for bullet points</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Use <kbd>1.</kbd> for numbered lists</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Use <kbd>#</kbd> to add headings</p>
    </div>
    
    <div style="background: hsl(var(--accent) / 0.6); padding: 14px; border-radius: 8px; margin: 16px 0; border-left: 3px solid hsl(var(--accent-foreground));">
      <p style="margin: 0; font-size: 0.85em; color: hsl(var(--foreground) / 0.9);">
        <strong style="color: hsl(var(--accent-foreground));">💡 Pro tip:</strong> Type <kbd>/</kbd> while writing to see a menu of formatting options and special blocks!
      </p>
    </div>
  `,
    attachTo: {
      element: '[data-tour="tiptapContent"]',
      on: "auto",
    },
  });

  tour.value.addStep({
    title: "Content Linking",
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">Earlier you may have noticed the option to create a whiteboard rather than a document. While documents are great for formatting beautiful typed notes, whiteboards excel at letting your creativity flourish!</p>
      <p style="margin: 8px 0; font-size: 0.9em;">They're perfect for brainstorming, mind mapping, and sketching out ideas. You can easily integrate both by attaching whiteboard previews to your notes.</p>
    </div>
    
    <div style="margin: 16px 0;">
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">1.</strong> Type the <kbd>/</kbd> command in the editor</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">2.</strong> Start typing "whiteboard"</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">3.</strong> Click the whiteboard option when it appears</p>
    </div>
    
    <div style="background: hsl(var(--accent) / 0.6); padding: 14px; border-radius: 8px; margin: 16px 0; border-left: 3px solid hsl(var(--accent-foreground));">
      <p style="margin: 0; font-size: 0.85em; color: hsl(var(--foreground) / 0.9);">
        <strong style="color: hsl(var(--accent-foreground));">✨ Magic trick:</strong> This seamlessly blends visual and text-based thinking in one note!
      </p>
    </div>
    
    <p style="margin: 16px 0 0 0; color: hsl(var(--muted-foreground)); font-size: 0.85em; text-align: center; font-style: italic;">
      The tour continues automatically when the whiteboard popup opens
    </p>
  `,
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
            console.log(
              "Whiteboard select popup appeared. Auto-progressing..."
            );
            clearInterval(checkInterval);

            // Auto-progress after short delay to show the popup
            setTimeout(() => {
              if (tour.value && tour.value.getCurrentStep()) {
                tour.value.next();
              }
            }, 300);
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
      },
    },
    buttons: [
      {
        text: "← Back",
        classes: "shepherd-button-secondary",
        action() {
          return this.back();
        },
      },
      {
        text: "Skip this step →",
        classes: "shepherd-button-primary",
        action() {
          return this.next();
        },
      },
    ],
  });

  tour.value.addStep({
    title: "Select whiteboard",
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">In this popup you can select an existing whiteboard or create a new one. As we haven't made one yet, let's create a new one.</p>
    </div>
    
    <div style="margin: 16px 0;">
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">1.</strong> Type a name for your whiteboard</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">2.</strong> Click the "Create" button</p>
    </div>
    
    <div style="background: hsl(var(--accent) / 0.6); padding: 14px; border-radius: 8px; margin: 16px 0; border-left: 3px solid hsl(var(--accent-foreground));">
      <p style="margin: 0; font-size: 0.85em; color: hsl(var(--foreground) / 0.9);">
        <strong style="color: hsl(var(--accent-foreground));">🔗 Auto-magic:</strong> The new whiteboard will automatically be added to your knowledge graph!
      </p>
    </div>
    
    <p style="margin: 16px 0 0 0; color: hsl(var(--muted-foreground)); font-size: 0.85em; text-align: center; font-style: italic;">
      The tour continues automatically when the whiteboard is created
    </p>
  `,
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
            console.log(
              "Whiteboard select popup disappeared. Auto-progressing..."
            );
            clearInterval(checkInterval);

            // Auto-progress after short delay
            setTimeout(() => {
              if (tour.value && tour.value.getCurrentStep()) {
                tour.value.next();
              }
            }, 300);
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
      },
    },
    buttons: [
      {
        text: "← Back",
        classes: "shepherd-button-secondary",
        action() {
          return this.back();
        },
      },
      {
        text: "Skip this step →",
        classes: "shepherd-button-primary",
        action() {
          return this.next();
        },
      },
    ],
  });

  tour.value.addStep({
    title: "Whiteboard Preview",
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">Great! You now have a whiteboard attached to your note. You may notice it's looking a little blank - let's fix that!</p>
    </div>
    
    <div style="margin: 16px 0;">
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">1.</strong> Click the edit button in the top right to open it in a new tab and start sketching out your ideas</p>
    </div>
    
    <div style="background: hsl(var(--accent) / 0.6); padding: 14px; border-radius: 8px; margin: 16px 0; border-left: 3px solid hsl(var(--accent-foreground));">
      <p style="margin: 0; font-size: 0.85em; color: hsl(var(--foreground) / 0.9);">
        <strong style="color: hsl(var(--accent-foreground));">🎨 Visual thinking:</strong> This is a powerful way to visualize your thoughts and connect them to your notes!
      </p>
    </div>
    
    <p style="margin: 16px 0 0 0; color: hsl(var(--muted-foreground)); font-size: 0.85em; text-align: center; font-style: italic;">
      The tour continues automatically when you open the whiteboard editor
    </p>
  `,
    attachTo: {
      element: ".whiteboard-embed",
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
            console.log(
              `Active tab changed from ${initialTabId} to ${currentTabId}. Auto-progressing...`
            );
            clearInterval(checkInterval);

            // Auto-progress after short delay to show the new tab
            setTimeout(() => {
              if (tour.value && tour.value.getCurrentStep()) {
                tour.value.next();
              }
            }, 100);
          }
        }, 100); // Check every 500ms

        // Store interval ID on the step for cleanup
        this.tabCheckInterval = checkInterval;
      },
      hide() {
        // Clean up interval when step is hidden
        if (this.tabCheckInterval) {
          clearInterval(this.tabCheckInterval);
          this.tabCheckInterval = null;
        }
      },
    },
    buttons: [
      {
        text: "← Back",
        classes: "shepherd-button-secondary",
        action() {
          return this.back();
        },
      },
      {
        text: "Skip this step →",
        classes: "shepherd-button-primary",
        action() {
          return this.next();
        },
      },
    ],
  });

  tour.value.addStep({
    title: "Whiteboard Editor",
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">Welcome to the Whiteboard Editor! This is where you can draw, sketch, and brainstorm your ideas.</p>
      <p style="margin: 8px 0; font-size: 0.9em;">Let's explore what makes this editor so powerful!</p>
    </div>
    
    <div style="margin: 16px 0;">
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Use various tools to create shapes and draw freehand</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Add images and text to enhance your sketches</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> All your changes are saved automatically</p>
    </div>
    
    <div style="background: hsl(var(--accent) / 0.6); padding: 14px; border-radius: 8px; margin: 16px 0; border-left: 3px solid hsl(var(--accent-foreground));">
      <p style="margin: 0; font-size: 0.85em; color: hsl(var(--foreground) / 0.9);">
        <strong style="color: hsl(var(--accent-foreground));">🎨 Creative freedom:</strong> Perfect for visual thinking, mind maps, and bringing your ideas to life!
      </p>
    </div>
  `, attachTo: {
      element: "",
      on: "auto",
    },
  });

  tour.value.addStep({
    title: "Toolbar",
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">The toolbar provides quick access to drawing tools and whiteboard controls.</p>
    </div>
    
    <div style="margin: 16px 0;">
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Switch between auto, draw, and select input modes</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Adjust pen controls like color and thickness</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Access shapes, text, images, and other drawing tools</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> View whiteboard history and undo changes</p>
    </div>
    
    <div style="background: hsl(var(--accent) / 0.6); padding: 14px; border-radius: 8px; margin: 16px 0; border-left: 3px solid hsl(var(--accent-foreground));">
      <p style="margin: 0; font-size: 0.85em; color: hsl(var(--foreground) / 0.9);">
        <strong style="color: hsl(var(--accent-foreground));">🖱️ Smart switching:</strong> Auto mode detects whether you're using a stylus or mouse and switches tools accordingly!
      </p>
    </div>
  `,attachTo: {
      element: '[data-tour="whiteboardToolbar"]',
      on: "auto",
    },
    scrollTo: false,
  });

  tour.value.addStep({
    title: "Main Content Area",
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">This is your main content area where you can see the whiteboard you just created. You can start creating right away!</p>
    </div>
    
    <div style="margin: 16px 0;">
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Use the pen tool to draw freehand</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Select shapes and images from the toolbar</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Drag and resize elements to organize your ideas</p>
    </div>
    
    <div style="background: hsl(var(--accent) / 0.6); padding: 14px; border-radius: 8px; margin: 16px 0; border-left: 3px solid hsl(var(--accent-foreground));">
      <p style="margin: 0; font-size: 0.85em; color: hsl(var(--foreground) / 0.9);">
        <strong style="color: hsl(var(--accent-foreground));">🖊️ Start creating:</strong> Your whiteboard is ready - let your creativity flow!
      </p>
    </div>
  `,attachTo: {
      element: '[data-tour="whiteboardCanvas"]',
      on: "auto",
    },
    scrollTo: false,
  });

  tour.value.addStep({
    title: "🎉 Congratulations!",
    text: `
    <div style="margin-bottom: 20px;">
      <p style="margin: 8px 0; font-size: 0.9em;">That's it for the tour! You've learned the basics of NeuroNote, including how to create notes, tags, and whiteboards.</p>
      <p style="margin: 8px 0; font-size: 0.9em;">You now have all the tools you need to build your personal knowledge management system!</p>
    </div>
    
    <div style="margin: 16px 0;">
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Access this tour again from your profile menu</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Find help resources in the profile dropdown</p>
      <p style="margin: 6px 0; font-size: 0.9em;"><strong style="color: hsl(var(--primary));">•</strong> Share feedback through the feedback form</p>
    </div>
    
    <div style="background: hsl(var(--accent) / 0.6); padding: 14px; border-radius: 8px; margin: 16px 0; border-left: 3px solid hsl(var(--accent-foreground));">
      <p style="margin: 0; font-size: 0.85em; color: hsl(var(--foreground) / 0.9);">
        <strong style="color: hsl(var(--accent-foreground));">🚀 Ready to start:</strong> Begin building your knowledge network and let your ideas flourish!
      </p>
    </div>
    
    <p style="margin: 16px 0 0 0; color: hsl(var(--muted-foreground)); font-size: 0.85em; text-align: center; font-style: italic;">
      Happy note-taking! 📝
    </p>
  `,
    attachTo: {
      element: "",
      on: "auto",
    },
    buttons: [
      {
        text: "← Back",
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
  if (graphStore.elements.length === 0) {
    console.error(
      "New user detected, starting tour...",
      graphStore.elements.length
    );
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
