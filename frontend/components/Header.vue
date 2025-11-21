<template>
  <header class="navigation-wrapper fixed top-0 left-0 right-0 z-50">
    <div class="w-full justify-center items-center flex">
      <nav class="navigation">
        <div class="navigation-left">
          <div class="logo">
            <NuxtLink class="flex items-center gap-2" to="/">
              <Logo />
              <span class="logo-text">Ainfographic</span>
            </NuxtLink>
          </div>
          <div class="navigation-left-links hidden md:flex">
            <NuxtLink
              class="nav-link"
              to="/#pricing"
              >Pricing</NuxtLink>
            <NuxtLink
              class="nav-link"
              to="/#faq"
              >FAQs</NuxtLink>
            <NuxtLink
              class="nav-link"
              to="/blog"
              >Blog</NuxtLink>
          </div>
        </div>
        <!-- Show user stats when authenticated -->
        <div v-if="isAuthenticated" class="hidden md:flex items-center mr-4">
          <div class="user-stats flex items-center">
            <div class="stat-item">
              {{  }}
              <span class="stat-icon">🔋</span>
              <span class="stat-value">{{ authStore.subscriptionInfo?.credits_remaining || 0}}</span>
              <span class="stat-label">Credits</span>
            </div>
            <div class="stat-item">
              <span class="stat-icon">⬇️</span>
              <span class="stat-value">{{ authStore.subscriptionInfo?.downloads_remaining  || 0}}</span>
              <span class="stat-label">Downloads</span>
            </div>
          </div>
        </div>
        <div v-if="!isAuthenticated" class="hidden md:flex justify-center items-center gap-4">
          <NuxtLink
            class="nav-button secondary"
            to="/login"
            >Sign in</NuxtLink>
          <NuxtLink
            class="nav-button bg-primary text-white"
            to="/signup"
            >Create Infographic</NuxtLink>
        </div>
        <div v-else class="hidden md:flex justify-center items-center gap-4">
          <button
            class="nav-button secondary"
            @click="logout"
            >Sign out</button>
          <NuxtLink
            class="nav-button bg-primary text-white"
            to="/dashboard"
            >Dashboard</NuxtLink>
        </div>
        
        <!-- Mobile Menu Button -->
        <button @click="mobileMenuOpen = !mobileMenuOpen" class="md:hidden flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </nav>
    </div>
    
    <!-- Mobile Menu -->
    <div v-if="mobileMenuOpen" class="mobile-menu md:hidden px-4 py-2 border-t">
      <NuxtLink class="mobile-nav-link" to="/#pricing">Pricing</NuxtLink>
      <NuxtLink class="mobile-nav-link" to="/#faq">FAQs</NuxtLink>
      <!-- User Stats for Mobile -->
      <div v-if="isAuthenticated" class="user-stats-mobile">
        <div class="stat-item-mobile">
          <span class="stat-icon">🔋</span>
          <span class="stat-value">{{ user?.ai_credits || 0 }}</span>
          <span class="stat-label">Credits</span>
        </div>
        <div class="stat-item-mobile">
          <span class="stat-icon">⬇️</span>
          <span class="stat-value">{{ user?.downloads_remaining || 0 }}</span>
          <span class="stat-label">Downloads</span>
        </div>
      </div>
      <!-- Auth Links -->
      <template v-if="!isAuthenticated">
        <NuxtLink class="mobile-nav-link" to="/login">Sign in</NuxtLink>
        <NuxtLink class="mobile-nav-link font-medium text-primary" to="/signup">Create Infographic</NuxtLink>
      </template>
      <template v-else>
        <NuxtLink class="mobile-nav-link" to="/dashboard">Dashboard</NuxtLink>
        <button @click="logout" class="mobile-nav-link w-full text-left">Sign out</button>
      </template>
    </div>
  </header>
</template>

<script setup>
import { useAuthStore } from '~/stores/auth';

const mobileMenuOpen = ref(false);
const authStore = useAuthStore();

const isAuthenticated = computed(() => {
  return authStore.isAuthenticated();
});

const user = computed(() => {
  return authStore.getUser();
});

const logout = async () => {
  await authStore.logout();
};

// Fetch user data when component is mounted if token exists
onMounted(() => {
  if (authStore.token && !authStore.user) {
    authStore.fetchUser();
  }
});
</script>

<style scoped>
.navigation-wrapper {
  width: 100%;
  transition: box-shadow 0.3s ease;
  background-color: #f9fafb;
}

.navigation {
  max-width: 1024px;
  width: 100%;
  height: 70px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 16px;
  margin: 0 auto;
}

.navigation-left {
  display: flex;
  justify-content: start;
  align-items: center;
  gap: 32px;
}

.navigation-left-links {
  display: flex;
  justify-content: center;
  gap: 24px;
  font-size: 16px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
}

.nav-link {
  color: #4b5563;
  font-weight: 400;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.nav-link:hover {
  background-color: #f3f4f6;
}

.nav-button {
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 500;
  font-size: 16px;
  transition: all 0.2s ease;
  text-align: center;
}

.nav-button.primary {
  background-color: #0D6EFD;
  color: white;
  border: 1px solid #0D6EFD;
}

.nav-button.primary:hover {
  background-color: #0b5ed7;
}

.nav-button.secondary {
  background-color: white;
  color: #111827;
  border: 1px solid #e5e7eb;
}

.nav-button.secondary:hover {
  background-color: #f9fafb;
}

/* Mobile Menu Styles */
.mobile-menu {
  display: flex;
  flex-direction: column;
  width: 100%;
  background-color: white;
}

.mobile-nav-link {
  padding: 12px 16px;
  font-size: 16px;
  color: #4b5563;
  border-bottom: 1px solid #f3f4f6;
  transition: background-color 0.2s ease;
}

.mobile-nav-link:hover {
  background-color: #f9fafb;
}

/* User Stats Styles */
.user-stats {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  background-color: #f3f4f6;
  padding: 6px 12px;
  border-radius: 6px;
  font-size: 14px;
}

.stat-value {
  font-weight: 600;
  color: #111827;
}

.stat-label {
  color: #6b7280;
  margin-left: 2px;
}

.stat-icon {
  font-size: 16px;
}

/* Mobile Stats */
.user-stats-mobile {
  display: flex;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid #f3f4f6;
  background-color: #f9fafb;
}

.stat-item-mobile {
  display: flex;
  align-items: center;
  gap: 4px;
}
</style>
