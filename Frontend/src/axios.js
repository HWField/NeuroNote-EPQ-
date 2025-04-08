import axios from 'axios';
import router from "@/router"; // Adjust the path based on your project structure
import { useUserStore } from "@/stores/useUserStore";

// Create an Axios instance
// const BASE_URL = 'http://127.0.0.1:8000';
const BASE_URL = 'http://192.168.1.232:8000';  // Alternate URL

const api = axios.create({
  baseURL: BASE_URL,  
  headers: {
    'Content-Type': 'application/json',
  },
});

// Function to get the base URL
export const getBaseUrl = () => BASE_URL; 

// Interceptor to add JWT token to request headers
api.interceptors.request.use(
  (config) => {
    //const token = localStorage.getItem('token');  // Retrieve the token from localStorage
    const token = useUserStore().token;  // Retrieve the token from Pinia store
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;  // Attach token to Authorization header
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Optionally, handle expired token (401 errors) globally
// api.interceptors.response.use(
//   response => response,  // Pass the successful response through
//   async (error) => {
//     if (error.response && error.response.status === 401) {
//       // Token might be expired; handle accordingly (e.g., redirect to login)
//       console.error('Session expired, please log in again.');
//       localStorage.removeItem('token');  // Remove expired token
//       window.location.href = '/login';   // Or redirect to login page using Vue Router
//     }
//     return Promise.reject(error);
//   }
// );



api.interceptors.response.use(
  response => response, // Pass the successful response through
  async (error) => {
    if (error.response && error.response.status === 401) {
      console.error('Session expired, please log in again.');

      // Remove expired token
      await useUserStore().InstantLogout(); //logout without saving as cant save

      // Save the original route in the query parameters
      const currentRoute = window.location.pathname;
      // window.location.replace(`login?redirect=${encodeURIComponent(currentRoute)}`);
      router.push({ 
        path: '/login', 
        query: { redirect: currentRoute }
      });
      
    }
    else if (!error.response) {
      console.error('Cannot connect to the server');

    
      

      // Redirect to login page
      const errorMessage = encodeURIComponent('Cannot connect to the server');
      // window.location.href = `/error?message=${errorMessage}`;
      //this method stops user retunring to the page which caused error message
      // window.location.replace(`/error?message=${errorMessage}`);
      router.push({ 
        path: '/error', 
        query: { message: errorMessage }
      });
    }
    return Promise.reject(error);
  }
);

export default api;