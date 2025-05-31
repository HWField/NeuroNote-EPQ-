<script setup>
import Cytoscape from "@/components/Cytoscape.vue";
import { useUserStore } from "@/stores/useUserStore";
import { useGraphStore } from "@/stores/useGraphStore";
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
import { useToast } from "@/components/ui/toast/use-toast";
import { Calendar } from "@/components/ui/calendar";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Check, ChevronsUpDown } from "lucide-vue-next";
import {
  Settings,
  FileText,
  Home,
  Book,
  Star,
  Search,
  Tag,
  Presentation,
  Plus,
  Pencil,
} from "lucide-vue-next";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import ScrollArea from "./ui/scroll-area/ScrollArea.vue";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
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

  tabStore.addTab(note.name, "note", { noteId: Id, creationTabId: 1 });
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
  active.value = true;
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
          format: noteElement.format,
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

let shortcutsDialogOpen = ref(false);
const editingShortcuts = ref([]);
const shortcutTypes = ["Note", "Tag"];

function openShortcutsDialog() {
  shortcutsDialogOpen.value = true;
  editingShortcuts.value = JSON.parse(JSON.stringify(userStore.shortcuts));
  setTimeout(() => {
    const inputElement = document.querySelector("#main");
    if (inputElement) inputElement.focus();
  }, 50);
}

function cancelDialogue() {
  shortcutsDialogOpen.value = false;
}

function closeDialogue() {
  shortcutsDialogOpen.value = false;
}
function addNewShortcut() {
  editingShortcuts.value.push({
    id: Date.now().toString(), // Generate a unique ID
    label: "New Shortcut",
    action: "",
    params: "",
  });
}
function deleteShortcut(index) {
  editingShortcuts.value.splice(index, 1);
}
async function saveShortcuts() {
  // userStore.updateShortcuts(editingShortcuts.value);
  const success = await useUserStore().saveUser({
    preferences: { shortcuts: editingShortcuts.value },
  });
  if (success) {
    userStore.shortcuts = editingShortcuts.value;
  }
  shortcutsDialogOpen.value = false;
}

// Helper function to update params based on action type
function updateShortcutParams(shortcut, action) {
  shortcut.action = action;
  if (action === "Note") {
    shortcut.params = { noteId: "" };
  } else if (action === "Tag") {
    shortcut.params = { tagId: "" };
  }
}
const availableNotes = computed(() => {
  return graphStore.elements
    .filter((el) => el.type === "note")
    .map((note) => ({
      value: note.id.toString(),
      label: note.name,
      format: note.format,
    }));
});

const availableTags = computed(() => {
  return graphStore.elements
    .filter((el) => el.type === "tag")
    .map((tag) => ({
      value: tag.id.toString(),
      label: tag.name,
    }));
});
const noteSearchQuery = ref("");
const tagSearchQuery = ref("");

const filteredNotes = computed(() => {
  const query = noteSearchQuery.value.toLowerCase();

  if (!query) return availableNotes.value;

  return availableNotes.value.filter((note) =>
    note.label.toLowerCase().includes(query)
  );
});

const filteredTags = computed(() => {
  const query = tagSearchQuery.value.toLowerCase();

  if (!query) return availableTags.value;

  return availableTags.value.filter((tag) =>
    tag.label.toLowerCase().includes(query)
  );
});

// For display selected note/tag name
function getNoteName(id) {
  const note = graphStore.elements.find(
    (el) => el.type === "note" && el.id === parseInt(id)
  );
  return note ? note.name : "Select a note";
}

function truncateName(name, limit = 20) {
  if (!name) return "";
  return name.length > limit ? `${name.substring(0, limit)}...` : name;
}
function getTagName(id) {
  const tag = graphStore.elements.find(
    (el) => el.type === "tag" && el.id === parseInt(id)
  );
  return tag ? tag.name : "Select a tag";
}

// For opening/closing popover state
const openNote = ref(null);
const openTag = ref(null);
</script>

