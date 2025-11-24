<template>
  <div class="min-h-screen flex items-start justify-center p-4">
    <div
      :class="[
        'w-full max-w-4xl mt-12 transition-all duration-500 space-y-6',
        isGenerating || hasResults
          ? 'max-w-3xl w-3xl items-start'
          : 'max-w-3xl w-3xl items-center',
      ]"
    >
      <!-- Main Heading -->
      <h1
        :class="[
          'font-bold text-center mb-8 transition-all duration-500',
          isGenerating || hasResults
            ? 'text-3xl md:text-4xl'
            : 'text-3xl md:text-4xl',
        ]"
      >
        Create Infographic from PDF
      </h1>

      <!-- Upload Section (shown when not generating and no results) -->
      <div v-if="!isGenerating && !hasResults" class="space-y-6">
        <!-- PDF Upload Button -->
        <div
          class="bg-card-bg border-2 border-dashed border-card-border rounded-2xl p-12 text-center hover:border-primary-500 transition-colors cursor-pointer"
          @click="triggerFileInput"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleDrop"
          :class="{ 'border-primary-500 bg-primary-500/5': isDragging }"
        >
          <input
            ref="fileInput"
            type="file"
            accept=".pdf"
            class="hidden"
            @change="handleFileSelect"
          />

          <!-- Upload Icon -->
          <div class="mb-4">
            <svg
              class="w-20 h-20 mx-auto text-text-secondary"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.5"
                d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1.5"
                d="M9 13h6m-3-3v6"
              />
            </svg>
          </div>

          <h3 class="text-xl font-semibold text-text-primary mb-2">
            Upload your PDF
          </h3>
          <p class="text-text-secondary text-sm mb-4">
            Drag and drop your PDF file here, or click to browse
          </p>
          <p class="text-text-secondary text-xs">
            Supported format: PDF (Max 10MB)
          </p>
        </div>

        <!-- Infograph Type Selector -->
        <div>
          <div>
            <h2 class="text-lg font-semibold text-text-primary">
              Choose an Infograph Type
            </h2>
            <p class="text-sm text-text-secondary mt-1 mb-4">
              Select an infograph type to start with
            </p>
          </div>
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
            <div
              v-for="infographType in infographTypes"
              :key="infographType.value"
              @click="selectInfographType(infographType)"
              :class="[
                'cursor-pointer bg-card-bg border-2 rounded-lg p-4 flex items-center justify-center flex-col gap-2 transition-all duration-300',
                selectedInfographType.value === infographType.value
                  ? 'border-primary-500 shadow-lg shadow-primary-500/20'
                  : 'border-card-border hover:border-primary-500/50 hover:shadow-md',
              ]"
            >
              <div v-html="infographType.icon"></div>
              <div
                :class="[
                  'text-sm font-medium text-center',
                  selectedInfographType.value === infographType.value
                    ? 'text-primary-500'
                    : 'text-text-primary',
                ]"
              >
                {{ infographType.label }}
              </div>
            </div>
          </div>
        </div>

        <!-- Template Gallery -->
        <div class="space-y-4">
          <div class="text-left">
            <h2 class="text-lg font-semibold text-text-primary">
              Choose a Template
            </h2>
            <p class="text-sm text-text-secondary mt-1">
              Select a template to style your infographic
            </p>
          </div>

          <div
            class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 max-w-6xl mx-auto"
          >
            <div
              v-for="template in templates"
              :key="template.id"
              @click="selectTemplate(template)"
              :class="[
                'group cursor-pointer rounded-lg border-2 transition-all duration-300 overflow-hidden',
                selectedTemplate?.id === template.id
                  ? 'border-primary-500 shadow-lg shadow-primary-500/20'
                  : 'border-card-border hover:border-primary-500/50 hover:shadow-md',
              ]"
            >
              <!-- Template Image Container with Fixed Height -->
              <div
                class="relative bg-background-secondary h-48 flex items-center justify-center p-1"
              >
                <div
                  class="w-full h-full flex items-center justify-center overflow-hidden rounded"
                >
                  <img
                    :src="template.image"
                    :alt="template.name"
                    class="max-w-full max-h-full object-contain"
                    :style="{ aspectRatio: template.aspectRatio }"
                  />
                </div>
                <!-- Selected Indicator -->
                <div
                  v-if="selectedTemplate?.id === template.id"
                  class="absolute top-2 right-2 w-6 h-6 bg-primary-500 rounded-full flex items-center justify-center"
                >
                  <svg
                    class="w-4 h-4 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                    stroke-width="3"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      d="M5 13l4 4L19 7"
                    />
                  </svg>
                </div>
              </div>
              <!-- Template Info -->
              <div class="p-3 bg-card-bg">
                <p
                  :class="[
                    'text-sm font-medium text-center transition-colors',
                    selectedTemplate?.id === template.id
                      ? 'text-primary-500'
                      : 'text-text-primary group-hover:text-primary-500',
                  ]"
                >
                  {{ template.name }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading Skeletons - Generation phase -->
      <div
        v-if="isGenerating"
        class="grid gap-6 transition-all duration-500 mt-8"
        :class="getGridClass()"
      >
        <div
          role="status"
          class="flex flex-col items-center justify-center h-56 max-w-sm bg-background-secondary rounded-lg border border-card-border"
        >
          <div
            class="animate-spin rounded-full h-10 w-10 border-b-2 border-primary-500 mb-3"
          ></div>
          <p class="text-text-primary text-sm font-medium">
            Processing your PDF...
          </p>
          <p class="text-text-secondary text-xs mt-1">
            This may take 30-60 seconds
          </p>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="showError" class="text-red-500 text-center mt-8">
        {{ errorMessage }}
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
              <!-- Image or Processing State -->
              <div
                class="relative overflow-hidden"
                :class="{
                  'cursor-pointer':
                    result.status === 'completed' && result.image,
                }"
                :style="{ aspectRatio: selectedAspectRatio?.value || '9/16' }"
                scale="0.5"
                @click="
                  result.status === 'completed' && result.image
                    ? openImageModal(result)
                    : null
                "
              >
                <!-- Processing State -->
                <div
                  v-if="
                    result.status === 'processing' ||
                    result.status === 'pending'
                  "
                  class="w-full h-64 bg-background-secondary flex flex-col items-center justify-center relative"
                >
                  <!-- Live polling indicator -->
                  <div
                    v-if="pollingIntervals.has(result.id)"
                    class="absolute top-3 right-3 flex items-center gap-2 bg-white/90 px-2 py-1 rounded-full border border-primary-500/30"
                    title="Checking status..."
                  >
                    <span class="text-xs text-primary-600 font-medium"
                      >Live</span
                    >
                    <span
                      class="w-2 h-2 bg-primary-500 rounded-full animate-pulse"
                    ></span>
                  </div>

                  <div
                    class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mb-4"
                  ></div>
                  <p class="text-text-primary text-sm font-medium">
                    Generating your infographic...
                  </p>
                  <p class="text-text-secondary text-xs mt-1">
                    This may take 30-60 seconds
                  </p>
                </div>

                <!-- Failed State -->
                <div
                  v-else-if="result.status === 'failed'"
                  class="w-full h-full bg-red-50 dark:bg-red-900/20 flex flex-col items-center justify-center"
                >
                  <svg
                    class="w-12 h-12 text-red-500 mb-4"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                  <p class="text-red-600 dark:text-red-400 text-sm font-medium">
                    Generation Failed
                  </p>
                  <p class="text-red-500 dark:text-red-500 text-xs mt-1">
                    Please try again
                  </p>
                </div>

                <!-- Completed Image -->
                <template
                  v-else-if="result.status === 'completed' && result.image"
                >
                  <!-- Status Badge for completed -->
                  <div class="absolute top-3 left-3 z-10">
                    <span
                      class="px-2 py-1 rounded-md text-xs font-semibold bg-white text-green-500 border border-green-500 shadow-sm"
                    >
                      ✓ Ready
                    </span>
                  </div>

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
                      <svg
                        class="w-12 h-12 mx-auto mb-2"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                        stroke-width="1.5"
                      >
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607zM10.5 7.5v6m3-3h-6"
                        />
                      </svg>
                      <p class="text-sm">Click to view full size</p>
                    </div>
                  </div>
                </template>
              </div>

              <!-- Action Buttons (only show when completed) -->
              <div
                v-if="result.status === 'completed' && result.image"
                class="p-3 flex gap-2"
              >
                <div class="relative group flex-1">
                  <button
                    @click="handleDownload(result)"
                    class="w-full h-8 bg-primary border border-card-border rounded-md p-2 text-xs flex items-center justify-center gap-1.5"
                  >
                    <svg
                      class="w-3.5 h-3.5"
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
                    <span v-if="numberOfInfographs === 1">Download</span>
                  </button>
                </div>
                <div class="relative group flex-1">
                  <button
                    @click="handleEdit(result)"
                    class="w-full h-8 bg-background-primary border border-card-border rounded-md p-2 text-xs flex items-center justify-center gap-1.5"
                  >
                    <svg
                      class="w-3.5 h-3.5"
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
                    <span v-if="numberOfInfographs === 1">Edit</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Try Another PDF Button -->
        <div class="text-center">
          <button
            @click="resetUpload"
            class="inline-flex items-center gap-2 px-6 py-3 rounded-full border border-primary-500/30 bg-primary-500/10 hover:bg-primary-500/20 transition-colors text-sm font-medium text-primary-500"
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
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L9 8m4-4v12"
              />
            </svg>
            Upload Another PDF
          </button>
        </div>
      </div>
    </div>

    <!-- Image Preview Modal -->
    <Teleport to="body">
      <Transition name="modal">
        <div
          v-if="showImageModal && selectedImage"
          class="fixed inset-0 z-50 flex items-center justify-center p-4"
          @click.self="closeImageModal"
        >
          <!-- Blurred backdrop -->
          <div
            class="absolute inset-0 bg-black/60 backdrop-blur-sm"
            @click="closeImageModal"
          ></div>

          <!-- Modal content -->
          <div
            class="relative max-w-6xl max-h-[90vh] bg-card-bg border border-card-border rounded-lg shadow-2xl overflow-hidden"
          >
            <!-- Close button -->
            <button
              type="button"
              class="absolute top-4 right-4 z-10 text-white hover:text-gray-300 transition-colors p-2 rounded-md bg-black/50 hover:bg-black/70"
              @click="closeImageModal"
              aria-label="Close modal"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
            <!-- Image -->
            <div class="relative">
              <img
                :src="selectedImage.image"
                :alt="selectedImage.name"
                class="w-full h-auto max-h-[80vh] object-contain"
              />
            </div>

            <!-- Action buttons -->
            <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex gap-3">
              <button
                @click="handleDownload(selectedImage)"
                class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-black/70 hover:bg-black/90 text-white transition-colors backdrop-blur-sm text-sm font-medium"
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
                @click="handleEdit(selectedImage)"
                class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-black/70 hover:bg-black/90 text-white transition-colors backdrop-blur-sm text-sm font-medium"
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
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from "vue";
import apiClient from "~/client/apiClient";
import { useToastStore } from "~/stores/toast";

