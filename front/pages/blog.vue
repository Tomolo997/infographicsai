<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <!-- Header -->
    <div class="text-center mb-12">
      <h1 class="text-4xl font-bold text-gray-900 mb-4">Blog</h1>
      <p class="text-xl text-gray-600 max-w-2xl mx-auto">
        Insights, tutorials, and updates from the SaaS MVP team.
      </p>
    </div>

    <!-- Featured Post -->
    <div class="mb-12">
      <article class="card overflow-hidden lg:grid lg:grid-cols-2 lg:gap-8">
        <div class="lg:p-8">
          <div class="text-sm text-primary-600 font-medium mb-2">Featured</div>
          <h2 class="text-2xl font-bold text-gray-900 mb-4">
            Building Your First SaaS Application: A Complete Guide
          </h2>
          <p class="text-gray-600 mb-6">
            Learn how to build, deploy, and scale a SaaS application from scratch. This comprehensive guide covers everything from initial planning to production deployment.
          </p>
          <div class="flex items-center text-sm text-gray-500">
            <time datetime="2024-01-15">January 15, 2024</time>
            <span class="mx-2">•</span>
            <span>10 min read</span>
          </div>
        </div>
        <div class="lg:p-0">
          <img 
            src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop&crop=entropy&auto=format"
            alt="Building SaaS Applications"
            class="w-full h-64 lg:h-full object-cover"
          >
        </div>
      </article>
    </div>

    <!-- Blog Posts Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <article class="card group cursor-pointer hover:shadow-lg transition-shadow">
        <img 
          src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=250&fit=crop&crop=entropy&auto=format"
          alt="Authentication Best Practices"
          class="w-full h-48 object-cover rounded-lg mb-4"
        >
        <div class="space-y-2">
          <h3 class="text-xl font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
            Authentication Best Practices for SaaS
          </h3>
          <p class="text-gray-600">
            Secure your SaaS application with these essential authentication patterns and security measures.
          </p>
          <div class="flex items-center text-sm text-gray-500">
            <time datetime="2024-01-10">January 10, 2024</time>
            <span class="mx-2">•</span>
            <span>7 min read</span>
          </div>
        </div>
      </article>

      <article class="card group cursor-pointer hover:shadow-lg transition-shadow">
        <img 
          src="https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=400&h=250&fit=crop&crop=entropy&auto=format"
          alt="Scaling SaaS Applications"
          class="w-full h-48 object-cover rounded-lg mb-4"
        >
        <div class="space-y-2">
          <h3 class="text-xl font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
            Scaling Your SaaS to Handle Millions of Users
          </h3>
          <p class="text-gray-600">
            Learn the strategies and technologies needed to scale your SaaS application effectively.
          </p>
          <div class="flex items-center text-sm text-gray-500">
            <time datetime="2024-01-05">January 5, 2024</time>
            <span class="mx-2">•</span>
            <span>12 min read</span>
          </div>
        </div>
      </article>

      <article class="card group cursor-pointer hover:shadow-lg transition-shadow">
        <img 
          src="https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=250&fit=crop&crop=entropy&auto=format"
          alt="Payment Integration"
          class="w-full h-48 object-cover rounded-lg mb-4"
        >
        <div class="space-y-2">
          <h3 class="text-xl font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
            Integrating Stripe for SaaS Billing
          </h3>
          <p class="text-gray-600">
            A step-by-step guide to implementing subscription billing with Stripe in your SaaS application.
          </p>
          <div class="flex items-center text-sm text-gray-500">
            <time datetime="2023-12-28">December 28, 2023</time>
            <span class="mx-2">•</span>
            <span>8 min read</span>
          </div>
        </div>
      </article>

      <article class="card group cursor-pointer hover:shadow-lg transition-shadow">
        <img 
          src="https://images.unsplash.com/photo-1553484771-371a605b060b?w=400&h=250&fit=crop&crop=entropy&auto=format"
          alt="API Design"
          class="w-full h-48 object-cover rounded-lg mb-4"
        >
        <div class="space-y-2">
          <h3 class="text-xl font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
            Designing RESTful APIs for SaaS
          </h3>
          <p class="text-gray-600">
            Best practices for designing clean, maintainable, and scalable REST APIs for your SaaS platform.
          </p>
          <div class="flex items-center text-sm text-gray-500">
            <time datetime="2023-12-20">December 20, 2023</time>
            <span class="mx-2">•</span>
            <span>6 min read</span>
          </div>
        </div>
      </article>

      <article class="card group cursor-pointer hover:shadow-lg transition-shadow">
        <img 
          src="https://images.unsplash.com/photo-1551434678-e076c223a692?w=400&h=250&fit=crop&crop=entropy&auto=format"
          alt="Database Design"
          class="w-full h-48 object-cover rounded-lg mb-4"
        >
        <div class="space-y-2">
          <h3 class="text-xl font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
            Database Design Patterns for Multi-Tenant SaaS
          </h3>
          <p class="text-gray-600">
            Explore different approaches to structuring your database for multi-tenant SaaS applications.
          </p>
          <div class="flex items-center text-sm text-gray-500">
            <time datetime="2023-12-15">December 15, 2023</time>
            <span class="mx-2">•</span>
            <span>9 min read</span>
          </div>
        </div>
      </article>

      <article class="card group cursor-pointer hover:shadow-lg transition-shadow">
        <img 
          src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=250&fit=crop&crop=entropy&auto=format"
          alt="DevOps for SaaS"
          class="w-full h-48 object-cover rounded-lg mb-4"
        >
        <div class="space-y-2">
          <h3 class="text-xl font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
            DevOps Best Practices for SaaS Deployment
          </h3>
          <p class="text-gray-600">
            Streamline your deployment process with these DevOps practices specifically for SaaS applications.
          </p>
          <div class="flex items-center text-sm text-gray-500">
            <time datetime="2023-12-10">December 10, 2023</time>
            <span class="mx-2">•</span>
            <span>11 min read</span>
          </div>
        </div>
      </article>
    </div>

    <!-- Newsletter Signup -->
    <div class="mt-16 bg-primary-600 rounded-lg p-8 text-center">
      <h2 class="text-2xl font-bold text-white mb-4">
        Stay Updated
      </h2>
      <p class="text-primary-100 mb-6 max-w-2xl mx-auto">
        Get the latest insights, tutorials, and updates delivered straight to your inbox.
      </p>
      <form class="max-w-md mx-auto flex gap-4">
        <input
          type="email"
          placeholder="Enter your email"
          class="flex-1 px-4 py-2 rounded-lg border-0 focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-primary-600"
        >
        <button
          type="submit"
          class="bg-white text-primary-600 hover:bg-gray-100 font-medium py-2 px-6 rounded-lg transition-colors"
        >
          Subscribe
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
useSeoMeta({
  title: 'Blog - SaaS MVP',
  description: 'Insights, tutorials, and updates from the SaaS MVP team. Learn how to build and scale your SaaS application.'
})
</script>