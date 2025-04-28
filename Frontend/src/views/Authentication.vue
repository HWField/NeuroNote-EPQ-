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
const isPrivacyDialogOpen = ref(false);
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
                          Welcome to NovaNote ("the App"), provided by Henry
                          Field ("Company," "we," "us," or "our"). By creating
                          an account, accessing, or using the App, you agree to
                          these Terms and Conditions ("Terms"). If you do not
                          agree, please do not use the App.
                        </p>

                        <h3 class="font-semibold mb-2">
                          0. Academic Nature of the App
                        </h3>
                        <p class="mb-2 text-sm">
                          0.1. This App is part of an academic project and is
                          provided as-is for experimental or educational use
                          only.
                        </p>
                        <p class="mb-2 text-sm">
                          0.2. We make no guarantees of availability,
                          reliability, or long-term support of either the
                          application or data stored.
                        </p>
                        <p class="mb-4 text-sm">
                          0.3. The App may be shut down or altered at any time
                          without notice.
                        </p>

                        <h3 class="font-semibold mb-2">
                          1. Account Registration and Security
                        </h3>
                        <p class="mb-2 text-sm">
                          1.1. To use the App, you must create an account and
                          provide accurate, up-to-date information.
                        </p>
                        <p class="mb-2 text-sm">
                          1.2. You are responsible for maintaining the
                          confidentiality of your password and account
                          credentials.
                        </p>
                        <p class="mb-4 text-sm">
                          1.3. All passwords are encrypted for security;
                          however, you acknowledge that no system is completely
                          secure.
                        </p>

                        <h3 class="font-semibold mb-2">
                          2. User-Generated Content
                        </h3>
                        <p class="mb-2 text-sm">
                          2.1. You retain ownership of any notes, text, images,
                          or other content ("User Content") you create within
                          the App.
                        </p>
                        <p class="mb-2 text-sm">
                          2.2. User Content is not encrypted. You acknowledge
                          and accept any risks associated with storing
                          unencrypted data.
                        </p>
                        <p class="mb-4 text-sm">
                          2.3. You grant us a non-exclusive, worldwide,
                          royalty-free license to use, store, display, and
                          distribute User Content as necessary to operate the
                          App.
                        </p>

                        <h3 class="font-semibold mb-2">
                          3. Intellectual Property
                        </h3>
                        <p class="mb-2 text-sm">
                          3.1. All software, designs, logos, trademarks, and
                          other elements of the App are owned by or licensed to
                          the Company.
                        </p>
                        <p class="mb-4 text-sm">
                          3.2. You may not copy, modify, distribute, or
                          reverse-engineer any part of the App without our
                          express permission.
                        </p>

                        <h3 class="font-semibold mb-2">
                          4. Data Privacy & Security
                        </h3>
                        <p class="mb-2 text-sm">
                          4.1. While passwords are encrypted, User Content is
                          stored in plaintext and is not encrypted. By using the
                          App, you accept this limitation.
                        </p>
                        <p class="mb-2 text-sm">
                          4.2. We take reasonable security measures to protect
                          your data but cannot guarantee complete security.
                        </p>
                        <p class="mb-4 text-sm">
                          4.3. Our use of personal data is governed by our
                          Privacy Policy.
                        </p>

                        <h3 class="font-semibold mb-2">
                          5. Prohibited Conduct
                        </h3>
                        <p class="mb-2 text-sm">5.1. You agree not to:</p>
                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Use the App for any illegal or unauthorised
                            purposes.
                          </li>
                          <li class="mb-1">
                            Upload content that infringes on third-party rights.
                          </li>
                          <li class="mb-1">
                            Attempt to hack, disrupt, or misuse the App.
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">6. Termination</h3>
                        <p class="mb-2 text-sm">
                          6.1. We may suspend or terminate your account if you
                          violate these Terms.
                        </p>
                        <p class="mb-4 text-sm">
                          6.2. You may delete your account at any time, but some
                          data may be retained for legal or operational
                          purposes.
                        </p>

                        <h3 class="font-semibold mb-2">
                          7. Disclaimers & Liability Limits
                        </h3>
                        <p class="mb-2 text-sm">
                          7.1. The App is provided "as is" without warranties of
                          any kind.
                        </p>
                        <p class="mb-4 text-sm">
                          7.2. We are not responsible for any loss, damage, or
                          unauthorised access to your data.
                        </p>

                        <h3 class="font-semibold mb-2">
                          8. Changes to These Terms
                        </h3>
                        <p class="mb-4 text-sm">
                          8.1. We may update these Terms from time to time.
                          Continued use of the App after updates means you
                          accept the new Terms.
                        </p>

                        <h3 class="font-semibold mb-2">9. Contact Us</h3>
                        <p class="mb-4 text-sm">
                          If you have any questions, please contact us at
                          <a
                            href="mailto:hf165122@hrsfc.ac.uk"
                            class="text-primary hover:underline"
                            >hf165122@hrsfc.ac.uk</a
                          >
                        </p>
        </div>
      </ScrollArea>
      <!-- <DialogFooter>
      <Button @click="isTermsDialogOpen = false">Close</Button>
    </DialogFooter> -->
    </DialogContent>
  </Dialog>

  <Dialog v-model:open="isPrivacyDialogOpen">
    <DialogContent class="overflow-y-none w-[900px] sm:w-[450px]">
      <!-- <DialogHeader>
        <DialogTitle>Terms and Conditions</DialogTitle>
        <DialogDescription>
          Please read our terms and conditions carefully.
        </DialogDescription>
      </DialogHeader>  -->
      <ScrollArea class="h-[60vh] overflow-y-auto">
        <div class="pr-4">
          <h2 class="text-xl font-bold mb-3">Privacy Policy</h2>
          <p class="text-sm text-gray-500 mb-4">Last Updated: 28/4/25</p>

          <p class="mb-4 text-sm">
                          Welcome to NovaNote (“the App”) . We respect your
                          privacy and are committed to protecting your personal
                          data. This Privacy Policy explains how we collect,
                          use, and store your information when you use the App.
                          The App is provided by Henry Field (“Company,” “we,”
                          “us,” or “our”) as part of an academic project, not
                          for commercial purposes. We comply with the UK General
                          Data Protection Regulation (“UK GDPR”) and the Data
                          Protection Act 2018.
                        </p>

                        <h3 class="font-semibold mb-2">1. Who We Are</h3>
                        <p class="mb-4 text-sm">
                          Henry Field is the data controller for the purposes of
                          UK data protection law. If you have any questions,
                          please contact us at:
                          <a
                            href="mailto:hf165122@hrsfc.ac.uk"
                            class="text-primary hover:underline"
                            >hf165122@hrsfc.ac.uk</a
                          >
                        </p>

                        <h3 class="font-semibold mb-2">
                          2. What Data We Collect
                        </h3>
                        <p class="mb-2 text-sm">
                          When you register or use the App, we collect:
                        </p>
                        <ul class="list-disc pl-8 mb-2 text-sm">
                          <li class="mb-1">Your email address</li>
                          <li class="mb-1">A username of your choice</li>
                        </ul>

                        <p class="mb-4 text-sm">
                          We do not collect any sensitive personal data, such as
                          health information or financial data.
                        </p>

                        <h3 class="font-semibold mb-2">
                          3. How We Use Your Data
                        </h3>
                        <p class="mb-2 text-sm">
                          We use your information for the following purposes:
                        </p>
                        <ul class="list-disc pl-8 mb-2 text-sm">
                          <li class="mb-1">
                            To create and manage your account
                          </li>
                          <li class="mb-1">
                            To provide you access to the App and its features
                          </li>
                          <li class="mb-1">
                            For academic research and analysis (in anonymised or
                            aggregated form)
                          </li>
                          <li class="mb-1">
                            To communicate with you if necessary about
                            service-related issues
                          </li>
                        </ul>

                        <p class="mb-4 text-sm">
                          We do not use your data for marketing purposes or
                          targeted advertising.
                        </p>

                        <h3 class="font-semibold mb-2">
                          4. Legal Basis for Processing
                        </h3>
                        <p class="mb-2 text-sm">
                          Under the UK GDPR, our lawful basis for processing
                          your personal data is:
                        </p>
                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Consent — when you create an account, you consent to
                            us using your information as described.
                          </li>
                          <li class="mb-1">
                            Legitimate interests — to operate and improve the
                            App for academic and research purposes.
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">
                          5. How We Store and Protect Your Data
                        </h3>

                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            Your data is stored securely on hardware owned an
                            operated by the company in the UK.
                          </li>
                          <li class="mb-1">Passwords are encrypted.</li>
                          <li class="mb-1">
                            We take reasonable steps to protect your information
                            but no system is completely secure.
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">6. Data Sharing</h3>
                        <p class="mb-2 text-sm">
                          We do not sell, rent, or share your personal data with
                          third parties.
                        </p>
                        <p class="mb-2 text-sm">
                          We may utilise anonymised, aggregated data for
                          academic research purposes only.
                        </p>
                        <p class="mb-4 text-sm">
                          We may disclose personal data if required to do so by
                          law.
                        </p>

                        <h3 class="font-semibold mb-2">7. Data Retention</h3>
                        <p class="mb-2 text-sm">
                          We will retain your personal information for as long
                          as necessary for the academic project.
                        </p>
                        <p class="mb-4 text-sm">
                          Once the project ends or your account is deleted, your
                          data will either be anonymised or securely deleted
                          within 30 days.
                        </p>

                        <h3 class="font-semibold mb-2">
                          8. Your Rights Under UK GDPR
                        </h3>
                        <p class="mb-2 text-sm">
                          You have the following rights:
                        </p>
                        <ul class="list-disc pl-8 mb-4 text-sm">
                          <li class="mb-1">
                            The right to access your personal data
                          </li>
                          <li class="mb-1">
                            Right to correct inaccurate or incomplete data
                          </li>
                          <li class="mb-1">
                            Right to request deletion of your data (“right to be
                            forgotten”)
                          </li>
                          <li class="mb-1">
                            The right to restrict processing of your data
                          </li>
                          <li class="mb-1">
                            Right to withdraw consent at any time
                          </li>
                        </ul>

                        <p class="mb-2 text-sm">
                          To exercise any of these rights, please contact us at
                          <a
                            href="mailto:hf165122@hrsfc.ac.uk"
                            class="text-primary hover:underline"
                            >hf165122@hrsfc.ac.uk</a
                          >
                        </p>

                        <p class="mb-4 text-sm">
                          If you are unhappy with how we handle your data, you
                          can also complain to the UK Information Commissioner’s
                          Office (ICO):
                          <a
                            href="https://ico.org.uk/concerns/"
                            target="_blank"
                            rel="noopener noreferrer"
                            class="text-primary hover:underline"
                            >https://ico.org.uk/concerns/</a
                          >
                        </p>

                        <h3 class="font-semibold mb-2">
                          9. Use of Local Storage and Session Storage
                        </h3>
                        <p class="mb-2 text-sm">
                          We use your device’s local storage and session storage
                          to enhance your experience within the App.
                          Specifically, we use storage for the following
                          purposes:
                        </p>
                        <p class="mb-2 text-sm">Session Storage:</p>
                        <ul class="list-disc pl-8 mb-2 text-sm">
                          <li class="mb-1">
                            We temporarily store authentication tokens
                            during your active session to enable secure login
                            and access to your account features.
                          </li>
                          <li class="mb-1">
                            To maintain your session state and preferences.
                          </li>
                        </ul>
                        <p class="mb-2 text-sm">Local Storage:</p>
                        <ul class="list-disc pl-8 mb-2 text-sm">
                          <li class="mb-1">
                            We store your documents locally on your device to
                            allow for offline access to your notes and content
                            when you are not connected to the internet.
                          </li>
                          <li class="mb-1">
                            We store user preferences and settings to enhance
                            your experience within the App.
                          </li>
                          <li class="mb-1">
                            We store authentication tokens to allow for
                            "remember me" functionality, enabling you to stay
                            logged in across browsing sessions.
                          </li>
                          <li class="mb-1">
                            We do not use local storage to track your activity
                            or collect personal data.
                          </li>
                        </ul>

                        <h3 class="font-semibold mb-2">
                          10. Changes to This Privacy Policy
                        </h3>
                        <p class="mb-4 text-sm">
                          We may update this Privacy Policy occasionally. If
                          significant changes are made, we will notify users via
                          the App or by email.
                        </p>

                        <h3 class="font-semibold mb-2">11. Contact us</h3>
                        <p class="mb-4 text-sm">
                          If you have any questions about this Privacy Policy or
                          how your data is handled, please contact:
                          <a
                            href="mailto:hf165122@hrsfc.ac.uk"
                            class="text-primary hover:underline"
                            >hf165122@hrsfc.ac.uk</a
                          >
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
                  >Terms and Conditions</a
                >

                and 

                <a
                  href="#"
                  class="text-blue-500"
                  @click.prevent="isPrivacyDialogOpen = true"
                  >Privacy Policy</a
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
