<template>
  <div class="min-h-screen p-6">
    <!-- Header Section -->
    <div class="flex items-start justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-primary mb-2">Templates</h1>
        <p class="text-md text-text-secondary">
          Browse and manage your template collection
        </p>
      </div>
      <button
        @click="handleAddTemplate"
        class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-primary-500 text-white transition-colors text-sm font-medium"
      >
        <svg
          class="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          stroke-width="2"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M12 4v16m8-8H4"
          />
        </svg>
        Add Template
      </button>
    </div>

    <!-- Filter Section -->
    <div class="mb-6 flex items-center gap-4">
      <!-- Ownership Filter Tabs -->
      <div class="flex rounded-lg border border-card-border overflow-hidden">
        <button
          @click="selectedOwnershipFilter = 'all'"
          :class="[
            'px-4 py-2 text-sm font-medium transition-colors',
            selectedOwnershipFilter === 'all'
              ? 'bg-primary-500 text-white'
              : 'bg-card-bg text-text-primary hover:bg-background-secondary',
          ]"
        >
          All Templates
        </button>
        <button
          @click="selectedOwnershipFilter = 'mine'"
          :class="[
            'px-4 py-2 text-sm font-medium transition-colors border-l border-card-border',
            selectedOwnershipFilter === 'mine'
              ? 'bg-primary-500 text-white'
              : 'bg-card-bg text-text-primary hover:bg-background-secondary',
          ]"
        >
          My Templates
        </button>
        <button
          @click="selectedOwnershipFilter = 'public'"
          :class="[
            'px-4 py-2 text-sm font-medium transition-colors border-l border-card-border',
            selectedOwnershipFilter === 'public'
              ? 'bg-primary-500 text-white'
              : 'bg-card-bg text-text-primary hover:bg-background-secondary',
          ]"
        >
          Public Templates
        </button>
      </div>

      <!-- Aspect Ratio Filter -->
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

    <!-- Templates Grid - Scrollable -->
    <div
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
          v-for="template in filteredTemplates"
          :key="template.id"
          @click="openTemplateModal(template)"
          class="group cursor-pointer rounded-lg border-2 transition-all duration-300 overflow-hidden border-card-border hover:border-primary-500/50 hover:shadow-md"
        >
          <!-- Template Image Container -->
          <div
            class="relative bg-background-secondary h-48 flex items-center justify-center p-1"
          >
            <div
              class="w-full h-full flex items-center justify-center overflow-hidden rounded"
            >
              <img
                :src="template.image_url"
                :alt="template.name"
                class="max-w-full max-h-full object-contain"
              />
            </div>
          </div>
          <!-- Template Info -->
          <div class="p-3 bg-card-bg">
            <p
              class="text-sm font-medium text-center text-text-primary group-hover:text-primary-500 transition-colors"
            >
              {{ template.name }}
            </p>
            <p class="text-xs text-text-secondary text-center mt-1">
              {{ getAspectRatioLabel(template.aspect_ratio) }}
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Template Modal -->
    <Modal
      :is-open="showTemplateModal"
      :title="selectedTemplate?.name || ''"
      :subtitle="
        selectedTemplate
          ? getAspectRatioLabel(selectedTemplate.aspect_ratio)
          : ''
      "
      max-width="max-w-4xl"
      @close="closeTemplateModal"
    >
      <template #body>
        <div v-if="selectedTemplate" class="space-y-4">
          <!-- Template Preview -->
          <div
            class="relative bg-background-secondary rounded-lg overflow-hidden"
          >
            <div class="w-full flex items-center justify-center p-8">
              <img
                :src="selectedTemplate.image_url"
                :alt="selectedTemplate.name"
                class="max-w-full max-h-[60vh] object-contain rounded"
              />
            </div>
          </div>
          <!-- Template Details -->
          <div class="space-y-2">
            <div>
              <span class="text-sm font-semibold text-text-primary"
                >Aspect Ratio:</span
              >
              <span class="text-sm text-text-secondary ml-2">
                {{ getAspectRatioLabel(selectedTemplate.aspect_ratio) }}
              </span>
            </div>
            <div>
              <span class="text-sm font-semibold text-text-primary"
                >Platforms:</span
              >
              <span class="text-sm text-text-secondary ml-2">
                {{ getPlatformsForAspectRatio(selectedTemplate.aspect_ratio) }}
              </span>
            </div>
            <div>
              <span class="text-sm font-semibold text-text-primary"
                >Ownership:</span
              >
              <span
                v-if="selectedTemplate.is_owner"
                class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-primary-500/10 text-primary-500 ml-2"
              >
                Your Template
              </span>
              <span
                v-else-if="selectedTemplate.is_public"
                class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-500/10 text-green-500 ml-2"
              >
                Public Template
              </span>
            </div>
          </div>
        </div>
      </template>
      <template #cta>
        <div class="flex gap-3 justify-end">
          <button
            @click="handleUseTemplate"
            class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-primary-500 text-white hover:bg-primary-600 transition-colors text-sm font-medium"
          >
            Use Template
          </button>
          <button
            v-if="selectedTemplate?.is_owner"
            @click="handleEditTemplate"
            class="inline-flex items-center gap-2 px-4 py-2 rounded-lg border border-card-border bg-card-bg hover:bg-background-secondary transition-colors text-sm font-medium text-text-primary"
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
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
            Edit
          </button>
        </div>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import Modal from "~/components/Modal.vue";
