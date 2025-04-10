<template>
  <div class="h-full flex flex-col overflow-hidden">
    <header class="border-b py-4 px-6">
      <h1 class="text-2xl font-bold">Settings</h1>
      <p class="text-muted-foreground text-sm mt-1">
        Manage your preferences and account settings
      </p>
    </header>

    <div class="flex flex-col md:flex-row flex-1 overflow-hidden">
      <!-- Settings Navigation -->
      <div class="w-full md:w-64 shrink-0 border-r bg-card">
        <nav class="p-2">
          <Button
            v-for="tab in tabs"
            :key="tab.id"
            :variant="currentTab === tab.id ? 'default' : 'ghost'"
            class="w-full justify-start mb-1 gap-2 font-medium"
            @click="currentTab = tab.id"
          >
            <component :is="tab.icon" class="h-4 w-4" />
            {{ tab.name }}
          </Button>
        </nav>
      </div>

      <!-- Settings Content -->

      <div class="w-full h-full p-6">
        <ScrollArea
          class="editor w-full h-full overflow-y-auto bg-primary-foreground rounded-lg border border-input"
        >
          <div class="flex-1 overflow-y-auto p-6">
            <!-- Account Settings -->
            <div v-if="currentTab === 'account'" class="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Your Profile</CardTitle>
                  <CardDescription>
                    Manage your account information and credentials
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div class="space-y-4">
                    <div class="flex items-center space-x-4">
                      <div class="flex items-center space-x-4">
                        <Avatar class="h-20 w-20 rounded-md border">
                          <AvatarImage :src="getBaseUrl() + userStore.avatar" alt="Profile" />
                          <AvatarFallback class="text-lg">{{
                            userStore.username[0]
                          }}</AvatarFallback>
                        </Avatar>
                        <div>
                          <!-- Hidden file input -->
                          <input
                            type="file"
                            id="avatar-upload"
                            ref="fileInput"
                            @change="uploadAvatar"
                            accept="image/*"
                            class="hidden"
                          />
                          <!-- Button that triggers the file input -->
                          <Button
                            size="sm"
                            variant="outline"
                            @click="$refs.fileInput.click()"
                            :disabled="isUploading"
                          >
                            {{ isUploading ? "Uploading..." : "Change Avatar" }}
                          </Button>
                        </div>
                      </div>
                    </div>

                    <div class="space-y-4 pt-4">
                      <div class="space-y-2">
                        <Label for="username">Username</Label>
                        <Input id="username" v-model="username" />
                      </div>
                      <div class="space-y-2">
                        <Label for="email">Email</Label>
                        <Input id="email" v-model="email" type="email" />
                      </div>
                    </div>
                  </div>
                </CardContent>
                <CardFooter class="flex justify-end">
                  <Button @click="ResetAccount" variant="outline" class="mr-2"
                    >Cancel</Button
                  >
                  <Button @click="SaveAccount">Save Changes</Button>
                </CardFooter>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Change Password</CardTitle>
                  <CardDescription>
                    Update your password to keep your account secure
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div class="space-y-4">
                    <div class="space-y-2">
                      <Label for="currentPassword">Current Password</Label>
                      <Input
                        id="currentPassword"
                        v-model="currentPassword"
                        type="password"
                      />
                    </div>
                    <div class="space-y-2">
                      <Label for="newPassword">New Password</Label>
                      <Input
                        id="newPassword"
                        v-model="newPassword"
                        type="password"
                      />

                      <div v-if="newPassword" class="mt-1">
                        <div
                          class="h-1 w-full bg-muted rounded-full overflow-hidden"
                        >
                          <div
                            class="h-full transition-all duration-300 rounded-full"
                            :class="passwordStrength.color"
                            :style="`width: ${passwordStrength.score}%`"
                          ></div>
                        </div>
                        <p
                          class="text-xs mt-1"
                          :class="passwordStrength.textColor"
                        >
                          {{ passwordStrength.text }}
                        </p>
                      </div>
                    </div>
                    <div class="space-y-2">
                      <Label for="confirmPassword">Confirm Password</Label>
                      <Input
                        id="confirmPassword"
                        v-model="confirmPassword"
                        type="password"
                      />
                    </div>
                  </div>
                </CardContent>
                <CardFooter class="flex justify-end">
                  <Button @click="ResetPassword" variant="outline" class="mr-2"
                    >Cancel</Button
                  >
                  <Button @click="SavePassword">Update Password</Button>
                </CardFooter>
              </Card>
            </div>

            <!-- Interface Settings -->
            <div v-if="currentTab === 'interface'" class="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Theme Preferences</CardTitle>
                  <CardDescription>
                    Customize the look and feel of your application
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div class="space-y-6">
                    <div>
                      <h3 class="text-sm font-medium mb-3">Color Theme</h3>
                      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div
                          v-for="theme in themes"
                          :key="theme.id"
                          class="border-2 rounded-lg p-2 cursor-pointer transition-all"
                          :class="{
                            'border-primary': selectedTheme === theme.id,
                            'border-border': selectedTheme !== theme.id,
                          }"
                          @click="selectedTheme = theme.id"
                        >
                          <div class="h-24 rounded-md overflow-hidden mb-2">
                            <img
                              :src="theme.preview"
                              :alt="theme.name"
                              class="w-full h-full object-cover"
                            />
                          </div>
                          <div class="flex items-center justify-between">
                            <span class="text-sm font-medium">{{
                              theme.name
                            }}</span>
                            <Check
                              v-if="selectedTheme === theme.id"
                              class="h-4 w-4 text-primary"
                            />
                          </div>
                        </div>
                      </div>
                    </div>

                    <Separator />

                    <div>
                      <h3 class="text-sm font-medium mb-3">Appearance Mode</h3>
                      <RadioGroup
                        v-model="colorMode"
                        class="grid grid-cols-1 sm:grid-cols-3 gap-4"
                      >
                        <div>
                          <RadioGroupItem
                            value="light"
                            id="light"
                            class="peer sr-only"
                          />
                          <Label
                            for="light"
                            class="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary cursor-pointer"
                          >
                            <Sun class="h-6 w-6 mb-3" />
                            <div class="font-medium">Light</div>
                            <span class="text-xs text-muted-foreground"
                              >Default light theme</span
                            >
                          </Label>
                        </div>
                        <div>
                          <RadioGroupItem
                            value="dark"
                            id="dark"
                            class="peer sr-only"
                          />
                          <Label
                            for="dark"
                            class="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary cursor-pointer"
                          >
                            <Moon class="h-6 w-6 mb-3" />
                            <div class="font-medium">Dark</div>
                            <span class="text-xs text-muted-foreground"
                              >Dark mode theme</span
                            >
                          </Label>
                        </div>
                        <div>
                          <RadioGroupItem
                            value="system"
                            id="system"
                            class="peer sr-only"
                          />
                          <Label
                            for="system"
                            class="flex flex-col items-center justify-between rounded-md border-2 border-muted bg-popover p-4 hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary cursor-pointer"
                          >
                            <Monitor class="h-6 w-6 mb-3" />
                            <div class="font-medium">System</div>
                            <span class="text-xs text-muted-foreground"
                              >Follow system preference</span
                            >
                          </Label>
                        </div>
                      </RadioGroup>
                    </div>

                    <Separator />

                    <div class="space-y-3">
                      <h3 class="text-sm font-medium">Interface Options</h3>
                      <div class="flex items-center justify-between">
                        <div>
                          <Label class="text-sm font-medium"
                            >Animation Effects</Label
                          >
                          <p class="text-sm text-muted-foreground">
                            Enable fluid animations throughout the interface
                          </p>
                        </div>
                        <Switch v-model="animationsEnabled" />
                      </div>
                      <div class="flex items-center justify-between">
                        <div>
                          <Label class="text-sm font-medium"
                            >Compact Mode</Label
                          >
                          <p class="text-sm text-muted-foreground">
                            Use less space in the interface
                          </p>
                        </div>
                        <Switch v-model="compactMode" />
                      </div>
                    </div>
                  </div>
                </CardContent>
                <CardFooter class="flex justify-end space-x-2">
                  <Button variant="outline">Reset to Defaults</Button>
                  <Button @click="saveInterfaceSettings">Save Changes</Button>
                </CardFooter>
              </Card>
            </div>

            <!-- Extensions Settings -->
            <div v-if="currentTab === 'extensions'" class="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Extensions</CardTitle>
                  <CardDescription>
                    Manage and customize installed extensions
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div class="space-y-2">
                    <div
                      v-for="extension in extensions"
                      :key="extension.id"
                      class="flex items-start space-x-4 p-3 rounded-lg hover:bg-muted/50"
                    >
                      <div class="rounded-md bg-primary/10 p-2 flex-shrink-0">
                        <component
                          :is="extension.icon"
                          class="h-5 w-5 text-primary"
                        />
                      </div>
                      <div class="flex-1 space-y-1">
                        <div class="flex items-center justify-between">
                          <h3 class="font-medium text-base">
                            {{ extension.name }}
                          </h3>
                          <Switch v-model="extension.enabled" />
                        </div>
                        <p class="text-sm text-muted-foreground">
                          {{ extension.description }}
                        </p>
                        <div class="flex items-center space-x-2 mt-2">
                          <Badge variant="outline">{{
                            extension.version
                          }}</Badge>
                          <Badge v-if="extension.author" variant="secondary"
                            >By {{ extension.author }}</Badge
                          >
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
                <CardFooter>
                  <Button variant="outline" class="w-full" disabled
                    >Browse Extension Marketplace (Coming Soon)</Button
                  >
                </CardFooter>
              </Card>
            </div>

            <!-- Advanced Settings -->
            <div v-if="currentTab === 'advanced'" class="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Data Management</CardTitle>
                  <CardDescription>
                    Manage your data and export options
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div class="space-y-4">
                    <div class="flex items-center justify-between">
                      <div>
                        <h3 class="text-sm font-medium">Auto-save</h3>
                        <p class="text-sm text-muted-foreground">
                          Automatically save your work every few minutes
                        </p>
                      </div>
                      <Switch v-model="autoSaveEnabled" />
                    </div>

                    <Separator />

                    <div class="space-y-2">
                      <h3 class="text-sm font-medium">Export Data</h3>
                      <p class="text-sm text-muted-foreground">
                        Export all your notes and tags as a backup
                      </p>
                      <div class="flex space-x-2 mt-2">
                        <Button variant="outline" size="sm"
                          >Export as JSON</Button
                        >
                        <Button variant="outline" size="sm"
                          >Export as Markdown</Button
                        >
                      </div>
                    </div>

                    <Separator />

                    <div class="space-y-2">
                      <h3 class="text-sm font-medium">Data Storage</h3>
                      <p class="text-sm text-muted-foreground">
                        You are currently using 42MB of storage (10% of your
                        quota)
                      </p>
                      <div class="w-full bg-muted h-2 rounded-full mt-2">
                        <div
                          class="bg-primary h-2 rounded-full"
                          style="width: 10%"
                        ></div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle class="text-destructive">Danger Zone</CardTitle>
                  <CardDescription>
                    Irreversible actions that affect your account
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div class="space-y-4">
                    <div
                      class="flex flex-col sm:flex-row sm:items-center justify-between space-y-2 sm:space-y-0 sm:space-x-4"
                    >
                      <div>
                        <h3 class="text-sm font-medium">Delete All Data</h3>
                        <p class="text-sm text-muted-foreground">
                          Remove all notes, tags, and connections
                        </p>
                      </div>
                      <Button variant="destructive" size="sm"
                        >Delete All Data</Button
                      >
                    </div>

                    <Separator />

                    <div
                      class="flex flex-col sm:flex-row sm:items-center justify-between space-y-2 sm:space-y-0 sm:space-x-4"
                    >
                      <div>
                        <h3 class="text-sm font-medium">Delete Account</h3>
                        <p class="text-sm text-muted-foreground">
                          Permanently delete your account and all associated
                          data
                        </p>
                      </div>
                      <Button variant="destructive" size="sm"
                        >Delete Account</Button
                      >
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </ScrollArea>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios, { getBaseUrl } from "../axios.js";
import { useToast } from "@/components/ui/toast/use-toast";
import { useGraphStore } from "@/stores/useGraphStore";
import { useUserStore } from "@/stores/useUserStore";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import {
  User,
  Palette,
  Puzzle,
  Settings as SettingsIcon,
  Check,
  Sun,
  Moon,
  Monitor,
  FileText,
  Eye,
  Brain,
  Calculator,
  Calendar,
  Clock,
  Code,
} from "lucide-vue-next";

