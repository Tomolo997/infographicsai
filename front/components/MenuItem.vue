<template>
  <NuxtLink
    :to="item.route"
    :class="[
      'flex items-center transition-all duration-200 mx-2 rounded-lg relative group',
      isCollapsed ? 'justify-center px-12 py-3' : 'px-2.5 py-2.5 space-x-3',
      isActive
        ? 'bg-sidebar-orange-bg text-sidebar-orange'
        : 'text-sidebar-text-secondary hover:text-sidebar-text-primary hover:bg-sidebar-border',
    ]"
  >
    <!-- Icon -->
    <div
      class="flex-shrink-0 w-5 h-5 flex items-center justify-center"
      :class="[isActive ? 'text-sidebar-orange' : 'text-current']"
    >
      <SidebarIcon :name="item.icon" />
    </div>

    <!-- Label (hidden when collapsed) -->
    <span
      v-if="!isCollapsed"
      :class="[
        'font-medium text-sm transition-colors',
        isActive ? 'text-sidebar-orange' : '',
      ]"
    >
      {{ item.label }}
    </span>

    <!-- Tooltip for collapsed state -->
    <div
      v-if="isCollapsed"
      class="absolute left-full ml-2 px-3 py-2 bg-sidebar-border text-sidebar-text-primary text-sm rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap z-50 pointer-events-none"
    >
      {{ item.label }}
    </div>

    <!-- Active indicator -->
  </NuxtLink>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    required: true,
  },
  isCollapsed: {
    type: Boolean,
    default: false,
  },
  isActive: {
    type: Boolean,
    default: false,
  },
});
</script>