<template>
  <Dialog
    :open="shortcutsDialogOpen"
    @update:open="(val) => !val && cancelDialogue()"
  >
    <DialogContent class="overflow-y-hidden min-auto sm:max-w-[800px]">
      <DialogHeader>
        <DialogTitle>Manage Shortcuts</DialogTitle>
        <DialogDescription>
          Create and edit shortcuts for quick access to frequently used
          features.
        </DialogDescription>
      </DialogHeader>

      <div class="py-4 overflow-y-hidden">
        <div class="overflow-hidden pr-1">
          <ScrollArea id="main" class="bl-5 h-[300px]">
            <div
              v-for="(shortcut, index) in editingShortcuts"
              :key="shortcut.id"
              class="flex items-center space-x-3 mb-3 p-2 rounded-md bg-muted/40 hover:bg-muted/70"
            >
              <!-- Shortcut Label (unchanged) -->
              <div class="flex-1">
                <label class="text-xs text-muted-foreground mb-1 block"
                  >Label</label
                >
                <Input v-model="shortcut.label" placeholder="Shortcut name" />
              </div>

              <!-- Action Type (unchanged) -->
              <div class="flex-1">
                <label class="text-xs text-muted-foreground mb-1 block"
                  >Type</label
                >
                <Select
                  v-model="shortcut.action"
                  @update:modelValue="
                    (val) => updateShortcutParams(shortcut, val)
                  "
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem
                      v-for="type in shortcutTypes"
                      :key="type"
                      :value="type"
                    >
                      {{ type }}
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <!-- Params (with searchable dropdowns) -->
              <div class="flex-1">
                <label class="text-xs text-muted-foreground mb-1 block"
                  >Value</label
                >

                <!-- Note Selector -->
                <div v-if="shortcut.action === 'Note'">
                  <Popover
                    :open="openNote === shortcut.id"
                    @update:open="
                      (val) => {
                        openNote = val ? shortcut.id : null;
                        if (!val) noteSearchQuery = ''; // Clear search when closing
                      }
                    "
                  >
                    <PopoverTrigger as-child>
                      <Button
                        variant="outline"
                        role="combobox"
                        :aria-expanded="openNote === shortcut.id"
                        class="w-full justify-between"
                      >
                        {{
                          shortcut.params?.noteId
                            ? truncateName(getNoteName(shortcut.params.noteId))
                            : "Select note..."
                        }}
                        <ChevronsUpDown
                          class="ml-2 h-4 w-4 shrink-0 opacity-50"
                        />
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent class="w-full p-0">
                      <div class="flex items-center px-3 pb-2">
                        <Search class="mr-2 h-4 w-4 shrink-0 opacity-50" />
                        <Input
                          v-model="noteSearchQuery"
                          placeholder="Search notes..."
                          class="h-9 w-full border-none bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0"
                        />
                      </div>
                      <div class="flex w-full">
                        <div
                          v-if="filteredNotes.length === 0"
                          class="w-full py-6 text-center text-sm"
                        >
                          No Notes found.
                        </div>

                        <ScrollArea v-else class="max-h-[200px] w-full">
                          <div class="flex flex-col gap-1 p-1">
                            <Button
                              v-for="note in filteredNotes"
                              :key="note.value"
                              variant="ghost"
                              @click="
                                () => {
                                  shortcut.params.noteId = note.value;
                                  noteSearchQuery = '';
                                  openNote = null;
                                }
                              "
                              class="justify-start text-left font-normal"
                              :class="{
                                'bg-accent':
                                  shortcut.params?.noteId === note.value,
                              }"
                            >
                              <FileText
                                v-if="note.format === 'document'"
                                class="mr-0 h-4 w-4 text-primary"
                              />
                              <Presentation
                                v-else-if="note.format === 'whiteboard'"
                                class="mr-0 h-4 w-4 text-primary"
                              />
                              <Check
                                :class="[
                                  'mr-2 h-4 w-4',
                                  shortcut.params?.noteId === note.value
                                    ? 'opacity-100'
                                    : 'opacity-0',
                                ]"
                              />
                              {{ truncateName(note.label, 50) }}
                            </Button>
                          </div>
                        </ScrollArea>
                      </div>
                    </PopoverContent>
                  </Popover>
                </div>

                <!-- Tag Selector -->
                <!-- Tag Selector -->
                <div v-else-if="shortcut.action === 'Tag'">
                  <Popover
                    :open="openTag === shortcut.id"
                    @update:open="
                      (val) => {
                        openTag = val ? shortcut.id : null;
                        if (!val) tagSearchQuery = ''; // Clear search when closing
                      }
                    "
                  >
                    <PopoverTrigger as-child>
                      <Button
                        variant="outline"
                        role="combobox"
                        :aria-expanded="openTag === shortcut.id"
                        class="w-full justify-between"
                      >
                        {{
                          shortcut.params?.tagId
                            ? truncateName(getTagName(shortcut.params.tagId))
                            : "Select tag..."
                        }}
                        <ChevronsUpDown
                          class="ml-2 h-4 w-4 shrink-0 opacity-50"
                        />
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent class="w-full p-0">
                      <div class="flex items-center px-3 pb-2">
                        <Search class="mr-2 h-4 w-4 shrink-0 opacity-50" />
                        <Input
                          v-model="tagSearchQuery"
                          placeholder="Search tags..."
                          class="h-9 w-full border-none bg-transparent focus-visible:ring-0 focus-visible:ring-offset-0"
                        />
                      </div>
                      <div class="flex w-full">
                        <div
                          v-if="filteredTags.length === 0"
                          class="w-full py-6 text-center text-sm"
                        >
                          No Tags found.
                        </div>

                        <ScrollArea v-else class="max-h-[200px] w-full">
                          <div class="flex flex-col gap-1 p-1">
                            <Button
                              v-for="tag in filteredTags"
                              :key="tag.value"
                              variant="ghost"
                              @click="
                                () => {
                                  shortcut.params.tagId = tag.value;
                                  tagSearchQuery = '';
                                  openTag = null;
                                }
                              "
                              class="justify-start text-left font-normal"
                              :class="{
                                'bg-accent':
                                  shortcut.params?.tagId === tag.value,
                              }"
                            >
                              <Tag class="mr-0 h-4 w-4 text-primary" />
                              <Check
                                :class="[
                                  'mr-2 h-4 w-4',
                                  shortcut.params?.tagId === tag.value
                                    ? 'opacity-100'
                                    : 'opacity-0',
                                ]"
                              />
                              {{ truncateName(tag.label, 500) }}
                            </Button>
                          </div>
                        </ScrollArea>
                      </div>
                    </PopoverContent>
                  </Popover>
                </div>

                <!-- Existing field for Create type -->
                <!-- <Input
                  v-else-if="shortcut.action === 'Create'"
                  v-model="shortcut.params.type"
                  placeholder="Creation type"
                />
                for search type
                <Input
                  v-else-if="shortcut.action === 'Search'"
                  v-model="shortcut.params.query"
                  placeholder="Search query"
                /> -->
              </div>

              <!-- Delete button (unchanged) -->
              <Button
                variant="destructive"
                size="icon"
                @click="deleteShortcut(index)"
                class="flex-shrink-0 self-end mb-1"
                title="Delete shortcut"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M3 6h18"></path>
                  <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                  <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
                </svg>
              </Button>
            </div>
          </ScrollArea>
        </div>

        <!-- Add new shortcut button -->
        <Button
          variant="outline"
          size="sm"
          @click="addNewShortcut"
          class="mt-3 w-full"
        >
          <Plus class="w-4 h-4 mr-1" />
          Add New Shortcut
        </Button>
      </div>

      <DialogFooter>
        <Button variant="outline" @click="cancelDialogue">Cancel</Button>
        <Button @click="saveShortcuts">Save Changes</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>

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
            class="w-2/3 h-full mb-4 bg-primary-foreground hover:shadow-lg rounded-xl shadow-md border border-border/30"
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
                        <FileText
                          v-if="note.format === 'document'"
                          class="w-4 h-4"
                        />
                        <Presentation
                          v-else-if="note.format === 'whiteboard'"
                          class="w-4 h-4"
                        />
                        <Presentation v-else class="w-4 h-4" />
                      </div>
                      <div class="truncate font-medium">{{ note.title }}</div>
                    </li>
                  </ul>
                </ScrollArea>
              </div>
            </div>
            <!-- Shortcuts -->
            <div
              class="bg-primary-foreground max-h-[50%] rounded-xl shadow-md border border-border/30 overflow-hidden transition-all duration-300 hover:shadow-lg flex flex-col flex-shrink-0"
            >
              <div class="flex items-center px-5 py-4">
                <div class="w-1.5 h-6 bg-primary rounded-full mr-2"></div>
                <h2 class="text-xl font-bold flex-grow">Shortcuts</h2>
                <Button
                  variant="ghost"
                  size="icon"
                  class="rounded-full hover:bg-primary/10"
                  @click="openShortcutsDialog()"
                >
                  <Pencil class="h-5 w-5" />
                </Button>
              </div>

              <!-- bento style -->
              <!-- <div class="flex flex-wrap gap-2 p-5">
                <Button
                  v-for="shortcut in userStore.shortcuts"
                  :key="shortcut.id"
                  @click="userStore.runShortcut(shortcut.id)"
                  class="flex items-center justify-start p-3 h-auto border-border/30 hover:border-primary/50 group shrink-0 grow-0"
                  style="min-width: fit-content; max-width: 180px"
                >
                  <div class="mr-2 rounded-md p-1.5">
                    <FileText
                      v-if="shortcut.action === 'Note'"
                      class="w-4 h-4"
                    />
                    <Tag v-if="shortcut.action === 'Tag'" class="w-4 h-4" />
                    <Plus v-if="shortcut.action === 'Create'" class="w-4 h-4" />
                    <Search
                      v-if="shortcut.action === 'Search'"
                      class="w-4 h-4"
                    />
                  </div>
                  <span class="truncate">{{ shortcut.label }}</span>
                </Button>
              </div> -->
              <div class="overflow-hidden">
                <div
                  v-if="
                    !userStore.shortcuts || userStore.shortcuts.length === 0
                  "
                  class="flex flex-col items-center justify-center p-6 h-full"
                >
                  <div class="text-center mb-2 text-muted-foreground">
                    No shortcuts set up yet
                  </div>
                  <div class="flex items-center text-sm text-primary">
                    <span>Click the pencil to add shortcuts</span>
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
                      class="ml-2 animate-bounce-right"
                    >
                      <path d="m18 15-6-6-6 6" />
                    </svg>
                  </div>
                </div>

                <ScrollArea class="h-full w-full p-5">
                  <div class="grid grid-cols-2 gap-3">
                    <Button
                      variant="outline"
                      :disabled="!shortcut.action || !shortcut.params"
                      class="flex items-center justify-start p-3 h-auto border-border/30 hover:border-primary/50 hover:shadow-lg group"
                      v-for="shortcut in userStore.shortcuts"
                      :key="shortcut.id"
                      @click="userStore.runShortcut(shortcut)"
                    >
                      <div
                        class="mr-3 flex-shrink-0 text-primary transition-transform group-hover:rotate-12"
                      >
                        <FileText
                          v-if="shortcut.action === 'Note'"
                          class="w-4 h-4 mr-2"
                        />
                        <Tag
                          v-if="shortcut.action === 'Tag'"
                          class="w-4 h-4 mr-2"
                        />
                        <Plus
                          v-if="shortcut.action === 'Create'"
                          class="w-4 h-4 mr-2"
                        />
                      </div>
                      <span class="truncate">{{ shortcut.label }}</span>
                    </Button>
                  </div>
                </ScrollArea>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
