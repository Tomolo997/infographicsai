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
        Create Your Infograph
      </h1>

      <!-- Input Container -->
      <div class="bg-card-bg border border-card-border rounded-2xl shadow-sm">
        <!-- Text Area -->
        <div class="py-4 px-6">
          <textarea
            ref="textareaRef"
            v-model="prompt"
            placeholder="Content of your infograph..."
            class="w-full bg-transparent text-text-primary placeholder:text-text-secondary resize-none outline-none text-lg transition-all duration-300"
            :disabled="isGenerating"
            style="
              line-height: 1.5;
              min-height: 60px;
              max-height: 300px;
              overflow-y: auto;
            "
            @input="autoResize"
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
                class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded whitespace-nowrap opacity-0 transition-opacity pointer-events-none z-50"
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
                    'p-3 cursor-pointer border-b border-card-border last:border-b-0 transition-colors flex items-center gap-2',
                    selectedAspectRatio.value === ratio.value
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
                    v-if="selectedAspectRatio.value === ratio.value"
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
                class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded whitespace-nowrap opacity-0 transition-opacity pointer-events-none z-50"
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
                    'p-3 cursor-pointer border-b border-card-border last:border-b-0 text-text-primary text-sm transition-colors flex items-center gap-2',
                    selectedResolution === res
                      ? 'bg-primary-500/10'
                      : 'hover:bg-background-secondary',
                  ]"
                >
                  <span class="flex-1">{{ res }}</span>
                  <svg
                    v-if="selectedResolution === res"
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
                class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded whitespace-nowrap opacity-0 transition-opacity pointer-events-none z-50"
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
                    'p-3 cursor-pointer border-b border-card-border last:border-b-0 text-text-primary text-sm transition-colors flex items-center gap-2',
                    numberOfInfographs === num
                      ? 'bg-primary-500/10'
                      : 'hover:bg-background-secondary',
                  ]"
                >
                  <span class="flex-1">{{ num }}</span>
                  <svg
                    v-if="numberOfInfographs === num"
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
                    class="h-9 px-3 pr-8 bg-background-primary border rounded-md text-text-primary text-sm focus:outline-none focus:border-primary-500 transition-colors min-w-[200px]"
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

            <div class="relative group">
              <!-- Hidden file input -->
              <input
                id="file-upload-input"
                type="file"
                accept="image/*"
                class="hidden"
                @change="handleFileUpload"
                :disabled="isGenerating"
              />

              <!-- Upload button (shown when no file uploaded) -->
              <button
                v-if="!uploadedFilePreview"
                @click="toggleFileUpload"
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
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                  <polyline points="17 8 12 3 7 8" />
                  <line x1="12" y1="3" x2="12" y2="15" />
                </svg>
                <span class="text-sm font-medium mt-0.5">Own Template</span>
              </button>

              <!-- Tooltip -->
              <div
                v-if="!uploadedFilePreview"
                class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded whitespace-nowrap opacity-0 transition-opacity pointer-events-none z-50"
              >
                Own Template
              </div>

              <!-- File preview (shown when file is uploaded) -->
              <div
                v-if="uploadedFilePreview"
                class="flex items-center gap-2 animate-in"
              >
                <div class="relative">
                  <div
                    class="h-9 px-3 pr-8 bg-background-primary border border-card-border rounded-md flex items-center gap-2"
                  >
                    <img
                      :src="uploadedFilePreview"
                      alt="Uploaded preview"
                      class="h-6 w-6 object-cover rounded"
                    />
                    <span
                      class="text-sm text-text-primary truncate max-w-[150px]"
                    >
                      {{ uploadedFile?.name }}
                    </span>
                  </div>
                </div>
                <button
                  @click="removeUploadedFile"
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

            <!-- Selected Template Badge -->
            <div v-if="selectedTemplate" class="relative group">
              <button
                @click="deselectTemplate"
                class="h-9 px-3 inline-flex items-center justify-center gap-2 rounded-md bg-primary-500/10 border border-primary-500/30 hover:bg-primary-500/20 transition-colors text-text-primary"
                :disabled="isGenerating"
              >
                <svg
                  class="h-4 w-4 text-primary-500"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path
                    d="M4 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1H5a1 1 0 01-1-1v-3zM14 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1h-4a1 1 0 01-1-1v-3z"
                  />
                </svg>
                <span class="text-sm font-medium mt-0.5">{{
                  selectedTemplate.name
                }}</span>
                <svg
                  class="h-3 w-3 text-text-secondary"
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
              <!-- Tooltip -->
              <div
                class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none z-50"
              >
                Click to remove template
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
              class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 bg-gray-900 text-white text-xs rounded whitespace-nowrap opacity-0 transition-opacity pointer-events-none z-50"
            >
              Generate
            </div>
          </div>
        </div>
      </div>

      <!-- Template Gallery -->
      <div v-if="!isGenerating && !hasResults" class="space-y-4">
        <div class="text-center">
          <h2 class="text-lg font-semibold text-text-primary">
            Choose a Template
          </h2>
          <p class="text-sm text-text-secondary mt-1">
            Select a template to start with or create from scratch
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
              <!-- Image -->
              <div
                class="relative overflow-hidden cursor-pointer"
                :style="{ aspectRatio: selectedAspectRatio.value }"
                scale="0.5"
                @click="openImageModal(result)"
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
                    <p class="text-xs mt-1 opacity-75">
                      {{ selectedAspectRatio.label }} • {{ selectedResolution }}
                    </p>
                  </div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="p-3 flex gap-2">
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
                  <div
                    v-if="numberOfInfographs > 1"
                    class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-gray-900 text-white text-xs rounded whitespace-nowrap opacity-0 transition-opacity pointer-events-none z-50"
                  >
                    Download
                  </div>
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
                  <div
                    v-if="numberOfInfographs > 1"
                    class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-gray-900 text-white text-xs rounded whitespace-nowrap opacity-0 transition-opacity pointer-events-none z-50"
                  >
                    Edit
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Try Another Template Button -->
        <div class="text-center">
          <button
            @click="tryAnotherTemplate"
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
                d="M4 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1H5a1 1 0 01-1-1v-3zM14 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1h-4a1 1 0 01-1-1v-3z"
              />
            </svg>
            Try Another Template
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
import { ref, watch, onMounted, nextTick } from "vue";
import apiClient from "~/client/apiClient";
definePageMeta({
  layout: "dashboard",
  middleware: "auth",
});

