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
import visualisation from '@/components/visualisation.vue'
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
                          Welcome to NeuroNote ("the App"), provided by Henry
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
                          Welcome to NeuroNote (“the App”) . We respect your
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
  <visualisation class="fixed inset-0 w-full h-full" />

  <!-- Authentication overlay -->
  <div class="relative z-10 min-h-screen flex items-center justify-center p-4">
    <!-- Logo in top left -->
    <div class="absolute top-6 left-6 z-20 hidden lg:blockn">
      <div class="logo-container">
        <img 
            src="/Logo.png" 
            alt="Neuronote Logo" 
            class="size-8 object-contain"
          />
        <span class="logo-text">NeuroNote</span>
      </div>
    </div>

    <!-- Dark/Light toggle in top right -->
    <!-- <div class="absolute top-6 right-6 z-20">
      <div class="glass-container p-2">
        <LightDark />
      </div>
    </div> -->

    <!-- Quote in bottom left (desktop only) -->
    <div class="absolute bottom-6 left-6 z-20 hidden lg:block max-w-sm">
      <div class="quote-container">
        <blockquote class="space-y-3">
          <p class="text-white/90 font-medium leading-relaxed">
            "The project is looking really good, it's quite impressive what you've created"
          </p>
          <footer class="text-sm text-purple-300">
            — Critical Software Developer
          </footer>
        </blockquote>
      </div>
    </div>

    <!-- Main authentication card -->
    <div class="auth-card">
      <form @submit.prevent="isRegisterView ? register() : login()">
        <!-- Header -->
        <div class="text-center space-y-3 mb-8">
          <h1 class="auth-title">
            {{ isRegisterView ? "Create Account" : "Welcome Back" }}
          </h1>
          <p class="auth-subtitle">
            {{ isRegisterView 
              ? "Join NeuroNote to start connecting your ideas" 
              : "Sign in to continue your journey" 
            }}
          </p>
        </div>

        <!-- Form fields -->
        <div class="space-y-5">
          <!-- Username (registration only) -->
          <div v-if="isRegisterView" class="form-group">
            <label for="username" class="form-label">Username</label>
            <input
              id="username"
              type="text"
              v-model="username"
              placeholder="Choose a username"
              class="form-input"
              required
            />
          </div>

          <!-- Email -->
          <div class="form-group">
            <label for="email" class="form-label">Email</label>
            <input
              id="email"
              type="email"
              v-model="email"
              placeholder="Enter your email"
              class="form-input"
              required
            />
          </div>

          <!-- Password -->
          <div class="form-group">
            <label for="password" class="form-label">Password</label>
            <input
              id="password"
              type="password"
              v-model="password"
              placeholder="Enter your password"
              class="form-input"
              required
            />
          </div>

          <!-- Terms checkbox (registration only) -->
          <div v-if="isRegisterView" class="flex items-start space-x-3 pt-2">
            <input
              id="terms"
              type="checkbox"
              v-model="terms"
              class="form-checkbox"
            />
            <label for="terms" class="text-sm text-white/80 leading-relaxed">
              I agree to the
              <button
                type="button"
                class="text-purple-300 hover:text-purple-200 underline"
                @click="isTermsDialogOpen = true"
              >
                Terms and Conditions
              </button>
              and
              <button
                type="button"
                class="text-purple-300 hover:text-purple-200 underline"
                @click="isPrivacyDialogOpen = true"
              >
                Privacy Policy
              </button>
            </label>
          </div>
        </div>

        <!-- Submit button -->
        <button type="submit" class="auth-button">
          {{ isRegisterView ? "Create Account" : "Sign In" }}
        </button>

        <!-- Toggle between login/register -->
        <div class="text-center mt-6">
          <span class="text-sm text-white/70">
            {{ isRegisterView ? "Already have an account?" : "Don't have an account?" }}
          </span>
          <button
            type="button"
            class="text-sm text-purple-300 hover:text-purple-200 ml-1 font-medium underline"
            @click="isRegisterView = !isRegisterView"
          >
            {{ isRegisterView ? "Sign in" : "Create one" }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>
<style scoped>
/* Glass container base */
.glass-container {
  background: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(168, 85, 247, 0.15);
  border-radius: 12px;
}

/* Logo styling */
.logo-container {
  @apply glass-container;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
}

.logo-text {
  font-size: 1.25rem;
  font-weight: 700;
  background: linear-gradient(135deg, #a855f7, #e879f9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Quote styling */
.quote-container {
  @apply glass-container;
  padding: 24px;
  background: rgba(0, 0, 0, 0.25);
}

/* Main auth card */
.auth-card {
  width: 100%;
  max-width: 420px;
  background: rgba(0, 0, 0, 0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(168, 85, 247, 0.2);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.08);
}

/* Typography */
.auth-title {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, #a855f7, #e879f9);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
}

.auth-subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.95rem;
  line-height: 1.5;
}

/* Form elements */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  color: rgba(255, 255, 255, 0.9);
  font-size: 0.875rem;
  font-weight: 500;
}

.form-input {
  height: 48px;
  padding: 0 16px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(168, 85, 247, 0.2);
  border-radius: 12px;
  color: white;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.4);
}

.form-input:focus {
  outline: none;
  border-color: rgba(168, 85, 247, 0.5);
  background: rgba(255, 255, 255, 0.12);
  box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.1);
}

.form-checkbox {
  width: 18px;
  height: 18px;
  margin-top: 2px;
  accent-color: #a855f7;
}

/* Auth button */
.auth-button {
  width: 100%;
  height: 48px;
  margin-top: 32px;
  background: linear-gradient(135deg, #a855f7, #c084fc);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 
    0 8px 24px rgba(168, 85, 247, 0.4),
    0 0 0 1px rgba(255, 255, 255, 0.1);
}

.auth-button:hover {
  transform: translateY(-2px);
  background: linear-gradient(135deg, #9333ea, #a855f7);
  box-shadow: 
    0 12px 32px rgba(168, 85, 247, 0.5),
    0 0 0 1px rgba(255, 255, 255, 0.2);
}

.auth-button:active {
  transform: translateY(0);
}

/* Dialog styling */
.dialog-content {
  background: rgba(0, 0, 0, 0.9);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(168, 85, 247, 0.2);
  color: white;
}

/* Mobile responsive */
@media (max-width: 768px) {
  .auth-card {
    margin: 20px;
    padding: 32px 24px;
  }
  
  .auth-title {
    font-size: 1.75rem;
  }
  
  .quote-container {
    display: none;
  }
}
</style>