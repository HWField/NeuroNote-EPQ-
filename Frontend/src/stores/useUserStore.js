import { defineStore } from "pinia";
import { ref, watch } from "vue";
import { set, useColorMode } from '@vueuse/core'
import { useGraphStore } from "@/stores/useGraphStore";
import { useTabStore } from "@/stores/useTabStore";
import { useRouter, useRoute } from "vue-router"; // Vue Router for navigation
import axios from "../axios"; // Import the Axios instance


export const useUserStore = defineStore("userStore", () => {
  const isAuthenticated = ref(false);
  const username = ref("");
  const email = ref("");
  const role = ref("");
  const token = ref("");
  const preferences = ref({}); // User preferences
  const theme = useColorMode(); theme.value = 'auto';
  
  const router = useRouter(); // Router instance for programmatic navigation

  async function fetchUser() {
    if (isAuthenticated) {
      try {
        const response = await axios.post("/load", {
          operation: "user",
        });
        console.log("user data:", response.data);
        setUser(response.data);
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    }
  }

  async function sendUser() {
    if (isAuthenticated) {
      try {
        const response = await axios.post("/update", {
          operation: "user",
          data: {
            username: username.value,
            email: email.value,
            preferences: preferences.value,
          },
        });
        console.log("user data:", response.data);
        setUser(response.data);
      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    }
  }



  function setUser(data) {
    username.value = data.username;
    email.value = data.email;
    role.value = data.userStatus;
    preferences.value = data.preferences;
    theme.value = data.preferences.theme;
  }

 

  async function Login(userData, redirect = null) {
    username.value = userData.username;
    email.value = userData.email;
    role.value = userData.userStatus;
    token.value = userData.token;
    preferences.value = userData.preferences;
    isAuthenticated.value = true;
    const graphStore = useGraphStore();
    await graphStore.fetchGraph();
    
    if (redirect) {
      router.replace(decodeURIComponent(redirect));
    }
    else {
      router.replace("/dashboard"); // Default route after login
    }
  }

  function logout() {
    username.value = "";
    email.value = "";
    role.value = "";
    token.value = "";
    isAuthenticated.value = false;

    const graphStore = useGraphStore();
    graphStore.resetGraph();

    const tabStore = useTabStore();
    // Router instance for programmatic navigation

    // const router = useRouter(); // Router instance for programmatic navigation
    router.replace("/login"); // Or redirect to login page using Vue Router
  }

  return {
    isAuthenticated,
    username,
    email,
    role,
    token,
    Login,
    logout,
    setUser,
    fetchUser,
  };
}, 
// ✅ Enable persistence
{
  persist: {
    enabled: true,
    strategies: [
      {
        key: "userStore",  // LocalStorage key
        storage: sessionStorage,  // Change to localStorage if you want it to persist after closing the browser
      },
    ],
  },
});