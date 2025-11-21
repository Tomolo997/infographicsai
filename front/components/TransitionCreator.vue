<template>
  <div
    class="w-full pb-4 mx-auto relative space-y-2 flex justify-center items-center gap-8 h-full"
  >
    <!-- Main Video Preview -->
    <div class="space-y-3 space-x-3">
      <!-- Images Row -->
      <div class="flex items-center justify-center gap-8">
        <!-- Front Image Upload -->
        <div class="space-y-2 flex flex-col items-center justify-center">
          <label class="block text-card-text-primary text-xs font-medium">
            <!-- Front Image -->
          </label>
          <div
            @click="triggerFileInput('front')"
            class="bg-card-bg border border-card-border rounded-lg cursor-pointer h-36 w-36 hover:border-primary-500 transition-colors"
          >
            <div
              v-if="!frontImage"
              class="w-full h-full flex items-center justify-center"
            >
              <p class="text-card-text-secondary text-xs">front image</p>
            </div>
            <img
              v-else
              :src="frontImage"
              alt="Front image"
              class="w-full h-full object-cover rounded-lg"
            />
          </div>
          <input
            ref="frontInput"
            type="file"
            accept="image/*"
            class="hidden"
            @change="handleImageUpload($event, 'front')"
          />
        </div>
      </div>
    </div>
    <div class="flex justify-center">
      <div
        class="w-[300px] bg-card-bg border border-card-border rounded-lg overflow-hidden"
        style="aspect-ratio: 9/16"
      >
        <div
          v-if="!previewVideo"
          class="w-full h-full flex items-center justify-center"
        >
          <p class="text-card-text-secondary text-xs text-center px-2">
            created video
          </p>
        </div>
        <video
          v-else
          :src="previewVideo"
          class="w-full h-full object-cover"
          controls
        />
      </div>
    </div>

    <!-- Input Section -->
    <div class="space-y-3">
      <!-- Images Row -->
      <div class="flex items-center justify-center gap-8">
        <!-- Tail Image Upload -->
        <div class="space-y-2 flex flex-col items-center justify-center">
          <label class="block text-card-text-primary text-xs font-medium">
            <!-- Tail Image -->
          </label>
          <div
            @click="triggerFileInput('tail')"
            class="bg-card-bg border border-card-border rounded-lg cursor-pointer h-36 w-36 hover:border-primary-500 transition-colors"
          >
            <div
              v-if="!tailImage"
              class="w-full h-full flex items-center justify-center"
            >
              <p class="text-card-text-secondary text-xs">tail image</p>
            </div>
            <img
              v-else
              :src="tailImage"
              alt="Tail image"
              class="w-full h-full object-cover rounded-lg"
            />
          </div>
          <input
            ref="tailInput"
            type="file"
            accept="image/*"
            class="hidden"
            @change="handleImageUpload($event, 'tail')"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useDashboardVideoStore } from "~/stores/dashboardVideo";

export default {
  setup() {
    const videoStore = useDashboardVideoStore();
    return { videoStore };
  },
  computed: {
    frontImage() {
      return this.videoStore.frontImage;
    },
    tailImage() {
      return this.videoStore.tailImage;
    },
    previewVideo() {
      return this.videoStore.previewVideo;
    },
  },
  methods: {
    triggerFileInput(type) {
      if (type === "front") {
        this.$refs.frontInput.click();
      } else {
        this.$refs.tailInput.click();
      }
    },
    async handleImageUpload(event, type) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = async (e) => {
          const dataUrl = e.target.result;

          // Set preview image immediately
          if (type === "front") {
            this.videoStore.setFrontImage(dataUrl);
          } else {
            this.videoStore.setTailImage(dataUrl);
          }

          // Upload to R2 in background
          try {
            if (type === "front") {
              await this.videoStore.uploadFrontImage(dataUrl);
              console.log("Front image uploaded to R2");
            } else {
              await this.videoStore.uploadTailImage(dataUrl);
              console.log("Tail image uploaded to R2");
            }
          } catch (error) {
            console.error(`Failed to upload ${type} image:`, error);
            // You can show a toast notification here
          }
        };
        reader.readAsDataURL(file);
      }
    },
  },
};
</script>

<style scoped>
/* Additional custom styles if needed */
</style>

