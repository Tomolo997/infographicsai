<template>
  <div
    class="w-1/2 h-screen bg-card-bg flex items-center justify-center p-8 overflow-y-auto"
  >
    <div class="max-w-xl w-full space-y-12 border-sidebar-border">
      <!-- App Preview Section -->
      <div class="space-y-6">
        <div class="flex items-center justify-center gap-4">
          <!-- Front Image -->
          <div class="flex-shrink-0">
            <div
              class="w-48 bg-card-bg border border-card-border rounded-xl flex items-center justify-center overflow-hidden"
              style="aspect-ratio: 1/1"
            >
              <img
                v-if="frontImageSrc"
                :src="frontImageSrc"
                alt="Front image"
                class="w-full h-full object-cover"
              />
              <span v-else class="text-text-secondary text-sm"
                >front image</span
              >
            </div>
          </div>

          <!-- Created Video (Center - Larger) -->
          <div class="flex-shrink-0">
            <div
              class="w-72 bg-card-bg border-2 border-sidebar-orange rounded-2xl flex items-center justify-center overflow-hidden shadow-xl shadow-sidebar-orange/20"
              style="aspect-ratio: 9/16"
            >
              <video
                v-if="videoSrc"
                :src="videoSrc"
                class="w-full h-full object-cover"
                autoplay
                loop
                muted
                playsinline
              />
              <span v-else class="text-text-primary text-sm font-medium"
                >created video</span
              >
            </div>
          </div>

          <!-- Tail Image -->
          <div class="flex-shrink-0">
            <div
              class="w-48 bg-card-bg border border-card-border rounded-xl flex items-center justify-center overflow-hidden"
              style="aspect-ratio: 1/1"
            >
              <img
                v-if="tailImageSrc"
                :src="tailImageSrc"
                alt="Tail image"
                class="w-full h-full object-cover"
              />
              <span v-else class="text-text-secondary text-sm">tail image</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Reviews Section -->
      <div class="text-center space-y-6">
        <!-- User Avatars -->
        <div class="flex justify-center items-center">
          <div class="flex items-center">
            <div
              v-for="(avatar, index) in userAvatars"
              :key="index"
              class="relative"
              :style="{ marginLeft: index > 0 ? '-12px' : '0' }"
            >
              <div
                class="w-14 h-14 rounded-full border-3 border-background-primary bg-card-bg overflow-hidden shadow-lg"
              >
                <img
                  v-if="avatar"
                  :src="avatar"
                  :alt="`User ${index + 1}`"
                  class="w-full h-full object-cover"
                />
                <div
                  v-else
                  class="w-full h-full bg-gradient-to-br from-sidebar-orange/30 to-sidebar-orange/10"
                ></div>
              </div>
            </div>
          </div>

          <!-- Stars -->
          <div class="flex items-center gap-1 ml-6">
            <svg
              v-for="star in 5"
              :key="star"
              class="w-6 h-6 text-sidebar-orange fill-current"
              viewBox="0 0 24 24"
            >
              <path
                d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
              />
            </svg>
          </div>
        </div>

        <!-- Trust Badge -->
        <div class="space-y-2">
          <p class="text-text-secondary text-base">
            Trusted by 27,000+ creators
          </p>
        </div>

        <!-- Main Heading -->
        <div class="space-y-3">
          <h2 class="text-2xl font-bold text-text-primary">
            Join Thousands Of Content Creators
          </h2>
          <p class="text-base text-text-secondary max-w-md mx-auto">
            Who use EvoClips to create and share their stories.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// You can pass these as props or fetch from an API
const frontImageSrc = ref("");
const tailImageSrc = ref("");
const videoSrc = ref("");

// Array of user avatars (can be populated with real image URLs)
const userAvatars = ref([
  "", // Add real avatar URLs here
  "",
  "",
  "",
  "",
  "",
]);
</script>

<style scoped>
/* Optional: Add custom scrollbar styling */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #2e2e2e;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #3e3e3e;
}
</style>