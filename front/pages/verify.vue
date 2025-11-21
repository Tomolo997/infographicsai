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

    <div class="text-center py-12">
      <div
        class="w-20 h-20 border-4 border-sidebar-orange border-t-transparent rounded-full animate-spin mx-auto mb-6"
      ></div>
      <p class="text-text-secondary">
        Verifying your email and logging you in...
      </p>
    </div>
  </div>
</template>

<script setup>
import apiClient from "~/client/apiClient";
definePageMeta({
  layout: "auth",
  middleware: "guest",
});

useSeoMeta({
  title: "Verifying Email - EvoClips",
  description: "Verifying your EvoClips account",
});

const route = useRoute();

// Note: This page is not actually used anymore since backend redirects directly
// But keeping it here in case someone navigates to /verify manually
onMounted(async () => {
  const { uid, token } = route.query;
  if (!uid || !token) {
    navigateTo("/signup");
    return;
  }

  console.log("uid", uid);
  console.log("token", token);

  try {
    const response = await apiClient.get(`/account/verify/${uid}/${token}/`);
    if (response.status === 200) {
      navigateTo("/verify-success");
    } else {
      navigateTo("/verify-error");
    }
  } catch (error) {
    console.error("Error verifying email:", error);
    navigateTo("/verify-error");
  }
});
</script>