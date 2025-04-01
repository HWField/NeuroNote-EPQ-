<template>
  <div class="w-full h-full p-6">
    <ScrollArea
      class="editor w-full h-full overflow-y-auto bg-primary-foreground rounded-lg border border-input"
    >
  <!-- max-h-[calc(100vh-12rem)]  -->
    <div class="max-w-2xl mx-auto p-6">
      <Card class="w-full">
        <CardHeader>
          <CardTitle class="text-2xl">Share Your Feedback</CardTitle>
          <CardDescription>
            Help us improve by sharing your experience. Your feedback is
            valuable to us.
          </CardDescription>
        </CardHeader>

        <CardContent class="space-y-6">
          <!-- Rating Stars -->
          <div class="space-y-2">
            <Label>Your Overall Experience</Label>
            <div class="flex items-center">
              <div class="flex space-x-1">
                <button
                  v-for="star in 5"
                  :key="star"
                  type="button"
                  @click="rating = star"
                  @mouseover="hoverRating = star"
                  @mouseleave="hoverRating = 0"
                  class="transition-transform hover:scale-110 focus:outline-none"
                >
                  <Star
                    :class="[
                      'w-8 h-8 transition-colors',
                      hoverRating >= star || rating >= star
                        ? 'text-yellow-400 fill-yellow-400'
                        : 'text-gray-300 dark:text-gray-600',
                    ]"
                  />
                </button>
              </div>
              <span class="ml-3 text-sm text-muted-foreground">
                {{ rating ? ratingLabels[rating - 1] : "Select a rating" }}
              </span>
            </div>
          </div>

          <!-- Category Selection -->
          <div class="space-y-2">
            <Label for="category">Feedback Category</Label>
            <Select v-model="category">
              <SelectTrigger id="category" class="w-full">
                <SelectValue placeholder="Select a category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="general">General Feedback</SelectItem>
                <SelectItem value="ui">User Interface</SelectItem>
                <SelectItem value="feature">Feature Request</SelectItem>
                <SelectItem value="bug">Bug Report</SelectItem>
                <SelectItem value="performance">Performance Issues</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <!-- Feedback Message -->
          <div class="space-y-2">
            <Label for="message">Your Feedback</Label>
            <Textarea
              id="message"
              v-model="message"
              placeholder="Please share your thoughts, suggestions, or report any issues you encountered..."
              class="min-h-32"
            />
          </div>

          <!-- Contact Info (Optional) -->
          <!-- <div>
            <div class="flex items-center space-x-2 mb-4">
              <Label for="includeContact" class="text-sm font-medium">Include Acount Information</Label>
              <Switch id="includeContact" v-model="includeContact" />
            </div>
            
            <div v-if="includeContact" class="space-y-4">
              <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div class="space-y-2">
                  <Label for="name">Name</Label>
                  <Input id="name" v-model="name" placeholder="Your name" />
                </div>
                <div class="space-y-2">
                  <Label for="email">Email</Label>
                  <Input id="email" v-model="email" type="email" placeholder="your.email@example.com" />
                </div>
              </div>
            </div>
          </div> -->

          <!-- Screenshots -->
          <div class="space-y-2">
            <Label class="text-sm font-medium"
              >Add Screenshots (Optional)</Label
            >
            <div
              class="border-2 border-dashed rounded-lg p-6 text-center hover:bg-muted/50 cursor-pointer transition-colors"
            >
              <div
                class="flex flex-col items-center justify-center gap-1"
                @click="$refs.fileInput.click()"
              >
                <Upload class="h-6 w-6 text-muted-foreground" />
                <p class="text-sm text-muted-foreground">
                  Click to upload, or drag and drop
                </p>
                <p class="text-xs text-muted-foreground">PNG, JPG up to 5MB</p>
                <input
                  ref="fileInput"
                  type="file"
                  class="hidden"
                  accept="image/*"
                  @change="handleFileUpload"
                  multiple
                />
              </div>
            </div>

            <!-- Preview Uploaded Images -->
            <div
              v-if="screenshots.length > 0"
              class="flex flex-wrap gap-2 mt-3"
            >
              <div
                v-for="(screenshot, index) in screenshots"
                :key="index"
                class="relative"
              >
                <img
                  :src="screenshot.preview"
                  alt="Screenshot"
                  class="h-16 w-16 object-cover rounded-md"
                />
                <button
                  @click="removeScreenshot(index)"
                  class="absolute -top-2 -right-2 bg-background border rounded-full p-0.5"
                >
                  <X class="h-3 w-3" />
                </button>
              </div>
            </div>
          </div>
        </CardContent>

        <CardFooter class="flex-col sm:flex-row gap-2">
          <Button variant="outline" class="sm:mr-auto" @click="resetForm">
            Reset Form
          </Button>
          <Button
            type="submit"
            :disabled="isSubmitting || !isValid"
            @click="submitFeedback"
            class="min-w-24"
          >
            <Loader2 v-if="isSubmitting" class="mr-2 h-4 w-4 animate-spin" />
            {{ isSubmitting ? "Submitting..." : "Submit Feedback" }}
          </Button>
        </CardFooter>
      </Card>

      <!-- Success Message -->
      <Transition name="fade">
        <div
          v-if="showSuccess"
          class="fixed inset-0 flex items-center justify-center bg-black/30 z-50"
        >
          <Card class="w-[90%] max-w-md">
            <CardHeader>
              <div
                class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-green-100 dark:bg-green-900"
              >
                <Check class="h-6 w-6 text-green-600 dark:text-green-400" />
              </div>
              <CardTitle class="text-center mt-3"
                >Thank You For Your Feedback!</CardTitle
              >
            </CardHeader>
            <CardContent>
              <p class="text-center text-muted-foreground">
                We appreciate your input and will use it to improve your
                experience.
              </p>
            </CardContent>
            <CardFooter class="flex justify-center">
              <Button @click="closeSuccess">Done</Button>
            </CardFooter>
          </Card>
        </div>
      </Transition>
    </div>
  </ScrollArea>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from "vue";

