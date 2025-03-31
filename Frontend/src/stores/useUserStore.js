import { defineStore } from "pinia";
import { ref, watch } from "vue";
import { set, useColorMode } from "@vueuse/core";
import { useGraphStore } from "@/stores/useGraphStore";
import { useTabStore } from "@/stores/useTabStore";
import { useRouter, useRoute } from "vue-router"; // Vue Router for navigation
import axios from "../axios"; // Import the Axios instance

export const useUserStore = defineStore(
  "userStore",
  () => {
    const isAuthenticated = ref(false);
    const username = ref("");
    const email = ref("");
    const role = ref("");
    const token = ref("");
    const preferences = ref({}); // User preferences
    const recentNotes = ref([]); // Array to store recent note IDs
    const theme = useColorMode();
    theme.value = "auto";

    watch(theme, (newTheme) => {
      if (isAuthenticated.value) {
        console.error("Theme changed to:", newTheme);
        saveUser({ theme: newTheme });
      }
    });

    const router = useRouter(); // Router instance for programmatic navigation

    async function FetchUser() {
      try {
        const response = await axios.post("/load", {
          operation: "user",
        });

        isAuthenticated.value = true;
        console.log("user data:", response.data);
        UpdateUser(response.data);
        return true;
      } catch (error) {
        console.error("Error fetching user data:", error);
        isAuthenticated.value = false;
        return false;
      }
    }

    function UpdateUser(data) {
      username.value = data.username;
      email.value = data.email;
      role.value = data.userStatus;

      // Set preferences and extract important values
      if (data.preferences) {
        preferences.value = data.preferences || {};

        // Load theme if available
        if (data.preferences?.theme) {
          theme.value = data.preferences.theme;
        }

        // Load recent notes if available
        if (data.preferences?.recentNotes) {
          recentNotes.value = data.preferences.recentNotes;
          console.error("Loaded recent notes:", recentNotes.value);
        }

        if (data.preferences?.tabs) {
          const tabStore = useTabStore();
          tabStore.loadTabsFromPreferences(data.preferences.tabs);
          console.error("Loaded recent notes:", tabStore.tabs.value);
        }
      }
    }

    async function saveUser(updates = {}) {
      console.error("Saving user updates:", updates);

      try {
        const response = await axios.post("/update", {
          operation: "user",
          ...updates, // This spreads all updates directly into the request body
        });
        console.error("Server response:", response.data);
        // Update local state with any returned values
        if (response.data.status === "success") {
          // Update local state for each field that was updated
          Object.keys(updates).forEach((key) => {
            if (key === "username" && updates.username) {
              username.value = updates.username;
            } else if (key === "email" && updates.email) {
              email.value = updates.email;
            } else if (key === "preferences" && updates.preferences) {
              // preferences.value = {...preferences.value, ...updates.preferences};
            } else if (key === "recentNotes" && updates.recentNotes) {
              // recentNotes.value = updates.recentNotes;
            }
          });

          console.log("User data updated successfully");
          return true;
        }
        return false;
      } catch (error) {
        console.error("Error saving user data:", error);
        return false;
      }
    }

    async function Login(userData, redirect = null) {
      username.value = userData.username;
      email.value = userData.email;
      role.value = userData.userStatus;
      token.value = userData.token;
      preferences.value = userData.preferences;
      isAuthenticated.value = true;

      // Set theme from preferences
      if (preferences.value?.theme) {
        console.error("---loaded theme:", preferences.value.theme);
        theme.value = preferences.value.theme;
      }

      // Load recent notes if available
      if (preferences.value?.recentNotes) {
        recentNotes.value = preferences.value.recentNotes;
      }

      // Load tabs if available
      if (preferences.value?.tabs) {
        const tabStore = useTabStore();
        tabStore.loadTabsFromPreferences(preferences.value.tabs);
      }

      const graphStore = useGraphStore();
      await graphStore.fetchGraph();

      if (redirect) {
        router.replace(decodeURIComponent(redirect));
      } else {
        router.replace("/dashboard"); // Default route after login
      }
    }

    async function InstantLogout() {
      isAuthenticated.value = false;
      username.value = "";
      email.value = "";
      role.value = "";
      token.value = "";
      preferences.value = {};
      theme.value = "auto";
      router.replace("/login");
    }

    async function Logout() {
      const graphStore = useGraphStore();
      graphStore.resetGraph();

      const tabStore = useTabStore();
      tabStore.setActiveTab(1); //saves current state of tab
      saveUser({ tabs: tabStore.tabs.value });
      // saveUser({ tabs: Array.from(tabStore.tabs) });

      tabStore.clearStore();
      graphStore.resetGraph();
      username.value = "";
      email.value = "";
      role.value = "";
      token.value = "";
      isAuthenticated.value = false;
      // Router instance for programmatic navigation

      // const router = useRouter(); // Router instance for programmatic navigation
      router.replace("/login"); // Or redirect to login page using Vue Router
    }

    function addToRecentNotes(noteId) {
      // Convert to number if it's not already
      noteId = Number(noteId);

      // Remove the note if it already exists in the list
      recentNotes.value = recentNotes.value.filter((id) => id !== noteId);

      // Add the note at the beginning of the array
      recentNotes.value.unshift(noteId);

      if (recentNotes.value.length > 15) {
        recentNotes.value.pop();
      }
      saveUser({ recentNotes: Array.from(recentNotes.value) });
      console.log("Recent Notes after update:", recentNotes.value);
    }

    return {
      isAuthenticated,
      username,
      email,
      role,
      token,
      recentNotes,
      Login,
      Logout,
      InstantLogout,
      UpdateUser,
      FetchUser,
      addToRecentNotes,
      saveUser,
    };
  },
  // ✅ Enable persistence
  {
    persist: {
      enabled: true,
      strategies: [
        {
          key: "userStore", // LocalStorage key
          storage: localStorage, // Change to localStorage if you want it to persist after closing the browser
          // path : ["isAuthenticated", "username", "email", "role", "token", "preferences", "recentNotes"], // Only save these properties
          paths: ["token"], // Only persist the token, not the entire state
        },
      ],
    },
  }
);
