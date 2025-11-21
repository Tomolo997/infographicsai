<!-- Template Card Component -->
<template>
  <div
    class="w-[280px]  border border-gray-200 rounded-lg flex flex-col p-4 relative justify-between group hover:border-blue-500 transition-colors"
  >
    <div class="flex flex-col h-full">
      <div class="flex justify-between items-start">
        <span
          v-if="isNew"
          class="text-xs font-medium px-2 py-1 rounded-md bg-blue-50 text-blue-600"
        >
          New
        </span>
      </div>

      <!-- Preview Area -->
      <div
        class="flex-1 my-4 rounded-lg bg-gray-100 flex items-center justify-center overflow-hidden"
      >
        <!-- Template preview with proper aspect ratio -->
        <div 
          class="shadow-sm rounded border border-gray-200"
          :style="{
            width: getPreviewWidth(),
            height: getPreviewHeight(),
            maxWidth: '90%',
            maxHeight: '90%',
            backgroundColor: backgroundColor || '#FFFFFF'
          }"
        >
          <InfographicPreview 
            v-if="content && showLivePreview"
            :elements="parseContent(content.canvas_data).elements || []"
            :canvasWidth="width"
            :canvasHeight="height"
            :backgroundColor="backgroundColor || '#ffffff'"
            :backgroundImage="parseContent(content).backgroundImage"
            :backgroundPatternUrl="parseContent(content).backgroundPatternUrl"
            :backgroundImageSettings="parseContent(content).backgroundImageSettings"
            :backgroundPatternSettings="parseContent(content).backgroundPatternSettings"
            class="w-full h-full"
          />
          <img 
            v-else-if="previewImageUrl" 
            :src="previewImageUrl" 
            :alt="name"
            class="w-full h-full object-contain"
          />
          <div v-else class="w-full h-full flex items-center justify-center p-2 text-center">
            <div class="text-xs" :class="getTextColorClass()">{{ name }}</div>
          </div>
        </div>
      </div>

      <div class="flex flex-col gap-2 mt-auto">
        <div class="flex justify-between items-end">
          <div class="flex flex-col">
            <h3 class="text-sm font-medium text-gray-700 truncate max-w-[220px]">{{ name }}</h3>
            <p v-if="width && height" class="text-xs text-gray-500">
              {{ width }} × {{ height }}px
            </p>
            <p v-if="category" class="text-xs text-gray-500 truncate max-w-[220px]">
              {{ category }}
            </p>
          </div>
        </div>

        <div class="flex gap-2">
          <Button @click="showPreview" variant="primary" class="flex-1">
            Preview
          </Button>
          <Button @click="duplicateInfoGraphic" variant="secondary" class="flex-1" :disabled="loadingDuplicate">
            <template v-if="loadingDuplicate">
              <span class="inline-block animate-spin mr-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="12" r="10"></circle>
                  <path d="M12 6v6l4 2"></path>
                </svg>
              </span>
            </template>
            <template v-else>
              Use
            </template>
          </Button>
        </div>
      </div>
    </div>

    <!-- Preview Modal -->
    <Modal 
      :is-open="isPreviewModalOpen" 
      :title="name" 
      :sub-title="`${width} × ${height}px - ${category}`"
      size="large"
      @close="isPreviewModalOpen = false"
    >
      <div class="p-4 flex flex-col items-center">
        <div 
          class="border border-gray-200 rounded-lg shadow-sm overflow-hidden"
          :style="{
            width: getFullPreviewWidth(),
            height: getFullPreviewHeight(),
            backgroundColor: backgroundColor || '#FFFFFF'
          }"
        >
          <InfographicPreview 
            v-if="content && showLivePreview"
            :scale="3"
            :elements="parseContent(content.canvas_data).elements || []"
            :canvasWidth="width"
            :canvasHeight="height"
            :backgroundColor="backgroundColor || '#ffffff'"
            :backgroundImage="parseContent(content).backgroundImage"
            :backgroundPatternUrl="parseContent(content).backgroundPatternUrl"
            :backgroundImageSettings="parseContent(content).backgroundImageSettings"
            :backgroundPatternSettings="parseContent(content).backgroundPatternSettings"
            class="w-full h-full"
          />
          <img 
            v-else-if="previewImageUrl" 
            :src="previewImageUrl" 
            :alt="name"
            class="w-full h-full object-contain"
          />
          <div v-else class="w-full h-full flex items-center justify-center p-4 text-center">
            <div class="text-lg" :class="getTextColorClass()">{{ name }}</div>
          </div>
        </div>
        
        
        <div class="mt-6 w-full flex justify-center gap-4">
          <Button @click="createInfoGraphic" variant="secondary" class="px-6">
            Create from Template
          </Button>
        </div>
      </div>
    </Modal>
  </div>
</template>