definePageMeta({
  layout: "dashboard",
  middleware: "auth",
});

const toastStore = useToastStore();

// Refs
const fileInput = ref(null);

// State
const isDragging = ref(false);
const selectedFile = ref(null);
const selectedResolution = ref("2K");
const numberOfInfographs = ref(1);
const isGenerating = ref(false);
const hasResults = ref(false);
const results = ref([]);
const showImageModal = ref(false);
const selectedImage = ref(null);
const selectedTemplate = ref(null);
const showError = ref(false);
const errorMessage = ref("");
const pollingIntervals = ref(new Map());

// Infograph types with icons
const infographTypes = ref([
  {
    value: "infograph",
    label: "Infograph",
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><rect width="7" height="9" x="3" y="3" rx="1" /><rect width="7" height="5" x="14" y="3" rx="1" /><rect width="7" height="9" x="14" y="12" rx="1" /><rect width="7" height="5" x="3" y="16" rx="1" /></g></svg>`,
  },
  {
    value: "flowchart",
    label: "Flowchart",
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><rect width="8" height="8" x="3" y="3" rx="2" /><path d="M7 11v4a2 2 0 0 0 2 2h4" /><rect width="8" height="8" x="13" y="13" rx="2" /></g></svg>`,
  },
  {
    value: "mindmap",
    label: "Mindmap",
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M12 5a3 3 0 1 0-5.997.125a4 4 0 0 0-2.526 5.77a4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z" /><path d="M9 13a4.5 4.5 0 0 0 3-4M6.003 5.125A3 3 0 0 0 6.401 6.5m-2.924 4.396a4 4 0 0 1 .585-.396M6 18a4 4 0 0 1-1.967-.516M12 13h4m-4 5h6a2 2 0 0 1 2 2v1M12 8h8m-4 0V5a2 2 0 0 1 2-2" /><circle cx="16" cy="13" r=".5" /><circle cx="18" cy="3" r=".5" /><circle cx="20" cy="21" r=".5" /><circle cx="20" cy="8" r=".5" /></g></svg>`,
  },
  {
    value: "timeline",
    label: "Timeline",
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"><path fill="currentColor" d="M6 17h6v-2H6zm3-4h6v-2H9zm3-4h6V7h-6zM5 21q-.825 0-1.412-.587T3 19V5q0-.825.588-1.412T5 3h14q.825 0 1.413.588T21 5v14q0 .825-.587 1.413T19 21z" /></svg>`,
  },
  {
    value: "organization_chart",
    label: "Organization Chart",
    icon: `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24"><path fill="currentColor" d="M20.01 10.99h-7v-2h-2v2H3.47v4h2v-2h5.54v2h2v-2h5.5v2h2v-4z" /><circle cx="12.01" cy="4.51" r="2.5" fill="currentColor" /><circle cx="4.47" cy="19.49" r="2.5" fill="currentColor" /><circle cx="12.01" cy="19.49" r="2.5" fill="currentColor" /><circle cx="19.51" cy="19.49" r="2.5" fill="currentColor" /></svg>`,
  },
]);
const selectedInfographType = ref(infographTypes.value[0]);

