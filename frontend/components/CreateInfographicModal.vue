<!-- 
  This component is a modal for creating infographics with size selection functionality.
  It provides:
  1. Blog/Custom content input
  2. Template size selection via dropdown
  3. Template gallery with previews
-->
<template>
  <Modal
    :isOpen="isOpen"
    @close="closeModal"
    title="Create Infographic"
    subTitle="Transform your blog content into stunning infographics with AI"
    size="full-screen"
  >
    <div class="flex flex-col h-[89%] max-h-[calc(100vh-140px)]">
      <div class="h-px w-full bg-gray-200"></div>

      <div class="flex flex-1 overflow-hidden">
        <!-- Left Column - Content Input -->
        <div class="w-[320px] p-4 flex flex-col border-r border-gray-200">
          <!-- Tab Navigation -->
          <div class="flex space-x-4 mb-4">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              class="relative pb-1.5 text-sm font-medium transition-colors"
              :class="[
                activeTab === tab.id
                  ? 'text-primary'
                  : 'text-gray-500 hover:text-gray-700',
              ]"
            >
              {{ tab.label }}
              <div
                class="absolute bottom-0 left-0 w-full h-0.5 transition-colors"
                :class="[
                  activeTab === tab.id ? 'bg-primary' : 'bg-transparent',
                ]"
              ></div>
            </button>
          </div>

          <!-- Content Input Section -->
          <div class="flex-1 min-h-0">
            <div v-if="activeTab === 'blog'" class="space-y-3">
              <div class="space-y-1.5">
                <label class="text-sm font-medium text-gray-700" for="url">
                  Blog URL
                </label>
                <input
                  id="url"
                  v-model="url"
                  type="text"
                  placeholder="https://example.com/blog-post"
                  class="w-full px-3 py-1.5 text-sm rounded-lg bg-gray-50 border border-gray-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-200 transition-all"
                />
              </div>
            </div>

            <div v-else class="space-y-3">
              <div class="space-y-1.5">
                <label class="text-sm font-medium text-gray-700" for="content">
                  Custom Content
                </label>
                <textarea
                  id="content"
                  v-model="content"
                  rows="6"
                  placeholder="Enter your content here..."
                  class="w-full px-3 py-1.5 text-sm rounded-lg bg-gray-50 border border-gray-200 focus:border-blue-500 focus:ring-1 focus:ring-blue-200 transition-all"
                ></textarea>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="space-y-2 mt-4">
            <Button @click="createInfograph" class="w-full" variant="secondary">
              Create Infographic
            </Button>
            <Button @click="createFromScratch" class="w-full">
              Create from Scratch
            </Button>
          </div>
        </div>

        <!-- Right Column - Templates -->
        <div class="flex-1 p-4 bg-gray-50 overflow-scroll">
          <!-- Size Selection Header -->
          <div class="flex items-center mb-4 gap-4">
            <span class="text-sm font-semibold">Templates</span>
            <ResizeDropdown
              ref="sizeDropdown"
              v-model="selectedSize"
              :items="dropdownItems"
              placeholder="Select a size"
            >
              <template #trigger>
                <div
                  class="border gap-4 flex justify-between min-w-[150px] cursor-pointer border-gray-200 rounded-lg px-3 py-2 hover:border-blue-500 transition-colors text-sm bg-white"
                  @click="$refs.sizeDropdown?.toggleDropdown()"
                >
                  <span>{{ selectedSize || "Select size" }}</span>
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

          <!-- Template Grid -->
          <div class="grid grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-4">
            <div
              v-for="(template, index) in filteredTemplates"
              :key="index"
              class="group relative"
            >
              <!-- Template Preview -->
              <div
                class="aspect-[1/1.5] rounded-lg bg-white shadow-sm border border-gray-200 overflow-hidden transition-all group-hover:shadow-md"
                :style="{
                  aspectRatio:
                    template.width && template.height
                      ? `${template.width}/${template.height}`
                      : '1/1.5',
                }"
              >
                <div class="w-full h-full bg-gray-100"></div>
              </div>

              <!-- Template Info -->
              <div class="mt-2 flex justify-between items-start">
                <div class="space-y-0.5">
                  <h3 class="text-sm font-medium text-gray-700">
                    {{ template.name }}
                  </h3>
                  <p class="text-xs text-gray-500">
                    {{ template.width }} × {{ template.height }}px
                  </p>
                </div>
                <button
                  @click="useTemplate(index)"
                  class="px-2 py-0.5 text-xs font-medium text-blue-600 bg-blue-50 rounded-full hover:bg-blue-100 transition-colors"
                >
                  Use
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Modal>
</template>