<!-- Medium layout (tablets, smaller laptops) -->
<div
  v-else-if="screenSize === 'medium'"
  class="flex w-full h-full flex-col p-4 space-y-3"
>
  <div class="h-full flex flex-col relative w-full">
    <!-- Welcome banner (slightly smaller for medium screens) -->
    <div class="relative mb-3 rounded-xl overflow-hidden fade-in h-auto min-h-[100px]">
      <!-- Glass background with purple gradient -->
      <div class="absolute inset-0 bg-gradient-to-r from-purple-600/80 via-purple-500/70 to-indigo-600/60 backdrop-blur-sm"></div>

      <!-- Decorative elements -->
      <div class="absolute -top-10 -right-10 w-24 h-24 bg-purple-300/20 rounded-full blur-xl"></div>
      <div class="absolute bottom-0 left-1/3 w-32 h-32 bg-indigo-300/20 rounded-full blur-xl"></div>
      
      <!-- Content with improved spacing -->
      <div class="relative z-10 px-6 py-5 flex items-center">
        <!-- Left side -->
        <div class="flex-1">
          <h1 class="text-2xl font-bold text-white flex items-center">
            Welcome, {{ userStore.username }}
            <span class="inline-block ml-2 animate-bounce">👋</span>
          </h1>
          <p class="text-white/80 mt-1 max-w-md text-sm">
            Your knowledge awaits :)
          </p>
        </div>
      </div>

      <!-- Bottom glass border -->
      <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-purple-300/50 via-white/30 to-indigo-300/50 backdrop-blur-md"></div>
    </div>

    <!-- Stats row -->
    <div class="flex flex-row w-full space-x-3 justify-evenly mb-3 fade-in-delay-200 opacity-0">
      <div class="rounded-xl p-3 w-full flex flex-col bg-primary/10">
        <span class="text-xs uppercase text-muted-foreground font-medium">Notes</span>
        <span class="text-xl font-bold text-primary">{{ stats.notes }}</span>
      </div>
      <div class="rounded-xl p-3 w-full flex flex-col bg-purple-500/10">
        <span class="text-xs uppercase text-muted-foreground font-medium">Tags</span>
        <span class="text-xl font-bold text-purple-500">{{ stats.tags }}</span>
      </div>
      <div class="rounded-xl p-3 w-full flex flex-col bg-green-500/10">
        <span class="text-xs uppercase text-muted-foreground font-medium">Connections</span>
        <span class="text-xl font-bold text-green-500">{{ stats.edges }}</span>
      </div>
    </div>

    <!-- Main content area - adjusted for medium screens -->
    <div class="flex flex-col space-y-3 h-full">
      <!-- Graph (takes full width) -->
      <div class="w-full h-1/2 mb-3 bg-primary-foreground hover:shadow-lg rounded-xl shadow-md border border-border/30 overflow-hidden">
        <Cytoscape
          v-if="active"
          @note-selected="OpenNote"
          :hasControls="true"
          :tabId="1"
          class="overflow-hidden"
        />
      </div>

      <!-- Bottom row (split for recent notes and shortcuts) -->
      <div class="flex flex-row space-x-3 h-1/2">
        <!-- Recent notes -->
        <div class="w-1/2 bg-primary-foreground rounded-xl shadow-md border border-border/30 overflow-hidden transition-all duration-300 hover:shadow-lg flex flex-col">
          <div class="flex items-center px-4 py-3 flex-shrink-0">
            <div class="w-1.5 h-5 bg-primary rounded-full mr-2"></div>
            <h2 class="text-lg font-bold flex-grow">Recent Notes</h2>
          </div>

          <div class="flex-1 min-h-0 overflow-auto px-4 pb-4">
            <ScrollArea className="h-full">
              <ul class="pr-4 space-y-2">
                <li
                  v-for="(note, index) in recentNotes"
                  :key="note.id"
                  @click="OpenNote(`note_${note.id}`)"
                  class="p-2 rounded-lg bg-background/80 backdrop-blur-sm shadow-sm border border-border/20 cursor-pointer transition-all duration-200 hover:bg-background hover:shadow-md hover:-translate-y-[2px] flex items-center group"
                >
                  <div class="mr-2 flex-shrink-0 w-6 h-6 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-xs font-semibold transition-transform group-hover:scale-110">
                    {{ index + 1 }}
                  </div>
                  <div class="mr-2 flex-shrink-0 text-primary transition-transform group-hover:rotate-12">
                    <FileText v-if="note.format === 'document'" class="w-4 h-4" />
                    <Presentation v-else-if="note.format === 'whiteboard'" class="w-4 h-4" />
                    <Presentation v-else class="w-4 h-4" />
                  </div>
                  <div class="truncate font-medium text-sm">{{ note.title }}</div>
                </li>
              </ul>
            </ScrollArea>
          </div>
        </div>

        <!-- Shortcuts -->
        <div class="w-1/2 bg-primary-foreground rounded-xl shadow-md border border-border/30 overflow-hidden transition-all duration-300 hover:shadow-lg flex flex-col">
          <div class="flex items-center px-4 py-3">
            <div class="w-1.5 h-5 bg-primary rounded-full mr-2"></div>
            <h2 class="text-lg font-bold flex-grow">Shortcuts</h2>
            <Button variant="ghost" size="icon" class="rounded-full hover:bg-primary/10" @click="openShortcutsDialog()">
              <Pencil class="h-4 w-4" />
            </Button>
          </div>

          <div class="overflow-hidden">
            <div v-if="!userStore.shortcuts || userStore.shortcuts.length === 0" class="flex flex-col items-center justify-center p-4 h-full">
              <div class="text-center mb-2 text-muted-foreground text-sm">
                No shortcuts set up yet
              </div>
              <div class="flex items-center text-xs text-primary">
                <span>Click the pencil to add shortcuts</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="ml-2 animate-bounce-right">
                  <path d="m18 15-6-6-6 6" />
                </svg>
              </div>
            </div>

            <ScrollArea class="h-full w-full p-3">
              <div class="grid grid-cols-1 gap-2">
                <Button
                  variant="outline"
                  :disabled="!shortcut.action || !shortcut.params"
                  class="flex items-center justify-start p-2 h-auto border-border/30 hover:border-primary/50 hover:shadow-lg group text-sm"
                  v-for="shortcut in userStore.shortcuts"
                  :key="shortcut.id"
                  @click="userStore.runShortcut(shortcut)"
                >
                  <div class="mr-2 flex-shrink-0 text-primary transition-transform group-hover:rotate-12">
                    <FileText v-if="shortcut.action === 'Note'" class="w-3 h-3 mr-1" />
                    <Tag v-if="shortcut.action === 'Tag'" class="w-3 h-3 mr-1" />
                    <Plus v-if="shortcut.action === 'Create'" class="w-3 h-3 mr-1" />
                  </div>
                  <span class="truncate">{{ shortcut.label }}</span>
                </Button>
              </div>
            </ScrollArea>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
 
