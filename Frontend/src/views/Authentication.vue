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
import Toaster from "@/components/ui/toast/Toaster.vue";
import { useToast } from "@/components/ui/toast/use-toast";
import { ScrollArea } from "@/components/ui/scroll-area";
import { cn } from "@/lib/utils";
import { ref } from "vue";
import axios from "../axios"; // Import the Axios instance
import { useRouter, useRoute } from "vue-router"; // Vue Router for navigation
import { useUserStore } from "@/stores/useUserStore";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";

// Add this ref for dialog state
const isTermsDialogOpen = ref(false);
const { toast } = useToast();
const userStore = useUserStore();
const isRegisterView = ref(false);
const email = ref("");
const username = ref("");
const password = ref("");
const terms = ref(false); //default to false
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
    //localStorage.setItem("token", response.data.access_token);
    toast({
      title: "Success",
      description: "Sucesfully Logged in",
      variant: "success",
    });

    const redirect = route.query.redirect as string;

    userStore.Login({
      access_token: response.data.access_token,
      refresh_token: response.data.refresh_token,
      redirect: redirect ? redirect : null,
    });

    // Handle successful login
    console.log(response.data.access_token, "success logging in");
  } catch (error) {
    console.error("Login failed", error.response ? error.response.data : error);
    toast({
      title: "Login failed",
      description: error.response.data.message,
      variant: "destructive",
    });
  }
};

// Register function
const register = async () => {
  try {
    const response = await axios.post("/register", {
      email: email.value,
      password: password.value,
      username: username.value,
      terms: terms.value,
    });
    toast({
      title: "Success",
      description: "Sucesfully Registered and Logged in",
      variant: "success",
    });

    const redirect = route.query.redirect as string;
    console.error(
      "Registration successful",
      "access_token: ",
      response.data.access_token,
      "refresh_token: ",
      response.data.refresh_token
    );
    userStore.Login({
      access_token: response.data.access_token,
      refresh_token: response.data.refresh_token,
      redirect: redirect ? redirect : null,
    });

    //await new Promise(resolve => setTimeout(resolve, 1000)); // Waitm for 500ms to show message before going to dashboard
  } catch (error) {
    console.error(
      "Registration failed:",
      error.response ? error.response.data : error
    );
    toast({
      title: "Registration failed",
      description: error.response.data.message,
      variant: "destructive",
    });
  }
};

// Logout function
// const logout = () => {
//   // Remove token from localStorage
//   const token = localStorage.getItem("token");
//   if (token) {
//     localStorage.removeItem("token");
//     console.log("Logged out successfully");
//   } else {
//     console.error("No token found. Cannot logout.");
//   }
// };

// Function to access the protected route
// const accessProtectedRoute = async () => {
//   try {
//     const token = localStorage.getItem("token");
//     if (!token) {
//       console.error("No token found. Please login first.");
//       return;
//     }

//     const response = await axios.get("/test", {
//       headers: {
//         Authorization: `Bearer ${token}`,
//       },
//     });

//     console.log("Access to protected route successful:", response.data);
//   } catch (error) {
//     console.error(
//       "Failed to access protected route:",
//       error.response ? error.response.data : error
//     );
//   }
// };
</script>