<script>
import { useDashboardStore } from "@/stores/dashboardStore";
import { ref } from "vue";
import Modal from "@/components/Modal.vue";
import Button from "@/components/Button.vue";
import { useToastStore } from "~/stores/toast";
import InfographicPreview from "./InfographicPreview.vue";


export default {
  name: "TemplateCard",
  components: {
    Modal,
    Button,
    InfographicPreview
  },
  props: {
    name: {
      type: String,
      default: "Untitled Template",
    },
    width: {
      type: Number,
      default: null,
    },
    uuid: {
      type: String,
      default: "",
    },
    height: {
      type: Number,
      default: null,
    },
    isNew: {
      type: Boolean,
      default: false,
    },
    section: {
      type: String,
      default: "",
    },
    category: {
      type: String,
      default: "",
    },
    description: {
      type: String,
      default: "",
    },
    backgroundColor: {
      type: String,
      default: "",
    },
    previewImageUrl: {
      type: String,
      default: "",
    },
    content: {
      type: Object,
      default: null,
    },
    showLivePreview: {
      type: Boolean,
      default: true
    }
  },
  setup() {
    const dashboardStore = useDashboardStore();
    const isPreviewModalOpen = ref(false);
    const toast = useToastStore();
    
    return { 
      dashboardStore,
      isPreviewModalOpen,
      toast
    };
  },
  data() {
    return {
      loadingDuplicate: false
    };
  },
  methods: {
    parseContent(contentString) {
      if (!contentString) return {};
      try {
        return typeof contentString === 'string' ? JSON.parse(contentString) : contentString;
      } catch (e) {
        console.error("Error parsing infographic content:", e);
        return {};
      }
    },
    async createInfoGraphic() {
      this.isPreviewModalOpen = false;
      await this.dashboardStore.createInfograph(this.name);
    },
    async duplicateInfoGraphic() {
      try {
        this.loadingDuplicate = true;
        this.isPreviewModalOpen = false;
        
        // Use the store method to duplicate the infographic
        await this.dashboardStore.duplicateInfograph(this.uuid);
        
        // Toast notification will be shown after navigation
        this.toast.success("Template duplicated successfully");
        this.loadingDuplicate = false;
      } catch (error) {
        console.error("Error duplicating template:", error);
        this.toast.error(error.response?.data?.error || "Failed to duplicate template");
        this.loadingDuplicate = false;
      }
    },
    showPreview() {
      this.isPreviewModalOpen = true;
    },
    getPreviewWidth() {
      if (!this.width || !this.height) return '120px';
      
      // Calculate the preview dimensions while maintaining aspect ratio
      const aspectRatio = this.width / this.height;
      
      if (aspectRatio > 1) {
        // Landscape orientation
        return '140px';
      } else if (aspectRatio < 1) {
        // Portrait orientation
        return '100px';
      } else {
        // Square
        return '120px';
      }
    },
    getPreviewHeight() {
      if (!this.width || !this.height) return '120px';
      
      const aspectRatio = this.width / this.height;
      
      if (aspectRatio > 1) {
        // Landscape orientation
        return `${140 / aspectRatio}px`;
      } else if (aspectRatio < 1) {
        // Portrait orientation
        return `${100 / aspectRatio}px`;
      } else {
        // Square
        return '120px';
      }
    },
    getFullPreviewWidth() {
      if (!this.width || !this.height) return '500px';
      
      const aspectRatio = this.width / this.height;
      const maxWidth = 800;
      const maxHeight = 600;
      
      if (aspectRatio > 1) {
        // Landscape orientation - constrain by width
        return `${Math.min(maxWidth, this.width)}px`;
      } else {
        // Portrait or square - constrain by height
        const calculatedWidth = Math.min(maxHeight * aspectRatio, maxWidth);
        return `${calculatedWidth}px`;
      }
    },
    getFullPreviewHeight() {
      if (!this.width || !this.height) return '500px';
      
      const aspectRatio = this.width / this.height;
      const maxWidth = 800;
      const maxHeight = 600;
      
      if (aspectRatio > 1) {
        // Landscape orientation - constrain by width
        const calculatedHeight = Math.min(maxWidth / aspectRatio, maxHeight);
        return `${calculatedHeight}px`;
      } else {
        // Portrait or square - constrain by height
        return `${Math.min(maxHeight, this.height)}px`;
      }
    },
    getTextColorClass() {
      // If background is dark, use light text
      if (this.backgroundColor) {
        // Simple check for dark backgrounds
        const hex = this.backgroundColor.replace('#', '');
        const r = parseInt(hex.substr(0, 2), 16);
        const g = parseInt(hex.substr(2, 2), 16);
        const b = parseInt(hex.substr(4, 2), 16);
        
        // Calculate perceived brightness
        const brightness = (r * 299 + g * 587 + b * 114) / 1000;
        
        return brightness < 128 ? 'text-white' : 'text-gray-700';
      }
      
      return 'text-gray-500';
    }
  },
};
</script>