const graphStore = useGraphStore();
const userStore = useUserStore();
const { toast } = useToast();

// Tab navigation
const currentTab = ref("account");
const tabs = [
  { id: "account", name: "Account", icon: User },
  { id: "interface", name: "Interface", icon: Palette },
  { id: "extensions", name: "Extensions", icon: Puzzle },
  { id: "advanced", name: "Advanced", icon: SettingsIcon },
];

// Account settings
const fileInput = ref(null);
const isUploading = ref(false);
const username = ref("");
const email = ref("");
const currentPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");
const passwordStrength = computed(() => {
  if (!newPassword.value)
    return { score: 0, text: "", color: "", textColor: "" };

  // Simple password scoring logic
  const password = newPassword.value;
  let score = 0;

  // Length check
  if (password.length > 0) score += 20;
  if (password.length >= 8) score += 20;

  // Character type checks
  if (/[A-Z]/.test(password)) score += 20;
  if (/[0-9]/.test(password)) score += 20;
  if (/[^A-Za-z0-9]/.test(password)) score += 20;

  // Determine text and color based on score
  let text, color, textColor;

  if (score <= 20) {
    text = "Very weak";
    color = "bg-red-500";
    textColor = "text-red-500";
  } else if (score <= 40) {
    text = "Weak";
    color = "bg-orange-500";
    textColor = "text-orange-500";
  } else if (score <= 60) {
    text = "Fair";
    color = "bg-yellow-500";
    textColor = "text-yellow-500";
  } else if (score <= 80) {
    text = "Good";
    color = "bg-blue-500";
    textColor = "text-blue-500";
  } else {
    text = "Strong";
    color = "bg-green-500";
    textColor = "text-green-500";
  }

  return { score, text, color, textColor };
});
const avatar = ref(""); // Default avatar path

