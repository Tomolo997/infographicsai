<template>
  <div class="flex justify-between items-center p-4 px-6">
    <div class="flex items-center text-sidebar-text-secondary space-x-6">
      <UpperNavBarMenuItem :icon="icon" />
      <div class="w-[1px] h-4 bg-sidebar-border rounded-full"></div>
      <span class="text-sidebar-text-secondary font-medium text-md">
        {{ activeItem }}
      </span>
      <div v-if="secondActiveItem">
        <div>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 24 24"
          >
            <!-- Icon from Material Symbols by Google - https://github.com/google/material-design-icons/blob/master/LICENSE -->
            <path
              fill="currentColor"
              d="M12.6 12L8.7 8.1q-.275-.275-.275-.7t.275-.7t.7-.275t.7.275l4.6 4.6q.15.15.213.325t.062.375t-.062.375t-.213.325l-4.6 4.6q-.275.275-.7.275t-.7-.275t-.275-.7t.275-.7z"
            />
          </svg>
        </div>
      </div>
      <span
        v-if="secondActiveItem"
        class="text-sidebar-text-secondary font-medium text-md"
      >
        {{ secondActiveItem }}
      </span>
    </div>
  </div>
</template>

<script
>
export default {
  name: "UpperNavBar",
  setup() {
    return {};
  },
  data() {
    return {};
  },
  computed: {
    icon() {
      const path = this.$route.path;
      if (path === "/ai-agent") return "ai-agent";
      if (path === "/subscriptions") return "subscriptions";
      if (path === "/analytics") return "analytics";
      if (path === "/categories") return "categories";
      if (path === "/family") return "family";
      if (path === "/notifications") return "notifications";
      if (path === "/billing") return "billing";
      if (path === "/settings") return "settings";
      if (path === "/feedback") return "feedback";
      if (path === "/discord") return "discord";
      return "dashboard";
    },
    activeItem() {
      const path = this.$route.path;
      if (path === "/ai-agent") return "AI Agent";
      if (path === "/subscriptions") return "My Subscriptions";
      if (path === "/analytics") return "Analytics";
      if (path === "/categories") return "Categories";
      if (path === "/family") return "Family";
      if (path === "/notifications") return "Notifications";
      if (path === "/billing") return "Billing";
      if (path === "/settings") return "Settings";
      if (path === "/feedback") return "Feedback";
      if (path === "/discord") return "Discord";
      return "Dashboard";
    },
    secondActiveItem() {
      const path = this.$route.path;
      if (path === "/dashboard/create/templates") return "Templates";
      if (path === "/dashboard/create") return "Create from Scratch";
      if (path === "/dashboard/create/own-templates")
        return "Create from Own Templates";
      if (path === "/dashboard/saved") return "Saved";
      if (path === "/dashboard/credits") return "Credits";
      return "Create";
    },
  },
};
</script>