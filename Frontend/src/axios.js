import axios from 'axios';

// Create an Axios instance
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',  // Replace with your Flask API base URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to add JWT token to request headers
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');  // Retrieve the token from localStorage
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
      localStorage.removeItem('token');

      // Save the original route in the query parameters
      const currentRoute = window.location.pathname;
      window.location.href = `/login?redirect=${encodeURIComponent(currentRoute)}`;
    }
    return Promise.reject(error);
  }
);

export default api;