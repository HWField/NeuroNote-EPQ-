<script lang="ts">
export const description = "A sidebar that collapses to icons.";
export const iframeHeight = "800px";
export const containerClass = "w-full h-full";
</script>

<script setup lang="ts">
import Cytoscape from "@/components/Cytoscape.vue";
import tabview from "@/components/tabview.vue";
import Note from "@/components/Note.vue";
import LightDark from "@/components/LightDark.vue";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import Toaster from '@/components/ui/toast/Toaster.vue'
import { useToast } from '@/components/ui/toast/use-toast'
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Separator } from "@/components/ui/separator";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarInset,
  SidebarMenu,
  SidebarMenuAction,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
  SidebarProvider,
  SidebarRail,
  SidebarTrigger,
  SidebarSeparator,
  SidebarGroupAction,
  SidebarGroupContent,
  SidebarMenuBadge,
} from "@/components/ui/sidebar";
import {
  Command,
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
  CommandShortcut,
} from "@/components/ui/command";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { useRouter, useRoute } from "vue-router"; // Vue Router for navigation
import {
  Settings,
  Bell,
  ChevronsUpDown,
  GalleryVerticalEnd,
  LogOut,
  MoreHorizontal,
  Plus,
  Sparkles,
  Search,
  Home,
  MessagesSquare,
  X,
  GripVertical,
} from "lucide-vue-next";
import * as icons from "lucide-vue-next";

import { useMagicKeys } from "@vueuse/core";
import { watch } from "vue";
import { computed } from "vue";
import { ref, markRaw } from "vue";
import draggable from "vuedraggable";

import { useTabStore } from '@/stores/useTabStore';

const router = useRouter(); // Router instance for programmatic navigation
const route = useRoute(); // Current route to access query parameters
const { toast } = useToast();
const tabStore = useTabStore();
const tabs = computed(() => tabStore.tabs);
const activeTab = computed(() => tabStore.activeTab);


const activeTabKey = computed(() => `${activeTab.value}-${Date.now()}`);


const getActiveComponent = computed(() => {
  return tabs.value.find(tab => tab.id === activeTab.value)?.component || null;
});

function closeTab(id) {
  tabStore.removeTab(id);
}

function switchTab(id) {
  tabStore.setActiveTab(id);
}

function openNewTab() {
  // Example: Adding a new tab dynamically
  tabStore.addTab('New Tab','cytoscape');
}

async function logOut() {
  toast({
        title: 'Success',
        description: 'Sucesfully logged out',
         variant: 'success'
      });
  //await new Promise(resolve => setTimeout(resolve, 500)); // Wait for 1 second to show message before going to dashboard
  localStorage.removeItem('token');  // Remove expired token
  tabStore.clearStore();  // Clear tab store
  router.replace("/login");   // Or redirect to login page using Vue Router
  console.error("Logging out")

  
}
// This is sample data.
const data = {
  user: {
    name: "Henry",
    email: "Henry@henryfield.net",
    avatar: "/avatars/shadcn.jpg",
  },
  teams: [
    {
      name: "School",
      logo: GalleryVerticalEnd,
      plan: "Personal",
    },
  ],
  navMain: [
    {
      title: "Getting Started",
      url: "#",
      items: [
        { title: "Installation", url: "#" },
        { title: "Project Structure", url: "#" },
      ],
    },
    {
      title: "Building Your Application",
      url: "#",
      items: [
        { title: "Routing", url: "#" },
        { title: "Data Fetching", url: "#", isActive: true },
        { title: "Rendering", url: "#" },
        { title: "Caching", url: "#" },
        { title: "Styling", url: "#" },
        { title: "Optimizing", url: "#" },
        { title: "Configuring", url: "#" },
        { title: "Testing", url: "#" },
        { title: "Authentication", url: "#" },
        { title: "Deploying", url: "#" },
        { title: "Upgrading", url: "#" },
        { title: "Examples", url: "#" },
      ],
    },
    {
      title: "API Reference",
      url: "#",
      items: [
        { title: "Components", url: "#" },
        { title: "File Conventions", url: "#" },
        { title: "Functions", url: "#" },
        { title: "next.config.js Options", url: "#" },
        { title: "CLI", url: "#" },
        { title: "Edge Runtime", url: "#" },
      ],
    },
    {
      title: "Architecture",
      url: "#",
      items: [
        { title: "Accessibility", url: "#" },
        { title: "Fast Refresh", url: "#" },
        { title: "Next.js Compiler", url: "#" },
        { title: "Supported Browsers", url: "#" },
        { title: "Turbopack", url: "#" },
      ],
    },
  ],
};


