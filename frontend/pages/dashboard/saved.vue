<template>
  <div class="px-8 py-4">
    <div class="flex gap-[5px] flex-col">
      <div class="flex justify-start items-center">
        <span class="text-sm font-semibold flex justify-center items-center"
          >Saved</span
        >
        <div class="ml-4"></div>
      </div>
      <div class="h-[1px] w-full bg-grayBackgroundLight"></div>
    </div>
    <div class="mt-4 flex flex-wrap justify-start gap-4">
      <template v-if="dashboardStore.infographicsSaved && dashboardStore.infographicsSaved.length > 0">
        <div
          v-for="infograph in dashboardStore.infographicsSaved"
          :key="infograph.uuid"
        >
          <ListTemplateCard :infograph="infograph"></ListTemplateCard>
        </div>
      </template>
      <div v-else-if="isLoading" class="w-full flex justify-center items-center flex-col text-center py-8">
        <div class="animate-spin h-12 w-12 mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-full w-full text-primary" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
        <p class="text-gray-600">Loading saved infographics...</p>
      </div>
      <div v-else class="w-full text-center py-8">
        <p class="text-gray-600 mb-4">You don't have any saved infographics yet.</p>
        <NuxtLink to="/dashboard" class="text-blue-600 hover:text-blue-800 font-medium">
          Go to Dashboard
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script>
import { useDashboardStore } from "@/stores/dashboardStore";

export default {
  name: "dashboard",
  async setup() {
    const dashboardStore = useDashboardStore();
    definePageMeta({
      layout: "dashboard",
    });

    return {
      dashboardStore,
    };
  },
  data() {
    return {
      userInfo: null,
      selectedFile: null,
      userProfilePicture: null,
      isLoading: true,
    };
  },
  async mounted() {
    try {
      await this.dashboardStore.getSavedInfographics();
    } finally {
      this.isLoading = false;
    }
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
  },
  computed: {},
};
</script>

<style scoped>
img {
  max-width: 200px;
  max-height: 200px;
}
</style>
