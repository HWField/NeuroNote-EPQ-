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
    const avatar = ref("");
    const token = ref("");
    const preferences = ref({}); // User preferences
    const recentNotes = ref([]); // Array to store recent note IDs
    const theme = useColorMode({emitAuto: true});
    const streamerMode = ref("");
    theme.value = "auto";
    // const theme = ref("auto"); // Default theme is "auto"
    

    watch(theme, (newTheme) => {
      console.error("Theme changed:", newTheme);
      if (isAuthenticated.value) {
        saveUser({ theme: newTheme });
      }
    });

    const router = useRouter(); // Router instance for programmatic navigation

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
          console.error("Theme found on load:", data.preferences.theme);
        }

        // Load recent notes if available
        if (data.preferences?.recentNotes) {
          recentNotes.value = data.preferences.recentNotes;
        }

        if (data.preferences?.tabs) {
          const tabStore = useTabStore();
          tabStore.loadTabsFromPreferences(data.preferences.tabs);
        }

        // Load avatar if available
        if (data.preferences?.avatar) {
          avatar.value = data.preferences.avatar;
        }

        // Load streamer mode if available
        if (data.preferences?.streamerMode) {
          console.error("streamermode found on load:", data.preferences.streamerMode);
          streamerMode.value = data.preferences.streamerMode;
        }
      }
    }

    async function saveUser(updates = {}) {
      try {
        const response = await axios.post("/update", {
          operation: "user",
          ...updates, // This spreads all updates directly into the request body
        });
        // Update local state with any returned values
        if (response.data.status === "success") {
          // Update local state for each field that was updated
          Object.keys(updates).forEach((key) => {
            if (key === "username" && updates.username) {
              username.value = updates.username;
            } else if (key === "email" && updates.email) {
              email.value = updates.email;
            // } else if (key === "avatar" && updates.avatar) {
            //   console.error("Avatar update acknowledged:", updates.avatar);
            //   avatar.value = updates.avatar.avatar; //no not a mistake intentional
            } else if (key === "preferences" && updates.preferences) {
              // preferences.value = {...preferences.value, ...updates.preferences};
            } else if (key === "recentNotes" && updates.recentNotes) {
              // recentNotes.value = updates.recentNotes;
            // } else if (key === "streamerMode" && updates.streamerMode) {
            //   console.error("streamermodeupdate update: acknowledged", updates.streamerMode);
            //   streamerMode.value = updates.streamerMode;
            }
            //do nothing for password
          });

          console.log("User data updated successfully");
          return true;
        }
        console.error("Failed to update user data:", response.data.message);
        return false;
      } catch (error) {
        console.error("Error saving user data:", error);
        return false;
      }
    }

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

    async function Login(userData, redirect = null) {
      token.value = userData.token;
      isAuthenticated.value = true;

      const graphStore = useGraphStore();
      await graphStore.fetchGraph();
      FetchUser();

      if (redirect) {
        router.replace(decodeURIComponent(redirect));
      } else {
        router.replace("/dashboard"); // Default route after login
      }
    }

    async function InstantLogout() {
      // used for quick wiping of data
      isAuthenticated.value = false;
      username.value = "";
      email.value = "";
      role.value = "";
      token.value = "";
      preferences.value = {};
      recentNotes.value = [];
      avatar.value = "";
      streamerMode.value = "";

      theme.value = "auto";
      router.replace("/login");
    }

    async function Logout() {
      const graphStore = useGraphStore();
      const tabStore = useTabStore();
      tabStore.setActiveTab(0); //saves current state of tab (as saves on tab change)
      saveUser({ tabs: tabStore.tabs.value });
      // saveUser({ tabs: Array.from(tabStore.tabs) });

      tabStore.clearStore();
      graphStore.resetGraph();
      username.value = "";
      email.value = "";
      role.value = "";
      token.value = "";
      isAuthenticated.value = false;
      recentNotes.value = [];
      avatar.value = "";
      streamerMode.value = "";

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
      avatar,
      theme,
      streamerMode,
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
