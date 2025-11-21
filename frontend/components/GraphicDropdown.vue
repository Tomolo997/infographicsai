<template>
  <div class="dropdown-wrapper" ref="dropdownRef">
    <div class="dropdown-trigger" @click="toggleDropdown">
      <slot name="trigger"></slot>
    </div>
    <transition name="fade">
      <div v-if="isOpen" class="dropdown" :style="dropdownStyle">
        <!-- Header and tabs -->
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
        <div class="px-4 mb-4" v-if="currentTab !== 'upload'">
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
              ref="searchInput"
            />
          </div>
        </div>

        <!-- Content based on current tab -->
        <div class="px-4 pb-4">
          <div
            v-if="currentTab === 'icons'"
            class="icons-container"
            style="max-height: 400px; overflow-y: auto"
          >
            <div class="text-[12px] py-3">Popular</div>

            <!-- Icon Type Filter -->
            <div class="flex gap-2 mb-4">
              <button
                v-for="type in iconTypes"
                :key="type.id"
                @click="selectedIconType = type.id"
                :class="[
                  'px-3 py-1.5 rounded-md text-[12px] transition-colors',
                  selectedIconType === type.id
                    ? 'bg-primaryLight text-primary'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200',
                ]"
              >
                {{ type.name }}
              </button>
            </div>

            <!-- Loading State -->
            <div
              v-if="isLoading"
              class="min-h-[200px] flex items-center justify-center"
            >
              <div class="flex flex-col items-center gap-3">
                <div
                  class="inline-block animate-spin rounded-full h-8 w-8 border-3 border-gray-300 border-t-blue-600"
                ></div>
                <div class="text-sm text-gray-500">Loading icons...</div>
              </div>
            </div>

            <!-- Icons Grid -->
            <div v-else>
              <div class="min-h-[200px]">
                <div class="grid grid-cols-6 gap-1">
                  <img
                    v-for="icon in popularIcons"
                    :key="icon.cdn_url"
                    :src="icon.cdn_url"
                    @click="addIconElement(icon.cdn_url, 'icon', selectedIconType)"
                    class="aspect-square w-full h-full cursor-pointer rounded hover:bg-gray-50"
                    @load="handleIconLoad"
                    @error="handleIconError"
                  />
                </div>
              </div>

              <!-- Show More Button -->
              <div v-if="pagination.icons.hasMore" class="text-center py-4">
                <button
                  @click.stop="loadMoreIcons"
                  :disabled="pagination.icons.loading"
                  class="px-4 py-2 bg-primary text-white rounded-md text-sm hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <div
                    v-if="pagination.icons.loading"
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

              <!-- End of results message -->
              <div
                v-if="
                  !pagination.icons.hasMore &&
                  popularIcons.length > 0 &&
                  !isLoading
                "
                class="text-center text-gray-500 text-sm py-4"
              >
                No more icons to load
              </div>
            </div>
          </div>

          <div
            v-if="currentTab === 'vectors'"
            class="icons-container"
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
                <div class="text-sm text-gray-500">Loading vectors...</div>
              </div>
            </div>

            <!-- Vectors Grid -->
            <div v-else>
              <div class="min-h-[200px]">
                <div class="grid grid-cols-2 gap-1">
                  <img
                    v-for="vector in popularVectors"
                    :key="vector.cdn_url"
                    :src="vector.cdn_url"
                    @click="addIconElement(vector.cdn_url, 'vector')"
                    class="aspect-square cursor-pointer rounded hover:bg-gray-50"
                    @load="handleVectorLoad"
                    @error="handleVectorError"
                  />
                </div>
              </div>

              <!-- Show More Button -->
              <div v-if="pagination.vectors.hasMore" class="text-center py-4">
                <button
                  @click.stop="loadMoreVectors"
                  :disabled="pagination.vectors.loading"
                  class="px-4 py-2 bg-primary text-white rounded-md text-sm hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <div
                    v-if="pagination.vectors.loading"
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

              <!-- End of results message -->
              <div
                v-if="
                  !pagination.vectors.hasMore &&
                  popularVectors.length > 0 &&
                  !isLoading
                "
                class="text-center text-gray-500 text-sm py-4"
              >
                No more vectors to load
              </div>
            </div>
          </div>
          <div v-if="currentTab === 'upload'" class="text-center">
            <div
              class="border-2 border-dashed border-gray-300 rounded-lg p-8 hover:border-blue-500 transition-colors cursor-pointer"
              @click="triggerFileUpload"
              @dragover.prevent
              @drop.prevent="handleFileDrop"
            >
              <div class="text-gray-500">
                <svg
                  class="mx-auto h-12 w-12 mb-4"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                  />
                </svg>
                <p class="mb-1">
                  Drop your file here, or
                  <span class="text-blue-600">browse</span>
                </p>
                <p class="text-sm">Supports: PNG, SVG</p>
              </div>
            </div>
            <input
              type="file"
              ref="fileInput"
              class="hidden"
              accept=".svg,.png,image/svg+xml,image/png"
              @change="handleFileSelect"
            />
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>


