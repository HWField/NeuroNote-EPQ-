<script setup>
import Cytoscape from "@/components/Cytoscape.vue";
import { useUserStore } from "@/stores/useUserStore";
import { useGraphStore } from "@/stores/useGraphStore";
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { useToast } from "@/components/ui/toast/use-toast";
import { Calendar } from "@/components/ui/calendar";
import {
  Settings,
  FileText,
  Home,
  Book,
  Star,
  Search,
  Tag,
} from "lucide-vue-next";
import { Button } from "@/components/ui/button";
import ScrollArea from "./ui/scroll-area/ScrollArea.vue";

import { useTabStore } from "@/stores/useTabStore";
const tabStore = useTabStore();

const userStore = useUserStore();
const graphStore = useGraphStore();
const { toast } = useToast();
const screenSize = ref("small");
let active = ref(false);

const activeFilters = ref([]);
const tabData = computed(() => {
  const tab = tabStore.getTab(1);
  if (!tab) return {};
  return tab.state;
});

const handleFilterChange = (newFilters) => {
  activeFilters.value = newFilters;
  tabStore.updateTabState(1, {
    ...tabData.value,
    filters: newFilters,
  });
};

const OpenNote = (noteId) => {
  const Id = noteId.split("_")[1];
  console.error("Note selected", Id);
  const note = graphStore.elements.find((el) => el.id === parseInt(Id));

  if (!note) {
    toast({
      title: "Oops something went wrong",
      description: `that note doesn't seem to exist?`,
      variant: "destructive",
    });
    return;
  }

  tabStore.addTab(note.name, "generic", { view: "note", noteId: Id });
};

const updateScreenSize = () => {
  const width = window.innerWidth;
  if (width >= 1024) {
    screenSize.value = "large";
  } else if (width >= 768) {
    screenSize.value = "medium";
  } else {
    screenSize.value = "small";
  }
};

onMounted(() => {
  updateScreenSize();
  window.addEventListener("resize", updateScreenSize);
  if (tabData.value.filters) {
    activeFilters.value = tabData.value.filters;
  }
  active = true;
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", updateScreenSize);
  active = false;
});

const recentNotes = computed(() => {
  if (!userStore.recentNotes || userStore.recentNotes.length === 0) {
    return [];
  }

  return (
    userStore.recentNotes
      // First filter out notes that don't exist in graphStore
      .filter(
        (noteId) =>
          graphStore.elements &&
          graphStore.elements.some(
            (el) => el.type === "note" && el.id === noteId
          )
      )
      // Then map the remaining valid notes
      .map((noteId) => {
        const noteElement = graphStore.elements.find(
          (el) => el.type === "note" && el.id === noteId
        );

        return {
          id: noteId,
          title: noteElement.name, // We can safely access name since we filtered
        };
      })
  );
});

// Get total counts for stats
const stats = computed(() => {
  const notes =
    graphStore.elements?.filter((el) => el.type === "note")?.length || 0;
  const tags =
    graphStore.elements?.filter((el) => el.type === "tag")?.length || 0;

  // Count all connections
  let edgeCount = 0;

  // Count tag-tag connections (parent-child relationships)
  graphStore.elements?.forEach((element) => {
    if (element.type === "tag" && element.children?.length) {
      edgeCount += element.children.length;
    }
  });

  // Count tag-note connections
  graphStore.elements?.forEach((element) => {
    if (element.type === "note" && element.tags?.length) {
      edgeCount += element.tags.length;
    }
  });

  return { notes, tags, edges: edgeCount };
});
</script>