const activeTeam = ref(data.teams[0]);

function setActiveTeam(team: (typeof data.teams)[number]) {
  activeTeam.value = team;
}

const open = ref(false);

const { Meta_J, Ctrl_J } = useMagicKeys({
  passive: false,
  onEventFired(e) {
    if (e.key === "j" && (e.metaKey || e.ctrlKey)) e.preventDefault();
  },
});

watch([Meta_J, Ctrl_J], (v) => {
  if (v[0] || v[1]) handleOpenChange();
});

function handleOpenChange() {
  open.value = !open.value;
}
</script>

<template>
  <Toaster /> 

  <CommandDialog v-model:open="open">
    <CommandInput placeholder="Type a command or search..." />
    <CommandList>
      <CommandEmpty>No results found.</CommandEmpty>
      <CommandGroup heading="Suggestions">
        <CommandItem value="calendar"> Calendar </CommandItem>
        <CommandItem value="search-emoji"> Search Emoji </CommandItem>
        <CommandItem value="calculator"> Calculator </CommandItem>
      </CommandGroup>
      <CommandSeparator />
      <CommandGroup heading="Settings">
        <CommandItem value="profile"> Profile </CommandItem>
        <CommandItem value="billing"> Billing </CommandItem>
        <CommandItem value="settings"> Settings </CommandItem>
      </CommandGroup>
    </CommandList>
  </CommandDialog>

  <SidebarProvider>
    <Sidebar collapsible="icon" variant="floating" side="left">
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <DropdownMenu>
              <DropdownMenuTrigger as-child>
                <SidebarMenuButton
                  size="lg"
                  class="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
                >
                  <div
                    class="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground"
                  >
                    <component :is="activeTeam.logo" class="size-4" />
                  </div>
                  <div class="grid flex-1 text-left text-sm leading-tight">
                    <span class="truncate font-semibold">{{
                      activeTeam.name
                    }}</span>
                    <span class="truncate text-xs">{{ activeTeam.plan }}</span>
                  </div>
                  <ChevronsUpDown class="ml-auto" />
                </SidebarMenuButton>
              </DropdownMenuTrigger>
              <DropdownMenuContent
                class="w-[--radix-dropdown-menu-trigger-width] min-w-56 rounded-lg"
                align="start"
                side="bottom"
                :side-offset="4"
              >
                <DropdownMenuLabel class="text-xs text-muted-foreground">
                  Views
                </DropdownMenuLabel>
                <DropdownMenuItem
                  v-for="(team, index) in data.teams"
                  :key="team.name"
                  class="gap-2 p-2"
                  @click="setActiveTeam(team)"
                >
                  <div
                    class="flex size-6 items-center justify-center rounded-sm border"
                  >
                    <component :is="team.logo" class="size-4 shrink-0" />
                  </div>
                  {{ team.name }}
                  <DropdownMenuShortcut>⌘{{ index + 1 }}</DropdownMenuShortcut>
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem class="gap-2 p-2">
                  <div
                    class="flex size-6 items-center justify-center rounded-md border bg-background"
                  >
                    <Plus class="size-4" />
                  </div>
                  <div class="font-medium text-muted-foreground">Add View</div>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarSeparator />

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton>
                  <Search />
                  <a href="#"> Search </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton>
                  <Home />
                  <a @click="tabStore.activeTabId = 'home'"> Home </a>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton disabled>
                  <MessagesSquare />
                  <span> Chat (coming soon)</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>

        <SidebarSeparator />
        <SidebarGroup>
  <SidebarGroupLabel>Tabs:</SidebarGroupLabel>

  <!-- Add new tab button -->
  <SidebarGroupAction title="Add Tab" @click="openNewTab">
    <Plus /> <span class="sr-only">Add Tab</span>
  </SidebarGroupAction>

  <!-- Tab List -->
  <SidebarGroupContent>
    <div v-for="tab in tabs" :key="tab.id" class="flex items-center justify-between p-2 cursor-pointer rounded-md" 
         :class="{ 'bg-gray-200': tab.id === activeTab }" @click="switchTab(tab.id)">
      
      <span class="truncate">{{ tab.title }}</span>

      <!-- Close button (except for the first tab) -->
      <button  @click.stop="closeTab(tab.id)" class="text-red-500 hover:text-red-700">
        ✖
      </button>
    </div>
  </SidebarGroupContent>