// Mock templates
const templates = ref([
  {
    id: 1,
    name: "Modern Stats",
    image: "https://picsum.photos/seed/template1/400/600",
    aspectRatio: "9/16",
  },
  {
    id: 2,
    name: "Business Dashboard",
    image: "https://picsum.photos/seed/template2/600/400",
    aspectRatio: "16/9",
  },
  {
    id: 3,
    name: "Social Media Post",
    image: "https://picsum.photos/seed/template3/400/400",
    aspectRatio: "1/1",
  },
  {
    id: 4,
    name: "Instagram Story",
    image: "https://picsum.photos/seed/template4/400/500",
    aspectRatio: "4/5",
  },
  {
    id: 5,
    name: "Twitter Header",
    image: "https://picsum.photos/seed/template5/600/286",
    aspectRatio: "21/9",
  },
  {
    id: 6,
    name: "Pinterest Pin",
    image: "https://picsum.photos/seed/template6/400/600",
    aspectRatio: "2/3",
  },
  {
    id: 7,
    name: "Classic Post",
    image: "https://picsum.photos/seed/template7/400/300",
    aspectRatio: "4/3",
  },
  {
    id: 8,
    name: "Wide Banner",
    image: "https://picsum.photos/seed/template8/600/400",
    aspectRatio: "3/2",
  },
]);