<!-- Small layout (mobile, small tablets) -->
<div v-else-if="screenSize=='small'" class="flex w-full h-full flex-col p-3 space-y-3 overflow-auto">
  <!-- Welcome banner (compact for small screens) -->
  <div class="relative mb-3 rounded-xl overflow-hidden fade-in h-auto">
    <!-- Glass background with purple gradient -->
    <div class="absolute inset-0 bg-gradient-to-r from-purple-600/80 via-purple-500/70 to-indigo-600/60 backdrop-blur-sm"></div>
    
    <!-- Content -->
    <div class="relative z-10 px-4 py-4 flex items-center">
      <div class="flex-1">
        <h1 class="text-xl font-bold text-white flex items-center">
          Welcome, {{ userStore.username }}
          <span class="inline-block ml-2 animate-bounce">👋</span>
        </h1>
        <p class="text-white/80 mt-1 text-xs">
          Your knowledge awaits :)
        </p>
      </div>
    </div>
  </div>

  <!-- Stats (horizontal row) -->
  <div class="flex flex-row w-full space-x-2 justify-evenly mb-2 fade-in-delay-200 opacity-0">
    <div class="rounded-xl p-2 w-full flex flex-col bg-primary/10">
      <span class="text-xs uppercase text-muted-foreground font-medium">Notes</span>
      <span class="text-lg font-bold text-primary">{{ stats.notes }}</span>
    </div>
    <div class="rounded-xl p-2 w-full flex flex-col bg-purple-500/10">
      <span class="text-xs uppercase text-muted-foreground font-medium">Tags</span>
      <span class="text-lg font-bold text-purple-500">{{ stats.tags }}</span>
    </div>
    <div class="rounded-xl p-2 w-full flex flex-col bg-green-500/10">
      <span class="text-xs uppercase text-muted-foreground font-medium">Connections</span>
      <span class="text-lg font-bold text-green-500">{{ stats.edges }}</span>
    </div>
  </div>

  <!-- Graph (main content - taller) -->
  <div class="w-full flex-1 bg-primary-foreground hover:shadow-lg rounded-xl shadow-md border border-border/30 overflow-hidden min-h-[300px]">
    <Cytoscape
      v-if="active"
      @note-selected="OpenNote"
      :hasControls="true"
      :tabId="1"
      class="overflow-hidden"
    />
  </div>

  <!-- Bottom row with Recent Notes and Shortcuts side by side -->
  <div class="flex flex-row space-x-3">
    <!-- Recent Notes (side by side) -->
    <div class="w-1/2 bg-primary-foreground rounded-xl shadow-md border border-border/30 overflow-hidden transition-all duration-300 hover:shadow-lg flex flex-col">
      <div class="flex items-center px-3 py-2 flex-shrink-0">
        <div class="w-1 h-4 bg-primary rounded-full mr-2"></div>
        <h2 class="text-sm font-bold flex-grow">Recent Notes</h2>
      </div>

      <div class="overflow-hidden px-3 pb-3">
        <ScrollArea className="max-h-[120px]">
          <ul class="space-y-1">
            <li
              v-for="(note, index) in recentNotes.slice(0, 3)" 
              :key="note.id"
              @click="OpenNote(`note_${note.id}`)"
              class="p-2 rounded-lg bg-background/80 backdrop-blur-sm shadow-sm border border-border/20 cursor-pointer transition-all duration-200 hover:bg-background hover:shadow-md flex items-center group"
            >
              <div class="mr-1 flex-shrink-0 w-4 h-4 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-[10px] font-semibold">
                {{ index + 1 }}
              </div>
              <div class="mr-1 flex-shrink-0 text-primary">
                <FileText v-if="note.format === 'document'" class="w-3 h-3" />
                <Presentation v-else-if="note.format === 'whiteboard'" class="w-3 h-3" />
                <Presentation v-else class="w-3 h-3" />
              </div>
              <div class="truncate font-medium text-xs">{{ note.title }}</div>
            </li>
          </ul>
        </ScrollArea>
      </div>
    </div>

    <!-- Shortcuts (side by side) -->
    <div class="w-1/2 bg-primary-foreground rounded-xl shadow-md border border-border/30 overflow-hidden transition-all duration-300 hover:shadow-lg flex flex-col">
      <div class="flex items-center px-3 py-2">
        <div class="w-1 h-4 bg-primary rounded-full mr-2"></div>
        <h2 class="text-sm font-bold flex-grow">Shortcuts</h2>
        <Button variant="ghost" size="sm" class="rounded-full hover:bg-primary/10 h-6 w-6 p-0" @click="openShortcutsDialog()">
          <Pencil class="h-3 w-3" />
        </Button>
      </div>

      <div class="overflow-hidden">
        <div v-if="!userStore.shortcuts || userStore.shortcuts.length === 0" class="flex flex-col items-center justify-center p-2 h-full">
          <div class="text-center text-muted-foreground text-[10px]">
            No shortcuts set up yet
          </div>
        </div>

        <ScrollArea class="max-h-[120px] w-full p-2">
          <div class="grid grid-cols-1 gap-1">
            <Button
              variant="outline"
              :disabled="!shortcut.action || !shortcut.params"
              class="flex items-center justify-start p-1 h-auto border-border/30 hover:border-primary/50 text-[10px]"
              v-for="shortcut in userStore.shortcuts.slice(0, 3)"
              :key="shortcut.id"
              @click="userStore.runShortcut(shortcut)"
            >
              <div class="mr-1 flex-shrink-0 text-primary">
                <FileText v-if="shortcut.action === 'Note'" class="w-2 h-2" />
                <Tag v-if="shortcut.action === 'Tag'" class="w-2 h-2" />
                <Plus v-if="shortcut.action === 'Create'" class="w-2 h-2" />
              </div>
              <span class="truncate">{{ shortcut.label }}</span>
            </Button>
          </div>
        </ScrollArea>
      </div>
    </div>
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
