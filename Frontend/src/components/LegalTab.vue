<template>
  <div class="h-full flex flex-col overflow-hidden">
    <header class="border-b py-4 px-6">
      <h1 class="text-2xl font-bold">Legal</h1>
      <p class="text-muted-foreground text-sm mt-1">Select a tab below to view Legal content</p>
    </header>

    <div class="flex flex-col flex-1 overflow-hidden">
      <!-- Mobile: Dropdown selector -->
      <div class="md:hidden border-b bg-card p-4">
        <Select v-model="currentTab">
          <SelectTrigger class="w-full">
            <SelectValue>
              <div class="flex items-center gap-2">
                <component
                  :is="tabs.find((tab) => tab.id === currentTab)?.icon"
                  class="h-4 w-4"
                />
                {{ tabs.find((tab) => tab.id === currentTab)?.name }}
              </div>
            </SelectValue>
          </SelectTrigger>
          <SelectContent>
            <SelectItem v-for="tab in tabs" :key="tab.id" :value="tab.id">
              <div class="flex items-center gap-2">
                <component :is="tab.icon" class="h-4 w-4" />
                {{ tab.name }}
              </div>
            </SelectItem>
          </SelectContent>
        </Select>
      </div>

      <!-- Mobile Content -->
      <div class="md:hidden flex-1 min-h-0 overflow-hidden p-6">
        <ScrollArea class="h-full w-full bg-primary-foreground rounded-lg border border-input">
          <div class="p-6">
            <LegalContent :current-tab="currentTab" />
          </div>
        </ScrollArea>
      </div>

      <!-- Desktop & Tablet: Side navigation -->
      <div class="hidden md:flex flex-1 overflow-hidden">
        <div class="w-80 flex-shrink-0 border-r bg-card">
          <nav class="p-4 space-y-1">
            <Button
              v-for="tab in tabs"
              :key="tab.id"
              :variant="currentTab === tab.id ? 'default' : 'ghost'"
              class="w-full justify-start gap-3 h-12 text-sm font-medium"
              @click="currentTab = tab.id"
            >
              <component :is="tab.icon" class="h-5 w-5" />
              <span class="truncate">{{ tab.name }}</span>
            </Button>
          </nav>
        </div>

        <!-- Desktop Content Area -->
        <div class="flex-1 min-h-0 overflow-hidden p-6">
          <ScrollArea class="h-full w-full bg-primary-foreground rounded-lg border border-input">
            <div class="p-6">
              <LegalContent :current-tab="currentTab" />
            </div>
          </ScrollArea>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from "vue";
import axios, { getBaseUrl } from "../axios.js";
import { useToast } from "@/components/ui/toast/use-toast";
import { useGraphStore } from "@/stores/useGraphStore";
import { useUserStore } from "@/stores/useUserStore";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
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
  EyeOff,
  Handshake,
} from "lucide-vue-next";
import LegalContent from "./LegalContent.vue";
const graphStore = useGraphStore();
const userStore = useUserStore();
const { toast } = useToast();

// Tab navigation
const currentTab = ref("TermsAndConditions");
const tabs = [
  { id: "TermsAndConditions", name: "Terms And Conditions", icon: Handshake },
  { id: "PrivacyPolicy", name: "Privacy Policy", icon: EyeOff },
  { id: "Acknowledgements", name: "Acknowledgements", icon: Puzzle },
];

// Load user data on component mount
onMounted(() => {});
</script>
