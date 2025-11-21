<template>
  <div class="main-container">
    <!-- Header with title -->
    <div class="px-8 py-4">
      <div class="flex gap-[5px] flex-col">
        <div class="flex justify-start items-center">
          <span class="text-sm font-semibold flex justify-center items-center">
          </span>
        </div>
        <div class="h-[1px] w-full bg-grayBackgroundLight"></div>
      </div>
    </div>

    <!-- Main content area with form (30%) and three-step process (70%) -->
    <div class="px-8 flex inner-container">
      <!-- Form section (30%) -->
      <div class="w-5/12">
        <!-- Main Content Form - Modernized -->
        <div
          class="bg-white rounded-xl shadow-lg border border-gray-100 p-6 transition-all"
        >
          <h3 class="text-xl font-semibold text-gray-800 mb-6">
            Create Infographic
          </h3>

          <!-- Template Selection - Modernized -->
          <div class="mb-6">
            <label
              class="text-sm font-medium text-gray-700 mb-2 flex items-center"
            >
              Select Template
            </label>
            <div class="relative">
              <ResizeDropdown
                ref="sizeDropdown"
                v-model="selectedSize"
                :items="dropdownItems"
                placeholder="Select a size"
              >
                <template #trigger>
                  <div
                    class="border gap-4 flex justify-between w-full cursor-pointer border-gray-200 rounded-lg px-4 py-3 hover:border-blue-500 transition-colors text-sm bg-white"
                    @click="$refs.sizeDropdown?.toggleDropdown()"
                  >
                    <span class="text-base">
                      {{ selectedSize ? selectedSize : "Select a template" }}
                    </span>
                    <svg
                      class="w-5 h-5 text-gray-500"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M19 9l-7 7-7-7"
                      />
                    </svg>
                  </div>
                </template>
              </ResizeDropdown>
            </div>
          </div>

          <!-- Tab Navigation - Modernized -->
          <div class="mb-6">
            <label
              class=" text-sm font-medium text-gray-700 mb-2 flex items-center"
            >
              Content Source
            </label>
            <div class="flex space-x-2 bg-gray-100 p-1 rounded-lg">
              <button
                v-for="tab in tabs"
                :key="tab.id"
                @click="activeTab = tab.id"
                class="relative py-1 px-2 text-sm font-medium transition-all rounded-md flex-1 text-center"
                :class="[
                  activeTab === tab.id
                    ? 'bg-white text-blue-600 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900',
                ]"
              >
                {{ tab.label }}
              </button>
            </div>
          </div>

          <!-- Content Input Section - Modernized -->
          <div class="space-y-6">
            <div v-if="activeTab === 'blog'" class="space-y-3">
              <div class="space-y-2">
                <label
                  class="block text-sm font-medium text-gray-700"
                  for="url"
                >
                  Blog URL
                </label>
                <div class="flex gap-2 relative">
                  <input
                    id="url"
                    v-model="url"
                    type="text"
                    placeholder="https://example.com/blog-post"
                    class="w-full px-4 py-3 text-base rounded-lg bg-gray-50 border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition-all placeholder-gray-400 hover:bg-gray-100"
                    :class="{
                      'border-red-300 focus:border-red-500 focus:ring-red-100':
                        showUrlError,
                    }"
                  />
                </div>
                <p
                  v-if="showUrlError"
                  class="text-red-500 text-sm mt-1 flex items-center"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-4 w-4 mr-1"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                      clip-rule="evenodd"
                    />
                  </svg>
                  Please enter a valid URL
                </p>
              </div>

              <!-- Analysis Results - Modernized -->
              <div v-if="urlAnalysis || analysisError" class="mt-4">
                <div
                  v-if="analysisError"
                  class="text-red-500 text-sm bg-red-50 p-4 rounded-lg flex items-start"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-5 w-5 mr-2 flex-shrink-0"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                      clip-rule="evenodd"
                    />
                  </svg>
                  {{ analysisError }}
                </div>
                <div
                  v-else
                  class="bg-blue-50 rounded-lg p-4 border border-blue-100"
                >
                  <h3
                    class="text-sm font-medium text-blue-700 mb-2 flex items-center"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-5 w-5 mr-1"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fill-rule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                        clip-rule="evenodd"
                      />
                    </svg>
                    Analysis Complete
                  </h3>
                  <p class="text-sm text-gray-600 whitespace-pre-line">
                    {{ urlAnalysis }}
                  </p>
                </div>
              </div>
            </div>

            <div v-else-if="activeTab === 'content'" class="space-y-3">
              <div class="space-y-2">
                <label
                  class="block text-sm font-medium text-gray-700"
                  for="content"
                >
                  Custom Content
                </label>
                <textarea
                  id="content"
                  v-model="content"
                  rows="8"
                  placeholder="Enter your content here..."
                  class="w-full px-4 py-3 text-base rounded-lg bg-gray-50 border border-gray-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-100 transition-all placeholder-gray-400 hover:bg-gray-100"
                  :class="{
                    'border-red-300 focus:border-red-500 focus:ring-red-100':
                      showContentError,
                  }"
                ></textarea>
                <p
                  v-if="showContentError"
                  class="text-red-500 text-sm mt-1 flex items-center"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-4 w-4 mr-1"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
                      clip-rule="evenodd"
                    />
                  </svg>
                  Please enter some content
                </p>
              </div>
            </div>

            <div v-else-if="activeTab === 'scratch'" class="space-y-3">
              <div class="space-y-2">
                <p class="text-sm text-gray-600">
                  Create a new infographic from scratch in our editor. You'll have full control over the design and content.
                </p>
                <div class="mt-4">
                  <button
                    @click="goToEditor"
                    class="w-full px-6 py-3 bg-gradient-to-r bg-primary text-white rounded-lg font-light text-sm transition-all transform hover:scale-[1.02] active:scale-[0.98] shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-300 flex items-center justify-center"
                  >
                    <span class="flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                      </svg>
                      Open Editor
                    </span>
                  </button>
                </div>
              </div>
            </div>

            <!-- Action Buttons - Modernized -->
            <div
              class="flex gap-4 justify-end mt-8 pt-4 border-t border-gray-100"
              v-if="activeTab !== 'scratch'"
            >
              <button
                @click="generateInfographic"
                class="px-6 py-3 bg-gradient-to-r bg-primary text-white rounded-lg font-light text-sm transition-all transform hover:scale-[1.02] active:scale-[0.98] shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-300 flex items-center justify-center"
                :disabled="!isFormValid || isGenerating"
                :class="{
                  'opacity-60 cursor-not-allowed': !isFormValid || isGenerating,
                }"
              >
                <span v-if="isGenerating" class="flex items-center">
                  <svg
                    class="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                    xmlns="http://www.w3.org/2000/svg"
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
                  Generating...
                </span>
                <span v-else class="flex items-center">
                  Generate Infographic
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Three-step process (70%) -->
      <div class="w-8/12 pl-6">
        <div class="p-6 rounded-lg bg-white shadow-sm border border-gray-100">
          <div class="flex justify-between items-start">
            <!-- Step 1 -->
            <div class="flex items-start space-x-4 w-1/3 pr-4">
              <div
                class="bg-blue-400 bg-opacity-20 p-3 rounded-full flex-shrink-0 mt-1"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-blue-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                  />
                </svg>
              </div>
              <div>
                <h3 class="font-medium mb-2 text-gray-800">
                  1. Select a template
                </h3>
                <p class="text-sm text-gray-600">
                  Choose what do you want to create
                </p>
              </div>
            </div>

            <!-- Step 2 -->
            <div class="flex items-start space-x-4 w-1/3 px-2">
              <div
                class="bg-blue-400 bg-opacity-20 p-3 rounded-full flex-shrink-0 mt-1"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-blue-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div>
                <h3 class="font-medium mb-2 text-gray-800">
                  2. Add your content
                </h3>
                <p class="text-sm text-gray-600">
                  Paste your blog URL or enter custom content.
                </p>
              </div>
            </div>

            <!-- Step 3 -->
            <div class="flex items-start space-x-4 w-1/3 pl-4">
              <div
                class="bg-blue-400 bg-opacity-20 p-3 rounded-full flex-shrink-0 mt-1"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-blue-400"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
              </div>
              <div>
                <h3 class="font-medium mb-2 text-gray-800">
                  3. Generate and Edit
                </h3>
                <p class="text-sm text-gray-600">
                  Create your infographic and edit it.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-6 generate-container">
          <div
            class="bg-white rounded-xl shadow-sm border h-[97%] overflow-scroll border-gray-100 p-4"
          >
            <div class="flex justify-between items-center mb-4">
              <h3 class="text-lg font-medium text-gray-800">
                Generated Infographics
                <p class="text-sm text-gray-400 mt-1 font-light">Choose URL or enter custom content, click on "Generate Infographic" and we'll generate an infographic for you.</p>
              </h3>
            </div>
                        <hr class="my-4 border-gray-200" />

            <div class="flex flex-wrap justify-start gap-4 items-start">
              <!-- Loading indicator when generating infographic -->
              <div v-if="isGenerating" class="w-full flex flex-col items-center justify-center py-8">
                <div class="animate-spin h-12 w-12 mb-4">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-full w-full text-primary" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </div>
                <p class="text-lg font-medium text-gray-700">Generating your infographic...</p>
                <p class="text-sm text-gray-500 mt-2">This will take about 1 minute. Please wait.</p>
              </div>
              
              <!-- Display infographics when not generating -->
              <div v-else class="mt-4 flex flex-wrap justify-start gap-4 ">
                <div
                  v-for="infograph in dashboardStore.infographicsCreated"
                  :key="infograph.uuid"
                >
                  <ListTemplateInfographCard
                    :infograph="infograph"
                  ></ListTemplateInfographCard>
                </div>
              </div>
            </div>

            <!-- Scrollable 2-column grid -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Button from "@/components/Button.vue";
