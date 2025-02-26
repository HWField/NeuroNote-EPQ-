import { defineStore } from "pinia";
import { ref, watch } from "vue";
import { useColorMode } from '@vueuse/core'
export const useUserStore = defineStore("userStore", () => {
  const isAuthenticated = ref(false);
  const username = ref("");
  const email = ref("");
  const role = ref("");
  const token = ref("");
  const theme = useColorMode(); theme.value = 'auto';
  







  function setUser(userData) {
    username.value = userData.username;
    email.value = userData.email;
    role.value = userData.role;
    token.value = userData.token;
    isAuthenticated.value = true;
  }

  function logout() {
    username.value = "";
    email.value = "";
    role.value = "";
    token.value = "";
    isAuthenticated.value = false;
  }

  return {
    isAuthenticated,
    username,
    email,
    role,
    token,
    setUser,
    logout,
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