// Interface settings
const selectedTheme = ref("system");
const colorMode = ref("system");
const animationsEnabled = ref(true);
const compactMode = ref(false);
const autoSaveEnabled = ref(true);
// Extension settings
const extensions = ref([
  {
    id: "markdown-extended",
    name: "Markdown Extended",
    description:
      "Advanced markdown features including tables, diagrams, and math equations",
    icon: FileText,
    version: "v1.3.2",
    // author:
    enabled: true,
  },
  {
    id: "focus-mode",
    name: "Focus Mode",
    description:
      "Distraction-free writing environment with pomodoro timer and goals tracking",
    icon: Eye,
    version: "v2.0.1",

    enabled: true,
  },
  {
    id: "ai-assistant",
    name: "AI Assistant",
    description:
      "Smart content suggestions and automated note organization using AI",
    icon: Brain,
    version: "v0.9.5",

    enabled: false,
  },
  {
    id: "calculator",
    name: "Calculator",
    description:
      "Inline calculations in your notes with support for unit conversions",
    icon: Calculator,
    version: "v1.1.0",

    enabled: false,
  },
  {
    id: "calendar-integration",
    name: "Calendar Integration",
    description:
      "Link notes to calendar events and get reminders for related content",
    icon: Calendar,
    version: "v2.2.1",

    enabled: true,
  },
]);