<template>
  <div class="h-full w-full">
    <!-- Desktop layout -->
    <div
      v-if="screenSize === 'large'"
      class="flex w-full h-full flex-col p-6 space-y-4"
    >
      <div class="h-full flex flex-col relative w-full">
        <!-- Welcome banner -->

        <div
          class="relative mb-4 rounded-xl overflow-hidden fade-in h-auto min-h-[120px]"
        >
          <!-- Glass background with purple gradient -->
          <div
            class="absolute inset-0 bg-gradient-to-r from-purple-600/80 via-purple-500/70 to-indigo-600/60 backdrop-blur-sm"
          ></div>

          <!-- Decorative elements (adjusted positioning) -->
          <div
            class="absolute -top-10 -right-10 w-32 h-32 bg-purple-300/20 rounded-full blur-xl"
          ></div>
          <div
            class="absolute bottom-0 left-1/3 w-40 h-40 bg-indigo-300/20 rounded-full blur-xl"
          ></div>
          <div
            class="absolute top-1/2 left-1/4 w-16 h-16 bg-pink-200/30 rounded-full blur-lg"
          ></div>

          <!-- Glass particles -->
          <div class="absolute inset-0 overflow-visible">
            <div
              class="absolute top-5 right-1/4 w-3 h-3 bg-white/40 rounded-full"
            ></div>
            <div
              class="absolute top-12 right-1/3 w-2 h-2 bg-white/30 rounded-full"
            ></div>
            <div
              class="absolute bottom-10 left-1/4 w-2 h-2 bg-white/30 rounded-full"
            ></div>
            <div
              class="absolute bottom-16 right-1/2 w-3 h-3 bg-white/20 rounded-full"
            ></div>
          </div>

          <!-- Content with improved spacing -->
          <div class="relative z-10 px-8 py-7 flex items-center">
            <!-- Left side -->
            <div class="flex-1">
              <h1 class="text-3xl font-bold text-white flex items-center">
                Welcome, {{ userStore.username }}
                <span class="inline-block ml-2 animate-bounce">👋</span>
              </h1>
              <p class="text-white/80 mt-2 mb-1 max-w-md">
                Your knowledge awaits :)
              </p>
            </div>

            <!-- Right side - decorative icon -->
            <div
              class="hidden md:flex items-center justify-center w-14 h-14 bg-white/10 backdrop-blur-md rounded-xl rotate-3 shadow-lg border border-white/20"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="text-white"
              >
                <circle cx="18" cy="5" r="3"></circle>
                <circle cx="6" cy="12" r="3"></circle>
                <circle cx="18" cy="19" r="3"></circle>
                <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
                <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
              </svg>
            </div>
          </div>

          <!-- Bottom glass border -->
          <div
            class="absolute bottom-0 left-0 right-0 h-1.5 bg-gradient-to-r from-purple-300/50 via-white/30 to-indigo-300/50 backdrop-blur-md"
          ></div>
        </div>

        <!-- Stats row -->
        <div
          class="flex flex-row w-full h-1/7 space-x-4 justify-evenly mb-4 fade-in-delay-200 opacity-0"
        >
          <div class="rounded-xl p-4 w-full flex flex-col bg-primary/10">
            <span class="text-xs uppercase text-muted-foreground font-medium"
              >Notes</span
            >
            <span class="text-2xl font-bold text-primary">{{
              stats.notes
            }}</span>
          </div>
          <div class="rounded-xl p-4 w-full flex flex-col bg-purple-500/10">
            <span class="text-xs uppercase text-muted-foreground font-medium"
              >Tags</span
            >
            <span class="text-2xl font-bold text-purple-500">{{
              stats.tags
            }}</span>
          </div>
          <div class="rounded-xl p-4 w-full flex flex-col bg-green-500/10">
            <span class="text-xs uppercase text-muted-foreground font-medium"
              >Connections</span
            >
            <span class="text-2xl font-bold text-green-500">{{
              stats.edges
            }}</span>
          </div>
        </div>

        <div class="flex flex-row space-x-4 h-full">
          <!-- Left Column (Tall) -->
          <div
            class="w-2/3 h-full mb-4 bg-primary-foreground rounded-xl shadow-md border border-border/30"
          >
            <Cytoscape
              v-if="active"
              @note-selected="OpenNote"
              :hasControls="true"
              :tabId="1"
              class="overflow-hidden"
            />
          </div>

          <!-- Right Column (Two Short Divs) -->
          <div class="relative flex w-1/3 flex-col h-full space-y-4">
            <!-- recent notes -->
            <div
              class="bg-primary-foreground rounded-xl flex-1 h-0 min-h-0 shadow-md border border-border/30 overflow-hidden transition-all duration-300 hover:shadow-lg flex flex-col"
            >
              <div class="flex items-center px-5 py-4 flex-shrink-0">
                <div class="w-1.5 h-6 bg-primary rounded-full mr-2"></div>
                <h2 class="text-xl font-bold flex-grow">Recent Notes</h2>
              </div>

              <div class="flex-1 min-h-0 overflow-auto px-5 pb-5">
                <ScrollArea
                  className="h-full"
                  style="
                    --scrollbar-size: 5px;
                    --scrollbar-thumb: rgb(var(--primary));
                    --scrollbar-track: transparent;
                  "
                >
                  <ul class="pr-4 space-y-2">
                    <li
                      v-for="(note, index) in recentNotes"
                      :key="note.id"
                      @click="OpenNote(`note_${note.id}`)"
                      class="p-3 rounded-lg bg-background/80 backdrop-blur-sm shadow-sm border border-border/20 cursor-pointer transition-all duration-200 hover:bg-background hover:shadow-md hover:-translate-y-[2px] flex items-center group"
                    >
                      <div
                        class="mr-3 flex-shrink-0 w-7 h-7 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-xs font-semibold transition-transform group-hover:scale-110"
                      >
                        {{ index + 1 }}
                      </div>
                      <div
                        class="mr-3 flex-shrink-0 text-primary transition-transform group-hover:rotate-12"
                      >
                        <FileText class="w-4 h-4" />
                      </div>
                      <div class="truncate font-medium">{{ note.title }}</div>
                    </li>
                  </ul>
                </ScrollArea>
              </div>
            </div>
            <!-- Shortcuts -->
            <div
              class="bg-primary-foreground rounded-xl shadow-md border border-border/30 overflow-hidden transition-all duration-300 hover:shadow-lg flex flex-col flex-shrink-0"
            >
              <div class="flex items-center px-5 py-4">
                <div class="w-1.5 h-6 bg-primary rounded-full mr-2"></div>
                <h2 class="text-xl font-bold flex-grow">Shortcuts</h2>
                <Button
                  variant="ghost"
                  size="icon"
                  class="rounded-full hover:bg-primary/10"
                >
                  <Settings class="h-5 w-5" />
                </Button>
              </div>

              <div class="grid grid-cols-2 gap-3 p-5">
                <Button
                  class="flex items-center justify-start p-3 h-auto border-border/30 hover:border-primary/50 group"
                >
                  <Home
                    class="mr-2 p-1 rounded-full bg-primary/10 transition-colors shortcut-icon"
                  />
                  <span>Home</span>
                </Button>
                <Button
                  class="flex items-center justify-start p-3 h-auto border-border/30 hover:border-primary/50 group"
                >
                  <Search
                    class="mr-2 p-1 rounded-full bg-primary/10 transition-colors shortcut-icon"
                  />
                  <span>Search</span>
                </Button>
                <Button
                  class="flex items-center justify-start p-3 h-auto border-border/30 hover:border-primary/50 group"
                >
                  <Book
                    class="mr-2 p-1 rounded-full bg-primary/10 transition-colors shortcut-icon"
                  />
                  <span>Notes</span>
                </Button>
                <Button
                  class="flex items-center justify-start p-3 h-auto border-border/30 hover:border-primary/50 group"
                >
                  <Tag
                    class="mr-2 p-1 rounded-full bg-primary/10 transition-colors shortcut-icon"
                  />
                  <span>Tags</span>
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Medium layout -->
    <div
      v-if="screenSize === 'medium'"
      class="flex w-full h-full flex-col p-4 space-y-4"
    >
      <div
        class="w-full h-1/2 mb-4 bg-primary-foreground rounded-xl shadow-md border border-border/30 overflow-hidden"
      >
        <Cytoscape
          v-if="active"
          @note-selected="OpenNote"
          :hasControls="true"
          :tabId="1"
          class="overflow-hidden"
        />
      </div>

      <div class="flex w-full h-1/2 space-x-4">
        <div
          class="bg-primary-foreground rounded-xl shadow-md border border-border/30 overflow-hidden transition-all duration-300 hover:shadow-lg flex-1 flex flex-col"
        >
          <div class="flex items-center px-5 py-4">
            <div class="w-1.5 h-6 bg-primary rounded-full mr-2"></div>
            <h2 class="text-xl font-bold flex-grow">Recent Notes</h2>
          </div>

          <div class="flex-1 overflow-hidden px-5 pb-5">
            <ScrollArea
              className="h-full"
              style="
                --scrollbar-size: 5px;
                --scrollbar-thumb: rgb(var(--primary));
                --scrollbar-track: transparent;
              "
            >
              <ul class="pr-4 space-y-2">
                <li
                  v-for="(note, index) in recentNotes"
                  :key="note.id"
                  @click="OpenNote(`note_${note.id}`)"
                  class="p-3 rounded-lg bg-background/80 backdrop-blur-sm shadow-sm border border-border/20 cursor-pointer transition-all duration-200 hover:bg-background hover:shadow-md hover:-translate-y-[2px] flex items-center group"
                >
                  <div
                    class="mr-3 flex-shrink-0 w-7 h-7 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-xs font-semibold transition-transform group-hover:scale-110"
                  >
                    {{ index + 1 }}
                  </div>
                  <div
                    class="mr-3 flex-shrink-0 text-primary transition-transform group-hover:rotate-12"
                  >
                    <FileText class="w-4 h-4" />
                  </div>
                  <div class="truncate font-medium">{{ note.title }}</div>
                </li>
              </ul>
            </ScrollArea>
          </div>
        </div>

        <div
          class="bg-primary-foreground rounded-xl shadow-md border border-border/30 overflow-hidden transition-all duration-300 hover:shadow-lg flex-1 flex flex-col"
        >
          <div class="flex items-center px-5 py-4">
            <div class="w-1.5 h-6 bg-primary rounded-full mr-2"></div>
            <h2 class="text-xl font-bold flex-grow">Shortcuts</h2>
            <Button
              variant="ghost"
              size="icon"
              class="rounded-full hover:bg-primary/10"
            >
              <Settings class="h-5 w-5" />
            </Button>
          </div>

          <div class="grid grid-cols-2 gap-3 p-5">
            <Button
              class="flex items-center justify-start p-3 h-auto border-border/30 hover:border-primary/50 group"
            >
              <Home
                class="mr-2 p-1 rounded-full bg-primary/10 transition-colors shortcut-icon"
              />
              <span>Home</span>
            </Button>
            <Button
              class="flex items-center justify-start p-3 h-auto border-border/30 hover:border-primary/50 group"
            >
              <Search
                class="mr-2 p-1 rounded-full bg-primary/10 transition-colors shortcut-icon"
              />
              <span>Search</span>
            </Button>
            <Button
              class="flex items-center justify-start p-3 h-auto border-border/30 hover:border-primary/50 group"
            >
              <Book
                class="mr-2 p-1 rounded-full bg-primary/10 transition-colors shortcut-icon"
              />
              <span>Notes</span>
            </Button>
            <Button
              class="flex items-center justify-start p-3 h-auto border-border/30 hover:border-primary/50 group"
            >
              <Tag
                class="mr-2 p-1 rounded-full bg-primary/10 transition-colors shortcut-icon"
              />
              <span>Tags</span>
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Small layout (mobile) -->
    <div
      v-if="screenSize === 'small'"
      class="flex w-full h-full flex-col p-3 space-y-4"
    >
      <!-- Welcome banner with explicit height -->
      <div
        class="relative mb-4 rounded-xl overflow-hidden fade-in h-auto min-h-[120px]"
      >
        <!-- Glass background with purple gradient -->
        <div
          class="absolute inset-0 bg-gradient-to-r from-purple-600/80 via-purple-500/70 to-indigo-600/60 backdrop-blur-sm"
        ></div>

        <!-- Decorative elements (adjusted positioning) -->
        <div
          class="absolute -top-10 -right-10 w-32 h-32 bg-purple-300/20 rounded-full blur-xl"
        ></div>
        <div
          class="absolute bottom-0 left-1/3 w-40 h-40 bg-indigo-300/20 rounded-full blur-xl"
        ></div>
        <div
          class="absolute top-1/2 left-1/4 w-16 h-16 bg-pink-200/30 rounded-full blur-lg"
        ></div>

        <!-- Glass particles -->
        <div class="absolute inset-0 overflow-visible">
          <div
            class="absolute top-5 right-1/4 w-3 h-3 bg-white/40 rounded-full"
          ></div>
          <div
            class="absolute top-12 right-1/3 w-2 h-2 bg-white/30 rounded-full"
          ></div>
          <div
            class="absolute bottom-10 left-1/4 w-2 h-2 bg-white/30 rounded-full"
          ></div>
          <div
            class="absolute bottom-16 right-1/2 w-3 h-3 bg-white/20 rounded-full"
          ></div>
        </div>

        <!-- Content with improved spacing -->
        <div class="relative z-10 px-8 py-7 flex items-center">
          <!-- Left side -->
          <div class="flex-1">
            <h1 class="text-3xl font-bold text-white flex items-center">
              Welcome, {{ userStore.username }}
              <span class="inline-block ml-2 animate-bounce">👋</span>
            </h1>
            <p class="text-white/80 mt-2 mb-1 max-w-md">
              Your knowledge graph awaits :)
            </p>
          </div>

          <!-- Right side - decorative icon -->
          <div
            class="hidden md:flex items-center justify-center w-14 h-14 bg-white/10 backdrop-blur-md rounded-xl rotate-3 shadow-lg border border-white/20"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="24"
              height="24"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="text-white"
            >
              <circle cx="18" cy="5" r="3"></circle>
              <circle cx="6" cy="12" r="3"></circle>
              <circle cx="18" cy="19" r="3"></circle>
              <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
              <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
            </svg>
          </div>
        </div>

        <!-- Bottom glass border -->
        <div
          class="absolute bottom-0 left-0 right-0 h-1.5 bg-gradient-to-r from-purple-300/50 via-white/30 to-indigo-300/50 backdrop-blur-md"
        ></div>
      </div>

      <div
        class="w-full h-full border border-border/30 bg-primary-foreground rounded-xl shadow-md overflow-hidden"
      >
        <Cytoscape
          v-if="active"
          @note-selected="OpenNote"
          :hasControls="true"
          :tabId="1"
          class="overflow-hidden"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.fade-in {
  animation: fadeIn 0.6s ease-out forwards;
}

.fade-in-delay-200 {
  animation: fadeIn 0.6s ease-out 0.2s forwards;
}

.welcome-banner-bg {
  background: linear-gradient(
    to right,
    rgba(var(--primary), 0.8),
    rgba(var(--primary), 0.3)
  );
}

:global(.dark) .welcome-banner-bg {
  background: linear-gradient(
    to right,
    rgba(var(--primary), 0.6),
    rgba(var(--primary), 0.2)
  );
}
</style>
