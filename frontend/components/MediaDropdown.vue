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
        <div class="px-4 mb-4" v-if="currentTab !== 'upload'">
          <div class="relative flex gap-2">
            <div class="relative flex-1">
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
                @keyup.enter="handleSearch"
              />
            </div>
            <button
              @click="handleSearch"
              class="px-4 py-2 text-[12px] bg-primary text-white rounded-lg hover:bg-primaryDark transition-colors"
            >
              Search
            </button>
          </div>
        </div>

        <!-- Content based on current tab -->
        <div class="px-4 pb-4">
          <!-- Color Tab -->
          <div v-if="currentTab === 'color'" class="grid grid-cols-4 gap-3">
            <button
              v-for="color in colors"
              :key="color.hex"
              @click="selectColor(color)"
              class="w-full aspect-square rounded-lg border border-gray-200 hover:border-blue-500 transition-colors"
              :style="{ backgroundColor: color.hex }"
            />
          </div>

          <!-- Pattern Tab -->
          <div v-if="currentTab === 'pattern'" class="grid grid-cols-2 gap-3">
            <button
              v-for="pattern in patterns"
              :key="pattern.id"
              @click="selectPattern(pattern)"
              class="aspect-square rounded-lg border border-gray-200 hover:border-blue-500 transition-colors overflow-hidden"
            >
              <img
                :src="pattern.preview"
                :alt="pattern.name"
                class="w-full h-full object-cover"
              />
            </button>
          </div>

          <!-- Upload Tab -->
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
                <p class="text-sm">Supports: JPG, PNG, SVG</p>
              </div>
            </div>
            <input
              type="file"
              ref="fileInput"
              class="hidden"
              accept="image/*"
              @change="handleFileSelect"
            />
            <!-- Recent Uploads Section -->
            <div v-if="editorStore.recentUploads.length > 0" class="mt-6">
              <div class="flex items-center justify-between mb-3">
                <div class="text-[12px] text-left text-gray-700">
                  Recent Uploads
                </div>
                <div v-if="isLoading" class="text-[12px] text-gray-500">
                  Loading...
                </div>
              </div>
              <div class="grid grid-cols-4 gap-2">
                <button
                  v-for="upload in editorStore.recentUploads"
                  :key="upload.id"
                  @click="selectRecentUpload(upload)"
                  class="aspect-square rounded-lg border border-gray-200 hover:border-blue-500 transition-colors overflow-hidden group relative"
                >
                  <img
                    :src="upload.url"
                    :alt="upload.filename"
                    class="w-full h-full object-cover"
                  />
                  <div
                    class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 transition-opacity"
                  />
                </button>
              </div>
            </div>
          </div>

          <!-- Images Tab -->
          <div v-if="currentTab === 'images'" class="images-grid">
            <div v-if="isLoading" class="text-center py-4">
              <div class="text-gray-500">Loading...</div>
            </div>

            <div
              v-else-if="pexelsImages.length > 0"
              class="grid grid-cols-3 gap-3"
            >
              <button
                v-for="photo in pexelsImages"
                :key="photo.id"
                @click="selectPexelsImage(photo)"
                class="aspect-square rounded-lg border border-gray-200 hover:border-blue-500 transition-colors overflow-hidden group relative"
              >
                <img
                  :src="photo.src.small"
                  :alt="photo.alt"
                  class="w-full h-full object-cover"
                />
                <div
                  class="absolute bottom-0 left-0 right-0 bg-black bg-opacity-50 text-white text-[10px] p-2 opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  Photo by {{ photo.photographer }}
                </div>
              </button>
            </div>

            <div v-else-if="searchQuery" class="text-center py-4">
              <div class="text-gray-500">No images found</div>
            </div>

            <div v-else class="text-center py-4">
              <div class="text-gray-500">Search for images to get started</div>
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

