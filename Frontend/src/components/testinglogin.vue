<script setup>
import { ref } from 'vue';
import axios from '../axios';  // Import the Axios instance

const username = ref('');
const password = ref('');

// Login function
const login = async () => {
  try {
    const response = await axios.post('/login', {
      email: username.value,
      password: password.value
    });
    
    // Store the token in localStorage
    localStorage.setItem('token', response.data.access_token);
    
    // Handle successful login
    console.log(response.data.access_token, "success logging in");
  } catch (error) {
    console.error('Login failed', error.response ? error.response.data : error);
  }
};

// Logout function
const logout = () => {
  // Remove token from localStorage
const token = localStorage.getItem('token');
if (token) {
    localStorage.removeItem('token');
    console.log("Logged out successfully");
} else {
    console.error("No token found. Cannot logout.");
}
};

// Function to access the protected route
const accessProtectedRoute = async () => {
  try {
    const token = localStorage.getItem('token');
    if (!token) {
      console.error('No token found. Please login first.');
      return;
    }

    const response = await axios.get('/test', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });

    console.log('Access to protected route successful:', response.data);
  } catch (error) {
    console.error('Failed to access protected route:', error.response ? error.response.data : error);
  }
};
</script>

<template>
  <div>
    <!-- Login Form -->
    <form @submit.prevent="login">
      <input v-model="username" placeholder="Email" />
      <input type="password" v-model="password" placeholder="Password" />
      <button type="submit">Login</button>
    </form>

    <!-- Logout Button -->
    <button @click="logout">Logout</button>

    <!-- Access Protected Route Button -->
    <button @click="accessProtectedRoute">Access Protected Route</button>
  </div>
</template>