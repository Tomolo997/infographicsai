<template>
  <div class="w-full max-w-[500px] mx-auto px-8">
    <div class="mb-12">
      <div class="flex items-center gap-3 mb-8">
        <div
          class="w-10 h-10 bg-sidebar-orange flex items-center justify-center rounded-lg"
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
        <span class="text-2xl font-bold text-text-primary">Ainfographic</span>
      </div>
    </div>
    <h1 class="text-2xl font-bold text-text-primary">Create your account</h1>
    <div class="text-start">
      <span class="text-sm text-text-secondary">Already have an account? </span>
      <NuxtLink
        to="/login"
        class="text-text-primary text-sm hover:text-sidebar-orange transition-colors font-medium"
      >
        Sign in
      </NuxtLink>
    </div>

    <form @submit.prevent="handleSignup" class="mt-8 space-y-6">
      <div
        v-if="error"
        class="bg-red-500/10 border border-red-500/30 text-red-400 px-4 py-3 rounded-lg"
      >
        {{ error }}
      </div>

      <div>
        <label
          for="email"
          class="block text-sm font-medium mb-2 text-text-primary"
        >
          Email address
        </label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          required
          class="w-full px-4 py-3.5 bg-card-bg border border-card-border text-text-primary rounded-xl focus:outline-none focus:ring-2 focus:ring-sidebar-orange focus:border-transparent transition-all placeholder:text-text-secondary"
          placeholder="john@example.com"
        />
      </div>

      <div>
        <label
          for="password1"
          class="block text-sm font-medium mb-2 text-text-primary"
        >
          Password
        </label>
        <input
          id="password1"
          v-model="form.password1"
          type="password"
          required
          class="w-full px-4 py-3.5 bg-card-bg border border-card-border text-text-primary rounded-xl focus:outline-none focus:ring-2 focus:ring-sidebar-orange focus:border-transparent transition-all placeholder:text-text-secondary"
          placeholder="Enter your password"
        />
        <p class="mt-1 text-xs text-gray-500">
          Must be at least 8 characters long
        </p>
      </div>

      <div>
        <label
          for="password2"
          class="block text-sm font-medium mb-2 text-text-primary"
        >
          Confirm password
        </label>
        <input
          id="password2"
          v-model="form.password2"
          type="password"
          required
          class="w-full px-4 py-3.5 bg-card-bg border border-card-border text-text-primary rounded-xl focus:outline-none focus:ring-2 focus:ring-sidebar-orange focus:border-transparent transition-all placeholder:text-text-secondary"
          placeholder="Confirm your password"
        />
      </div>

      <div>
        <button
          type="submit"
          :disabled="loading"
          class="w-full py-3.5 bg-sidebar-orange hover:bg-sidebar-orange/90 text-background-primary font-semibold rounded-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="loading">Creating account...</span>
          <span v-else>Create account</span>
        </button>
      </div>

      <div class="mt-6">
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-card-border" />
          </div>
          <div class="relative flex justify-center">
            <span class="px-4 bg-background-primary text-text-secondary text-sm"
              >Or continue with</span
            >
          </div>
        </div>

        <div class="mt-6">
          <button
            type="button"
            @click="signupWithGoogle"
            class="w-full flex justify-center items-center gap-3 px-4 py-3.5 bg-card-bg border border-card-border rounded-xl text-text-primary font-medium hover:bg-card-bg/80 hover:border-sidebar-orange/30 transition-all"
          >
            <svg class="w-5 h-5 mr-2" viewBox="0 0 24 24">
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
        </div>
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
      </div>
    </form>
  </div>
</template>

<script setup>
definePageMeta({
  layout: "auth",
  middleware: "guest",
});

useSeoMeta({
  title: "Sign Up - Ainfographic",
  description: "Create your Ainfographic account and get started",
});

const authStore = useAuthStore();
const loading = ref(false);
const error = ref("");

const form = reactive({
  email: "",
  password1: "",
  password2: "",
});

const handleSignup = async () => {
  if (loading.value) return;

  if (form.password1 !== form.password2) {
    error.value = "Passwords do not match";
    return;
  }

  if (form.password1.length < 8) {
    error.value = "Password must be at least 8 characters long";
    return;
  }

  loading.value = true;
  error.value = "";

  try {
    const response = await authStore.register({
      email: form.email,
      password1: form.password1,
      password2: form.password2,
    });

    console.log("response", response.message);

    if (response.success) {
      await navigateTo({
        path: "/verify-email-sent",
        query: { email: form.email },
      });
    }
  } catch (err) {
    console.error("Signup error:", err);

    if (err.response?.data?.email) {
      error.value = err.response.data.email[0];
    } else if (err.response?.data?.password1) {
      error.value = err.response.data.password1[0];
    } else if (err.response?.data?.password) {
      error.value = err.response.data.password[0];
    } else if (err.response?.data?.non_field_errors) {
      error.value = err.response.data.non_field_errors[0];
    } else {
      error.value = "Failed to create account. Please try again.";
    }
  } finally {
    loading.value = false;
  }
};

const signupWithGoogle = () => {
  const apiBase =
    process.env.NODE_ENV === "production"
      ? "https://ainfographic.com/api"
      : "http://localhost:8000/api";

  window.location.href = `${apiBase}/account/google/login/`;
};
</script>