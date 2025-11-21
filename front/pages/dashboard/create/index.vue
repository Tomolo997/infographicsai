<template>
  <div class="min-h-screen flex items-start justify-center p-4">
    <div
      :class="[
        'w-full max-w-3xl mt-12 transition-all duration-500 space-y-6',
        isGenerating || hasResults
          ? 'max-w-3xl w-3xl items-start pt-4'
          : 'max-w-3xl w-3xl items-center',
      ]"
    >
      <!-- Main Heading -->
      <h1
        :class="[
          'font-bold text-center mb-8 transition-all duration-500',
          isGenerating || hasResults
            ? 'text-3xl md:text-4xl'
            : 'text-5xl md:text-6xl',
        ]"
      >
        Create Your Infograph
      </h1>

      <!-- Input Container -->
      <div class="bg-card-bg border border-card-border rounded-2xl shadow-sm">
        <!-- Text Area -->
        <div class="py-4 px-6">
          <textarea
            v-model="prompt"
            placeholder="Describe your infograph..."
            :rows="isGenerating || hasResults ? 2 : 4"
            class="w-full bg-transparent h-16 text-text-primary placeholder:text-text-secondary resize-none outline-none text-lg transition-all duration-300"
            :disabled="isGenerating"
            style="line-height: 1.5"
          ></textarea>
        </div>

        <!-- Toolbar -->
        <div class="px-4 pb-2 flex items-center justify-between">
          <div class="flex items-center gap-1">
            <!-- Aspect Ratio Dropdown -->
            <div class="relative group">
              <button
                @click="toggleDropdown('aspectRatio')"
                class="h-9 px-3 inline-flex items-center justify-center gap-2 rounded-md hover:bg-background-secondary transition-colors text-text-primary"
                :disabled="isGenerating"
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
                <span class="text-sm font-medium mt-0.5">{{
                  selectedAspectRatio.label
                }}</span>
              </button>
              <!-- Tooltip -->
              <div
                class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50"
              >
                Aspect Ratio
              </div>
              <!-- Dropdown -->
              <div
                v-if="dropdowns.aspectRatio"
                class="absolute top-full left-0 mt-2 w-80 bg-card-bg border border-card-border rounded-lg shadow-xl z-50 max-h-96 overflow-y-auto"
              >
                <div
                  class="sticky top-0 bg-card-bg border-b border-card-border px-4 py-3 font-semibold text-text-primary text-sm"
                >
                  Aspect Ratio
                </div>
                <div
                  v-for="ratio in aspectRatios"
                  :key="ratio.value"
                  @click="selectAspectRatio(ratio)"
                  :class="[
                    'p-3 cursor-pointer border-b border-card-border last:border-b-0 transition-colors flex items-center justify-between',
                    selectedAspectRatio.value === ratio.value
                      ? 'bg-primary-500/10'
                      : 'hover:bg-background-secondary',
                  ]"
                >
                  <div class="flex-1">
                    <div class="font-medium text-text-primary text-sm">
                      {{ ratio.label }}
                    </div>
                    <div class="text-xs text-text-secondary mt-1">
                      {{ ratio.platforms }}
                    </div>
                  </div>
                  <svg
                    v-if="selectedAspectRatio.value === ratio.value"
                    class="h-5 w-5 text-primary-500 flex-shrink-0 ml-2"
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

            <!-- Resolution Dropdown -->
            <div class="relative group">
              <button
                @click="toggleDropdown('resolution')"
                class="h-9 px-3 inline-flex items-center justify-center gap-2 rounded-md hover:bg-background-secondary transition-colors text-text-primary"
                :disabled="isGenerating"
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
                  <rect width="18" height="18" x="3" y="3" rx="2" ry="2" />
                  <circle cx="9" cy="9" r="2" />
                  <path d="m21 15l-3.086-3.086a2 2 0 0 0-2.828 0L6 21" />
                </svg>
                <span class="text-sm font-medium mt-0.5">{{
                  selectedResolution
                }}</span>
              </button>
              <!-- Tooltip -->
              <div
                class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50"
              >
                Resolution
              </div>
              <!-- Dropdown -->
              <div
                v-if="dropdowns.resolution"
                class="absolute top-full left-0 mt-2 w-40 bg-card-bg border border-card-border rounded-lg shadow-xl z-50"
              >
                <div
                  class="sticky top-0 bg-card-bg border-b border-card-border px-4 py-3 font-semibold text-text-primary text-sm"
                >
                  Resolution
                </div>
                <div
                  v-for="res in resolutions"
                  :key="res"
                  @click="selectResolution(res)"
                  :class="[
                    'p-3 cursor-pointer border-b border-card-border last:border-b-0 text-text-primary text-sm transition-colors flex items-center justify-between',
                    selectedResolution === res
                      ? 'bg-primary-500/10'
                      : 'hover:bg-background-secondary',
                  ]"
                >
                  <span>{{ res }}</span>
                  <svg
                    v-if="selectedResolution === res"
                    class="h-5 w-5 text-primary-500 flex-shrink-0 ml-2"
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

            <!-- Number of Infographs Dropdown -->
            <div class="relative group">
              <button
                @click="toggleDropdown('count')"
                class="h-9 px-3 inline-flex items-center justify-center gap-2 rounded-md hover:bg-background-secondary transition-colors text-text-primary"
                :disabled="isGenerating"
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
                  <rect width="7" height="7" x="3" y="3" rx="1" />
                  <rect width="7" height="7" x="14" y="3" rx="1" />
                  <rect width="7" height="7" x="14" y="14" rx="1" />
                  <rect width="7" height="7" x="3" y="14" rx="1" />
                </svg>
                <span class="text-sm font-medium mt-0.5">{{
                  numberOfInfographs
                }}</span>
              </button>
              <!-- Tooltip -->
              <div
                class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50"
              >
                Number of Infographs
              </div>
              <!-- Dropdown -->
              <div
                v-if="dropdowns.count"
                class="absolute top-full left-0 mt-2 w-48 bg-card-bg border border-card-border rounded-lg shadow-xl z-50"
              >
                <div
                  class="sticky top-0 bg-card-bg border-b border-card-border px-4 py-3 font-semibold text-text-primary text-sm"
                >
                  Number of Infographs
                </div>
                <div
                  v-for="num in [1, 2, 3, 4]"
                  :key="num"
                  @click="selectCount(num)"
                  :class="[
                    'p-3 cursor-pointer border-b border-card-border last:border-b-0 text-text-primary text-sm transition-colors flex items-center justify-between',
                    numberOfInfographs === num
                      ? 'bg-primary-500/10'
                      : 'hover:bg-background-secondary',
                  ]"
                >
                  <span>{{ num }}</span>
                  <svg
                    v-if="numberOfInfographs === num"
                    class="h-5 w-5 text-primary-500 flex-shrink-0 ml-2"
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

            <!-- Blog URL Input -->
            <div class="relative group">
              <button
                v-if="!showBlogInput"
                @click="toggleBlogInput"
                class="h-9 px-3 inline-flex items-center justify-center gap-2 rounded-md hover:bg-background-secondary transition-colors text-text-primary"
                :disabled="isGenerating"
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
                  <path
                    d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"
                  />
                  <path
                    d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"
                  />
                </svg>
                <span class="text-sm font-medium mt-0.5">Blog</span>
              </button>
              <!-- Tooltip -->
              <div
                v-if="!showBlogInput"
                class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50"
              >
                Add Blog URL
              </div>
              <!-- URL Input -->
              <div
                v-if="showBlogInput"
                class="flex items-center gap-2 animate-in"
              >
                <div class="relative">
                  <input
                    v-model="blogUrl"
                    type="url"
                    placeholder="https://example.com/blog-post"
                    class="h-9 px-3 pr-8 bg-background-primary border rounded-md text-text-primary text-sm focus:outline-none focus:border-primary-500 transition-colors min-w-[300px]"
                    :class="[
                      blogUrl && !isValidUrl
                        ? 'border-red-500'
                        : 'border-card-border',
                    ]"
                    @blur="validateUrl"
                    :disabled="isGenerating"
                  />
                  <div class="absolute right-2 top-1/2 -translate-y-1/2">
                    <svg
                      v-if="blogUrl && isValidUrl"
                      class="h-4 w-4 text-green-500"
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
                    <svg
                      v-if="blogUrl && !isValidUrl"
                      class="h-4 w-4 text-red-500"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                      stroke-width="2"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </div>
                </div>
                <button
                  @click="closeBlogInput"
                  class="h-9 w-9 inline-flex items-center justify-center rounded-md hover:bg-background-secondary transition-colors text-text-secondary hover:text-text-primary"
                  :disabled="isGenerating"
                >
                  <svg
                    class="h-4 w-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    stroke-width="2"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- Submit Button -->
          <div class="relative group">
            <button
              @click="handleGenerate"
              :disabled="!prompt.trim() || isGenerating"
              class="h-9 w-9 inline-flex items-center justify-center rounded-lg bg-primary-500 text-white hover:bg-primary-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg
                v-if="!isGenerating"
                class="h-5 w-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 10l7-7m0 0l7 7m-7-7v18"
                />
              </svg>
              <svg
                v-else
                class="w-5 h-5 animate-spin"
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
            </button>
            <!-- Tooltip -->
            <div
              v-if="!isGenerating"
              class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50"
            >
              Generate
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Action Button - Create from Templates -->
      <div v-if="!isGenerating && !hasResults" class="flex justify-center">
        <button
          @click="navigateToTemplates"
          class="inline-flex items-center gap-2 px-6 py-3 rounded-full border border-card-border bg-card-bg hover:bg-background-secondary transition-colors text-sm font-medium text-text-primary"
        >
          <svg
            class="h-4 w-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M4 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1H5a1 1 0 01-1-1v-3zM14 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1h-4a1 1 0 01-1-1v-3z"
            />
          </svg>
          Create from Templates
        </button>
      </div>

      <!-- Loading Skeletons -->
      <div
        v-if="isGenerating"
        class="grid gap-6 transition-all duration-500 mt-8"
        :class="getGridClass()"
      >
        <div
          v-for="i in numberOfInfographs"
          :key="`skeleton-${i}`"
          class="animate-pulse"
        >
          <div
            class="bg-card-bg border border-card-border rounded-lg"
            :style="{ aspectRatio: selectedAspectRatio.value }"
          >
            <div class="w-full h-full bg-background-secondary relative">
              <div
                class="absolute inset-0 flex items-center justify-center text-text-secondary"
              >
                <div class="text-center">
                  <svg
                    class="w-16 h-16 mx-auto mb-4 animate-pulse"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                    />
                  </svg>
                  <p class="text-sm">Generating infograph {{ i }}...</p>
                  <p class="text-xs mt-2 opacity-75">
                    {{ selectedAspectRatio.label }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Results Grid -->
      <div v-if="hasResults && !isGenerating" class="space-y-6 mt-8">
        <div
          class="grid gap-6 transition-all duration-500"
          :class="getGridClass()"
        >
          <div
            v-for="(result, index) in results"
            :key="`result-${index}`"
            class="group"
          >
            <div
              class="bg-card-bg border border-card-border rounded-lg hover:border-primary-500 transition-all duration-300 hover:shadow-xl"
            >
              <!-- Image -->
              <div
                class="relative overflow-hidden"
                :style="{ aspectRatio: selectedAspectRatio.value }"
              >
                <img
                  :src="result.image"
                  :alt="`Generated Infograph ${index + 1}`"
                  class="w-full h-full object-cover"
                />
                <!-- Overlay on hover -->
                <div
                  class="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center"
                >
                  <div class="text-white text-center">
                    <p class="text-sm">{{ selectedAspectRatio.label }}</p>
                    <p class="text-xs mt-1 opacity-75">
                      {{ selectedResolution }}
                    </p>
                  </div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="p-4 flex gap-2">
                <button
                  @click="handleDownload(result)"
                  class="flex-1 btn-secondary text-sm flex items-center justify-center gap-2"
                >
                  <svg
                    class="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                    />
                  </svg>
                  Download
                </button>
                <button
                  @click="handleEdit(result)"
                  class="flex-1 btn-secondary text-sm flex items-center justify-center gap-2"
                >
                  <svg
                    class="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                    />
                  </svg>
                  Edit
                </button>
                <button
                  @click="handleSave(result)"
                  class="flex-1 btn-primary text-sm flex items-center justify-center gap-2"
                >
                  <svg
                    class="w-4 h-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                  Save
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Generate More Button -->
        <div class="text-center">
          <button
            @click="generateMore"
            class="inline-flex items-center gap-2 px-6 py-3 rounded-full border border-card-border bg-card-bg hover:bg-background-secondary transition-colors text-sm font-medium text-text-primary"
          >
            <svg
              class="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 4v16m8-8H4"
              />
            </svg>
            Generate More
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

definePageMeta({
  layout: "dashboard",
  middleware: "auth",
});

// State
const prompt = ref("");
const selectedResolution = ref("2K");
const numberOfInfographs = ref(1);
const isGenerating = ref(false);
const hasResults = ref(false);
const results = ref([]);
const showBlogInput = ref(false);
const blogUrl = ref("");
const isValidUrl = ref(false);

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

const selectedAspectRatio = ref(aspectRatios.value[0]);

const resolutions = ref(["1K", "2K", "4K"]);

// Dropdowns state
const dropdowns = ref({
  aspectRatio: false,
  resolution: false,
  count: false,
});

// Methods
const toggleDropdown = (dropdown) => {
  // Close all dropdowns
  Object.keys(dropdowns.value).forEach((key) => {
    if (key !== dropdown) {
      dropdowns.value[key] = false;
    }
  });
  // Toggle the clicked dropdown
  dropdowns.value[dropdown] = !dropdowns.value[dropdown];
};

const selectAspectRatio = (ratio) => {
  selectedAspectRatio.value = ratio;
  dropdowns.value.aspectRatio = false;
};

const selectResolution = (res) => {
  selectedResolution.value = res;
  dropdowns.value.resolution = false;
};

const selectCount = (num) => {
  numberOfInfographs.value = num;
  dropdowns.value.count = false;
};

const toggleBlogInput = () => {
  showBlogInput.value = true;
};

const closeBlogInput = () => {
  showBlogInput.value = false;
  blogUrl.value = "";
  isValidUrl.value = false;
};

const validateUrl = () => {
  if (!blogUrl.value) {
    isValidUrl.value = false;
    return;
  }

  try {
    const url = new URL(blogUrl.value);
    isValidUrl.value = url.protocol === "http:" || url.protocol === "https:";
  } catch {
    isValidUrl.value = false;
  }
};

// Watch blogUrl for real-time validation
watch(blogUrl, () => {
  validateUrl();
});

const getGridClass = () => {
  if (numberOfInfographs.value === 1) return "grid-cols-1 max-w-2xl mx-auto";
  if (numberOfInfographs.value === 2) return "grid-cols-1 md:grid-cols-2";
  if (numberOfInfographs.value === 3)
    return "grid-cols-1 md:grid-cols-2 lg:grid-cols-3";
  return "grid-cols-1 md:grid-cols-2 lg:grid-cols-4";
};

const handleGenerate = async () => {
  isGenerating.value = true;
  hasResults.value = false;
  results.value = [];

  // Simulate API call with timeout
  await new Promise((resolve) => setTimeout(resolve, 3000));

  // Generate mock results
  const mockResults = [];
  for (let i = 0; i < numberOfInfographs.value; i++) {
    mockResults.push({
      id: `infograph-${Date.now()}-${i}`,
      image: `https://picsum.photos/seed/${Date.now()}-${i}/800/600`,
      prompt: prompt.value,
      aspectRatio: selectedAspectRatio.value.label,
      resolution: selectedResolution.value,
    });
  }

  results.value = mockResults;
  isGenerating.value = false;
  hasResults.value = true;
};

const generateMore = () => {
  hasResults.value = false;
  results.value = [];
  prompt.value = "";
  showBlogInput.value = false;
  blogUrl.value = "";
  isValidUrl.value = false;
};

const handleDownload = (result) => {
  console.log("Downloading:", result);
  // Add download logic here
};

const handleEdit = (result) => {
  console.log("Editing:", result);
  // Add edit logic here
};

const handleSave = (result) => {
  console.log("Saving:", result);
  // Add save logic here
};

const navigateToTemplates = () => {
  navigateTo("/dashboard/create/templates");
};

// Close dropdowns when clicking outside
if (typeof window !== "undefined") {
  window.addEventListener("click", (e) => {
    if (!e.target.closest("button")) {
      Object.keys(dropdowns.value).forEach((key) => {
        dropdowns.value[key] = false;
      });
    }
  });
}
</script>

<style scoped>
/* Custom scrollbar for dropdowns */
.max-h-96::-webkit-scrollbar {
  width: 8px;
}

.max-h-96::-webkit-scrollbar-track {
  background: transparent;
}

.max-h-96::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

.max-h-96::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Animate in for blog input */
.animate-in {
  animation: slideIn 0.2s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-10px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