<script>
import Modal from "./Modal.vue";
import ResizeDropdown from "./ResizeDropdown.vue";

export default {
  name: "CreateInfographicModal",
  components: {
    Modal,
    ResizeDropdown,
  },
  props: {
    isOpen: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      activeTab: "blog",
      url: "",
      content: "",
      selectedSize: "",
      tabs: [
        { id: "blog", label: "Blog/Url" },
        { id: "content", label: "Content" },
      ],
      dropdownItems: [
        {
          category: "Social Media Posts",
          items: [
            {
              label: "Facebook Post",
              value: "Facebook Post",
              width: 1200,
              height: 900,
              icon: "facebook",
            },
            {
              label: "Facebook Link",
              value: "Facebook Link",
              width: 1200,
              height: 628,
              icon: "facebook",
            },
            {
              label: "Instagram Post",
              value: "Instagram Post",
              width: 1080,
              height: 1080,
              icon: "instagram",
            },
            {
              label: "Instagram Story",
              value: "Instagram Story",
              width: 1080,
              height: 1920,
              icon: "instagram",
            },
            {
              label: "LinkedIn Post",
              value: "LinkedIn Post",
              width: 1200,
              height: 628,
              icon: "linkedin",
            },
            {
              label: "Pinterest Pin",
              value: "Pinterest Pin",
              width: 1000,
              height: 1500,
              icon: "pinterest",
            },
            {
              label: "X Post",
              value: "X Post",
              width: 1024,
              height: 512,
              icon: "twitter",
            },
            {
              label: "YouTube Thumbnail",
              value: "YouTube Thumbnail",
              width: 1280,
              height: 720,
              icon: "youtube",
            },
          ],
        },
        {
          category: "Blogging and Infographics",
          items: [
            {
              label: "Blog Featured Image",
              value: "Blog Featured Image",
              width: 1200,
              height: 628,
            },
            {
              label: "Infographic",
              value: "Infographic",
              width: 800,
              height: 2000,
            },
            {
              label: "eBook Cover",
              value: "eBook Cover",
              width: 1410,
              height: 2250,
            },
          ],
        },
        {
          category: "Headers and Banners",
          items: [
            {
              label: "Facebook Cover",
              value: "Facebook Cover",
              width: 820,
              height: 360,
              icon: "facebook",
            },
            {
              label: "Facebook Event Cover",
              value: "Facebook Event Cover",
              width: 1920,
              height: 1005,
              icon: "facebook",
            },
            {
              label: "LinkedIn Banner",
              value: "LinkedIn Banner",
              width: 1128,
              height: 191,
              icon: "linkedin",
            },
            {
              label: "X Header",
              value: "X Header",
              width: 1500,
              height: 500,
              icon: "twitter",
            },
            {
              label: "YouTube Banner",
              value: "YouTube Banner",
              width: 2560,
              height: 1440,
              icon: "youtube",
            },
            {
              label: "Twitch Cover",
              value: "Twitch Cover",
              width: 1200,
              height: 480,
              icon: "twitch",
            },
          ],
        },
      ],
    };
  },
  computed: {
    filteredTemplates() {
      if (!this.selectedSize) return this.templates;

      const selectedTemplate = this.dropdownItems
        .flatMap((category) => category.items)
        .find((item) => item.value === this.selectedSize);

      if (!selectedTemplate) return this.templates;

      return this.templates.filter(
        (template) =>
          template.width === selectedTemplate.width &&
          template.height === selectedTemplate.height
      );
    },
    templates() {
      // Transform dropdown items into template format
      return this.dropdownItems
        .flatMap((category) => category.items)
        .map((item) => ({
          name: item.label,
          width: item.width,
          height: item.height,
          icon: item.icon,
        }));
    },
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
    createFromScratch() {
      this.$emit("create-scratch");
    },
    createInfograph() {
      const data = {
        type: this.activeTab,
        content: this.activeTab === "blog" ? this.url : this.content,
        size: this.selectedSize,
      };
      this.$emit("create", data);
    },
    useTemplate(index) {
      this.$emit("use-template", this.filteredTemplates[index]);
    },
  },
};
</script>