export default {
  name: "GraphicsDropdown",
  props: {
    title: {
      type: String,
      default: "Add Media",
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
      currentTab: "upload",
      searchQuery: "",
      isLoading: false,
      editorStore: useEditorStore(),
      pexelsImages: [],
      pexelsPage: 1,
      tabs: [
        { id: "upload", name: "Upload" },
        { id: "images", name: "Images" },
      ],
      colors: [
        { name: "Red", hex: "#EF4444" },
        { name: "Blue", hex: "#3B82F6" },
        { name: "Green", hex: "#10B981" },
        { name: "Yellow", hex: "#F59E0B" },
        { name: "Purple", hex: "#8B5CF6" },
        { name: "Pink", hex: "#EC4899" },
        { name: "Gray", hex: "#6B7280" },
        { name: "Black", hex: "#111827" },
        // Add more colors as needed
      ],
      patterns: [
        { id: 1, name: "Dots", preview: "/api/placeholder/150/150" },
        { id: 2, name: "Stripes", preview: "/api/placeholder/150/150" },
        { id: 3, name: "Grid", preview: "/api/placeholder/150/150" },
        { id: 4, name: "Waves", preview: "/api/placeholder/150/150" },
        // Add more patterns as needed
      ],
    };
  },
  computed: {
    dropdownStyle() {
      return {
        top: this.positionTop,
        left: this.positionLeft,
      };
    },
    searchPlaceholder() {
      switch (this.currentTab) {
        case "color":
          return "Search Color";
        case "pattern":
          return "Search Pattern";
        case "images":
          return "Search Pexels images";
        default:
          return "Search";
      }
    },
  },
  methods: {
    toggleDropdown() {
      this.isOpen = !this.isOpen;
    },
    closeDropdown(event) {
      if (
        this.$refs.dropdownRef &&
        !this.$refs.dropdownRef.contains(event.target)
      ) {
        this.isOpen = false;
      }
    },
    async loadRecentUploads() {
      try {
        this.isLoading = true;
        const response = await apiClient.get("/infos/recent-uploads/");
        this.editorStore.recentUploads = response.data;
      } catch (error) {
        console.error("Error loading recent uploads:", error);
      } finally {
        this.isLoading = false;
      }
    },

    selectRecentUpload(upload) {
      this.editorStore.addMediaElement({
        url: upload.url,
        name: upload.filename,
        type: "image",
      });
      this.isOpen = false;
    },

    selectColor(color) {
      this.$emit("graphic-selected", { type: "color", ...color });
      this.isOpen = false;
    },
    selectPattern(pattern) {
      this.$emit("graphic-selected", { type: "pattern", ...pattern });
      this.isOpen = false;
    },
    triggerFileUpload() {
      this.$refs.fileInput.click();
    },
    handleFileSelect(event) {
      const file = event.target.files[0];
      if (file) {
        this.handleUpload(file);
      }
    },
    handleFileDrop(event) {
      const file = event.dataTransfer.files[0];
      if (file) {
        this.handleUpload(file);
      }
    },
    async handleUpload(file) {
      try {
        const formData = new FormData();
        formData.append("file", file);

        // Upload file through the editor store
        await this.editorStore.addMediaElement(file);

        // Refresh recent uploads
        await this.loadRecentUploads();

        this.isOpen = false;
      } catch (error) {
        console.error("Error uploading file:", error);
      }
    },
    async searchPexelsImages() {
      try {
        this.isLoading = true;
        const response = await apiClient.get("/icons/pexels/photos/", {
          params: {
            query: this.searchQuery,
            page: this.pexelsPage,
            per_page: 12,
            orientation: undefined,
            size: undefined,
            color: undefined,
          },
        });

        this.pexelsImages = response.data.photos;
      } catch (error) {
        console.error("Error fetching Pexels images:", error);
      } finally {
        this.isLoading = false;
      }
    },

    async loadCuratedPhotos() {
      try {
        this.isLoading = true;
        const response = await apiClient.get("/icons/pexels/photos/", {
          params: {
            page: this.pexelsPage,
            per_page: 12,
          },
        });

        this.pexelsImages = response.data.photos;
      } catch (error) {
        console.error("Error fetching curated photos:", error);
      } finally {
        this.isLoading = false;
      }
    },

    selectPexelsImage(photo) {
      this.editorStore.addMediaElement({
        url: photo.src.medium,
        name: photo.alt || "Pexels Image",
        type: "image",
        attribution: {
          photographer: photo.photographer,
          photographerUrl: photo.photographer_url,
          source: "Pexels",
          sourceUrl: photo.url,
        },
      });
      this.isOpen = false;
    },
    handleSearch() {
      if (this.currentTab === "images") {
        if (this.searchQuery.trim()) {
          this.searchPexelsImages();
        } else {
          this.loadCuratedPhotos();
        }
      }
    },
  },
  mounted() {
    document.addEventListener("click", this.closeDropdown);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.closeDropdown);
  },
  watch: {
    isOpen: {
      handler(opened) {
        if (opened) {
          this.loadRecentUploads();
          if (this.currentTab === "images") {
            this.loadCuratedPhotos();
          }
        }
        if (!opened) {
          this.editorStore.selectedNavigationDesign = null;
        }
      },
    },
    currentTab: {
      handler(newTab) {
        if (newTab === "images") {
          if (this.searchQuery.trim()) {
            this.searchPexelsImages();
          } else {
            this.loadCuratedPhotos();
          }
        }
      },
    },
    searchQuery: {
      handler(newQuery) {
        if (this.currentTab === "images") {
          if (this.searchTimeout) {
            clearTimeout(this.searchTimeout);
          }
          this.searchTimeout = setTimeout(() => {
            if (newQuery.trim()) {
              this.searchPexelsImages();
            } else {
              this.loadCuratedPhotos();
            }
          }, 500);
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
  z-index: 10;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.images-grid {
  max-height: 400px;
  overflow-y: auto;
}

.pexels-attribution {
  font-size: 10px;
  color: #666;
  text-align: center;
  padding: 8px;
  border-top: 1px solid #eee;
}
</style>