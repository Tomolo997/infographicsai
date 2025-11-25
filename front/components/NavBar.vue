<template>
  <nav
    :class="[
      ' transition-all duration-500 ease-out w-full pt-2 bg-sidebar-orange-bg flex w-ma justify-center items-center',
      isScrolled ? 'top-2' : 'top-6',
    ]"
  >
    <div
      class="max-w-[1152px] w-full gap-12 flex mx-auto p-4 rounded-full nav-glass border border-sidebar-border shadow-lg"
    >
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-2">
          <div
            class="w-8 h-8 bg-primary-500 rounded-md flex items-center justify-center"
          >
            <Logo />
          </div>
          <span class="text-text-primary font-bold text-lg mt-1"
            >Ainfographics</span
          >
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <NuxtLink
          to="/#pricing"
          class="text-text-primary mt-1 hover:bg-sidebar-border transition-all duration-300 px-4 py-2 rounded-full"
          >Pricing</NuxtLink
        >
        <!-- <NuxtLink to="/blog" class="text-text-primary font-bold text-sm"
          >Blog</NuxtLink
        > -->
        <NuxtLink
          to="/#features"
          class="text-text-primary mt-1 hover:bg-sidebar-border transition-all duration-300 px-4 py-2 rounded-full"
          >Features</NuxtLink
        >
        <NuxtLink
          to="/#contact"
          class="text-text-primary mt-1 hover:bg-sidebar-border transition-all duration-300 px-4 py-2 rounded-full"
          >Contact</NuxtLink
        >
      </div>
      <div
        class="flex items-center space-x-4 ml-auto"
        v-if="authStore.isAuthenticated"
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
      <div class="flex items-center space-x-4 ml-auto" v-else>
        <button
          class="btn-primary font-semibold text-sm p-4 py-3 rounded-full"
          @click="navigateTo('/dashboard')"
        >
          Dashboard
        </button>
      </div>
    </div>
  </nav>
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