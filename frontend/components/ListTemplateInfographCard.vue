<template>
  <div>
    <!-- Card Component -->
    <div @click="showModal = true" class="container border border-gray-200 hover:border-gray-300 cursor-pointer">
      <div class="preview-wrapper">
        <InfographicPreview 
          v-if="infograph.content && showLivePreview"
          :elements="parseContent(infograph.content.canvas_data).elements || []"
          :canvasWidth="infograph.width"
          :canvasHeight="infograph.height"
          :backgroundColor="infograph.background_color || '#ffffff'"
          :backgroundImage="parseContent(infograph.content).backgroundImage"
          :backgroundPatternUrl="parseContent(infograph.content).backgroundPatternUrl"
          :backgroundImageSettings="parseContent(infograph.content).backgroundImageSettings"
          :backgroundPatternSettings="parseContent(infograph.content).backgroundPatternSettings"
        />
        <img
          v-else-if="infograph.preview_image_url"
          :src="infograph.preview_image_url"
          :alt="infograph.title"
          class="preview-image"
        />
        <div v-else class="preview-placeholder">No preview available</div>
      </div>

      <div class="info-section">
        <!-- Title (non-editable in this version) -->
        <div class="title-container">
          <div class="flex-1 flex items-center min-w-0">
            <span class="title">{{ infograph.title }}</span>
          </div>
        </div>

        <!-- Simplified Actions -->
        <div class="actions-container">
          <Button @click="() => showModal = true" class="preview-btn">Preview</Button>
          <Button @click="openEditor" class="edit-btn">Edit</Button>
          <button 
            @click.stop="saveTemplate" 
            class="save-icon-btn" 
            :disabled="isSaving"
            :title="isSaving ? 'Saving...' : 'Save Infograph'"
          >
            <div v-if="isSaving" class="loading-spinner"></div>
            <svg v-else class="save-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path 
                d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z" 
                stroke-width="2" 
                stroke-linecap="round" 
                stroke-linejoin="round"
              />
              <path 
                d="M17 21v-8H7v8M7 3v5h8" 
                stroke-width="2" 
                stroke-linecap="round" 
                stroke-linejoin="round"
              />
            </svg>
            <span v-if="saveSuccess" class="save-success-indicator"></span>
          </button>
        </div>
      </div>

      <div class="dimensions">{{ infograph.width }} x {{ infograph.height }}</div>
    </div>

    <!-- Modal for Full Image Preview -->
    <div v-if="showModal" class="modal-overlay" @click="showModal = false">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">{{ infograph.title }}</h3>
          <button @click="showModal = false" class="close-button">
            <svg class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path
                d="M6 18L18 6M6 6l12 12"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </button>
        </div>
        <div class="modal-content">
          <InfographicPreview 
            :scale="computedScale[`${infograph.width}x${infograph.height}`]"
            v-if="infograph.content && showLivePreview"
            :elements="parseContent(infograph.content.canvas_data).elements || []"
            :canvasWidth="infograph.width"
            :canvasHeight="infograph.height"
            :backgroundColor="infograph.background_color || '#ffffff'"
            :backgroundImage="parseContent(infograph.content).backgroundImage"
            :backgroundPatternUrl="parseContent(infograph.content).backgroundPatternUrl"
            :backgroundImageSettings="parseContent(infograph.content).backgroundImageSettings"
            :backgroundPatternSettings="parseContent(infograph.content).backgroundPatternSettings"
            class="modal-image"
          />
          <img
            v-else-if="infograph.preview_image_url"
            :src="infograph.preview_image_url"
            :alt="infograph.title"
            class="modal-image"
          />
          <div v-else class="modal-placeholder">No preview available</div>
        </div>
        <div class="modal-footer">
          <button 
            @click.stop="saveTemplate" 
            class="save-icon-btn" 
            :disabled="isSaving"
            :title="isSaving ? 'Saving...' : 'Save Infograph'"
          >
            <div v-if="isSaving" class="loading-spinner"></div>
            <svg v-else class="save-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path 
                d="M19 21H5a2 2 0 01-2-2V5a2 2 0 012-2h11l5 5v11a2 2 0 01-2 2z" 
                stroke-width="2" 
                stroke-linecap="round" 
                stroke-linejoin="round"
              />
              <path 
                d="M17 21v-8H7v8M7 3v5h8" 
                stroke-width="2" 
                stroke-linecap="round" 
                stroke-linejoin="round"
              />
            </svg>
            <span v-if="saveSuccess" class="save-success-indicator"></span>
          </button>
          <Button @click="openEditor" class="edit-btn">Edit Design</Button>
          <Button @click="() => showModal = false" class="cancel-btn">Close</Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useDashboardStore } from "@/stores/dashboardStore";