<script>
import { useEditorStore } from "@/stores/editorStore";
import apiClient, { getProxyUrl } from "~/services/apiClient";

// Add this debounce utility function
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
  name: "GraphicsDropdown",
  setup() {
    const editorStore = useEditorStore();
    return { editorStore };
  },
  props: {
    title: {
      type: String,
      default: "Add Graphic",
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
      currentTab: "icons",
      searchQuery: "",
      selectedIconType: "all",
      iconTypes: [
        { id: "all", name: "All" },
        { id: "flat", name: "Flat" },
        { id: "outline", name: "Outline" },
      ],
      tabs: [
        { id: "icons", name: "Icons" },
        { id: "vectors", name: "Vectors" },
        { id: "upload", name: "Upload" },
      ],
      popularIcons: [],
      popularVectors: [],
      pagination: {
        icons: {
          page: 1,
          totalPages: 1,
          hasMore: true,
          loading: false,
          perPage: 150,
        },
        vectors: {
          page: 1,
          totalPages: 1,
          hasMore: true,
          loading: false,
          perPage: 150,
        },
      },
      initialLoadDone: {
        icons: false,
        vectors: false,
      },
      isLoading: false,
      loadedItems: {
        icons: 0,
        vectors: 0,
      },
      isSearching: false,
      minLoadingTime: 1000,
      loadingTimers: {
        icons: null,
        vectors: null,
      },
    };
  },
  computed: {
    dropdownStyle() {
      return {
        top: this.positionTop,
        left: this.positionLeft,
      };
    },
    backgroundPicked: {
      get() {
        return this.editorStore.backgroundColorCanvas;
      },
      set(value) {
        this.editorStore.backgroundColorCanvas = value;
      },
    },
    searchPlaceholder() {
      if (this.currentTab === "icons") {
        return "Search Icons";
      }
      if (this.currentTab === "vectors") {
        return "Search Vectors";
      }
      return "Search";
    },
  },
  created() {
    // Create the debounced search method
    this.debouncedSearch = debounce(this.performSearch, 300);
  },
  methods: {
    // Make sure the input keeps focus after search
    focusSearchInput() {
      if (this.$refs.searchInput) {
        this.$nextTick(() => {
          this.$refs.searchInput.focus();
        });
      }
    },

    // Add the upload-related methods
    triggerFileUpload() {
      this.$refs.fileInput.click();
    },

    handleFileSelect(event) {
      const file = event.target.files[0];
      if (!file) return;

      // Check file type
      const validTypes = ["image/svg+xml", "image/png"];
      if (!validTypes.includes(file.type)) {
        alert("Please select only SVG or PNG files");
        event.target.value = ""; // Reset file input
        return;
      }

      this.handleUpload(file);
    },

    handleFileDrop(event) {
      const file = event.dataTransfer.files[0];
      if (file) {
        this.handleUpload(file);
      }
    },

    handleUpload(file) {
      this.editorStore.addMediaElement(file);
      this.isOpen = false;
    },

    // Separate methods for search action and data fetching
    performSearch() {
      this.isSearching = true;

      // Clear any existing timers when performing a new search
      if (this.currentTab === "icons") {
        if (this.loadingTimers.icons) {
          clearTimeout(this.loadingTimers.icons);
        }
        this.pagination.icons.page = 1;
        this.pagination.icons.hasMore = true;
        this.fetchIcons().then(() => {
          this.isSearching = false;
          this.focusSearchInput();
        });
      } else if (this.currentTab === "vectors") {
        if (this.loadingTimers.vectors) {
          clearTimeout(this.loadingTimers.vectors);
        }
        this.pagination.vectors.page = 1;
        this.pagination.vectors.hasMore = true;
        this.fetchVectors().then(() => {
          this.isSearching = false;
          this.focusSearchInput();
        });
      }
    },

    async fetchVectors() {
      try {
        this.isLoading = true;
        this.loadedItems.vectors = 0;
        this.pagination.vectors.loading = true;

        // Start a timer to ensure loading state shows for at least minLoadingTime
        const startTime = Date.now();

        // Clear any existing timer
        if (this.loadingTimers.vectors) {
          clearTimeout(this.loadingTimers.vectors);
        }

        const response = await apiClient.get("/icons/vectors/", {
          params: {
            page: this.pagination.vectors.page,
            per_page: this.pagination.vectors.perPage,
            search: this.searchQuery,
          },
        });

        // Make sure we're accessing the right properties from the response
        if (response.data) {
          this.popularVectors = response.data.icons || [];
          this.pagination.vectors.page = response.data.page || 1;
          this.pagination.vectors.totalPages = response.data.total_pages || 1;
          this.pagination.vectors.hasMore = response.data.has_next || false;
        } else {
          this.popularVectors = [];
          this.pagination.vectors.hasMore = false;
        }

        this.initialLoadDone.vectors = true;

        // Calculate remaining time to meet minLoadingTime requirement
        const elapsedTime = Date.now() - startTime;
        const remainingTime = Math.max(0, this.minLoadingTime - elapsedTime);

        if (remainingTime > 0) {
          // Keep loading state for the remaining time
          this.loadingTimers.vectors = setTimeout(() => {
            this.pagination.vectors.loading = false;
            this.isLoading = false;
          }, remainingTime);
        } else {
          // If minimum time already passed, remove loading state immediately
          this.pagination.vectors.loading = false;
          this.isLoading = false;
        }
      } catch (error) {
        console.error("Error loading vectors:", error);
        this.popularVectors = [];
        this.pagination.vectors.hasMore = false;

        // Even on error, maintain minimum loading time
        const elapsedTime = Date.now() - startTime;
        const remainingTime = Math.max(0, this.minLoadingTime - elapsedTime);

        if (remainingTime > 0) {
          this.loadingTimers.vectors = setTimeout(() => {
            this.pagination.vectors.loading = false;
            this.isLoading = false;
          }, remainingTime);
        } else {
          this.pagination.vectors.loading = false;
          this.isLoading = false;
        }
      }
    },

    async loadMoreVectors() {
      if (this.pagination.vectors.loading || !this.pagination.vectors.hasMore)
        return;

      try {
        this.pagination.vectors.loading = true;

        const response = await apiClient.get("/icons/vectors/", {
          params: {
            page: this.pagination.vectors.page + 1,
            per_page: this.pagination.vectors.perPage,
            search: this.searchQuery,
          },
        });

        if (response.data && Array.isArray(response.data.icons)) {
          // Append new vectors to existing ones
          this.popularVectors = [
            ...this.popularVectors,
            ...response.data.icons,
          ];

          // Update pagination state
          this.pagination.vectors.page =
            response.data.page || this.pagination.vectors.page + 1;
          this.pagination.vectors.totalPages =
            response.data.total_pages || this.pagination.vectors.totalPages;
          this.pagination.vectors.hasMore = response.data.has_next || false;
        } else {
          this.pagination.vectors.hasMore = false;
        }
      } catch (error) {
        console.error("Error loading more vectors:", error);
        this.pagination.vectors.hasMore = false;
      } finally {
        this.pagination.vectors.loading = false;
      }
    },

    handleVectorLoad() {
      this.loadedItems.vectors++;
      if (this.loadedItems.vectors === this.popularVectors.length) {
        this.isLoading = false;
      }
    },

    handleVectorError() {
      this.loadedItems.vectors++;
      if (this.loadedItems.vectors === this.popularVectors.length) {
        this.isLoading = false;
      }
    },

    handleIconLoad() {
      this.loadedItems.icons++;
      if (this.loadedItems.icons === this.popularIcons.length) {
        this.isLoading = false;
      }
    },

    handleIconError() {
      this.loadedItems.icons++;
      if (this.loadedItems.icons === this.popularIcons.length) {
        this.isLoading = false;
      }
    },

    async fetchIcons() {
      try {
        this.isLoading = true;
        this.loadedItems.icons = 0;
        this.pagination.icons.loading = true;

        // Start a timer to ensure loading state shows for at least minLoadingTime
        const startTime = Date.now();

        // Clear any existing timer
        if (this.loadingTimers.icons) {
          clearTimeout(this.loadingTimers.icons);
        }

        const response = await apiClient.get("/icons/svg/", {
          params: {
            page: this.pagination.icons.page,
            per_page: this.pagination.icons.perPage,
            search: this.searchQuery,
            type: this.selectedIconType === "all" ? undefined : this.selectedIconType,
          },
        });

        if (response.data) {
          this.popularIcons = response.data.icons || [];
          this.pagination.icons.page = response.data.page || 1;
          this.pagination.icons.totalPages = response.data.total_pages || 1;
          this.pagination.icons.hasMore = response.data.has_next || false;
        } else {
          this.popularIcons = [];
          this.pagination.icons.hasMore = false;
        }

        this.initialLoadDone.icons = true;

        // Calculate remaining time to meet minLoadingTime requirement
        const elapsedTime = Date.now() - startTime;
        const remainingTime = Math.max(0, this.minLoadingTime - elapsedTime);

        if (remainingTime > 0) {
          // Keep loading state for the remaining time
          this.loadingTimers.icons = setTimeout(() => {
            this.pagination.icons.loading = false;
            this.isLoading = false;
          }, remainingTime);
        } else {
          // If minimum time already passed, remove loading state immediately
          this.pagination.icons.loading = false;
          this.isLoading = false;
        }
      } catch (error) {
        console.error("Error loading icons:", error);
        this.popularIcons = [];
        this.pagination.icons.hasMore = false;

        // Even on error, maintain minimum loading time
        const elapsedTime = Date.now() - startTime;
        const remainingTime = Math.max(0, this.minLoadingTime - elapsedTime);

        if (remainingTime > 0) {
          this.loadingTimers.icons = setTimeout(() => {
            this.pagination.icons.loading = false;
            this.isLoading = false;
          }, remainingTime);
        } else {
          this.pagination.icons.loading = false;
          this.isLoading = false;
        }
      }
    },

    toggleDropdown() {
      this.isOpen = !this.isOpen;
      if (this.isOpen) {
        if (this.currentTab === "icons" && !this.initialLoadDone.icons) {
          this.fetchIcons();
        } else if (
          this.currentTab === "vectors" &&
          !this.initialLoadDone.vectors
        ) {
          this.fetchVectors();
        }
      }
    },

    async loadMoreIcons() {
      if (this.pagination.icons.loading || !this.pagination.icons.hasMore)
        return;

      try {
        this.pagination.icons.loading = true;

        const response = await apiClient.get("/icons/svg/", {
          params: {
            page: this.pagination.icons.page + 1,
            per_page: this.pagination.icons.perPage,
            search: this.searchQuery,
          },
        });

        // Append new icons to existing ones
        this.popularIcons = [...this.popularIcons, ...response.data.icons];

        // Update pagination state
        this.pagination.icons.page = response.data.page;
        this.pagination.icons.totalPages = response.data.total_pages;
        this.pagination.icons.hasMore = response.data.has_next;
      } catch (error) {
        console.error("Error loading more icons:", error);
      } finally {
        this.pagination.icons.loading = false;
      }
    },

    closeDropdown(event) {
      if (
        this.$refs.dropdownRef &&
        !this.$refs.dropdownRef.contains(event.target)
      ) {
        this.isOpen = false;
      }
    },

    selectColor(color) {
      this.editorStore.backgroundColorCanvas = color.hex;
      this.isOpen = false;
    },

    selectPattern(pattern) {
      this.$emit("graphic-selected", { type: "pattern", ...pattern });
      this.isOpen = false;
    },

    async addIconElement(url, type, iconType) {
      const svg = await this.loadSvg(url);
      this.editorStore.addIconElement(svg, type, iconType);
    },

    getProxiedUrl(originalUrl) {
      return getProxyUrl(originalUrl);
    },

    async loadSvg(url) {
      try {
        const proxiedUrl = this.getProxiedUrl(url);
        const response = await fetch(proxiedUrl);
        if (!response.ok) throw new Error("Failed to load SVG");
        const text = await response.text();

        // Basic SVG validation
        if (!text.includes("<svg")) {
          throw new Error("Invalid SVG content");
        }

        // Parse and sanitize SVG
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, "image/svg+xml");
        const svg = doc.querySelector("svg");

        // Set consistent size
        svg.setAttribute("width", "100%");
        svg.setAttribute("height", "100%");

        const svgContent = svg.outerHTML;
        return svgContent;
      } catch (error) {
        console.error("Error loading SVG:", error);
        return null;
      }
    },

    async searchPexelsImages() {
      if (!this.searchQuery.trim()) return;
      
      try {
        this.isLoading = true;
        const response = await apiClient.get("/icons/pexels/photos/", {
          params: {
            query: this.searchQuery,
            page: this.pexelsPage,
            per_page: 12,
            orientation: undefined, // Optional parameters can be added later
            size: undefined,
            color: undefined
          },
        });
        
        this.pexelsImages = response.data.photos;
      } catch (error) {
        console.error('Error fetching Pexels images:', error);
      } finally {
        this.isLoading = false;
      }
    },
  },
  mounted() {
    document.addEventListener("click", this.closeDropdown);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.closeDropdown);

    // Clear any pending timers
    if (this.loadingTimers.icons) {
      clearTimeout(this.loadingTimers.icons);
    }
    if (this.loadingTimers.vectors) {
      clearTimeout(this.loadingTimers.vectors);
    }
  },
  watch: {
    searchQuery: {
      handler() {
        if (!this.isSearching) {
          this.debouncedSearch();
        }
      },
    },
    currentTab: {
      immediate: true,
      handler(newTab) {
        if (this.isOpen) {
          if (newTab === "icons" && !this.initialLoadDone.icons) {
            this.fetchIcons();
          } else if (newTab === "vectors" && !this.initialLoadDone.vectors) {
            this.fetchVectors();
          }

          // Focus the search input when changing tabs
          this.$nextTick(() => {
            if (this.$refs.searchInput && newTab !== "upload") {
              this.$refs.searchInput.focus();
            }
          });
        }
      },
    },
    isOpen: {
      handler(opened) {
        if (opened) {
          if (!this.initialLoadDone.icons && this.currentTab === "icons") {
            this.fetchIcons();
          } else if (
            !this.initialLoadDone.vectors &&
            this.currentTab === "vectors"
          ) {
            this.fetchVectors();
          }

          // Focus the search input when opening the dropdown
          this.$nextTick(() => {
            if (this.$refs.searchInput && this.currentTab !== "upload") {
              this.$refs.searchInput.focus();
            }
          });
        }
        if (!opened) {
          this.editorStore.selectedNavigationDesign = null;
        }
      },
    },
    selectedIconType: {
      handler() {
        this.pagination.icons.page = 1;
        this.pagination.icons.hasMore = true;
        this.fetchIcons();
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