# templates/index.vue
<template>
  <div class="px-8 py-4">
    <div class="flex gap-[5px] flex-col">
      <div class="flex justify-start items-center">
        <span class="text-sm font-semibold flex justify-center items-center"
          >Templates</span
        >
        <div class="ml-4">
          <ResizeDropdown
            v-model="selectedSize"
            :items="dropdownItemsSize"
            placeholder="Select size"
            :is-open="isDropdownOpen"
            @update:is-open="isDropdownOpen = $event"
          >
            <template #trigger>
              <button
                @click="toggleDropdown"
                class="flex items-center gap-2 px-3 py-1.5 text-sm border border-gray-200 rounded-md hover:bg-gray-50"
              >
                <span>{{ selectedSizeLabel || 'All Sizes' }}</span>
                <span class="text-xs text-gray-500">▼</span>
              </button>
            </template>
          </ResizeDropdown>
        </div>
      </div>
      <div class="h-[1px] w-full bg-grayBackgroundLight"></div>
    </div>
    <div class="flex flex-wrap gap-4 mt-4"> 
      <template v-if="loading">
        <div class="w-full flex justify-center items-center py-8 col-span-full">
          <span class="text-sm text-gray-500">Loading templates...</span>
        </div>
      </template>
      <template v-else-if="templates.length === 0">
        <div class="w-full flex justify-center items-center py-8 flex-col gap-2 col-span-full">
          <span class="text-sm text-gray-500">
            No templates found for {{ selectedSizeLabel }}, they are being added soon!
          </span>
          <button 
            @click="resetFilter" 
            class="text-xs text-blue-500 hover:underline"
          >
            Show all templates
          </button>
        </div>
      </template>
      <template v-else>
        <TemplateCard
          v-for="(template, index) in templates"
          :key="template.uuid || index"
          :name="template.title"
          :width="template.width"
          :height="template.height"
          :category="template.template_type"
          :uuid="template.uuid"
          :preview-image-url="template.preview_image_url"
          :description="template.description || ''"
          :background-color="template.background_color || '#FFFFFF'"
          :is-new="isNewTemplate(template)"
          :content="template.content" 
        />
      </template>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from "@/stores/auth";
import { useDashboardStore } from "@/stores/dashboardStore";
import { useRoute, useRouter } from "vue-router";
import apiClient from "@/services/apiClient";
import { ref, watch, computed } from "vue";
import ResizeDropdown from "@/components/ResizeDropdown.vue";

export default {
  name: "dashboard",
  components: {
    ResizeDropdown
  },
  async setup() {
    definePageMeta({
      layout: "dashboard",
    });
    const route = useRoute();
    const router = useRouter();
    const dashboardStore = useDashboardStore();
    const authStore = useAuthStore();
    const { user, getUser, fetchUser, isAuthenticated } = authStore;

    // Template state
    const templates = ref([]);
    const loading = ref(false);

    const tokenFromQuery = route.query?.token;
    if (tokenFromQuery) {
      authStore.setToken(tokenFromQuery);
    } else {
      if (!isAuthenticated()) {
        if (typeof window !== "undefined") {
          window.location.href = "/login";
        }
      }
    }

    return {
      user,
      getUser,
      fetchUser,
      dashboardStore,
      templates,
      loading,
    };
  },
  data() {
    return {
      dropdownItemsSize: [
        {
          category: "All Sizes",
          items: [
            {
              label: "All Sizes",
              value: "all",
              width: null,
              height: null,
            },
          ],
        },
        {
          category: "Social Media Posts",
          items: [
            {
              label: "Infograph",
              value: "normal", 
              width: 800,
              height: 2000,
              icon: "infograph",
            },
           {
              label: "Infograph Letter",
              value: "letter", 
              width: 1000,
              height: 500,
              icon: "infograph",
            },
            {
              label: "Instagram Post",
              value: "Instagram Post",
              width: 1080,
              height: 1080,
              icon: "instagram",
            },
            {
              label: "Twitter Post",
              value: "Twitter Post",
              width: 1200,
              height: 675,
              icon: "twitter",
            },
            {
              label: "LinkedIn Post",
              value: "LinkedIn Post",
              width: 1200,
              height: 627,
              icon: "linkedin",
            },
          ],
        },
        {
          category: "Presentations",
          items: [
            {
              label: "Presentation (16:9)",
              value: "Presentation 16:9",
              width: 1920,
              height: 1080,
            },
            {
              label: "Presentation (4:3)",
              value: "Presentation 4:3",
              width: 1024,
              height: 768,
            },
          ],
        },
      ],
      isDropdownOpen: false,
      newTemplates: [],
    };
  },
  computed: {
    selectedSize: {
      get() {
        return this.dashboardStore.selectedSize;
      },
      set(newValue) {
        const selectedOption = this.dropdownItemsSize.reduce(
          (found, category) => {
            if (found) return found;
            return category.items.find((item) => item.value === newValue);
          },
          null
        );
        this.dashboardStore.selectedSize = newValue;
        this.fetchTemplates(selectedOption);
      },
    },
    selectedSizeLabel() {
      const selectedOption = this.dropdownItemsSize.reduce(
        (found, category) => {
          if (found) return found;
          return category.items.find((item) => item.value === this.selectedSize);
        },
        null
      );
      return selectedOption?.label || 'All Sizes';
    }
  },
  methods: {
    async fetchTemplates(selectedSize) {
      try {
        this.loading = true;

        const params = {};
        if (selectedSize && selectedSize.value !== "all") {
          params.width = selectedSize.width;
          params.height = selectedSize.height;
        }
        let template_type = null;
        if (selectedSize && selectedSize.value !== "all") {
          template_type = selectedSize.value;
        }
        const response = await apiClient.get("/infos/templates/", { params });
        this.templates = response.data;
        
        if (selectedSize && selectedSize.value !== "all") {
          this.templates = this.templates.filter(template => 
            template.width === selectedSize.width && 
            template.height === selectedSize.height
          );
        }
      } catch (error) {
        console.error("Error fetching templates:", error);
      } finally {
        this.loading = false;
      }
    },
    toggleDropdown() {
      this.isDropdownOpen = !this.isDropdownOpen;
    },
    isNewTemplate(template) {
      return this.newTemplates.includes(template.uuid) || this.newTemplates.includes(template.title);
    },
    resetFilter() {
      this.selectedSize = 'all';
      this.fetchTemplates(
        this.dropdownItemsSize
          .flatMap((category) => category.items)
          .find((item) => item.value === 'all')
      );
    },
  },
  async mounted() {
    await this.fetchTemplates(
      this.dropdownItemsSize
        .flatMap((category) => category.items)
        .find((item) => item.value === this.selectedSize)
    );
  },
  watch: {
    '$route'() {
      this.fetchTemplates(
        this.dropdownItemsSize
          .flatMap((category) => category.items)
          .find((item) => item.value === this.selectedSize)
      );
    }
  },
};
</script>