import apiClient from "~/services/apiClient";
import { useDashboardStore } from "@/stores/dashboardStore";

export default {
  name: "CreateInfographic",
  components: {
    Button,
  },
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
      activeTab: "blog",
      url: "",
      content: "",
      selectedTemplate: "",
      isAnalyzing: false,
      isGenerating: false,
      isLoading: false,
      urlAnalysis: null,
      analysisError: null,
      previewContent: null,
      templates: [],
      tabs: [
        { id: "blog", label: "Url" },
        { id: "content", label: "Content" },
        { id: "scratch", label: "From Scratch" },
      ],
      selectedSize: null,
      dropdownItems: [
        // {
        //   category: "Social Media Posts",
        //   items: [
        //     {
        //       label: "Facebook Post",
        //       value: "Facebook Post",
        //       width: 1200,
        //       height: 900,
        //       icon: "facebook",
        //     },
        //     {
        //       label: "Instagram Post",
        //       value: "Instagram Post",
        //       width: 1080,
        //       height: 1080,
        //       icon: "instagram",
        //     },
        //     {
        //       label: "LinkedIn Post",
        //       value: "LinkedIn Post",
        //       width: 1200,
        //       height: 628,
        //       icon: "linkedin",
        //     },
        //   ],
        // },
        {
          category: "Blogging and Infographics",
          items: [
            {
              label: "Infographic",
              value: "Infographic",
              width: 800,
              height: 2000,
            },
            {
              label: "Infographic Letter",
              value: "Infographic_letter",
              width: 1000,
              height: 500,
            },
          ],
        },
        // {
        //   category: "Headers and Banners",
        //   items: [
        //     {
        //       label: "Facebook Cover",
        //       value: "Facebook Cover",
        //       width: 820,
        //       height: 360,
        //       icon: "facebook",
        //     },
        //     {
        //       label: "Facebook Event Cover",
        //       value: "Facebook Event Cover",
        //       width: 1920,
        //       height: 1005,
        //       icon: "facebook",
        //     },
        //     {
        //       label: "LinkedIn Banner",
        //       value: "LinkedIn Banner",
        //       width: 1128,
        //       height: 191,
        //       icon: "linkedin",
        //     },
        //     {
        //       label: "X Header",
        //       value: "X Header",
        //       width: 1500,
        //       height: 500,
        //       icon: "twitter",
        //     },
        //     {
        //       label: "YouTube Banner",
        //       value: "YouTube Banner",
        //       width: 2560,
        //       height: 1440,
        //       icon: "youtube",
        //     },
        //     {
        //       label: "Twitch Cover",
        //       value: "Twitch Cover",
        //       width: 1200,
        //       height: 480,
        //       icon: "twitch",
        //     },
        //   ],
        // },
      ],
    };
  },
  computed: {
    showUrlError() {
      return (
        this.activeTab === "blog" &&
        this.url.trim() !== "" &&
        !this.isValidUrl(this.url)
      );
    },
    showContentError() {
      return (
        this.activeTab === "content" &&
        this.content.trim() !== "" &&
        this.content.length < 10
      );
    },
    isFormValid() {
      if (!this.selectedSize) return false;

      if (this.activeTab === "blog") {
        return this.url.trim() !== "" && this.isValidUrl(this.url);
      } else if (this.activeTab === "content") {
        return this.content.trim().length >= 10;
      } else if (this.activeTab === "scratch") {
        return true; // Always valid for "Create from Scratch"
      }
      
      return false;
    },
    groupedTemplates() {
      // Group templates by category
      const groups = {};

      this.templates.forEach((template) => {
        if (!groups[template.category]) {
          groups[template.category] = {
            name: template.category,
            templates: [],
          };
        }
        groups[template.category].templates.push(template);
      });

      return Object.values(groups);
    },
    selectedTemplateInfo() {
      return this.templates.find((t) => t.name === this.selectedTemplate);
    },
  },
  created() {
    this.fetchTemplates();
  },
  methods: {
    getSelectedTemplate() {
      if (!this.selectedSize) return null;

      for (const category of this.dropdownItems) {
        const found = category.items.find(
          (item) => item.value === this.selectedSize
        );
        if (found) return found;
      }

      return null;
    },
    calculateAspectRatio(width, height) {
      if (!width || !height) return "";

      const gcd = (a, b) => {
        return b === 0 ? a : gcd(b, a % b);
      };

      const divisor = gcd(width, height);
      return `${width / divisor}:${height / divisor}`;
    },
    isValidUrl(string) {
      try {
        new URL(string);
        return true;
      } catch (_) {
        return false;
      }
    },
    async fetchTemplates() {
      this.isLoading = true;
      try {
        // CSRF token is now set up automatically by the plugin
        const response = await apiClient.get("/infos/template-list/");
        this.templates = response.data;
      } catch (error) {
        console.error("Error fetching templates:", error);
      } finally {
        this.isLoading = false;
      }
    },
    async analyzeContent() {
      this.isAnalyzing = true;
      this.urlAnalysis = null;
      this.analysisError = null;
      this.previewContent = null;

      try {
        // CSRF token is now set up automatically by the plugin
        const response = await apiClient.post("/infos/analyze-content/", {
          content: this.content,
        });

        if (response.status !== 200) {
          throw new Error("Failed to analyze content");
        }

        const data = response.data;
        this.urlAnalysis = data.analysis;
      } catch (error) {
        console.error("Error analyzing content:", error);
        this.analysisError = "Failed to analyze content. Please try again.";
      } finally {
        this.isAnalyzing = false;
      }
    },
    async analyzeUrl() {
      if (!this.url || !this.isValidUrl(this.url)) {
        return;
      }

      this.isAnalyzing = true;
      this.urlAnalysis = null;
      this.analysisError = null;
      this.previewContent = null;

      try {
        // CSRF token is now set up automatically by the plugin
        const response = await apiClient.post("/infos/analyze-url/", {
          url: this.url,
        });

        if (response.status !== 200) {
          throw new Error("Failed to analyze URL");
        }

        const data = response.data;
        this.urlAnalysis = data.analysis;
        this.content = data.analysis; // Automatically fill content
      } catch (error) {
        console.error("Error analyzing URL:", error);
        this.analysisError = "Failed to analyze URL. Please try again.";
      } finally {
        this.isAnalyzing = false;
      }
    },
    async generateInfographic() {
      if (!this.isFormValid) {
        return;
      }

      this.isGenerating = true;
      this.previewContent = null;
      console.log(this.selectedSize);

      try {
        // CSRF token is now set up automatically by the plugin
        const response = await apiClient.post(
          "/infos/analyze-and-generate/",
          {
            template_section: this.selectedSize,
            content: this.content,
            url: this.url,
            
          }
        );

        // Handle the response
        if (response.data && response.data.redirect_url) {
          // Display preview before redirecting
          if (response.data.preview) {
            this.previewContent = response.data.preview;
          } else {
            // Redirect immediately if no preview
          }
        }
        
        // Show success message
        
        // Extract UUIDs of newly created infographics
        if (response.data && response.data.infographics) {
          const newInfographicUuids = response.data.infographics.map(
            infographic => infographic.uuid
          );
          
          await this.dashboardStore.getNewInfographics(newInfographicUuids);
        }
      } catch (error) {
        console.error("Error generating infographic:", error);
      } finally {
        // Keep isGenerating true for a bit longer to show the loading state
        this.isGenerating = false;
      }
    },
    
    goToEditor() {
      // Navigate to the editor page
      window.location.href = '/dashboard/editor';
      // this.$router.push('/dashboard/editor');
    },
  },
};
</script>

<style scoped>
.animate-spin {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
.main-container {
  height: calc(100% - 64px);
}

.inner-container {
  height: calc(100% - 59px);
}

.generate-container {
  height: calc(100% - 150px);
}
</style>