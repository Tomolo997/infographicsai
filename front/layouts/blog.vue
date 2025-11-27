<template>
  <div class="min-h-screen flex flex-col">
    <NavBar />
    <main class="flex-grow bg-sidebar-orange-bg">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <slot />
      </div>
    </main>
    <Footer class="mt-auto" />
  </div>
</template>

<script setup>
import NavBar from "~/components/NavBar.vue";
import Footer from "~/components/Footer.vue";
</script>

<style scoped>
/* Add any specific blog layout styles here */
</style>
