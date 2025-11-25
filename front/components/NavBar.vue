<template>
  <nav
    :class="[
      'fixed left-0 right-0 z-50 transition-all duration-500 ease-out',
      isScrolled ? 'top-2' : 'top-6',
    ]"
  ></nav>
</template>

<script setup>
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