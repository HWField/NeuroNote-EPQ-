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
import LightDark from "@/components/LightDark.vue";
import { Checkbox } from "@/components/ui/checkbox";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";
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
    console.log(
      response.data.access_token,
      "success registering and logging in"
    );

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
   <div class="absolute top-4 right-4">
    <LightDark class="bg-white p-4 rounded-lg shadow-lg"></LightDark>
  </div>
  <!-- Large login form -->
 
  <div
    class="container hidden h-screen flex-col lg:grid lg:max-w-none lg:grid-cols-2 lg:px-0 "
  >
    <!-- compensate for the height of the inset -->
    <div
      class="relative hidden inset-5 flex-col h-[calc(100vh-2.5rem)] bg-none p-10 text-white dark:border-r lg:flex"
    >
      <img
        class="h-full object-cover absolute rounded-2xl border-none inset-0 bg-none"
        src="/Images/login.jpg"
        alt="Logo"
      />
      <div class="relative z-20 flex items-center text-lg font-medium">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          class="mr-2 h-6 w-6"
        >
          <path
            d="M15 6v12a3 3 0 1 0 3-3H6a3 3 0 1 0 3 3V6a3 3 0 1 0-3 3h12a3 3 0 1 0-3-3"
          />
        </svg>
        Second Brain
      </div>
      <div class="relative z-20 mt-auto">
        <blockquote class="space-y-2">
          <p class="text-lg">
            &ldquo;The Best software project management tool I have ever
            used.&rdquo;
          </p>
          <footer class="text-sm">- Anynomous user</footer>
        </blockquote>
      </div>
    </div>

    <div class="flex items-center justify-center">
      <div class="w-2/3 h-fill">
        <form @submit.prevent="isRegisterView ? register() : login()">
          <CardHeader>
            <CardTitle class="text-4xl pb-6">
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
          <CardContent class="grid gap-8">
            <div v-if="isRegisterView" class="grid gap-2">
              <Label for="username">Username</Label>
              <Input
                class="h-14"
                v-model:="username"
                placeholder="Username"
                required
              />
            </div>

            <div class="grid gap-2">
              <Label for="email">Email</Label>
              <Input
                class="h-14"
                v-model="email"
                placeholder="Email"
                required
              />
            </div>

            <div class="grid gap-2">
              <Label for="password">Password</Label>
              <Input
                class="h-14"
                type="password"
                v-model="password"
                placeholder="Password"
                required
              />
            </div>

            <!-- <div v-if="isRegisterView" class="grid gap-2">
              <Label for="confirmPassword">Confirm Password</Label>
              <Input
                class="h-14"
                type="password"
                v-model="confirmPassword"
                placeholder="Confirm Password"
                required
              />
            </div> -->
            <div class="items-center flex space-x-2">
              <Checkbox class="h-6 w-6" id="terms1" />
              <label
                for="terms1"
                class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                Accept terms and conditions
              </label>
            </div>
          </CardContent>
          <CardFooter class="flex flex-col gap-4">
            <Button class="w-full h-12" type="submit">
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
      </div>
    </div>
  </div>

  <!-- small / mobile login form -->
  <!-- <img
      class=" inset-0 h-full w-full object-cover"
      src="/Images/login.jpg"
      alt="Background Image"
    /> -->
  <div
    class="flex items-center justify-center h-screen lg:hidden bg-[url(/Images/login.jpg)]"
  >
    <Card class="w-full max-w-sm">
      <form @submit.prevent="isRegisterView ? register() : login()">
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

          <!-- <div v-if="isRegisterView" class="grid gap-2">
            <Label for="confirmPassword">Confirm Password</Label>
            <Input
              type="password"
              v-model="confirmPassword"
              placeholder="Confirm Password"
              required
            />
          </div> -->
          <div class="items-center flex space-x-2">
            <Checkbox class="h-4 w-4" id="terms1" />
            <label
              for="terms1"
              class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            >
              Accept terms and conditions
            </label>
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