const aspectRatios = ref([
  { value: "9:16", label: "9:16" },
  { value: "1:1", label: "1:1" },
  { value: "4:5", label: "4:5" },
  { value: "16:9", label: "16:9" },
  { value: "21:9", label: "21:9" },
  { value: "3:2", label: "3:2" },
  { value: "4:3", label: "4:3" },
  { value: "2:3", label: "2:3" },
]);

const selectedAspectRatio = ref(aspectRatios.value[0]);

// Clean up polling intervals when component unmounts
onBeforeUnmount(() => {
  stopAllPolling();
});

// Methods
const triggerFileInput = () => {
  if (fileInput.value) {
    fileInput.value.click();
  }
};

const handleFileSelect = (event) => {
  const file = event.target.files?.[0];
  if (file) {
    processFile(file);
  }
};

const handleDrop = (event) => {
  isDragging.value = false;
  const file = event.dataTransfer.files?.[0];
  if (file && file.type === "application/pdf") {
    processFile(file);
  } else {
    toastStore.error("Please upload a valid PDF file");
  }
};

const processFile = async (file) => {
  // Validate file size (10MB max)
  if (file.size > 10 * 1024 * 1024) {
    toastStore.error("File size must be less than 10MB");
    return;
  }

  // Validate file type
  if (file.type !== "application/pdf") {
    toastStore.error("Please upload a PDF file");
    return;
  }

  selectedFile.value = file;

  // Immediately upload and generate
  await handleGenerate();
};

