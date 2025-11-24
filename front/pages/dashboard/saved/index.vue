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
            <span class="flex-1 text-text-primary text-sm"
              >All Aspect Ratios</span
            >
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
    <div v-if="isLoading" class="flex items-center justify-center py-20">
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
            <!-- Status Badge -->
            <div class="absolute top-2 left-2 z-10 flex items-center gap-1">
              <span
                :class="[
                  'px-2 py-1 rounded-md text-xs font-semibold',
                  infograph.status === 'completed'
                    ? 'bg-white text-green-500 border border-green-500'
                    : infograph.status === 'processing'
                    ? 'bg-white text-blue-500 border border-blue-500'
                    : 'bg-white text-red-500 border border-red-500',
                ]"
              >
                {{ infograph.status }}
              </span>
              <!-- Live polling indicator -->
              <span
                v-if="pollingIntervals.has(infograph.id)"
                class="flex items-center justify-center w-5 h-5 bg-white rounded-full border border-blue-500"
                title="Checking for updates..."
              >
                <span
                  class="w-2 h-2 bg-blue-500 rounded-full animate-pulse"
                ></span>
              </span>
            </div>
            <!-- Credits Badge -->
            <div
              class="w-full h-full flex items-center justify-center overflow-hidden rounded"
            >
              <img
                v-if="infograph.image_url"
                :src="infograph.image_url"
                :alt="getInfographTitle(infograph)"
                class="max-w-full max-h-full object-contain"
                :style="{
                  aspectRatio: normalizeAspectRatio(infograph.aspect_ratio),
                }"
              />
              <div
                v-else
                class="flex flex-col items-center justify-center text-text-secondary"
              >
                <svg
                  class="w-16 h-16 mb-2"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  stroke-width="1.5"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"
                  />
                </svg>
                <span class="text-xs">No image</span>
              </div>
            </div>
          </div>
          <!-- Infograph Info -->
          <div class="p-3 bg-card-bg">
            <p
              class="text-sm font-medium text-center text-text-primary group-hover:text-primary-500 transition-colors truncate"
              :title="getInfographTitle(infograph)"
            >
              {{ getInfographTitle(infograph) }}
            </p>
            <p class="text-xs text-text-secondary text-center mt-1">
              {{ getAspectRatioLabel(infograph.aspect_ratio) }} •
              {{ infograph.resolution }}
            </p>
            <p class="text-xs text-text-secondary text-center">
              {{ formatDate(infograph.created_at) }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Infograph Modal -->
    <Modal
      :is-open="showInfographModal"
      :title="selectedInfograph ? getInfographTitle(selectedInfograph) : ''"
      :subtitle="
        selectedInfograph
          ? getAspectRatioLabel(selectedInfograph.aspect_ratio)
          : ''
      "
      max-width="max-w-4xl"
      @close="closeInfographModal"
    >
      <template #body>
        <div v-if="selectedInfograph" class="space-y-4">
          <!-- Infograph Preview -->
          <div
            v-if="selectedInfograph.image_url"
            class="relative rounded-lg overflow-hidden"
          >
            <div
              class="w-full flex items-center justify-center p-8 max-h-[1200px]"
            >
              <img
                :src="selectedInfograph.image_url"
                :alt="getInfographTitle(selectedInfograph)"
                class="max-w-full max-h-[60vh] object-contain rounded"
                :style="{
                  aspectRatio: normalizeAspectRatio(
                    selectedInfograph.aspect_ratio
                  ),
                }"
              />
            </div>
          </div>
          <div
            v-else
            class="relative bg-background-secondary rounded-lg overflow-hidden p-20 flex flex-col items-center justify-center"
          >
            <svg
              class="w-24 h-24 text-text-secondary mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              stroke-width="1.5"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z"
              />
            </svg>
            <p class="text-text-secondary">
              {{
                selectedInfograph.status === "processing"
                  ? "Image is being generated..."
                  : "No image available"
              }}
            </p>
          </div>

          <!-- Infograph Details -->
          <div class="space-y-2">
            <div>
              <span class="text-sm font-semibold text-text-primary"
                >Aspect Ratio:</span
              >
              <span class="text-sm text-text-secondary ml-2">
                {{ getAspectRatioLabel(selectedInfograph.aspect_ratio) }}
              </span>
            </div>
            <div>
              <span class="text-sm font-semibold text-text-primary"
                >Resolution:</span
              >
              <span class="text-sm text-text-secondary ml-2">
                {{ selectedInfograph.resolution }}
              </span>
            </div>
            <div>
              <span class="text-sm font-semibold text-text-primary"
                >Source URL:</span
              >
              <a
                :href="selectedInfograph.blog_url"
                target="_blank"
                rel="noopener noreferrer"
                class="text-sm text-primary-500 hover:text-primary-600 ml-2 underline"
              >
                {{ truncateUrl(selectedInfograph.blog_url) }}
              </a>
            </div>
          </div>
        </div>
      </template>
      <template #cta>
        <div class="flex gap-3 justify-end">
          <button
            v-if="selectedInfograph?.image_url"
            @click="handleDownload"
            class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-primary-500 text-white hover:bg-primary-600 transition-colors text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="!selectedInfograph?.image_url"
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
import apiClient from "~/client/apiClient";
import { ref, computed, onMounted, onBeforeUnmount } from "vue";
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
const pollingIntervals = ref(new Map()); // Track polling intervals for each infograph

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
  return infographs.value.filter((i) => {
    const normalized = normalizeAspectRatio(i.aspect_ratio);
    return normalized === selectedRatio.value;
  });
});

// Methods
const toggleAspectRatioFilter = () => {
  showAspectRatioDropdown.value = !showAspectRatioDropdown.value;
};

