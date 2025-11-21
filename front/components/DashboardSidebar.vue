<template>
  <aside
    :class="[
      'fixed left-0 top-0 h-screen bg-sidebar-bg border-r border-sidebar-border transition-all duration-300 z-50 flex flex-col',
      isCollapsed ? 'w-16' : 'w-64',
    ]"
  >
    <!-- Header with Logo and Toggle -->
    <div class="flex items-center justify-between p-4 border-sidebar-border">
      <div v-if="!isCollapsed" class="flex items-center space-x-2">
        <div
          class="w-8 h-8 bg-sidebar-orange rounded-full flex items-center justify-center"
        >
          <span class="text-sidebar-text-primary font-bold text-sm">EV</span>
        </div>
        <span class="text-sidebar-text-primary font-semibold text-lg"
          >ainfographic</span
        >
      </div>
      <div v-else class="w-full flex items-center justify-center">
        <div
          class="w-8 h-8 bg-sidebar-orange rounded-full flex items-center justify-center"
        >
          <span class="text-sidebar-text-primary font-bold text-sm">V</span>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 overflow-y-auto px-2 pt-4">
      <!-- <button
        @click="toggleSidebar"
        class="w-full flex items-center justify-center"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="w-6 h-6 text-sidebar-text-secondary"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button> -->
      <!-- MAIN Section -->
      <div class="mb-6">
        <div v-if="!isCollapsed" class="px-2 mb-2">
          <span
            class="text-sidebar-text-secondary text-xs font-semibold uppercase tracking-wider"
            >Main</span
          >
        </div>
        <MenuItem
          v-for="item in mainItems"
          :key="item.id"
          :item="item"
          :isCollapsed="isCollapsed"
          :isActive="activeItem === item.id"
        />
      </div>

      <!-- INFOPRAPHS Section -->
      <div class="mb-6">
        <div v-if="!isCollapsed" class="px-2 mb-2">
          <span
            class="text-sidebar-text-secondary text-xs font-semibold uppercase tracking-wider"
            >Infographs</span
          >
        </div>
        <MenuItem
          v-for="item in infographs"
          :key="item.id"
          :item="item"
          :isCollapsed="isCollapsed"
          :isActive="activeItem === item.id"
        />
      </div>

      <!-- ACCOUNT Section -->
      <div class="mb-6">
        <div v-if="!isCollapsed" class="px-2 mb-2">
          <span
            class="text-sidebar-text-secondary text-xs font-semibold uppercase tracking-wider"
            >Account</span
          >
        </div>
        <MenuItem
          v-for="item in accountItems"
          :key="item.id"
          :item="item"
          :isCollapsed="isCollapsed"
          :isActive="activeItem === item.id"
        />
      </div>
    </nav>

    <!-- User Profile Section -->

    <ClientOnly>
      <div ref="dropdownRef" class="p-4 relative">
        <button
          @click="toggleDropdown"
          :class="[
            'w-full flex items-center justify-between transition-all duration-200 rounded-lg hover:bg-sidebar-border p-2',
            isCollapsed ? 'justify-center' : '',
          ]"
        >
          <div class="flex items-center space-x-3">
            <!-- User Avatar -->
            <div
              class="w-10 h-10 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center flex-shrink-0"
            >
              <span class="text-white font-semibold text-sm">{{
                userInitials
              }}</span>
            </div>

            <!-- User Info (hidden when collapsed) -->
            <div
              v-if="!isCollapsed"
              class="flex flex-col items-start text-left"
            >
              <span class="text-sidebar-text-primary font-semibold text-sm">{{
                userName
              }}</span>
              <span class="text-sidebar-text-secondary text-xs">{{
                userEmail
              }}</span>
            </div>
          </div>

          <!-- Dropdown Arrow (hidden when collapsed) -->
        </button>
        <!-- Dropdown Menu -->
        <transition
          enter-active-class="transition ease-out duration-100"
          enter-from-class="transform opacity-0 scale-95"
          enter-to-class="transform opacity-100 scale-100"
          leave-active-class="transition ease-in duration-75"
          leave-from-class="transform opacity-100 scale-100"
          leave-to-class="transform opacity-0 scale-95"
        >
          <div
            v-if="isDropdownOpen && !isCollapsed"
            class="absolute bottom-full left-4 right-4 bg-sidebar-bg border border-sidebar-border rounded-lg shadow-lg overflow-hidden"
          >
            <!-- Dark Mode Toggle -->
            <button
              @click="buyCredits"
              class="w-full flex items-center space-x-3 px-4 py-3 hover:bg-sidebar-border transition-colors text-left"
            >
              <SidebarIcon name="credits" />
              <span class="text-sidebar-text-primary font-medium text-sm"
                >Buy Credits</span
              >
            </button>

            <button
              @click="settings"
              class="w-full flex items-center space-x-3 px-4 py-3 hover:bg-sidebar-border transition-colors text-left"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                class="text-sidebar-text-secondary"
                height="20"
                viewBox="0 0 24 24"
                fill="currentColor"
              >
                <!-- Icon from Material Symbols by Google - https://github.com/google/material-design-icons/blob/master/LICENSE -->
                <path
                  fill="currentColor"
                  d="m9.25 22l-.4-3.2q-.325-.125-.612-.3t-.563-.375L4.7 19.375l-2.75-4.75l2.575-1.95Q4.5 12.5 4.5 12.338v-.675q0-.163.025-.338L1.95 9.375l2.75-4.75l2.975 1.25q.275-.2.575-.375t.6-.3l.4-3.2h5.5l.4 3.2q.325.125.613.3t.562.375l2.975-1.25l2.75 4.75l-2.575 1.95q.025.175.025.338v.674q0 .163-.05.338l2.575 1.95l-2.75 4.75l-2.95-1.25q-.275.2-.575.375t-.6.3l-.4 3.2zM11 20h1.975l.35-2.65q.775-.2 1.438-.587t1.212-.938l2.475 1.025l.975-1.7l-2.15-1.625q.125-.35.175-.737T17.5 12t-.05-.787t-.175-.738l2.15-1.625l-.975-1.7l-2.475 1.05q-.55-.575-1.212-.962t-1.438-.588L13 4h-1.975l-.35 2.65q-.775.2-1.437.588t-1.213.937L5.55 7.15l-.975 1.7l2.15 1.6q-.125.375-.175.75t-.05.8q0 .4.05.775t.175.75l-2.15 1.625l.975 1.7l2.475-1.05q.55.575 1.213.963t1.437.587zm1.05-4.5q1.45 0 2.475-1.025T15.55 12t-1.025-2.475T12.05 8.5q-1.475 0-2.488 1.025T8.55 12t1.013 2.475T12.05 15.5M12 12"
                />
              </svg>
              <span class="text-sidebar-text-primary font-medium text-sm"
                >Settings</span
              >
            </button>

            <!-- Divider -->
            <div class="border-t border-sidebar-border"></div>

            <!-- Log out -->
            <button
              @click="handleLogout"
              class="w-full flex items-center space-x-3 px-4 py-3 hover:bg-sidebar-border transition-colors text-left"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="w-5 h-5 text-sidebar-text-secondary"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
                />
              </svg>
              <span class="text-sidebar-text-primary font-medium text-sm"
                >Log out</span
              >
            </button>
          </div>
        </transition>
      </div>
    </ClientOnly>
  </aside>
