<template>
  <div class="dropdown-wrapper" ref="dropdownRef">
    <div class="dropdown-trigger" @click="toggleDropdown">
      <slot name="trigger"></slot>
    </div>
    <transition name="fade">
      <div v-if="isOpen" class="dropdown" :style="dropdownStyle">
        <div>
          <div class="text-[12px] py-3 px-3">{{ title }}</div>
          <div class="w-full h-[1px] bg-gray-200"></div>
        </div>
        <div>
          <div class="tabs mt-2 flex px-4 gap-2 mb-4">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="currentTab = tab.id"
              :class="[
                'px-4 py-2 rounded-md text-[12px] transition-colors',
                currentTab === tab.id
                  ? 'bg-primaryLight text-primary'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
              ]"
            >
              {{ tab.name }}
            </button>
          </div>
        </div>

        <!-- Search Bar -->
        <div
          class="px-4 mb-4"
          v-if="currentTab !== 'color' && currentTab !== 'image'"
        >
          <div class="relative">
            <div
              class="absolute inset-y-0 left-3 flex items-center pointer-events-none"
            >
              <svg
                class="w-4 h-4 text-gray-400"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
              >
                <path
                  d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </div>
            <input
              type="text"
              class="w-full pl-10 pr-4 text-[12px] py-2 rounded-lg border border-gray-200 focus:outline-none focus:border-blue-500"
              :placeholder="searchPlaceholder"
              v-model="searchQuery"
              :disabled="isLoading"
            />
          </div>
        </div>

        <!-- Content based on current tab -->
        <div class="px-4 pb-4">
          <!-- Color Tab -->
          <div v-if="currentTab === 'color'">
            <div class="text-[12px] py-3">Popular</div>
            <div class="grid grid-cols-12 gap-1">
              <button
                v-for="color in grayColors"
                :key="color.hex"
                @click="selectColor(color)"
                class="w-full aspect-square rounded-lg border border-gray-200 hover:border-blue-500 transition-colors"
                :style="{ backgroundColor: color.hex }"
              />
            </div>

            <div class="grid grid-cols-12 gap-1 mt-4">
              <button
                v-for="color in colors"
                :key="color.hex"
                @click="selectColor(color)"
                class="w-full aspect-square rounded-lg border border-gray-200 hover:border-blue-500 transition-colors"
                :style="{ backgroundColor: color.hex }"
              />
            </div>
            <div class="flex flex-col justify-start items-start">
              <div class="text-[12px] text-start py-3">Custom</div>
              <ColorPicker
                v-model="editorStore.backgroundColorCanvas"
              ></ColorPicker>
            </div>
          </div>

          <!-- Pattern Tab -->
          <div
            v-if="currentTab === 'pattern'"
            class="patterns-container"
            style="max-height: 400px; overflow-y: auto"
          >
            <div class="text-[12px] py-3">Popular</div>

            <!-- Loading State -->
            <div
              v-if="isLoading"
              class="min-h-[200px] flex items-center justify-center"
            >
              <div class="flex flex-col items-center gap-3">
                <div
                  class="inline-block animate-spin rounded-full h-8 w-8 border-3 border-gray-300 border-t-blue-600"
                ></div>
                <div class="text-sm text-gray-500">Loading patterns...</div>
              </div>
            </div>

            <!-- Patterns Grid -->
            <div v-else>
              <div class="min-h-[200px]">
                <div class="grid grid-cols-2 gap-3">
                  <button
                    v-for="pattern in patterns"
                    :key="pattern.cdn_url"
                    @click="selectPattern(pattern)"
                    class="aspect-square rounded-lg border border-gray-200 hover:border-blue-500 transition-colors overflow-hidden"
                  >
                    <img
                      :src="pattern.cdn_url"
                      :alt="pattern.title"
                      class="w-full h-full object-cover"
                      @load="handlePatternLoad"
                      @error="handlePatternError"
                    />
                  </button>
                </div>
              </div>

              <!-- Show More Button -->
              <div v-if="pagination.patterns.hasMore" class="text-center py-4">
                <button
                  @click.stop="loadMorePatterns"
                  :disabled="pagination.patterns.loading"
                  class="px-4 py-2 bg-primary text-white rounded-md text-sm hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <div
                    v-if="pagination.patterns.loading"
                    class="flex items-center gap-2"
                  >
                    <div
                      class="inline-block animate-spin rounded-full h-4 w-4 border-2 border-white/50 border-t-white"
                    ></div>
                    Loading...
                  </div>
                  <span v-else>Show More</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Image Tab -->
          <div v-if="currentTab === 'image'">
            <div class="text-[12px] py-3">Upload Image</div>
            <div
              class="border-2 border-dashed border-gray-300 rounded-lg p-8 hover:border-blue-500 transition-colors cursor-pointer"
              @click="triggerFileUpload"
              @dragover.prevent
              @drop.prevent="handleFileDrop"
            >
              <input
                type="file"
                ref="fileInput"
                class="hidden"
                accept="image/*"
                @change="handleFileSelect"
              />
              <div class="text-center text-gray-500">
                <svg
                  class="mx-auto h-12 w-12 mb-4"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
                <p class="mb-1">
                  Drop your image here, or
                  <span class="text-primary">browse</span>
                </p>
                <p class="text-xs text-gray-400">
                  Supports: JPG, PNG, SVG (Max 5MB)
                </p>
              </div>
            </div>

            <!-- Recent Uploads Section -->
            <div v-if="editorStore.recentUploads.length > 0" class="mt-6">
              <div class="text-[12px] py-3">Recent Uploads</div>
              <div class="grid grid-cols-3 gap-3">
                <button
                  v-for="image in editorStore.recentUploads"
                  :key="image.id"
                  @click="selectImage(image)"
                  class="aspect-square rounded-lg border border-gray-200 hover:border-blue-500 transition-colors overflow-hidden"
                >
                  <img
                    :src="image.url"
                    :alt="image.name"
                    class="w-full h-full object-cover"
                  />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { useEditorStore } from "@/stores/editorStore";