// Theme options
const themes = [
  {
    id: "system",
    name: "Default",
    preview:
      "https://via.placeholder.com/300x150/3498db/ffffff?text=Default+Theme",
  },
  {
    id: "purple",
    name: "Purple Haze",
    preview:
      "https://via.placeholder.com/300x150/9b59b6/ffffff?text=Purple+Theme",
  },
  {
    id: "green",
    name: "Forest",
    preview:
      "https://via.placeholder.com/300x150/27ae60/ffffff?text=Green+Theme",
  },
];

// Load user data on component mount
onMounted(() => {
  username.value = userStore.username || "";
  email.value = userStore.email || "";
  avatar.value = userStore.avatar || ""; // Load avatar from user store
});

// Save functions
async function SaveAccount() {
  try {
    const success = await useUserStore().saveUser({
      username: username.value,
      email: email.value,
    });

    if (success) {
      toast({
        title: "Account updated",
        description: "Your account information has been updated.",
        variant: "success",
      });
    } else {
      toast({
        title: "Error",
        description:
          "oops there was an error updating your account, please try again later",
        variant: "destructive",
      });
    }
  } catch (error) {
    toast({
      title: "Error",
      description: "An unexpected error occurred. Please try again.",
      variant: "destructive",
    });
  }
}

function ResetAccount() {
  // Reset to original values
  username.value = userStore.username;
  email.value = userStore.email;
}
async function uploadAvatar(event) {
  const file = event.target.files[0];
  if (!file) return;

  isUploading.value = true;

  try {
    // Create form data
    const formData = new FormData();
    formData.append("file", file);

    // Send to server
    const response = await axios.post("/upload-file", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
        Authorization: `Bearer ${userStore.token}`, // Assuming token is stored in userStore
      },
    });

    // Update avatar with new URL
    avatar.value = response.data.url;
    console.error("Avatar URL:", avatar.value);
    // Save to user profile
    await userStore.saveUser({
      avatar: { avatar: avatar.value },
    });

    toast({
      title: "Avatar updated",
      description: "Your profile picture has been changed successfully.",
      variant: "success",
    });
  } catch (error) {
    console.error("Error uploading avatar:", error);
    toast({
      title: "Upload failed",
      description:
        "There was a problem uploading your image. Please try again.",
      variant: "destructive",
    });
  } finally {
    isUploading.value = false;
    // Clear the file input so the same file can be selected again
    event.target.value = "";
  }
}
async function SavePassword() {
  if (newPassword.value !== confirmPassword.value) {
    toast({
      title: "Error",
      description: "New password and confirmation do not match.",
      variant: "destructive",
    });
    ResetPassword();
    return;
  }
  try {
    const success = await useUserStore().saveUser({
      currentPassword: currentPassword.value,
      newPassword: newPassword.value,
    });

    if (success) {
      toast({
        title: "Password updated",
        description: "Your password has been changed successfully.",
        variant: "success",
      });
    } else {
      toast({
        title: "Error",
        description:
          "Failed to update password. Please check your current password.",
        variant: "destructive",
      });
    }
  } catch (error) {
    toast({
      title: "Error",
      description: "An unexpected error occurred. Please try again.",
      variant: "destructive",
    });
  }
  ResetPassword();
}
function ResetPassword() {
  // Reset password fields
  currentPassword.value = "";
  newPassword.value = "";
  confirmPassword.value = "";
}

function saveInterfaceSettings() {
  // In a real app, you'd save these preferences
  localStorage.setItem("theme", selectedTheme.value);
  localStorage.setItem("colorMode", colorMode.value);
  localStorage.setItem("animations", animationsEnabled.value);
  localStorage.setItem("compactMode", compactMode.value);

  toast({
    title: "Interface preferences saved",
    description: "Your interface settings have been updated.",
    variant: "success",
  });
}
</script>
