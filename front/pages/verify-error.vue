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
        <span class="text-2xl font-bold text-text-primary">ainfographic</span>
      </div>
    </div>

    <div class="text-center">
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

      <h1 class="text-2xl font-bold text-text-primary mb-4">
        Verification Failed
      </h1>
      <p class="text-text-secondary mb-6">
        This verification link is invalid or has expired.<br />
        Please try signing up again.
      </p>

      <div class="space-y-3">
        <NuxtLink
          to="/signup"
          class="block w-full py-3.5 bg-sidebar-orange hover:bg-sidebar-orange/90 text-background-primary font-semibold rounded-xl transition-all"
        >
          Create New Account
        </NuxtLink>

        <NuxtLink
          to="/login"
          class="block w-full py-3.5 border border-card-border hover:border-sidebar-orange text-text-primary font-semibold rounded-xl transition-all"
        >
          Try Logging In
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
  title: "Verification Failed - Ainfographic",
});
</script>