<template>
  <Dialog v-model:open="isTermsDialogOpen">
    <DialogContent class="overflow-y-none w-[900px] sm:w-[450px]">
      <!-- <DialogHeader>
        <DialogTitle>Terms and Conditions</DialogTitle>
        <DialogDescription>
          Please read our terms and conditions carefully.
        </DialogDescription>
      </DialogHeader>  -->
      <ScrollArea class="h-[60vh] overflow-y-auto">
        <div class="pr-4">
          <h2 class="text-xl font-bold mb-3">Terms and Conditions</h2>
          <p class="text-sm text-gray-500 mb-4">Last Updated: 25/4/25</p>

          <p class="mb-4 text-sm">
            Welcome to NovaNote ("the App"), provided by Henry Field ("Company,"
            "we," "us," or "our"). By creating an account, accessing, or using
            the App, you agree to these Terms and Conditions ("Terms"). If you
            do not agree, please do not use the App.
          </p>

          <h3 class="font-semibold mb-2">0. Academic Nature of the App</h3>
          <p class="mb-2 text-sm">
            0.1. This App is part of an academic project and is provided as-is
            for experimental or educational use only.
          </p>
          <p class="mb-2 text-sm">
            0.2. We make no guarantees of availability, reliability, or
            long-term support of either the application or data stored.
          </p>
          <p class="mb-4 text-sm">
            0.3. The App may be shut down or altered at any time without notice.
          </p>

          <h3 class="font-semibold mb-2">
            1. Account Registration and Security
          </h3>
          <p class="mb-2 text-sm">
            1.1. To use the App, you must create an account and provide
            accurate, up-to-date information.
          </p>
          <p class="mb-2 text-sm">
            1.2. You are responsible for maintaining the confidentiality of your
            password and account credentials.
          </p>
          <p class="mb-4 text-sm">
            1.3. All passwords are encrypted for security; however, you
            acknowledge that no system is completely secure.
          </p>

          <h3 class="font-semibold mb-2">2. User-Generated Content</h3>
          <p class="mb-2 text-sm">
            2.1. You retain ownership of any notes, text, images, or other
            content ("User Content") you create within the App.
          </p>
          <p class="mb-2 text-sm">
            2.2. User Content is not encrypted. You acknowledge and accept any
            risks associated with storing unencrypted data.
          </p>
          <p class="mb-4 text-sm">
            2.3. You grant us a non-exclusive, worldwide, royalty-free license
            to use, store, display, and distribute User Content as necessary to
            operate the App.
          </p>

          <h3 class="font-semibold mb-2">3. Intellectual Property</h3>
          <p class="mb-2 text-sm">
            3.1. All software, designs, logos, trademarks, and other elements of
            the App are owned by or licensed to the Company.
          </p>
          <p class="mb-4 text-sm">
            3.2. You may not copy, modify, distribute, or reverse-engineer any
            part of the App without our express permission.
          </p>

          <h3 class="font-semibold mb-2">4. Data Privacy & Security</h3>
          <p class="mb-2 text-sm">
            4.1. While passwords are encrypted, User Content is stored in
            plaintext and is not encrypted. By using the App, you accept this
            limitation.
          </p>
          <p class="mb-2 text-sm">
            4.2. We take reasonable security measures to protect your data but
            cannot guarantee complete security.
          </p>
          <p class="mb-4 text-sm">
            4.3. Our use of personal data is governed by our Privacy Policy.
          </p>

          <h3 class="font-semibold mb-2">5. Prohibited Conduct</h3>
          <p class="mb-2 text-sm">5.1. You agree not to:</p>
          <ul class="list-disc pl-8 mb-4 text-sm">
            <li class="mb-1">
              Use the App for any illegal or unauthorized purposes.
            </li>
            <li class="mb-1">
              Upload content that infringes on third-party rights.
            </li>
            <li class="mb-1">Attempt to hack, disrupt, or misuse the App.</li>
          </ul>

          <h3 class="font-semibold mb-2">6. Termination</h3>
          <p class="mb-2 text-sm">
            6.1. We may suspend or terminate your account if you violate these
            Terms.
          </p>
          <p class="mb-4 text-sm">
            6.2. You may delete your account at any time, but some data may be
            retained for legal or operational purposes.
          </p>

          <h3 class="font-semibold mb-2">7. Disclaimers & Liability Limits</h3>
          <p class="mb-2 text-sm">
            7.1. The App is provided "as is" without warranties of any kind.
          </p>
          <p class="mb-4 text-sm">
            7.2. We are not responsible for any loss, damage, or unauthorised
            access to your data.
          </p>

          <h3 class="font-semibold mb-2">8. Changes to These Terms</h3>
          <p class="mb-4 text-sm">
            8.1. We may update these Terms from time to time. Continued use of
            the App after updates means you accept the new Terms.
          </p>

          <h3 class="font-semibold mb-2">9. Contact Us</h3>
          <p class="mb-4 text-sm">
            If you have any questions, please contact us at
            hf165122@hrsfc.ac.uk.
          </p>
        </div>
      </ScrollArea>
      <!-- <DialogFooter>
      <Button @click="isTermsDialogOpen = false">Close</Button>
    </DialogFooter> -->
    </DialogContent>
  </Dialog>
  <Toaster />
  <!-- Toast component to show messages -->
  <!-- <Button
    variant="outline" @click="() => {
      toast({
        description: 'Your message has been sent.',
         variant: 'success'
      });
    }"
  >Show Toast</Button> -->
  <div class="absolute top-4 right-4">
    <LightDark class="bg-white p-4 rounded-lg shadow-lg"></LightDark>
  </div>
  <!-- Large login form -->

  <div
    class="container hidden h-screen flex-col lg:grid lg:max-w-none lg:grid-cols-2 lg:px-0"
  >
    <!-- compensate for the height of the inset -->
    <div
      class="relative hidden inset-5 flex-col h-[calc(100vh-2.5rem)] bg-none p-10 text-white lg:flex"
    >
      <img
        class="h-full object-cover absolute rounded-2xl border-2 inset-0 drop-shadow-lg border-input bg-none"
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
        NovaNote
      </div>
      <div class="relative z-20 mt-auto">
        <blockquote class="space-y-2">
          <p class="text-lg">
            &ldquo;the project is looking really good, its quite impressive what you’ve created&rdquo;
          </p>
          <footer class="text-sm">- Critical software developer</footer>
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
                class="h-14 text-sm"
                v-model="email"
                placeholder="Email"
                required
              />
            </div>

            <div class="grid gap-2">
              <Label for="password">Password</Label>
              <Input
                class="h-14 text-sm"
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
            <div v-if="isRegisterView" class="items-center flex space-x-2">
              <Checkbox class="h-6 w-6" id="terms" v-model:checked="terms" />
              <label
                for="terms"
                class="text-sm leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
              >
                Accept
                <a
                  href="#"
                  class="text-blue-500"
                  @click.prevent="isTermsDialogOpen = true"
                  >terms and conditions</a
                >
              </label>
            </div>
          </CardContent>
          <CardFooter class="flex flex-col gap-4">
            <Button class="w-full h-12 text-sm" type="submit">
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
    class="flex items-center justify-center h-screen lg:hidden bg-cover bg-center bg-[url(/Images/login.jpg)]"
  >
    <Card class="w-full max-w-sm rounded-2xl shadow-xl">
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
          <div v-if="isRegisterView" class="items-center flex space-x-2">
            <Checkbox class="h-4 w-4" id="terms" v-model:checked="terms" />
            <label
              for="terms"
              class="text-sm leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
            >
              Accept
              <a
                href="#"
                class="text-blue-500"
                @click.prevent="isTermsDialogOpen = true"
                >terms and conditions</a
              >
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
