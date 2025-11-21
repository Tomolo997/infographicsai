<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-900">
    <div class="text-center">
      <h1 class="text-4xl text-white mb-8">JavaScript Test Page</h1>
      <button
        @click="testClick"
        class="bg-blue-500 text-white px-8 py-4 rounded-lg text-xl hover:bg-blue-600"
      >
        Click Me - Test JavaScript
      </button>
      <p class="text-white mt-4">Clicks: {{ count }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const count = ref(0);

const testClick = () => {
  console.log("BUTTON CLICKED!");
  count.value++;
  console.log("New count:", count.value);
};
</script>

