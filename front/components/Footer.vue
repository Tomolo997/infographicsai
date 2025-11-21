<template>
  <footer class="bg-background-secondary border-t border-border-primary">
    <div class="container-custom py-12">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <div class="col-span-1 md:col-span-2">
          <div class="flex items-center">
            <span class="text-2xl font-bold gradient-text">Promptwatch</span>
          </div>
          <p class="mt-4 text-text-secondary max-w-md">
            Track and optimize visibility in ChatGPT, Gemini and other AI Search engines to drive traffic to your website that converts.
          </p>
        </div>

        <div>
          <h3
            class="text-sm font-semibold text-text-primary tracking-wider uppercase"
          >
            Product
          </h3>
          <ul class="mt-4 space-y-4">
            <li>
              <NuxtLink
                to="/features"
                class="text-text-secondary hover:text-text-primary transition-colors"
              >
                Features
              </NuxtLink>
            </li>
            <li>
              <NuxtLink
                to="/pricing"
                class="text-text-secondary hover:text-text-primary transition-colors"
              >
                Pricing
              </NuxtLink>
            </li>
            <li>
              <NuxtLink
                to="/calculator"
                class="text-text-secondary hover:text-text-primary transition-colors"
              >
                Calculator
              </NuxtLink>
            </li>
          </ul>
        </div>

        <div>
          <h3
            class="text-sm font-semibold text-text-primary tracking-wider uppercase"
          >
            Company
          </h3>
          <ul class="mt-4 space-y-4">
            <li>
              <NuxtLink
                to="/blog"
                class="text-text-secondary hover:text-text-primary transition-colors"
              >
                Blog
              </NuxtLink>
            </li>
            <li>
              <NuxtLink
                to="/terms"
                class="text-text-secondary hover:text-text-primary transition-colors"
              >
                Terms of Service
              </NuxtLink>
            </li>
            <li>
              <NuxtLink
                to="/privacy"
                class="text-text-secondary hover:text-text-primary transition-colors"
              >
                Privacy Policy
              </NuxtLink>
            </li>
          </ul>
        </div>
      </div>

      <div class="mt-8 pt-8 border-t border-border-primary">
        <p class="text-center text-text-secondary">
          © {{ new Date().getFullYear() }} Promptwatch. All rights reserved.
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
// Footer component
</script>