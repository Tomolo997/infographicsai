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
              d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
            />
          </svg>
        </div>
      </div>

      <h1 class="text-2xl font-bold text-text-primary mb-4">
        Check Your Email! 📧
      </h1>

      <p class="text-text-secondary mb-2">We've sent a verification link to</p>
      <p class="font-semibold text-text-primary mb-6">{{ email }}</p>

      <div
        class="bg-card-bg border border-card-border rounded-xl p-6 mb-6 text-left"
      >
        <p class="text-sm text-text-secondary mb-3">
          ✨ Click the link in the email to verify your account and you'll be
          automatically logged in!
        </p>
        <p class="text-xs text-text-secondary">
          The link expires in 24 hours. Didn't receive it? Check your spam
          folder.
        </p>
      </div>

      <NuxtLink
        to="/login"
        class="inline-block text-sidebar-orange hover:text-sidebar-orange/80 font-medium"
      >
        ← Back to Login
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: "auth",
  middleware: "guest",
});

const route = useRoute();
const email = computed(() => route.query.email || "your email");

useSeoMeta({
  title: "Verify Your Email - Ainfographic",
});
</script>