<template>
  <div class="flex min-h-screen bg-background-primary">
    <DashboardSidebar />
    <main
      class="flex-1 transition-all duration-300"
      :class="isCollapsed ? 'ml-16' : 'ml-64'"
    >
      <div class="">
        <UpperNavBar />
        <slot />
      </div>
    </main>
  </div>
</template>

<script>
import { useSidebar } from "~/composables/useSidebar";
import DashboardSidebar from "~/components/DashboardSidebar.vue";
import UpperNavBar from "~/components/UpperNavBar.vue";
export default {
  name: "DashboardLayout",
  components: {
    DashboardSidebar,
    UpperNavBar,
  },
  setup() {
    const { isCollapsed } = useSidebar();
    return {
      isCollapsed,
    };
  },
};
</script>
