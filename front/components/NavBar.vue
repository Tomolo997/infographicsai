<template>
  <div class="relative w-full">
    <nav
      :class="[
        'transition-all duration-500 ease-out w-full pt-4 bg-sidebar-orange-bg flex w-ma justify-center items-center',
        isScrolled ? 'top-2' : 'top-6',
      ]"
    >
      <div
        class="max-w-[1152px] w-full gap-12 flex mx-auto p-4 rounded-full nav-glass border border-sidebar-border shadow-lg"
      >
        <!-- Logo -->
        <div class="flex items-center justify-between">
          <NuxtLink to="/" class="flex items-center space-x-2">
            <div
              class="w-8 h-8 bg-primary-500 rounded-md flex items-center justify-center"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="24"
                height="24"
                viewBox="0 0 24 24"
              >
                <!-- Icon from Lucide by Lucide Contributors - https://github.com/lucide-icons/lucide/blob/main/LICENSE -->
                <g
                  fill="none"
                  stroke="white"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                >
                  <rect width="7" height="9" x="3" y="3" rx="1" />
                  <rect width="7" height="5" x="14" y="3" rx="1" />
                  <rect width="7" height="9" x="14" y="12" rx="1" />
                  <rect width="7" height="5" x="3" y="16" rx="1" />
                </g>
              </svg>
            </div>
            <span class="text-text-primary font-bold text-lg mt-1"
              >Ainfographics</span
            >
          </NuxtLink>
        </div>

        <!-- Desktop Navigation Links -->
        <div class="hidden md:flex items-center space-x-2">
          <NuxtLink
            to="/#pricing"
            class="text-text-primary mt-1 hover:bg-sidebar-border transition-all duration-300 px-4 py-2 rounded-full"
            >Pricing</NuxtLink
          >
          <NuxtLink
            to="/#features"
            class="text-text-primary mt-1 hover:bg-sidebar-border transition-all duration-300 px-4 py-2 rounded-full"
            >Features</NuxtLink
          >
          <NuxtLink
            to="/#gallery"
            class="text-text-primary mt-1 hover:bg-sidebar-border transition-all duration-300 px-4 py-2 rounded-full"
            >Templates</NuxtLink
          >
        </div>

        <!-- Desktop Auth Buttons -->
        <div
          class="hidden md:flex items-center space-x-4 ml-auto"
          v-if="!authStore.isAuthenticated"
        >
          <button
            class="btn-primary text-sm p-3 py-2 rounded-full"
            @click="navigateTo('/login')"
          >
            Sign in
          </button>
          <button
            class="btn-outline text-sm p-3 py-2 rounded-full"
            @click="navigateTo('/signup')"
          >
            Register
          </button>
        </div>
        <div class="hidden md:flex items-center space-x-4 ml-auto" v-else>
          <button
            class="btn-primary font-semibold text-sm p-4 py-3 rounded-full"
            @click="navigateTo('/dashboard')"
          >
            Dashboard
          </button>
        </div>

        <!-- Mobile Hamburger Menu -->
        <div class="flex md:hidden items-center ml-auto">
          <button
            @click="toggleMobileMenu"
            class="text-text-primary p-2 rounded-md hover:bg-sidebar-border transition-colors"
            aria-label="Toggle menu"
          >
            <svg
              v-if="!showMobileMenu"
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
            <svg
              v-else
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>
    </nav>

    <!-- Mobile Menu Dropdown -->
    <Transition name="mobile-menu">
      <div
        v-if="showMobileMenu"
        class="md:hidden absolute top-full left-0 right-0 mt-2 mx-4 bg-card-bg rounded-2xl border border-sidebar-border shadow-xl overflow-hidden z-50"
      >
        <div class="py-4">
          <!-- Mobile Navigation Links -->
          <NuxtLink
            to="/#pricing"
            @click="showMobileMenu = false"
            class="block px-6 py-3 text-text-primary hover:bg-sidebar-border transition-colors"
          >
            Pricing
          </NuxtLink>
          <NuxtLink
            to="/#features"
            @click="showMobileMenu = false"
            class="block px-6 py-3 text-text-primary hover:bg-sidebar-border transition-colors"
          >
            Features
          </NuxtLink>
          <NuxtLink
            to="/#gallery"
            @click="showMobileMenu = false"
            class="block px-6 py-3 text-text-primary hover:bg-sidebar-border transition-colors"
          >
            Templates
          </NuxtLink>

          <!-- Mobile Auth Buttons -->
          <div
            class="px-6 pt-4 pb-2 space-y-2 border-t border-sidebar-border mt-2"
          >
            <template v-if="!authStore.isAuthenticated">
              <button
                class="btn-primary text-sm w-full py-3 rounded-full"
                @click="
                  navigateTo('/login');
                  showMobileMenu = false;
                "
              >
                Sign in
              </button>
              <button
                class="btn-outline text-sm w-full py-3 rounded-full"
                @click="
                  navigateTo('/signup');
                  showMobileMenu = false;
                "
              >
                Register
              </button>
            </template>
            <template v-else>
              <button
                class="btn-primary font-semibold text-sm w-full py-3 rounded-full"
                @click="
                  navigateTo('/dashboard');
                  showMobileMenu = false;
                "
              >
                Dashboard
              </button>
            </template>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { useAuthStore } from "~/stores/auth";

const authStore = useAuthStore();
const showDropdown = ref(false);
const showMobileMenu = ref(false);
const isScrolled = ref(false);
const isDark = ref(false);

// Scroll detection
const handleScroll = () => {
  isScrolled.value = window.scrollY > 50;
};

onMounted(() => {
  window.addEventListener("scroll", handleScroll);

  // Check for dark mode preference
  if (
    localStorage.theme === "dark" ||
    (!("theme" in localStorage) &&
      window.matchMedia("(prefers-color-scheme: dark)").matches)
  ) {
    isDark.value = true;
    document.documentElement.classList.add("dark");
  } else {
    isDark.value = false;
    document.documentElement.classList.remove("dark");
  }
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});

const toggleTheme = () => {
  isDark.value = !isDark.value;
  if (isDark.value) {
    document.documentElement.classList.add("dark");
    localStorage.theme = "dark";
  } else {
    document.documentElement.classList.remove("dark");
    localStorage.theme = "light";
  }
};

const toggleDropdown = () => {
  showDropdown.value = !showDropdown.value;
};

const closeDropdown = () => {
  showDropdown.value = false;
};

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value;
};

const logout = async () => {
  try {
    await authStore.logout();
    showDropdown.value = false;
    showMobileMenu.value = false;
  } catch (error) {
    console.error("Logout error:", error);
  }
};

// Custom directive for click outside
const vClickOutside = {
  beforeMount(el, binding) {
    el.clickOutsideEvent = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value();
      }
    };
    document.addEventListener("click", el.clickOutsideEvent);
  },
  unmounted(el) {
    document.removeEventListener("click", el.clickOutsideEvent);
  },
};
</script>

<style scoped>
/* Mobile menu transitions */
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: all 0.3s ease;
}

.mobile-menu-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>