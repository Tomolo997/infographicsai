<template>
  <div class="w-full max-w-[500px] mx-auto px-8">
    <!-- Logo and Title -->
    <div class="mb-12">
      <div class="flex items-center gap-3 mb-8">
        <div
          class="w-10 h-10 bg-sidebar-orange flex items-center justify-center rounded-lg"
        >
          <svg
            class="w-6 h-6 text-background-primary"
            viewBox="0 0 24 24"
            fill="currentColor"
          >
            <path d="M8 5v14l11-7z" />
          </svg>
        </div>
        <span class="text-2xl font-bold text-text-primary">ainfographic</span>
      </div>

      <h1 class="text-2xl font-bold text-text-primary">
        Sign in to your account
      </h1>
      <div class="text-start">
        <span class="text-sm text-text-secondary">Don' have an account? </span>
        <NuxtLink
          to="/signup"
          class="text-text-primary text-sm hover:text-sidebar-orange transition-colors font-medium"
        >
          Sign up
        </NuxtLink>
      </div>
    </div>

    <form @submit.prevent="handleLogin" class="space-y-6">
      <div
        v-if="error"
        class="bg-red-500/10 border border-red-500/30 text-red-400 px-4 py-3 rounded-lg"
      >
        {{ error }}
      </div>

      <!-- Email Field -->
      <div>
        <label
          for="email"
          class="block text-sm font-medium text-text-primary mb-2"
        >
          Email address
        </label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          required
          class="w-full px-4 py-3.5 bg-card-bg border border-card-border text-text-primary rounded-xl focus:outline-none focus:ring-2 focus:ring-sidebar-orange focus:border-transparent transition-all placeholder:text-text-secondary"
          placeholder="hello@johndoe.com"
        />
      </div>

      <!-- Password Field -->
      <div>
        <label
          for="password"
          class="block text-sm font-medium text-text-primary mb-2"
        >
          Password
        </label>
        <div class="relative">
          <input
            id="password"
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            required
            class="w-full px-4 py-3.5 bg-card-bg border border-card-border text-text-primary rounded-xl focus:outline-none focus:ring-2 focus:ring-sidebar-orange focus:border-transparent transition-all placeholder:text-text-secondary"
            placeholder="••••••••"
          />
          <button
            type="button"
            @click="showPassword = !showPassword"
            class="absolute right-4 top-1/2 -translate-y-1/2 text-text-secondary hover:text-text-primary transition-colors"
          >
            <svg
              v-if="!showPassword"
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
              />
            </svg>
            <svg
              v-else
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Forgot Password -->
      <div class="text-left">
        <NuxtLink
          to="/forgot-password"
          class="text-sm text-text-secondary hover:text-text-primary transition-colors"
        >
          Forgot password?
        </NuxtLink>
      </div>

      <!-- Sign In Button -->
      <button
        type="submit"
        :disabled="loading"
        class="w-full py-3.5 bg-sidebar-orange hover:bg-sidebar-orange/90 text-background-primary font-semibold rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <span v-if="loading">Signing in...</span>
        <span v-else>Sign in</span>
      </button>

      <!-- Divider -->
      <div class="relative my-8">
        <div class="absolute inset-0 flex items-center">
          <div class="w-full border-t border-card-border"></div>
        </div>
        <div class="relative flex justify-center">
          <span class="px-4 bg-background-primary text-text-secondary text-sm"
            >Or continue with</span
          >
        </div>
      </div>

      <!-- Google Sign In -->
      <button
        type="button"
        @click="loginWithGoogle"
        class="w-full flex justify-center items-center gap-3 px-4 py-3.5 bg-card-bg border border-card-border rounded-xl text-text-primary font-medium hover:bg-card-bg/80 hover:border-sidebar-orange/30 transition-all"
      >
        <svg class="w-5 h-5" viewBox="0 0 24 24">
          <path
            fill="#4285f4"
            d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
          />
          <path
            fill="#34a853"
            d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
          />
          <path
            fill="#fbbc05"
            d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
          />
          <path
            fill="#ea4335"
            d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
          />
        </svg>
        Google
      </button>

      <!-- Terms and Privacy -->
      <p class="text-center text-sm text-text-secondary mt-8">
        By clicking on sign in, you agree to our
        <NuxtLink
          to="/terms"
          class="text-text-primary hover:text-sidebar-orange transition-colors"
        >
          Terms of Service
        </NuxtLink>
        and
        <NuxtLink
          to="/privacy"
          class="text-text-primary hover:text-sidebar-orange transition-colors"
        >
          Privacy Policy
        </NuxtLink>
      </p>
    </form>
  </div>
</template>

<script setup>
definePageMeta({
  layout: "auth",
  middleware: "guest",
});

useSeoMeta({
  title: "Sign In - SaaS MVP",
  description: "Sign in to your SaaS MVP account",
});

const authStore = useAuthStore();
const loading = ref(false);
const error = ref("");
const showPassword = ref(false);

const form = reactive({
  email: "",
  password: "",
  remember: false,
});

const handleLogin = async () => {
  if (loading.value) return;

  loading.value = true;
  error.value = "";

  try {
    await authStore.login({
      email: form.email,
      password: form.password,
    });
  } catch (err) {
    error.value =
      err.data?.message ||
      err.data?.non_field_errors?.[0] ||
      "Invalid email or password";
  } finally {
    loading.value = false;
  }
};

const loginWithGoogle = () => {
  // In development, use the proxy which forwards to backend
  // In production, this should point to your actual API URL
  const baseUrl =
    process.client && window.location.hostname === "localhost"
      ? "http://localhost:3000" // Use Nuxt dev server (with proxy)
      : window.location.origin; // Use current origin in production

  // Redirect to backend Google OAuth endpoint
  // The proxy will forward /api requests to Django backend
  window.location.href = `${baseUrl}/api/account/google/login/`;
};
</script>