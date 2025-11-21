<template>
  <div class="w-full max-w-[500px] mx-auto px-8">
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
        <span class="text-2xl font-bold text-text-primary">EvoClips</span>
      </div>
    </div>

    <div class="text-center">
      <div v-if="processing" class="py-12">
        <div
          class="w-20 h-20 border-4 border-sidebar-orange border-t-transparent rounded-full animate-spin mx-auto mb-6"
        ></div>
        <p class="text-text-secondary">Logging you in...</p>
      </div>

      <div v-else-if="success">
        <div class="mb-6">
          <div
            class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto"
          >
            <svg
              class="w-10 h-10 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
        </div>
        <h1 class="text-2xl font-bold text-text-primary mb-4">
          Welcome to EvoClips! ✨
        </h1>
        <p class="text-text-secondary mb-6">Redirecting to your dashboard...</p>
      </div>

      <div v-else-if="error">
        <div class="mb-6">
          <div
            class="w-20 h-20 bg-red-100 rounded-full flex items-center justify-center mx-auto"
          >
            <svg
              class="w-10 h-10 text-red-600"
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
          </div>
        </div>
        <h1 class="text-2xl font-bold text-text-primary mb-4">Login Failed</h1>
        <p class="text-text-secondary mb-6">{{ error }}</p>
        <NuxtLink
          to="/login"
          class="inline-block w-full py-3.5 bg-sidebar-orange hover:bg-sidebar-orange/90 text-background-primary font-semibold rounded-xl transition-all"
        >
          Go to Login
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: "auth",
  middleware: "guest",
});

useSeoMeta({
  title: "Email Verified - EvoClips",
});

const route = useRoute();
const authStore = useAuthStore();

const processing = ref(true);
const success = ref(false);
const error = ref("");

onMounted(async () => {
  const token = route.query.token;

  if (!token) {
    error.value = "No authentication token provided. Please try logging in.";
    processing.value = false;
    return;
  }

  try {
    // Store token
    if (typeof window !== "undefined") {
      localStorage.setItem("token", token);
    }

    console.log("token", token);

    const tokenCookie = useCookie("auth-token", {
      maxAge: 60 * 60 * 24 * 7,
    });
    tokenCookie.value = token;

    // Update auth store
    authStore.token = token;
    authStore.isAuthenticated = true;

    // Fetch user data
    await authStore.fetchUser();

    // Success!
    success.value = true;
    processing.value = false;

    // // Redirect to dashboard
    setTimeout(() => {
      navigateTo("/dashboard");
    }, 1500);
  } catch (err) {
    console.error("Auto-login error:", err);
    processing.value = false;
    error.value =
      "Failed to log in automatically. Please try logging in manually.";
  }
});
</script>