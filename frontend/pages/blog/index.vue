<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <section class="py-16 text-center bg-white shadow-sm">
      <div class="max-w-4xl mx-auto px-4">
        <h1 class="text-5xl font-bold text-gray-900 mb-6">Blog</h1>
        <p class="text-xl text-gray-600">
          Discover insights, tips, and updates about AI-powered infographics
        </p>
      </div>
    </section>

    <!-- Blog Posts Grid -->
    <section class="max-w-7xl mx-auto px-4 py-12">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <!-- Blog Post Card -->
        <article v-for="post in posts" :key="post.id" 
          class="bg-white rounded-xl shadow-md overflow-hidden transition-all duration-300 hover:shadow-lg hover:-translate-y-1">
          <div class="p-6">
            <h2 class="text-2xl font-semibold text-gray-900 mb-3 hover:text-primary transition-colors">
              {{ post.title }}
            </h2>
            <p class="text-gray-600 mb-4 line-clamp-3">{{ post.excerpt }}</p>
            <div class="flex items-center justify-between pt-4 border-t border-gray-100">
              <span class="text-sm text-gray-500">{{ post.date }}</span>
              <NuxtLink 
                :to="`/blog/${post.slug}`" 
                class="text-primary hover:text-primary-dark font-medium flex items-center gap-1 group">
                Read more 
                <span class="group-hover:translate-x-1 transition-transform">→</span>
              </NuxtLink>
            </div>
          </div>
        </article>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: "Blog",
  setup() {
    definePageMeta({
      layout: 'blog'
    })
  },
  
  data() {
    return {
      posts: [
        {
          id: 1,
          title: "Instagram Post Sizes: The Complete Guide for 2025",
          excerpt: "Learn everything you need to know about Instagram post sizes in 2025, ensuring your content displays perfectly across all devices and formats.",
          date: "April 8, 2024",
          slug: "instagram-post-sizes-complete-guide-2025"
        },
        {
          id: 2,
          title: "Getting Started with AI Infographics",
          excerpt: "Learn how to create stunning infographics using AI technology...",
          date: "April 7, 2024",
          slug: "getting-started-with-ai-infographics"
        },
        {
          id: 3,
          title: "Best Practices for Data Visualization",
          excerpt: "Discover the key principles of effective data visualization...",
          date: "April 6, 2024",
          slug: "best-practices-for-data-visualization"
        }
      ],
    };
  },
  
};
</script>

<style scoped>
/* Add any specific blog index styles here */
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>