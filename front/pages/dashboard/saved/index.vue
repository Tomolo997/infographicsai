<template>
  <div class="min-h-screen p-6">
    <!-- Header Section -->
    <div class="flex items-start justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-primary mb-2">Saved Infographs</h1>
        <p class="text-md text-text-secondary">
          View and manage your saved infographs
        </p>
      </div>
    </div>

    <!-- Filter Section -->
    <div class="mb-6">
      <div class="relative inline-block">
        <button
          @click="toggleAspectRatioFilter"
          class="h-10 px-4 inline-flex items-center justify-center gap-2 rounded-md border border-card-border bg-card-bg hover:bg-background-secondary transition-colors text-text-primary"
        >
          <svg
            class="h-4 w-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect width="20" height="16" x="2" y="4" rx="2" />
            <path d="M12 9v11" />
            <path d="M2 9h13a2 2 0 0 1 2 2v9" />
          </svg>
          <span class="text-sm font-medium">
            {{ selectedAspectRatioFilter || "All Aspect Ratios" }}
          </span>
          <svg
            class="h-4 w-4 transition-transform"
            :class="{ 'rotate-180': showAspectRatioDropdown }"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
            stroke-width="2"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </button>
        <!-- Dropdown -->
        <div
          v-if="showAspectRatioDropdown"
          class="absolute top-full left-0 mt-2 w-64 bg-card-bg border border-card-border rounded-lg shadow-xl z-50 max-h-96 overflow-y-auto"
        >
          <div
            class="sticky top-0 bg-card-bg border-b border-card-border px-4 py-3 font-semibold text-text-primary text-sm"
          >
            Filter by Aspect Ratio
          </div>
          <div
            @click="selectAspectRatioFilter(null)"
            :class="[
              'p-3 cursor-pointer border-b border-card-border transition-colors flex items-center gap-2',
              !selectedAspectRatioFilter
                ? 'bg-primary-500/10'
                : 'hover:bg-background-secondary',
            ]"
          >
            <span class="flex-1 text-text-primary text-sm">All Aspect Ratios</span>
            <svg
              v-if="!selectedAspectRatioFilter"
              class="h-5 w-5 text-primary-500 flex-shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
          <div
            v-for="ratio in aspectRatios"
            :key="ratio.value"
            @click="selectAspectRatioFilter(ratio.label)"
            :class="[
              'p-3 cursor-pointer border-b border-card-border last:border-b-0 transition-colors flex items-center gap-2',
              selectedAspectRatioFilter === ratio.label
                ? 'bg-primary-500/10'
                : 'hover:bg-background-secondary',
            ]"
          >
            <div class="flex-1 min-w-0">
              <div class="font-medium text-text-primary text-sm">
                {{ ratio.label }}
              </div>
              <div class="text-xs text-text-secondary mt-1">
                {{ ratio.platforms }}
              </div>
            </div>
            <svg
              v-if="selectedAspectRatioFilter === ratio.label"
              class="h-5 w-5 text-primary-500 flex-shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div
      v-if="isLoading"
      class="flex items-center justify-center py-20"
    >
      <svg
        class="w-10 h-10 animate-spin text-primary-500"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="4"
        ></circle>
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        ></path>
      </svg>
    </div>

    <!-- Empty State -->
    <div
      v-else-if="filteredInfographs.length === 0"
      class="flex flex-col items-center justify-center py-20"
    >
      <svg
        class="w-20 h-20 text-text-secondary mb-4"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="1.5"
          d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
        />
      </svg>
      <h3 class="text-lg font-semibold text-text-primary mb-2">
        No saved infographs
      </h3>
      <p class="text-text-secondary text-sm">
        Start creating infographs to see them here
      </p>
    </div>

    <!-- Infographs Grid - Scrollable -->
    <div
      v-else
      class="overflow-y-auto max-h-[calc(100vh-280px)] pr-2"
      style="
        scrollbar-width: thin;
        scrollbar-color: rgba(0, 0, 0, 0.2) transparent;
      "
    >
      <div
        class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4"
      >
        <div
          v-for="infograph in filteredInfographs"
          :key="infograph.id"
          @click="openInfographModal(infograph)"
          class="group cursor-pointer rounded-lg border-2 transition-all duration-300 overflow-hidden border-card-border hover:border-primary-500/50 hover:shadow-md"
        >
          <!-- Infograph Image Container -->
          <div
            class="relative bg-background-secondary h-48 flex items-center justify-center p-1"
          >
            <div
              class="w-full h-full flex items-center justify-center overflow-hidden rounded"
            >
              <img
                :src="infograph.image"
                :alt="infograph.name"
                class="max-w-full max-h-full object-contain"
                :style="{ aspectRatio: infograph.aspectRatio }"
              />
            </div>
          </div>
          <!-- Infograph Info -->
          <div class="p-3 bg-card-bg">
            <p
              class="text-sm font-medium text-center text-text-primary group-hover:text-primary-500 transition-colors"
            >
              {{ infograph.name }}
            </p>
            <p class="text-xs text-text-secondary text-center mt-1">
              {{ getAspectRatioLabel(infograph.aspectRatio) }} • {{ formatDate(infograph.created_at) }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Infograph Modal -->
    <Modal
      :is-open="showInfographModal"
      :title="selectedInfograph?.name || ''"
      :subtitle="
        selectedInfograph
          ? getAspectRatioLabel(selectedInfograph.aspectRatio)
          : ''
      "
      max-width="max-w-4xl"
      @close="closeInfographModal"
    >
      <template #body>
        <div v-if="selectedInfograph" class="space-y-4">
          <!-- Infograph Preview -->
          <div
            class="relative bg-background-secondary rounded-lg overflow-hidden"
          >
            <div class="w-full flex items-center justify-center p-8">
              <img
                :src="selectedInfograph.image"
                :alt="selectedInfograph.name"
                class="max-w-full max-h-[60vh] object-contain rounded"
                :style="{ aspectRatio: selectedInfograph.aspectRatio }"
              />
            </div>
          </div>
          <!-- Infograph Details -->
          <div class="space-y-2">
            <div>
              <span class="text-sm font-semibold text-text-primary"
                >Aspect Ratio:</span
              >
              <span class="text-sm text-text-secondary ml-2">
                {{ getAspectRatioLabel(selectedInfograph.aspectRatio) }}
              </span>
            </div>
            <div>
              <span class="text-sm font-semibold text-text-primary"
                >Created:</span
              >
              <span class="text-sm text-text-secondary ml-2">
                {{ formatDate(selectedInfograph.created_at) }}
              </span>
            </div>
          </div>
        </div>
      </template>
      <template #cta>
        <div class="flex gap-3 justify-end">
          <button
            @click="handleDownload"
            class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-primary-500 text-white hover:bg-primary-600 transition-colors text-sm font-medium"
          >
            <svg
              class="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
              />
            </svg>
            Download
          </button>
          <button
            @click="handleDelete"
            class="inline-flex items-center gap-2 px-4 py-2 rounded-lg border border-red-500 text-red-500 hover:bg-red-500/10 transition-colors text-sm font-medium"
          >
            <svg
              class="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
            Delete
          </button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import Modal from "~/components/Modal.vue";

definePageMeta({
  layout: "dashboard",
  middleware: "auth",
});

// State
const showAspectRatioDropdown = ref(false);
const selectedAspectRatioFilter = ref(null);
const showInfographModal = ref(false);
const selectedInfograph = ref(null);
const isLoading = ref(true);

// Mock saved infographs (replace with API call)
const infographs = ref([]);

// Aspect Ratios
const aspectRatios = ref([
  {
    value: "9/16",
    label: "9:16",
    platforms: "Instagram Story, TikTok, Facebook Story",
  },
  {
    value: "1/1",
    label: "1:1",
    platforms: "Instagram Post, Facebook Post, LinkedIn Post",
  },
  {
    value: "4/5",
    label: "4:5",
    platforms: "Instagram Portrait, Facebook Feed",
  },
  {
    value: "16/9",
    label: "16:9",
    platforms: "YouTube Thumbnail, LinkedIn Cover, Twitter Header",
  },
  {
    value: "21/9",
    label: "21:9",
    platforms: "Facebook Cover, Twitter Header (X Header)",
  },
  {
    value: "3/2",
    label: "3:2",
    platforms: "Twitter Post (X Post), General Photography",
  },
  {
    value: "4/3",
    label: "4:3",
    platforms: "Facebook Post, Classic Photography",
  },
  {
    value: "2/3",
    label: "2:3",
    platforms: "Pinterest Pin, Instagram Portrait",
  },
]);

// Computed
const filteredInfographs = computed(() => {
  if (!selectedAspectRatioFilter.value) {
    return infographs.value;
  }
  const selectedRatio = aspectRatios.value.find(
    (r) => r.label === selectedAspectRatioFilter.value
  );
  if (!selectedRatio) return infographs.value;
  return infographs.value.filter((i) => i.aspectRatio === selectedRatio.value);
});

// Methods
const toggleAspectRatioFilter = () => {
  showAspectRatioDropdown.value = !showAspectRatioDropdown.value;
};

const selectAspectRatioFilter = (label) => {
  selectedAspectRatioFilter.value = label;
  showAspectRatioDropdown.value = false;
};

const getAspectRatioLabel = (aspectRatio) => {
  const ratio = aspectRatios.value.find((r) => r.value === aspectRatio);
  return ratio ? ratio.label : aspectRatio;
};

const formatDate = (date) => {
  if (!date) return "";
  return new Date(date).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
};

const openInfographModal = (infograph) => {
  selectedInfograph.value = infograph;
  showInfographModal.value = true;
};

const closeInfographModal = () => {
  showInfographModal.value = false;
  selectedInfograph.value = null;
};

const handleDownload = () => {
  console.log("Download infograph:", selectedInfograph.value);
  // Add download logic here
  closeInfographModal();
};

const handleDelete = async () => {
  if (confirm("Are you sure you want to delete this infograph?")) {
    console.log("Delete infograph:", selectedInfograph.value);
    // Add delete logic here
    // Remove from local array
    const index = infographs.value.findIndex(
      (i) => i.id === selectedInfograph.value.id
    );
    if (index > -1) {
      infographs.value.splice(index, 1);
    }
    closeInfographModal();
  }
};

// Fetch saved infographs
const fetchInfographs = async () => {
  try {
    isLoading.value = true;
    const { $api } = useNuxtApp();
    const response = await $api("/infographs/saved/");
    infographs.value = response;
  } catch (error) {
    console.error("Error fetching saved infographs:", error);
    // Use mock data for development
    infographs.value = [
      {
        id: 1,
        name: "Marketing Stats",
        image: "https://picsum.photos/seed/saved1/400/600",
        aspectRatio: "9/16",
        created_at: "2024-01-15T10:30:00Z",
      },
      {
        id: 2,
        name: "Business Dashboard",
        image: "https://picsum.photos/seed/saved2/600/400",
        aspectRatio: "16/9",
        created_at: "2024-01-14T15:20:00Z",
      },
      {
        id: 3,
        name: "Social Media Post",
        image: "https://picsum.photos/seed/saved3/400/400",
        aspectRatio: "1/1",
        created_at: "2024-01-13T09:15:00Z",
      },
    ];
  } finally {
    isLoading.value = false;
  }
};

// Fetch infographs on mount
onMounted(() => {
  fetchInfographs();
});

// Close dropdown when clicking outside
if (typeof window !== "undefined") {
  window.addEventListener("click", (e) => {
    if (!e.target.closest(".relative")) {
      showAspectRatioDropdown.value = false;
    }
  });
}
</script>

<style scoped>
/* Custom scrollbar styling */
.overflow-y-auto::-webkit-scrollbar {
  width: 8px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 4px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}
</style>

