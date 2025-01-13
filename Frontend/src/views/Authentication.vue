<script lang="ts"></script>

<script setup lang="ts">
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

import { ref } from "vue";
import axios from "../axios"; // Import the Axios instance
import { useRouter, useRoute } from "vue-router"; // Vue Router for navigation

const isRegisterView = ref(false);
const email = ref("");
const username = ref("");
const password = ref("");
const confirmPassword = ref("");
const router = useRouter(); // Router instance for programmatic navigation
const route = useRoute(); // Current route to access query parameters

// Login function
const login = async () => {
  try {
    const response = await axios.post("/login", {
      email: email.value,
      password: password.value,
    });

    // Store the token in localStorage
    localStorage.setItem("token", response.data.access_token);

    const redirect = route.query.redirect as string;
    if (redirect) {
      router.push(decodeURIComponent(redirect)); // Navigate to the intended route
    } else {
      router.push("/dashboard"); // Default route after login
    }

    // Handle successful login
    console.log(response.data.access_token, "success logging in");
  } catch (error) {
    console.error("Login failed", error.response ? error.response.data : error);
  }
};

// Register function
const register = async () => {
  if (password.value !== confirmPassword.value) {
    console.error("Passwords do not match");
    return;
  }

  try {
    const response = await axios.post("/register", {
      email: email.value,
      password: password.value,
      username: username.value,
    });

    // Store the token in localStorage
    localStorage.setItem("token", response.data.access_token);

    const redirect = route.query.redirect as string;
    if (redirect) {
      router.push(decodeURIComponent(redirect)); // Navigate to the intended route
    } else {
      router.push("/dashboard"); // Default route after login
    }

    // Handle successful login
    console.log(response.data.access_token, "success registering and logging in");

    // Redirect to login view after successful registration
    isRegisterView.value = false;
  } catch (error) {
    console.error(
      "Registration failed:",
      error.response ? error.response.data : error
    );
  }
};

// Logout function
const logout = () => {
  // Remove token from localStorage
  const token = localStorage.getItem("token");
  if (token) {
    localStorage.removeItem("token");
    console.log("Logged out successfully");
  } else {
    console.error("No token found. Cannot logout.");
  }
};

// Function to access the protected route
const accessProtectedRoute = async () => {
  try {
    const token = localStorage.getItem("token");
    if (!token) {
      console.error("No token found. Please login first.");
      return;
    }

    const response = await axios.get("/test", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    console.log("Access to protected route successful:", response.data);
  } catch (error) {
    console.error(
      "Failed to access protected route:",
      error.response ? error.response.data : error
    );
  }
};
</script>

<template>
  <div class="flex items-center justify-center min-h-screen">
    <Card class="w-full max-w-sm">
      <form @submit.prevent="isRegisterView ? register() : login()">
        <!-- Toggle forms based on view -->
        <CardHeader>
          <CardTitle class="text-2xl">
            {{ isRegisterView ? "Register" : "Login" }}
          </CardTitle>

          <CardDescription>
            {{
              isRegisterView
                ? "Create a new account by filling in the details below."
                : "Enter your email below to login to your account."
            }}
          </CardDescription>
        </CardHeader>
        <CardContent class="grid gap-4">
          <div v-if="isRegisterView" class="grid gap-2">
            <Label for="username">Username</Label>
            <Input v-model:="username" placeholder="Username" required />
          </div>

          <div class="grid gap-2">
            <Label for="email">Email</Label>
            <Input v-model="email" placeholder="Email" required />
          </div>

          <div class="grid gap-2">
            <Label for="password">Password</Label>
            <Input
              type="password"
              v-model="password"
              placeholder="Password"
              required
            />
          </div>

          <div v-if="isRegisterView" class="grid gap-2">
            <Label for="confirmPassword">Confirm Password</Label>
            <Input
              type="password"
              v-model="confirmPassword"
              placeholder="Confirm Password"
              required
            />
          </div>
        </CardContent>
        <CardFooter class="flex flex-col gap-4">
          <Button class="w-full" type="submit">
            {{ isRegisterView ? "Sign up" : "Sign in" }}
          </Button>
          <label class="text-center text-sm text-gray-500">
            {{
              isRegisterView
                ? "Already have an account?"
                : "Don't have an account?"
            }}
            <a
              href="#"
              class="text-blue-500"
              @click.prevent="isRegisterView = !isRegisterView"
            >
              {{ isRegisterView ? "Login" : "Register" }}
            </a>
          </label>
        </CardFooter>
      </form>
    </Card>
  </div>
</template>