</template>

<script>
import { computed, ref, onMounted, onUnmounted } from "vue";
import { useRoute } from "vue-router";
import { useAuthStore } from "~/stores/auth";

export default {
  setup() {
    const route = useRoute();
    const authStore = useAuthStore();
    const { isCollapsed, toggleSidebar } = useSidebar();
    const isDropdownOpen = ref(false);
    const dropdownRef = ref(null);

    const activeItem = computed(() => {
      const path = route.path;
      if (path === "/dashboard") return "dashboard";
      if (path === "/dashboard/transitions") return "my-transitions";
      if (path === "/ai-agent") return "ai-agent";
      if (path === "/subscriptions") return "my-subscriptions";
      if (path === "/analytics") return "analytics";
      if (path === "/categories") return "categories";
      if (path === "/family") return "family";
      if (path === "/notifications") return "notifications";
      if (path === "/billing") return "billing";
      if (path === "/settings") return "settings";
      if (path === "/feedback") return "feedback";
      if (path === "/discord") return "discord";
      return "dashboard";
    });

    const mainItems = [
      {
        id: "dashboard",
        label: "Dashboard",
        icon: "dashboard",
        route: "/dashboard",
      },
      {
        id: "settings",
        label: "Settings",
        icon: "settings",
        route: "/dashboard/settings",
      },
    ];

    const infographs = [
      {
        id: "templates",
        label: "Templates",
        icon: "templates",
        route: "/dashboard/templates",
      },
      {
        id: "saved-infographs",
        label: "Saved",
        icon: "saved",
        route: "/dashboard/saved",
      },
    ];

    const accountItems = [
      {
        id: "credits",
        label: "Credits",
        icon: "credits",
        route: "/dashboard/credits",
      },
      {
        id: "feedback",
        label: "Feedback",
        icon: "feedback",
        route: "/dashboard/feedback",
      },
    ];

    const userName = computed(() => {
      if (authStore.user?.first_name && authStore.user?.last_name) {
        return `${authStore.user.first_name} ${authStore.user.last_name}`;
      }
      return authStore.user?.email?.split("@")[0] || "John Doe";
    });

    const userEmail = computed(() => {
      return authStore.user?.email || "JohnDoe@g...";
    });

    const userInitials = computed(() => {
      if (authStore.user?.first_name && authStore.user?.last_name) {
        return (
          authStore.user.first_name[0] + authStore.user.last_name[0]
        ).toUpperCase();
      }
      const email = authStore.user?.email || "John Doe";
      return email.substring(0, 2).toUpperCase();
    });

    const toggleDropdown = () => {
      isDropdownOpen.value = !isDropdownOpen.value;
    };

    const buyCredits = () => {
      // TODO: Navigate to buy credits page
      console.log("Buy credits");
      isDropdownOpen.value = false;
    };

    const settings = () => {
      navigateTo("/dashboard/settings");
      isDropdownOpen.value = false;
    };

    const handleLogout = async () => {
      try {
        await authStore.logout();
        isDropdownOpen.value = false;
      } catch (error) {
        console.error("Logout failed:", error);
      }
    };

    // Close dropdown when clicking outside
    const handleClickOutside = (event) => {
      if (dropdownRef.value && !dropdownRef.value.contains(event.target)) {
        isDropdownOpen.value = false;
      }
    };

    onMounted(() => {
      document.addEventListener("click", handleClickOutside);
    });

    onUnmounted(() => {
      document.removeEventListener("click", handleClickOutside);
    });

    return {
      activeItem,
      mainItems,
      infographs,
      accountItems,
      isDropdownOpen,
      userName,
      userEmail,
      userInitials,
      toggleDropdown,
      buyCredits,
      settings,
      handleLogout,
      dropdownRef,
      isCollapsed,
      toggleSidebar,
    };
  },
};
</script>
