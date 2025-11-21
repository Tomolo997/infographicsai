<template>
  <nav
    :class="[
      'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
      isScrolled ? 'nav-glass shadow-2xl' : 'bg-transparent',
    ]"
  >
    <div class="max-w-[1152px] mx-auto px-6">
      <div class="flex justify-between items-center h-14">
        <div class="flex items-center">
          <NuxtLink to="/" class="flex-shrink-0 flex items-center">
            <span class="text-2xl font-bold gradient-text">Promptwatch</span>
          </NuxtLink>
        </div>

        <div class="hidden md:flex items-center space-x-8">
          <NuxtLink to="/features" class="btn-ghost"> Features </NuxtLink>
          <NuxtLink to="/pricing" class="btn-ghost"> Pricing </NuxtLink>
          <NuxtLink to="/browse" class="btn-ghost"> Browse </NuxtLink>
          <NuxtLink to="/blog" class="btn-ghost"> Blog </NuxtLink>
          <NuxtLink to="/calculator" class="btn-ghost"> Calculator </NuxtLink>
          <NuxtLink to="/faq" class="btn-ghost"> FAQ </NuxtLink>
          <template v-if="authStore.isLoggedIn">
            <div class="relative" v-click-outside="closeDropdown">
              <button
                @click="toggleDropdown"
                class="flex items-center space-x-2 btn-ghost"
              >
                <img
                  v-if="authStore.user?.profile_picture"
                  :src="authStore.user.profile_picture"
                  :alt="authStore.user.full_name"
                  class="w-8 h-8 rounded-full"
                />
                <div
                  v-else
                  class="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center"
                >
                  <span class="text-white text-sm font-medium">
                    {{ authStore.user?.first_name?.charAt(0) || "U" }}
                  </span>
                </div>
                <ChevronDownIcon class="w-4 h-4" />
              </button>

              <div
                v-show="showDropdown"
                class="absolute right-0 mt-2 w-48 card-glass py-2 z-50"
              >
                <NuxtLink
                  to="/dashboard"
                  class="block px-4 py-2 text-sm text-text-primary hover:bg-background-secondary hover:bg-opacity-50 transition-colors"
                >
                  Dashboard
                </NuxtLink>
                <NuxtLink
                  to="/dashboard/profile"
                  class="block px-4 py-2 text-sm text-text-primary hover:bg-background-secondary hover:bg-opacity-50 transition-colors"
                >
                  Profile
                </NuxtLink>
                <NuxtLink
                  to="/dashboard/billing"
                  class="block px-4 py-2 text-sm text-text-primary hover:bg-background-secondary hover:bg-opacity-50 transition-colors"
                >
                  Billing
                </NuxtLink>
                <button
                  @click="logout"
                  class="block w-full text-left px-4 py-2 text-sm text-text-primary hover:bg-background-secondary hover:bg-opacity-50 transition-colors"
                >
                  Sign out
                </button>
              </div>
            </div>
          </template>
          <template v-else>
            <button class="btn-ghost">
              <svg
                class="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707"
                />
              </svg>
            </button>
            <NuxtLink to="/signup" class="btn-primary">Dashboard</NuxtLink>
          </template>
        </div>

        <!-- Mobile menu button -->
        <div class="md:hidden flex items-center">
          <button @click="toggleMobileMenu" class="btn-ghost">
            <Bars3Icon v-if="!showMobileMenu" class="w-6 h-6" />
            <XMarkIcon v-else class="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <div v-show="showMobileMenu" class="md:hidden">
      <div
        class="px-4 pt-4 pb-6 space-y-2 card-glass border-t border-border-primary"
      >
        <NuxtLink to="/features" class="btn-ghost block w-full text-left"
          >Features</NuxtLink
        >
        <NuxtLink to="/pricing" class="btn-ghost block w-full text-left"
          >Pricing</NuxtLink
        >
        <NuxtLink to="/browse" class="btn-ghost block w-full text-left"
          >Browse</NuxtLink
        >
        <NuxtLink to="/blog" class="btn-ghost block w-full text-left"
          >Blog</NuxtLink
        >
        <NuxtLink to="/calculator" class="btn-ghost block w-full text-left"
          >Calculator</NuxtLink
        >
        <NuxtLink to="/faq" class="btn-ghost block w-full text-left"
          >FAQ</NuxtLink
        >

        <template v-if="authStore.isLoggedIn">
          <div class="border-t border-border-primary pt-2 mt-2">
            <NuxtLink to="/dashboard" class="btn-ghost block w-full text-left"
              >Dashboard</NuxtLink
            >
            <NuxtLink
              to="/dashboard/profile"
              class="btn-ghost block w-full text-left"
              >Profile</NuxtLink
            >
            <NuxtLink
              to="/dashboard/billing"
              class="btn-ghost block w-full text-left"
              >Billing</NuxtLink
            >
            <button @click="logout" class="btn-ghost block w-full text-left">
              Sign out
            </button>
          </div>
        </template>
        <template v-else>
          <div class="border-t border-border-primary pt-2 mt-2 space-y-2">
            <NuxtLink to="/signup" class="btn-primary block w-full text-center"
              >Dashboard</NuxtLink
            >
          </div>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
const authStore = useAuthStore();
const showDropdown = ref(false);
const showMobileMenu = ref(false);
const isScrolled = ref(false);

// Scroll detection
const handleScroll = () => {
  isScrolled.value = window.scrollY > 10;
};

onMounted(() => {
  window.addEventListener("scroll", handleScroll);
});

onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll);
});

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