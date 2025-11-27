<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <!-- Header -->
    <div class="text-center mb-12">
      <h1 class="text-4xl font-bold text-text-primary mb-4">Blog</h1>
      <p class="text-xl text-gray-600 max-w-2xl mx-auto">
        Insights, tutorials, and updates from the Ainfographic team.
      </p>
    </div>

    <!-- Featured Post -->
    <div class="mb-12">
      <NuxtLink
        to="/blog/instagram-post-sizes-complete-guide-2025"
        class="card overflow-hidden lg:grid lg:grid-cols-2 lg:gap-8"
      >
        <div class="lg:p-8">
          <div class="text-sm text-primary-600 font-medium mb-2">Featured</div>
          <h2 class="text-2xl font-bold text-text-primary mb-4">
            Instagram Post Sizes: Complete Guide for 2025 | AI Infographic
          </h2>
          <p class="text-text-secondary mb-6">
            Master Instagram post sizes in 2025 with our comprehensive guide.
            Learn optimal dimensions for feed posts, stories, reels, and more to
            create perfect content.
          </p>
          <div class="flex items-center text-sm text-text-secondary">
            <time datetime="2025-11-27">November 27, 2025</time>
            <span class="mx-2">•</span>
            <span>5 min read</span>
          </div>
        </div>
        <div class="lg:p-0">
          <img
            src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop&crop=entropy&auto=format"
            alt="Instagram Post Sizes: Complete Guide for 2025 | AI Infographic"
            class="w-full h-64 lg:h-full object-cover"
          />
        </div>
      </NuxtLink>
    </div>

    <!-- Newsletter Signup -->
    <div class="mt-16 bg-sidebar-orange rounded-lg p-8 text-center">
      <h2 class="text-2xl font-bold text-white mb-4">Stay Updated</h2>
      <p class="text-primary-100 mb-6 max-w-2xl mx-auto">
        Get the latest insights, tutorials, and updates delivered straight to
        your inbox.
      </p>
      <form class="max-w-md mx-auto flex gap-4">
        <input
          type="email"
          placeholder="Enter your email"
          class="flex-1 px-4 py-2 rounded-lg border-0 focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-primary-600"
        />
        <button
          type="submit"
          class="bg-white text-sidebar-orange hover:bg-gray-100 font-medium py-2 px-6 rounded-lg transition-colors"
        >
          Subscribe
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  layout: "blog",
});
useSeoMeta({
  title: "Blog - Ainfographic",
  description:
    "Insights, tutorials, and updates from the Ainfographic team. Learn how to build and scale your SaaS application.",
});
</script>