const selectTemplate = (template) => {
  selectedTemplate.value = template;
  // Update aspect ratio based on template
  const templateAspectRatio = aspectRatios.value.find(
    (ar) => ar.value === template.aspectRatio.replace("/", ":")
  );
  if (templateAspectRatio) {
    selectedAspectRatio.value = templateAspectRatio;
  }
};

const selectInfographType = (type) => {
  selectedInfographType.value = type;
};

const handleGenerate = async () => {
  if (!selectedFile.value) {
    toastStore.error("Please upload a PDF file first");
    return;
  }

  resetError();
  results.value = [];
  hasResults.value = false;
  isGenerating.value = true;

  try {
    const formData = new FormData();
    formData.append("pdf_file", selectedFile.value);
    formData.append("prompt", ""); // Optional prompt
    formData.append("aspect_ratio", selectedAspectRatio.value.value);
    formData.append("resolution", selectedResolution.value);
    formData.append("number_of_infographs", numberOfInfographs.value);
    formData.append("type", selectedInfographType.value.value);

    const response = await apiClient.post("/infographs/create/pdf/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });

    console.log("API Response:", response.data);

    const infographsData =
      response.data.infograph?.infographs || response.data.infographs;

    if (
      infographsData &&
      Array.isArray(infographsData) &&
      infographsData.length > 0
    ) {
      results.value = infographsData.map((infograph) => ({
        id: infograph.id,
        request_id: infograph.request_id,
        status: infograph.status || "processing",
        image_url: null,
        image: null,
      }));

      isGenerating.value = false;
      hasResults.value = true;

      // Start polling for each infograph
      infographsData.forEach((infograph) => {
        startPollingStatus(infograph.id);
      });
    } else {
      showError.value = true;
      errorMessage.value = "Failed to process PDF. Please try again.";
      isGenerating.value = false;
    }
  } catch (error) {
    console.error("Error generating infographic:", error);
    showError.value = true;
    errorMessage.value =
      error.response?.data?.message ||
      "Failed to process PDF. Please try again.";
    isGenerating.value = false;
    toastStore.error(errorMessage.value);
  }
};

const startPollingStatus = (infographId) => {
  if (pollingIntervals.value.has(infographId)) {
    clearInterval(pollingIntervals.value.get(infographId));
  }

  checkInfographStatus(infographId);

  const interval = setInterval(() => {
    checkInfographStatus(infographId);
  }, 3000);

  pollingIntervals.value.set(infographId, interval);
};

const checkInfographStatus = async (infographId) => {
  try {
    const response = await apiClient.get(`/infographs/status/${infographId}/`);
    const statusData = response.data;

    const infographIndex = results.value.findIndex((r) => r.id === infographId);
    if (infographIndex !== -1) {
      results.value[infographIndex].status = statusData.status;
      results.value[infographIndex].image_url = statusData.image_url;

      if (statusData.image_url) {
        results.value[infographIndex].image = statusData.image_url;
      }
    }

    if (statusData.status === "completed" || statusData.status === "failed") {
      if (pollingIntervals.value.has(infographId)) {
        clearInterval(pollingIntervals.value.get(infographId));
        pollingIntervals.value.delete(infographId);
      }
    }
  } catch (error) {
    console.error(`Error checking status for infograph ${infographId}:`, error);
    if (pollingIntervals.value.has(infographId)) {
      clearInterval(pollingIntervals.value.get(infographId));
      pollingIntervals.value.delete(infographId);
    }
  }
};

const stopAllPolling = () => {
  pollingIntervals.value.forEach((interval) => {
    clearInterval(interval);
  });
  pollingIntervals.value.clear();
};

const resetError = () => {
  showError.value = false;
  errorMessage.value = "";
};

const resetUpload = () => {
  selectedFile.value = null;
  hasResults.value = false;
  results.value = [];
  selectedTemplate.value = null;
  if (fileInput.value) {
    fileInput.value.value = "";
  }
};

const getGridClass = () => {
  if (numberOfInfographs.value === 1) return "grid-cols-1 max-w-sm mx-auto";
  if (numberOfInfographs.value === 2) return "grid-cols-1 md:grid-cols-2";
  if (numberOfInfographs.value === 3)
    return "grid-cols-1 md:grid-cols-2 lg:grid-cols-3";
  return "grid-cols-1 md:grid-cols-2 lg:grid-cols-4";
};

const openImageModal = (result) => {
  selectedImage.value = result;
  showImageModal.value = true;
  if (typeof document !== "undefined") {
    document.body.style.overflow = "hidden";
  }
};

const closeImageModal = () => {
  showImageModal.value = false;
  selectedImage.value = null;
  if (typeof document !== "undefined") {
    document.body.style.overflow = "";
  }
};

const handleDownload = async (result) => {
  try {
    // Use backend proxy endpoint to bypass CORS
    const response = await apiClient.get(`/infographs/download/${result.id}/`, {
      responseType: "blob", // Important: tell axios to handle binary data
    });

    // Create a blob URL from the response data
    const blob = new Blob([response.data], { type: "image/png" });
    const blobUrl = window.URL.createObjectURL(blob);

    // Create a temporary anchor element and trigger download
    const link = document.createElement("a");
    link.href = blobUrl;
    link.download = `infograph-${result.id}.png`;
    document.body.appendChild(link);
    link.click();

    // Clean up
    document.body.removeChild(link);
    window.URL.revokeObjectURL(blobUrl);

    closeImageModal();
  } catch (error) {
    console.error("Error downloading infograph:", error);
    toastStore.error("Failed to download infograph. Please try again.");
    closeImageModal();
  }
};

const handleEdit = (result) => {
  console.log("Editing:", result);
  closeImageModal();
};

// Watch for modal state
watch(showImageModal, (newValue) => {
  if (newValue) {
    document.body.style.overflow = "hidden";
    const handleEscape = (e) => {
      if (e.key === "Escape") {
        closeImageModal();
      }
    };
    document.addEventListener("keydown", handleEscape);
    window._imageModalEscapeHandler = handleEscape;
  } else {
    document.body.style.overflow = "";
    if (window._imageModalEscapeHandler) {
      document.removeEventListener("keydown", window._imageModalEscapeHandler);
      delete window._imageModalEscapeHandler;
    }
  }
});
</script>

<style scoped>
/* Modal transition effects */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .relative,
.modal-leave-active .relative {
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.95);
  opacity: 0;
}
</style>