import apiClient from "@/services/apiClient";
import { setupCSRF } from "@/services/apiClient";
import InfographicPreview from "./InfographicPreview.vue";

export default {
  name: "ListTemplateInfographCard",
  
  components: {
    InfographicPreview
  },

  props: {
    infograph: {
      type: Object,
      required: true,
    },
    showLivePreview: {
      type: Boolean,
      default: true
    }
  },

  data() {
    return {
      dashboardStore: useDashboardStore(),
      showModal: false,
      isSaving: false,
      saveSuccess: false,
      saveError: null
      ,
      computedScale: {
        // Scale factors for different infographic widths
        '1000x500': 5,  // For Infographic (800x2000)
        '800x2000': 3,  // For Infographic Letter (1000x500)
        default: 0.2
      }
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
    
    async openEditor() {
      await this.saveTemplate();

      // Force a hard reload to ensure the editor loads with fresh state
      const editorUrl = `/dashboard/editor/${this.infograph.uuid}`;
      window.location.href = editorUrl;
      this.dashboardStore.infographicsCreated = []
    },
    
    async saveTemplate() {
      if (this.isSaving) return;
      
      try {
        this.isSaving = true;
        this.saveError = null;
        this.saveSuccess = false;
        
        // Setup CSRF token
        await setupCSRF();
        
        // Call the API to save the template
        const response = await apiClient.patch(
          `/infos/infographic/${this.infograph.uuid}/save/`,
          {
            is_saved: true
          }
        );
        
        if (response.data) {
          // Refresh the list of saved infographics
          await this.dashboardStore.getInfographics();
          this.saveSuccess = true;
          
          // Show success indicator instead of alert
          setTimeout(() => {
            this.saveSuccess = false;
          }, 3000);
        }
      } catch (error) {
        console.error("Error saving template:", error);
        this.saveError = error.response?.data?.error || "Failed to Save Infograph";
        alert(`Failed to Save Infograph: ${this.saveError}`);
      } finally {
        this.isSaving = false;
      }
    },
  },
};
</script>

<style scoped>
.container {
  width: 350px;
  height: 400px;
  background: white;
  border-radius: 8px;
  padding: 16px;
  position: relative;
  display: flex;
  flex-direction: column;
  transition: all 0.2s;
}

.container:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.preview-wrapper {
  height: 250px;
  width: 100%;
  overflow: hidden;
  border-radius: 4px;
  background-color: #f5f5f5;
  margin-bottom: 16px;
  flex-shrink: 0;
}

.preview-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.preview-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
  font-size: 14px;
}

.info-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.title-container {
  display: flex;
  align-items: center;
  gap: 8px;
  min-height: 28px;
}

.title {
  font-weight: 500;
  font-size: 16px;
  color: #333;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  padding: 3px 5px;
}

.actions-container {
  display: flex;
  gap: 8px;
  margin-top: auto;
}

.preview-btn, .edit-btn {
  flex: 1;
}

.save-icon-btn {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  background-color: var(--primary-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.save-icon-btn:hover {
  background-color: var(--primary-color);
}

.save-icon-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.save-icon {
  width: 16px;
  height: 16px;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.save-success-indicator {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 12px;
  height: 12px;
  background-color: #81C784;
  border: 2px solid white;
  border-radius: 50%;
}

.dimensions {
  position: absolute;
  top: 12px;
  right: 12px;
  font-size: 12px;
  color: #666;
  background-color: #f3f4f6;
  padding: 4px 8px;
  border-radius: 4px;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.75);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 50;
}

.modal-container {
  background-color: white;
  border-radius: 8px;
  max-width: 90vw;
  max-height: 90vh;
  width: auto;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  color: #718096;
  cursor: pointer;
}

.close-button:hover {
  color: #4a5568;
}

.modal-content {
  overflow: auto;
  padding: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex: 1;
}

.modal-image {
  max-width: 100%;
  max-height: 100vh;
  object-fit: contain;
}

.modal-placeholder {
  padding: 48px;
  background-color: #f7fafc;
  border-radius: 8px;
  color: #718096;
  font-size: 16px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  padding: 16px 24px;
  border-top: 1px solid #e2e8f0;
  gap: 12px;
}

.cancel-btn {
  background-color: #e2e8f0;
  color: #4a5568;
}

.cancel-btn:hover {
  background-color: #cbd5e0;
}
</style>