import axios from "../axios"; // Import the Axios instance
import { ScrollArea } from "@/components/ui/scroll-area";
import { useTabStore } from "@/stores/useTabStore";
import { useToast } from "@/components/ui/toast/use-toast";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from "@/components/ui/select";
import { Star, Upload, X, Check, Loader2 } from "lucide-vue-next";

const { toast } = useToast();

// Form Data
const rating = ref(0);
const hoverRating = ref(0);
const category = ref("");
const message = ref("");
const includeAccount = ref(true);
const name = ref("");
const email = ref("");
const screenshots = ref([]);
const isSubmitting = ref(false);
const showSuccess = ref(false);

// Rating Labels
const ratingLabels = ["Poor", "Fair", "Good", "Very Good", "Excellent"];

// Form Validation
const isValid = computed(() => {
  return rating.value > 0 && category.value && message.value.trim().length > 0;
});

const tabid = useTabStore().GetActiveTabID();
onMounted(() => {
  let tabid = useTabStore().GetActiveTabID();
  console.error("Tab ID:", tabid);
  const tab = useTabStore().getTab(tabid);
  if (tab && tab.state) {
    // Restore form values from tab state
    rating.value = tab.state.rating || 0;
    category.value = tab.state.category || "";
    message.value = tab.state.message || "";
    // includeAccount.value = tab.state.includeAccount !== undefined ? tab.state.includeAccount : true;
    
    // Restore screenshots if they exist
    if (tab.state.screenshots && Array.isArray(tab.state.screenshots)) {
      screenshots.value = [...tab.state.screenshots];
    }
  }
});

// Save state when component unmounts
onBeforeUnmount(() => {
  saveFormState();
});

// Save state when form values change
// watch([rating, category, message, includeAccount, name, email, screenshots], () => {
//   saveFormState();
// }, { deep: true });

// Function to save form state to tab store
function saveFormState() {
  useTabStore().updateTabState(tabid, {
    rating: rating.value,
    category: category.value,
    message: message.value,
    includeAccount: includeAccount.value,
    name: name.value,
    email: email.value,
    screenshots: screenshots.value,
  });
}

// Handle Screenshot Upload
function handleFileUpload(event) {
  const files = event.target.files;
  if (!files.length) return;

  Array.from(files).forEach((file) => {
    // Check file size (5MB limit)
    if (file.size > 5 * 1024 * 1024) {
      toast({
        title: "File too large",
        description: `${file.name} exceeds the 5MB limit.`,
        variant: "destructive",
      });
      return;
    }

    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      screenshots.value.push({
        file: file,
        preview: e.target.result,
      });
    };
    reader.readAsDataURL(file);
  });

  // Reset input
  event.target.value = "";
}

function removeScreenshot(index) {
  screenshots.value.splice(index, 1);
}

function resetForm() {
  rating.value = 0;
  hoverRating.value = 0;
  category.value = "";
  message.value = "";
  includeAccount.value = true;
  name.value = "";
  email.value = "";
  screenshots.value = [];
  saveFormState();
}

async function submitFeedback() {
  if (!isValid.value) return;

  isSubmitting.value = true;

  try {
    // Prepare screenshot data as an array of base64 strings
    const screenshotData = {};
    screenshots.value.forEach((item, index) => {
      screenshotData[`screenshot_${index}`] = item.preview;
    });

    // Send to backend
    const response = await axios.post("/feedback", {
      rating: rating.value,
      category: category.value,
      message: message.value,
      screenshots: screenshotData,
    });

    if (response.data.status === "success") {
      showSuccess.value = true;
      resetForm();

      toast({
        title: "Feedback submitted",
        description: "Thank you for your feedback!",
        variant: "success",
      });
    }
  } catch (error) {
    console.error("Error submitting feedback:", error);
    toast({
      title: "Submission failed",
      description:
        error.response?.data?.message ||
        "There was an error submitting your feedback. Please try again.",
      variant: "destructive",
    });
  } finally {
    isSubmitting.value = false;
  }
}

function closeSuccess() {
  showSuccess.value = false;
}


</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