</SidebarGroup>
      </SidebarContent>

      <SidebarFooter class="pb-[40px] md:pb-0"
        ><!-- lift up footer on mobile -->
        <SidebarMenu>
          <SidebarMenuItem>
            <DropdownMenu>
              <DropdownMenuTrigger as-child>
                <SidebarMenuButton
                  size="lg"
                  class="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
                >
                  <Avatar class="h-8 w-8 rounded-lg">
                    <AvatarImage
                      :src="data.user.avatar"
                      :alt="data.user.name"
                    />
                    <AvatarFallback class="rounded-lg">
                      {{ data.user.name[0] }}
                    </AvatarFallback>
                  </Avatar>
                  <div class="grid flex-1 text-left text-sm leading-tight">
                    <span class="truncate font-semibold">{{
                      data.user.name
                    }}</span>
                    <span class="truncate text-xs">{{ data.user.email }}</span>
                  </div>
                  <ChevronsUpDown class="ml-auto size-4" />
                </SidebarMenuButton>
              </DropdownMenuTrigger>
              <DropdownMenuContent
                class="w-[--radix-dropdown-menu-trigger-width] min-w-56 rounded-lg"
                side="bottom"
                align="end"
                :side-offset="4"
              >
                <DropdownMenuLabel class="p-0 font-normal">
                  <div
                    class="flex items-center gap-2 px-1 py-1.5 text-left text-sm"
                  >
                    <Avatar class="h-8 w-8 rounded-lg">
                      <AvatarImage
                        :src="data.user.avatar"
                        :alt="data.user.name"
                      />
                      <AvatarFallback class="rounded-lg"> CN </AvatarFallback>
                    </Avatar>
                    <div class="grid flex-1 text-left text-sm leading-tight">
                      <span class="truncate font-semibold">{{
                        data.user.name
                      }}</span>
                      <span class="truncate text-xs">{{
                        data.user.email
                      }}</span>
                    </div>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuGroup>
                  <DropdownMenuItem>
                    <Settings />
                    Settings
                  </DropdownMenuItem>

                  <DropdownMenuItem>
                    <Bell />
                    Notifications
                  </DropdownMenuItem>
                </DropdownMenuGroup>
                <DropdownMenuSeparator />
                <DropdownMenuItem @click="logOut()">
                  <LogOut />
                  Log out
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
      <!-- <SidebarRail /> -->
    </Sidebar>

    <SidebarInset class="overflow-hidden">
      <!-- Header -->
      <header class="flex h-16 shrink-0 items-center gap-2 border-b">
        <div class="flex items-center">
          <SidebarTrigger class="ml-1" />
          <Separator orientation="vertical" class="mx-2" />
          <span class="text-lg font-semibold">This is the Home Tab</span>

          <div class="absolute top-4 right-4">
            <LightDark class="bg-white p-4 rounded-lg shadow-lg"></LightDark>
          </div>
        </div>
      </header>

      <!-- Main Content -->

      <!-- <div class="flex flex-1 flex-col gap-4 p-4 pt-0 w-full">
        <KeepAlive>
          <Cytoscape class="grid auto-rows-min gap-4 w-full" />
        </KeepAlive> -->
        <!-- md:grid-cols-3 -->
      <!-- </div> -->
      

     
 

    <!-- Tab Content -->
    <div v-if="activeTab">
    <div class="flex flex-1 flex-col gap-4 p-4 pt-0 w-full" >
    
      <component
      :is="getActiveComponent"
      v-if="getActiveComponent"
      :key="activeTabKey"
      :tab-id="activeTab"    
      :tab-type="'cytoscape'"  
    />

    </div>
  </div>
    </SidebarInset>
  </SidebarProvider>
</template>