import apiClient from "~/client/apiClient";

definePageMeta({
  layout: "dashboard",
  middleware: "auth",
});

// State
const showAspectRatioDropdown = ref(false);
const selectedAspectRatioFilter = ref(null);
const selectedOwnershipFilter = ref("all"); // 'all', 'mine', 'public'
const showTemplateModal = ref(false);
const selectedTemplate = ref(null);

// Mock templates with different aspect ratios
const templates = ref([]);

// Fetch templates from API
const fetchTemplates = async () => {
  try {
    const response = await apiClient.get("/infographs/templates/list/");
    templates.value = response.data;
  } catch (error) {
    console.error("Error fetching templates:", error);
  }
};

// Aspect Ratios with social media recommendations
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
const filteredTemplates = computed(() => {
  let filtered = templates.value;

  // Filter by ownership
  if (selectedOwnershipFilter.value === "mine") {
    filtered = filtered.filter((t) => t.is_owner);
  } else if (selectedOwnershipFilter.value === "public") {
    filtered = filtered.filter((t) => t.is_public && !t.is_owner);
  }

  // Filter by aspect ratio
  if (selectedAspectRatioFilter.value) {
    const selectedRatio = aspectRatios.value.find(
      (r) => r.label === selectedAspectRatioFilter.value
    );
    if (selectedRatio) {
      filtered = filtered.filter((t) => t.aspectRatio === selectedRatio.value);
    }
  }

  return filtered;
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
  console.log("Aspect ratio:", aspectRatio);
  const ratio = aspectRatios.value.find((r) => r.value === aspectRatio);
  return ratio ? ratio.label : aspectRatio;
};

const getPlatformsForAspectRatio = (aspectRatio) => {
  const ratio = aspectRatios.value.find((r) => r.value === aspectRatio);
  return ratio ? ratio.platforms : "N/A";
};

const openTemplateModal = (template) => {
  selectedTemplate.value = template;
  showTemplateModal.value = true;
};

const closeTemplateModal = () => {
  showTemplateModal.value = false;
  selectedTemplate.value = null;
};

const handleAddTemplate = () => {
  console.log("Add template clicked");
  // Add logic to navigate to template creation page
};

const handleUseTemplate = () => {
  if (selectedTemplate.value) {
    navigateTo(`/dashboard/?templateId=${selectedTemplate.value.id}`);
  }
  closeTemplateModal();
};

const handleEditTemplate = () => {
  console.log("Edit template:", selectedTemplate.value);
  // Add logic to edit the template
  closeTemplateModal();
};

// Close dropdown when clicking outside
if (typeof window !== "undefined") {
  window.addEventListener("click", (e) => {
    if (!e.target.closest(".relative")) {
      showAspectRatioDropdown.value = false;
    }
  });
}

onMounted(() => {
  console.log("Fetching templates");
  fetchTemplates();
});
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
