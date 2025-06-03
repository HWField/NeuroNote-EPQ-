<script setup lang="ts">
import type { SidebarProps } from ".";
import { Sheet, SheetContent } from "@/components/ui/sheet";
import { cn } from "@/lib/utils";
import { SIDEBAR_WIDTH_MOBILE, useSidebar } from "./utils";
import { useUserStore } from "@/stores/useUserStore";
import { watch } from "vue";

defineOptions({
  inheritAttrs: false,
});

const props = withDefaults(defineProps<SidebarProps>(), {
  side: "left",
  variant: "sidebar",
  collapsible: "offcanvas",
});
const userStore = useUserStore();
// states can be "" for no control, "expanded for force expanded, "collapsed" for force collapsed
const { isMobile, state, openMobile, setOpenMobile } = useSidebar();

watch(
  () => userStore.tourState,
  (newTourState) => {
    // Only affect mobile state, not desktop
    if (isMobile.value) {
      if (newTourState === "expanded") {
        // Force open mobile sidebar
        setOpenMobile(true);
      } else if (newTourState === "collapsed") {
        // Force close mobile sidebar
        setOpenMobile(false);
      }
      // If newTourState === "", do nothing (no control)
    }
  },
  { immediate: true } // Run on mount as well
);
watch(isMobile, (newIsMobile) => {
  if (newIsMobile && userStore.tourState) {
    if (userStore.tourState === "expanded") {
      setOpenMobile(true);
    } else if (userStore.tourState === "collapsed") {
      setOpenMobile(false);
    }
  }
});
</script>

<template>
  <div
    v-if="collapsible === 'none'"
    :class="
      cn(
        'flex h-full w-[--sidebar-width] flex-col bg-sidebar text-sidebar-foreground',
        props.class
      )
    "
    v-bind="$attrs"
  >
    <slot />
  </div>

  <Sheet
    v-else-if="isMobile"
    :open="openMobile"
    v-bind="$attrs"
    @update:open="setOpenMobile"
    :modal="userStore.tourState === 'expanded' ? false : true"
   
  >
    <SheetContent
    
      data-sidebar="sidebar"
      data-mobile="true"
      :side="side"
      class="w-[--sidebar-width] bg-popover p-0 text-sidebar-foreground [&>button]:hidden"
      :style="{
      '--sidebar-width': SIDEBAR_WIDTH_MOBILE,
      }"
      @interact-outside="(e) => userStore.tourState === 'expanded' ? e.preventDefault() : null"
    >
      <div class="flex h-full w-full flex-col">
        <slot />
      </div>
    </SheetContent>
  </Sheet>

  <div
    v-else
    class="group peer hidden md:block"
    :data-state="state"a
    :data-collapsible="state === 'collapsed' ? collapsible : ''"
    :data-variant="variant"
    :data-side="side"
  >
    <!-- This is what handles the sidebar gap on desktop  -->
    <div
      :class="
        cn(
          'duration-200 relative h-svh w-[--sidebar-width] bg-transparent transition-[width] ease-linear',
          'group-data-[collapsible=offcanvas]:w-0',
          'group-data-[side=right]:rotate-180',
          variant === 'floating' || variant === 'inset'
            ? 'group-data-[collapsible=icon]:w-[calc(var(--sidebar-width-icon)_+_theme(spacing.4))]'
            : 'group-data-[collapsible=icon]:w-[--sidebar-width-icon]'
        )
      "
    />
    <div
      :class="
        cn(
          'duration-200 fixed inset-y-0 z-10 hidden h-svh w-[--sidebar-width] transition-[left,right,width] ease-linear md:flex',
          side === 'left'
            ? 'left-0 group-data-[collapsible=offcanvas]:left-[calc(var(--sidebar-width)*-1)]'
            : 'right-0 group-data-[collapsible=offcanvas]:right-[calc(var(--sidebar-width)*-1)]',
          // Adjust the padding for floating and inset variants.
          variant === 'floating' || variant === 'inset'
            ? 'p-2 group-data-[collapsible=icon]:w-[calc(var(--sidebar-width-icon)_+_theme(spacing.4)_+2px)]'
            : 'group-data-[collapsible=icon]:w-[--sidebar-width-icon] group-data-[side=left]:border-r group-data-[side=right]:border-l',
          props.class
        )
      "
      v-bind="$attrs"
    >
      <div
        data-sidebar="sidebar"
        class="flex h-full w-full flex-col bg-sidebar group-data-[variant=floating]:rounded-lg group-data-[variant=floating]:border group-data-[variant=floating]:border-sidebar-border group-data-[variant=floating]:shadow"
      >
     
        <slot />
       
      </div>
    </div>
  </div>
</template>
