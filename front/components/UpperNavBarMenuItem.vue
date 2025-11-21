<template>
  <!-- Icon -->
  <div class="flex-shrink-0 w-5 h-5 flex items-center justify-center">
    <SidebarIcon :name="icon" class="text-sidebar-text-secondary" />
  </div>
</template>

<script setup>
defineProps({
  icon: {
    type: String,
    required: true,
  },
});
</script>