const selectAspectRatioFilter = (label) => {
  selectedAspectRatioFilter.value = label;
  showAspectRatioDropdown.value = false;
};

// Normalize aspect ratio format (9:16 or 9/16 -> 9/16)
const normalizeAspectRatio = (aspectRatio) => {
  if (!aspectRatio) return "16/9";
  return aspectRatio.replace(":", "/");
};

const getAspectRatioLabel = (aspectRatio) => {
  const normalized = normalizeAspectRatio(aspectRatio);
  const ratio = aspectRatios.value.find((r) => r.value === normalized);
  return ratio ? ratio.label : aspectRatio.replace("/", ":");
};

const getInfographTitle = (infograph) => {
  if (!infograph) return "";
  // Try to extract domain from blog_url
  try {
    const url = new URL(infograph.blog_url);
    const hostname = url.hostname.replace("www.", "");
    return `Infograph #${infograph.id} - ${hostname}`;
  } catch {
    return `Infograph #${infograph.id}`;
  }
};

const truncateUrl = (url) => {
  if (!url) return "";
  if (url.length <= 60) return url;
  return url.substring(0, 57) + "...";
};

const formatDate = (date) => {
  if (!date) return "";
  return new Date(date).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
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

const handleDownload = async () => {
  if (!selectedInfograph.value?.image_url) return;

  try {
    // Use backend proxy endpoint to bypass CORS
    const response = await apiClient.get(
      `/infographs/download/${selectedInfograph.value.id}/`,
      {
        responseType: "blob", // Important: tell axios to handle binary data
      }
    );

    // Create a blob URL from the response data
    const blob = new Blob([response.data], { type: "image/png" });
    const blobUrl = window.URL.createObjectURL(blob);

    // Create a temporary anchor element and trigger download
    const link = document.createElement("a");
    link.href = blobUrl;
    link.download = `infograph-${selectedInfograph.value.id}.png`;
    document.body.appendChild(link);
    link.click();

    // Clean up
    document.body.removeChild(link);
    window.URL.revokeObjectURL(blobUrl);

    closeInfographModal();
  } catch (error) {
    console.error("Error downloading infograph:", error);
    alert("Failed to download infograph. Please try again.");
  }
};

const handleDelete = async () => {
  if (!confirm("Are you sure you want to delete this infograph?")) {
    return;
  }

  try {
    await apiClient.delete(`/infographs/delete/${selectedInfograph.value.id}/`);

    // Remove from local array
    const index = infographs.value.findIndex(
      (i) => i.id === selectedInfograph.value.id
    );
    if (index > -1) {
      infographs.value.splice(index, 1);
    }

    // Stop polling for this infograph if it was being polled
    if (pollingIntervals.value.has(selectedInfograph.value.id)) {
      clearInterval(pollingIntervals.value.get(selectedInfograph.value.id));
      pollingIntervals.value.delete(selectedInfograph.value.id);
    }

    closeInfographModal();
  } catch (error) {
    console.error("Error deleting infograph:", error);
    alert("Failed to delete infograph. Please try again.");
  }
};

// Fetch saved infographs
const fetchInfographs = async () => {
  try {
    isLoading.value = true;
    const response = await apiClient.get("/infographs/list/");
    console.log("Fetched infographs:", response);
    // Sort by created_at descending (newest first)
    infographs.value = response.data;

    // Start polling for any processing infographs
    startPollingForProcessingInfographs();
  } catch (error) {
    console.error("Error fetching saved infographs:", error);
    infographs.value = [];
  } finally {
    isLoading.value = false;
  }
};

/**
 * Poll the status API for a specific infograph
 * Stops polling when status is 'completed' or 'failed'
 */
const startPollingStatus = (infographId) => {
  // Clear any existing polling for this infograph
  if (pollingIntervals.value.has(infographId)) {
    clearInterval(pollingIntervals.value.get(infographId));
  }

  // Initial status check
  checkInfographStatus(infographId);

  // Poll every 5 seconds
  const interval = setInterval(() => {
    checkInfographStatus(infographId);
  }, 5000);

  pollingIntervals.value.set(infographId, interval);
};

const checkInfographStatus = async (infographId) => {
  try {
    const response = await apiClient.get(`/infographs/status/${infographId}/`);
    const statusData = response.data;

    // Update the infograph in the array
    const infographIndex = infographs.value.findIndex(
      (i) => i.id === infographId
    );
    if (infographIndex !== -1) {
      infographs.value[infographIndex].status = statusData.status;
      infographs.value[infographIndex].image_url = statusData.image_url;
    }

    // Stop polling if completed or failed
    if (statusData.status === "completed" || statusData.status === "failed") {
      if (pollingIntervals.value.has(infographId)) {
        clearInterval(pollingIntervals.value.get(infographId));
        pollingIntervals.value.delete(infographId);
      }
    }
  } catch (error) {
    console.error(`Error checking status for infograph ${infographId}:`, error);
    // On error, stop polling for this infograph
    if (pollingIntervals.value.has(infographId)) {
      clearInterval(pollingIntervals.value.get(infographId));
      pollingIntervals.value.delete(infographId);
    }
  }
};

/**
 * Clean up all polling intervals
 */
const stopAllPolling = () => {
  pollingIntervals.value.forEach((interval) => {
    clearInterval(interval);
  });
  pollingIntervals.value.clear();
};

/**
 * Start polling for all processing infographs
 */
const startPollingForProcessingInfographs = () => {
  infographs.value.forEach((infograph) => {
    if (infograph.status === "processing" || infograph.status === "pending") {
      startPollingStatus(infograph.id);
    }
  });
};

// Fetch infographs on mount
onMounted(() => {
  fetchInfographs();
});

// Clean up polling intervals when component unmounts
onBeforeUnmount(() => {
  stopAllPolling();
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