const route = useRoute();

// Refs
const textareaRef = ref(null);

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
const showImageModal = ref(false);
const selectedImage = ref(null);
const selectedTemplate = ref(null);
const showFileUpload = ref(false);
const uploadedFile = ref(null);
const uploadedFilePreview = ref(null);
const showError = ref(false);
const errorMessage = ref("");

// Mock templates with different aspect ratios
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

// Aspect Ratios with social media recommendations
const aspectRatios = ref([
  {
    value: "9:16",
    label: "9:16",
    platforms: "Instagram Story, TikTok, Facebook Story",
  },
  {
    value: "1:1",
    label: "1:1",
    platforms: "Instagram Post, Facebook Post, LinkedIn Post",
  },
  {
    value: "4:5",
    label: "4:5",
    platforms: "Instagram Portrait, Facebook Feed",
  },
  {
    value: "16:9",
    label: "16:9",
    platforms: "YouTube Thumbnail, LinkedIn Cover, Twitter Header",
  },
  {
    value: "21:9",
    label: "21:9",
    platforms: "Facebook Cover, Twitter Header (X Header)",
  },
  {
    value: "3:2",
    label: "3:2",
    platforms: "Twitter Post (X Post), General Photography",
  },
  {
    value: "4:3",
    label: "4:3",
    platforms: "Facebook Post, Classic Photography",
  },
  {
    value: "2:3",
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

const selectTemplate = (template) => {
  selectedTemplate.value = template;
  // Remove own template if one is uploaded
  if (uploadedFilePreview.value) {
    removeUploadedFile();
  }
  // Focus back on the textarea
  setTimeout(() => {
    if (textareaRef.value) {
      textareaRef.value.focus();
    }
  }, 100);
};

// Pre-select template from query parameter
onMounted(() => {
  const templateId = route.query.templateId;
  if (templateId) {
    const templateIdNum = parseInt(templateId, 10);
    const template = templates.value.find((t) => t.id === templateIdNum);
    if (template) {
      selectTemplate(template);
    }
  }
  // Initialize textarea height
  nextTick(() => {
    autoResize();
  });
});

const deselectTemplate = () => {
  selectedTemplate.value = null;
};

const toggleFileUpload = () => {
  showFileUpload.value = true;
  // Trigger file input
  const fileInput = document.getElementById("file-upload-input");
  if (fileInput) {
    fileInput.click();
  }
};

const autoResize = () => {
  const textarea = textareaRef.value;
  if (textarea) {
    // Reset height to auto to get the correct scrollHeight
    textarea.style.height = "auto";
    // Set the height to match the content
    textarea.style.height = `${textarea.scrollHeight}px`;
  }
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

// Watch prompt to auto-resize textarea
watch(prompt, () => {
  nextTick(() => {
    autoResize();
  });
});

// Watch for modal state to handle body overflow and keyboard events
watch(showImageModal, (newValue) => {
  if (newValue) {
    document.body.style.overflow = "hidden";
    // Add escape key listener
    const handleEscape = (e) => {
      if (e.key === "Escape") {
        closeImageModal();
      }
    };
    document.addEventListener("keydown", handleEscape);
    // Store the handler so we can remove it later
    window._imageModalEscapeHandler = handleEscape;
  } else {
    document.body.style.overflow = "";
    // Remove escape key listener
    if (window._imageModalEscapeHandler) {
      document.removeEventListener("keydown", window._imageModalEscapeHandler);
      delete window._imageModalEscapeHandler;
    }
  }
});

const getGridClass = () => {
  if (numberOfInfographs.value === 1) return "grid-cols-1 max-w-sm mx-auto";
  if (numberOfInfographs.value === 2) return "grid-cols-1 md:grid-cols-2";
  if (numberOfInfographs.value === 3)
    return "grid-cols-1 md:grid-cols-2 lg:grid-cols-3";
  return "grid-cols-1 md:grid-cols-2 lg:grid-cols-4";
};

const handleGenerate = async () => {
  resetError();
  console.log("handleGenerate");
  isGenerating.value = true;
  hasResults.value = false;
  results.value = [];

  if (
    !prompt.value ||
    !selectedAspectRatio.value ||
    !selectedResolution.value ||
    !numberOfInfographs.value
  ) {
    return;
  }

  if (uploadedFilePreview.value) {
    try {
      const response = await apiClient.post(
        "/infographs/create-own-template/",
        {
          prompt: prompt.value,
          blog_url: blogUrl.value,
          aspect_ratio: selectedAspectRatio.value.value,
          resolution: selectedResolution.value,
          number_of_infographs: numberOfInfographs.value,
          front_image: uploadedFilePreview.value,
        }
      );
      results.value = response.data;
      isGenerating.value = false;
      hasResults.value = true;
      return;
    } catch (error) {
      console.error(error);
    }
  }

  if (selectedTemplate.value) {
    try {
      const response = await apiClient.post("/infographs/create-template/", {
        prompt: prompt.value,
        blog_url: blogUrl.value,
        aspect_ratio: selectedAspectRatio.value.value,
        resolution: selectedResolution.value,
        number_of_infographs: numberOfInfographs.value,
        selected_template: selectedTemplate.value.id,
      });
      results.value = response.data;
      isGenerating.value = false;
      hasResults.value = true;
      return;
    } catch (error) {
      console.error(error);
    }
  }

  try {
    const response = await apiClient.post("/infographs/create/", {
      prompt: prompt.value,
      blog_url: blogUrl.value || null,
      aspect_ratio: selectedAspectRatio.value.value,
      resolution: selectedResolution.value,
      number_of_infographs: numberOfInfographs.value,
    });
    results.value = response.data;
    isGenerating.value = false;
    hasResults.value = true;
    return;
  } catch (error) {
    showError.value = true;
    if (error.response.data.errors.blog_url) {
      errorMessage.value = errorMapping.blog_url;
    } else if (error.response.data.errors.aspect_ratio) {
      errorMessage.value = errorMapping.aspect_ratio;
    } else if (error.response.data.errors.resolution) {
      errorMessage.value = errorMapping.resolution;
    } else if (error.response.data.errors.number_of_infographs) {
      errorMessage.value = errorMapping.number_of_infographs;
    } else if (error.response.data.errors.message) {
      errorMessage.value = error.response.data.errors.message;
    } else {
      errorMessage.value = "Please check your inputs and try again";
    }
    isGenerating.value = false;
    hasResults.value = true;
    return;
  }
};

const errorMapping = {
  blog_url: "Please enter a valid blog URL",
  aspect_ratio: "Please select a valid aspect ratio",
  resolution: "Please select a valid resolution",
  number_of_infographs: "Please enter a valid number of infographs",
  prompt: "Please enter a valid prompt",
};

const resetError = () => {
  showError.value = false;
  errorMessage.value = "";
};

const tryAnotherTemplate = () => {
  hasResults.value = false;
  results.value = [];
  selectedTemplate.value = null;
  // Keep the prompt, blog URL, and other settings
  // Focus back on textarea
  setTimeout(() => {
    if (textareaRef.value) {
      textareaRef.value.focus();
    }
  }, 100);
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

const handleDownload = (result) => {
  console.log("Downloading:", result);
  // Add download logic here
  closeImageModal();
};

const handleEdit = (result) => {
  console.log("Editing:", result);
  // Add edit logic here
  closeImageModal();
};

const handleSave = (result) => {
  console.log("Saving:", result);
  // Add save logic here
};

const navigateToScratch = () => {
  navigateTo("/dashboard/create");
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

const handleFileUpload = (event) => {
  const file = event.target.files?.[0];
  if (file && file.type.startsWith("image/")) {
    uploadedFile.value = file;
    // Deselect gallery template if one is selected
    if (selectedTemplate.value) {
      selectedTemplate.value = null;
    }
    // Create preview URL
    const reader = new FileReader();
    reader.onload = (e) => {
      uploadedFilePreview.value = e.target.result;
    };
    reader.readAsDataURL(file);
    showFileUpload.value = true;
  }
};

const removeUploadedFile = () => {
  uploadedFile.value = null;
  uploadedFilePreview.value = null;
  showFileUpload.value = false;
  // Reset file input
  const fileInput = document.getElementById("file-upload-input");
  if (fileInput) {
    fileInput.value = "";
  }
};
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