import apiClient from "~/services/apiClient";

function debounce(fn, delay) {
  let timeoutId;
  return function (...args) {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    timeoutId = setTimeout(() => {
      fn.apply(this, args);
    }, delay);
  };
}

export default {
  name: "BackgroundDropdown",
  setup() {
    const editorStore = useEditorStore();
    return { editorStore };
  },
  props: {
    title: {
      type: String,
      default: "Add Background",
    },
    positionTop: {
      type: String,
      default: "105%",
    },
    positionLeft: {
      type: String,
      default: "0",
    },
  },
  data() {
    return {
      isOpen: false,
      currentTab: "color",
      searchQuery: "",
      tabs: [
        { id: "color", name: "Color" },
        { id: "pattern", name: "Pattern" },
        { id: "image", name: "Image" },
      ],
      patterns: [],
      pagination: {
        patterns: {
          page: 1,
          totalPages: 1,
          hasMore: true,
          loading: false,
          perPage: 20,
        },
      },
      initialLoadDone: {
        patterns: false,
      },
      isLoading: false,
      loadedItems: {
        patterns: 0,
      },
      grayColors: [
        { name: "White", hex: "#FFFFFF" },
        { name: "Gray 50", hex: "#F9FAFB" },
        { name: "Gray 100", hex: "#F3F4F6" },
        { name: "Gray 200", hex: "#E5E7EB" },
        { name: "Gray 300", hex: "#D1D5DB" },
        { name: "Gray 400", hex: "#9CA3AF" },
        { name: "Gray 500", hex: "#6B7280" },
        { name: "Gray 600", hex: "#4B5563" },
        { name: "Gray 700", hex: "#374151" },
        { name: "Gray 800", hex: "#1F2937" },
        { name: "Gray 900", hex: "#111827" },
        { name: "Black", hex: "#000000" },
      ],
      colors: [
        // Red Shades
        { name: "Red 50", hex: "#FEF2F2" },
        { name: "Red 100", hex: "#FEE2E2" },
        { name: "Red 200", hex: "#FECACA" },
        { name: "Red 300", hex: "#FCA5A5" },
        { name: "Red 400", hex: "#F87171" },
        { name: "Red 500", hex: "#EF4444" },
        { name: "Red 600", hex: "#DC2626" },
        { name: "Red 700", hex: "#B91C1C" },
        { name: "Red 800", hex: "#991B1B" },
        { name: "Red 900", hex: "#7F1D1D" },

        // Orange Shades
        { name: "Orange 50", hex: "#FFF7ED" },
        { name: "Orange 100", hex: "#FFEDD5" },
        { name: "Orange 200", hex: "#FED7AA" },
        { name: "Orange 300", hex: "#FDBA74" },
        { name: "Orange 400", hex: "#FB923C" },
        { name: "Orange 500", hex: "#F97316" },
        { name: "Orange 600", hex: "#EA580C" },
        { name: "Orange 700", hex: "#C2410C" },
        { name: "Orange 800", hex: "#9A3412" },
        { name: "Orange 900", hex: "#7C2D12" },

        // Yellow Shades
        { name: "Yellow 50", hex: "#FEFCE8" },
        { name: "Yellow 100", hex: "#FEF9C3" },
        { name: "Yellow 200", hex: "#FEF08A" },
        { name: "Yellow 300", hex: "#FDE047" },
        { name: "Yellow 400", hex: "#FACC15" },
        { name: "Yellow 500", hex: "#EAB308" },
        { name: "Yellow 600", hex: "#CA8A04" },
        { name: "Yellow 700", hex: "#A16207" },
        { name: "Yellow 800", hex: "#854D0E" },
        { name: "Yellow 900", hex: "#713F12" },

        // Green Shades
        { name: "Green 50", hex: "#F0FDF4" },
        { name: "Green 100", hex: "#DCFCE7" },
        { name: "Green 200", hex: "#BBF7D0" },
        { name: "Green 300", hex: "#86EFAC" },
        { name: "Green 400", hex: "#4ADE80" },
        { name: "Green 500", hex: "#22C55E" },
        { name: "Green 600", hex: "#16A34A" },
        { name: "Green 700", hex: "#15803D" },
        { name: "Green 800", hex: "#166534" },
        { name: "Green 900", hex: "#14532D" },

        // Teal Shades
        { name: "Teal 50", hex: "#F0FDFA" },
        { name: "Teal 100", hex: "#CCFBF1" },
        { name: "Teal 200", hex: "#99F6E4" },
        { name: "Teal 300", hex: "#5EEAD4" },
        { name: "Teal 400", hex: "#2DD4BF" },
        { name: "Teal 500", hex: "#14B8A6" },
        { name: "Teal 600", hex: "#0D9488" },
        { name: "Teal 700", hex: "#0F766E" },
        { name: "Teal 800", hex: "#115E59" },
        { name: "Teal 900", hex: "#134E4A" },

        // Blue Shades
        { name: "Blue 50", hex: "#EFF6FF" },
        { name: "Blue 100", hex: "#DBEAFE" },
        { name: "Blue 200", hex: "#BFDBFE" },
        { name: "Blue 300", hex: "#93C5FD" },
        { name: "Blue 400", hex: "#60A5FA" },
        { name: "Blue 500", hex: "#3B82F6" },
        { name: "Blue 600", hex: "#2563EB" },
        { name: "Blue 700", hex: "#1D4ED8" },
        { name: "Blue 800", hex: "#1E40AF" },
        { name: "Blue 900", hex: "#1E3A8A" },

        // Indigo Shades
        { name: "Indigo 50", hex: "#EEF2FF" },
        { name: "Indigo 100", hex: "#E0E7FF" },
        { name: "Indigo 200", hex: "#C7D2FE" },
        { name: "Indigo 300", hex: "#A5B4FC" },
        { name: "Indigo 400", hex: "#818CF8" },
        { name: "Indigo 500", hex: "#6366F1" },
        { name: "Indigo 600", hex: "#4F46E5" },
        { name: "Indigo 700", hex: "#4338CA" },
        { name: "Indigo 800", hex: "#3730A3" },
        { name: "Indigo 900", hex: "#312E81" },

        // Purple Shades
        { name: "Purple 50", hex: "#FAF5FF" },
        { name: "Purple 100", hex: "#F3E8FF" },
        { name: "Purple 200", hex: "#E9D5FF" },
        { name: "Purple 300", hex: "#D8B4FE" },
        { name: "Purple 400", hex: "#C084FC" },
        { name: "Purple 500", hex: "#A855F7" },
        { name: "Purple 600", hex: "#9333EA" },
        { name: "Purple 700", hex: "#7E22CE" },
        { name: "Purple 800", hex: "#6B21A8" },
        { name: "Purple 900", hex: "#581C87" },

        // Pink Shades
        { name: "Pink 50", hex: "#FDF2F8" },
        { name: "Pink 100", hex: "#FCE7F3" },
        { name: "Pink 200", hex: "#FBCFE8" },
        { name: "Pink 300", hex: "#F9A8D4" },
        { name: "Pink 400", hex: "#F472B6" },
        { name: "Pink 500", hex: "#EC4899" },
        { name: "Pink 600", hex: "#DB2777" },
        { name: "Pink 700", hex: "#BE185D" },
        { name: "Pink 800", hex: "#9D174D" },
        { name: "Pink 900", hex: "#831843" },

        // Rose Shades
        { name: "Rose 50", hex: "#FFF1F2" },
        { name: "Rose 100", hex: "#FFE4E6" },
        { name: "Rose 200", hex: "#FECDD3" },
        { name: "Rose 300", hex: "#FDA4AF" },
        { name: "Rose 400", hex: "#FB7185" },
        { name: "Rose 500", hex: "#F43F5E" },
        { name: "Rose 600", hex: "#E11D48" },
        { name: "Rose 700", hex: "#BE123C" },
        { name: "Rose 800", hex: "#9F1239" },
        { name: "Rose 900", hex: "#881337" },

        // Brown Shades
        { name: "Brown 50", hex: "#FAF8F6" },
        { name: "Brown 100", hex: "#F5EBE4" },
        { name: "Brown 200", hex: "#E7D5C9" },
        { name: "Brown 300", hex: "#D4B7A5" },
        { name: "Brown 400", hex: "#B5947B" },
        { name: "Brown 500", hex: "#96715A" },
        { name: "Brown 600", hex: "#7D5544" },
        { name: "Brown 700", hex: "#63412F" },
        { name: "Brown 800", hex: "#4B2F1D" },
        { name: "Brown 900", hex: "#2C1810" },
      ],
    };
  },
  created() {
    this.debouncedSearch = debounce(this.handleSearch, 300);
  },
  methods: {
    handleFileSelect(event) {
      const file = event.target.files[0];
      if (!file) return;

      // Check file type
      const validTypes = ["image/jpeg", "image/png", "image/webp"];
      if (!validTypes.includes(file.type)) {
        alert("Please select only JPG, PNG, WEBP files");
        event.target.value = ""; // Reset file input
        return;
      }

      // Check file size (5MB limit)
      if (file.size > 5 * 1024 * 1024) {
        alert("File size should not exceed 5MB");
        event.target.value = "";
        return;
      }

      this.handleImageUpload(file);
    },
    handleFileDrop(event) {
      const file = event.dataTransfer.files[0];
      if (file) {
        this.handleImageUpload(file);
      }
    },

    async loadRecentUploads() {
      try {
        const response = await apiClient.get("/infos/recent-uploads/");
        this.editorStore.recentUploads = response.data;
      } catch (error) {
        console.error("Error loading recent uploads:", error);
      }
    },

    async handleImageUpload(file) {
      try {
        const formData = new FormData();
        formData.append("file", file);

        const response = await apiClient.post(
          "/infos/upload-media/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );

        // Set the background image
        this.editorStore.setBackgroundImage(response.data.url, {
          size: "cover",
          opacity: 1,
          position: "center",
        });

        // Refresh recent uploads
        await this.loadRecentUploads();

        this.isOpen = false;
      } catch (error) {
        console.error("Error uploading image:", error);
        alert("Failed to upload image. Please try again.");
      }
    },

    selectImage(image) {
      this.editorStore.setBackgroundImage(image.url);
      this.isOpen = false;
    },

    async getPatterns() {
      try {
        this.isLoading = true;
        this.loadedItems.patterns = 0;
        this.pagination.patterns.loading = true;

        const response = await apiClient.get("/icons/patterns/", {
          params: {
            page: 1,
            per_page: this.pagination.patterns.perPage,
            search: this.searchQuery,
          },
        });

        if (response.data) {
          this.patterns = response.data.patterns || [];
          this.pagination.patterns.page = response.data.page || 1;
          this.pagination.patterns.totalPages = response.data.total_pages || 1;
          this.pagination.patterns.hasMore = response.data.has_next || false;
        } else {
          this.patterns = [];
          this.pagination.patterns.hasMore = false;
        }

        this.initialLoadDone.patterns = true;
      } catch (error) {
        console.error("Error loading patterns:", error);
        this.patterns = [];
        this.pagination.patterns.hasMore = false;
      } finally {
        this.pagination.patterns.loading = false;
        this.isLoading = false;
      }
    },

    async loadMorePatterns() {
      if (this.pagination.patterns.loading || !this.pagination.patterns.hasMore)
        return;

      try {
        this.pagination.patterns.loading = true;

        const response = await apiClient.get("/icons/patterns/", {
          params: {
            page: this.pagination.patterns.page + 1,
            per_page: this.pagination.patterns.perPage,
            search: this.searchQuery,
          },
        });

        if (response.data && Array.isArray(response.data.patterns)) {
          this.patterns = [...this.patterns, ...response.data.patterns];
          this.pagination.patterns.page =
            response.data.page || this.pagination.patterns.page + 1;
          this.pagination.patterns.totalPages =
            response.data.total_pages || this.pagination.patterns.totalPages;
          this.pagination.patterns.hasMore = response.data.has_next || false;
        } else {
          this.pagination.patterns.hasMore = false;
        }
      } catch (error) {
        console.error("Error loading more patterns:", error);
        this.pagination.patterns.hasMore = false;
      } finally {
        this.pagination.patterns.loading = false;
      }
    },

    handlePatternLoad() {
      this.loadedItems.patterns++;
      if (this.loadedItems.patterns === this.patterns.length) {
        this.isLoading = false;
      }
    },

    handlePatternError() {
      this.loadedItems.patterns++;
      if (this.loadedItems.patterns === this.patterns.length) {
        this.isLoading = false;
      }
    },

    async handleSearch() {
      if (this.currentTab === "pattern") {
        this.pagination.patterns.page = 1;
        this.pagination.patterns.hasMore = true;
        this.patterns = [];
        await this.getPatterns();
      }
    },

    toggleDropdown() {
      this.isOpen = !this.isOpen;
      if (
        this.isOpen &&
        this.currentTab === "pattern" &&
        !this.initialLoadDone.patterns
      ) {
        this.getPatterns();
      }
    },

    closeDropdown(event) {
      if (
        this.$refs.dropdownRef &&
        !this.$refs.dropdownRef.contains(event.target) // ... Previous template and initial script code remains the same ...
      ) {
        this.isOpen = false;
      }
    },

    selectColor(color) {
      this.editorStore.setBackgroundColor(color.hex);
      this.isOpen = false;
    },

    selectPattern(pattern) {
      this.editorStore.setBackgroundPattern(pattern.cdn_url);
      this.isOpen = false;
    },

    triggerFileUpload() {
      this.$refs.fileInput.click();
    },
  },
  computed: {
    dropdownStyle() {
      return {
        top: this.positionTop,
        left: this.positionLeft,
      };
    },
    searchPlaceholder() {
      if (this.currentTab === "pattern") {
        return "Search Patterns";
      }
      return "";
    },
  },
  mounted() {
    document.addEventListener("click", this.closeDropdown);
    this.loadRecentUploads(); // Load recent uploads when component mounts
  },
  beforeUnmount() {
    document.removeEventListener("click", this.closeDropdown);
  },
  watch: {
    searchQuery: {
      handler() {
        this.debouncedSearch();
      },
    },
    currentTab: {
      immediate: true,
      handler(newTab) {
        if (this.isOpen) {
          if (newTab === "pattern" && !this.initialLoadDone.patterns) {
            this.getPatterns();
          }
        }
      },
    },
    isOpen: {
      handler(opened) {
        if (opened) {
          if (!this.initialLoadDone.patterns && this.currentTab === "pattern") {
            this.getPatterns();
          }
        }
      },
    },
  },
};
</script>

<style scoped>
.dropdown-wrapper {
  position: relative;
  display: inline-block;
}

.dropdown {
  width: 400px;
  position: absolute;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>