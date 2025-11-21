<template>
  <div class="container border border-gray-200 hover:border-gray-300">
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
      <!-- Title with edit functionality -->
      <div class="title-container">
        <div class="flex-1 flex items-center min-w-0">
          <span v-if="!isEditing" class="title">{{ infograph.title }}</span>
          <div v-else class="inline-edit-container">
            <input
              v-model="editedTitle"
              @blur="saveTitle"
              @keyup.enter="saveTitle"
              @keyup.esc="cancelEdit"
              ref="titleInput"
              class="title-input"
              type="text"
              :placeholder="infograph.title"
            />
          </div>
        </div>
        <button 
          @click="isEditing ? saveTitle() : startEditing()" 
          class="edit-button"
        >
          <svg
            v-if="!isEditing"
            class="h-4 w-4"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
          >
            <path
              d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"
              stroke-width="2"
            />
            <path
              d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"
              stroke-width="2"
            />
          </svg>
          <svg 
            v-else 
            class="h-4 w-4" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor"
          >
            <path 
              d="M5 13l4 4L19 7" 
              stroke-width="2"
            />
          </svg>
        </button>
      </div>

      <!-- Actions -->
      <div class="actions-container">
        <Button @click="openInfographic" class="edit-btn">Edit Design</Button>
        <Button @click="deleteInfograph" class="delete-btn" :disabled="deleteLoading">
          <!-- Loading spinner -->
          <div v-if="deleteLoading" class="spinner"></div>
          <!-- Delete icon when not loading -->
          <svg
            v-else
            class="h-4 w-4"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
          >
            <path
              d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"
              stroke-width="2"
            />
          </svg>
        </Button>
      </div>
    </div>

    <div class="dimensions">{{ infograph.width }} x {{ infograph.height }}</div>
  </div>
</template>
<script>
import { useDashboardStore } from "@/stores/dashboardStore";
import apiClient from "@/services/apiClient";
import InfographicPreview from "./InfographicPreview.vue";

export default {
  name: "InfographCard",
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
      isEditing: false,
      editedTitle: "",
      dashboardStore: useDashboardStore(),
      deleteLoading: false,
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
    
    startEditing() {
      this.isEditing = true;
      this.editedTitle = this.infograph.title;
      this.$nextTick(() => {
        this.$refs.titleInput?.focus();
      });
    },

    cancelEdit() {
      this.isEditing = false;
      this.editedTitle = this.infograph.title;
    },

    async saveTitle() {
      if (this.editedTitle && this.editedTitle !== this.infograph.title) {
        try {
          // Call the rename endpoint

          const response = await apiClient.patch(
            `/infos/infographic/${this.infograph.uuid}/rename/`,
            { title: this.editedTitle }
          );

          if (response.status === 200) {
            // Update the store
            await this.dashboardStore.getSavedInfographics();
          }
        } catch (error) {
          console.error("Error renaming infographic:", error);
          // Revert to original title on error
          this.editedTitle = this.infograph.title;
        }
      }
      this.isEditing = false;
    },

    async deleteInfograph() {
       try {
          // Set loading state to true
          this.deleteLoading = true;
          
          // Call the delete endpoint
          const response = await apiClient.delete(
            `/infos/infographic/${this.infograph.uuid}/delete/`,
          );

          if (response.status === 200) {
            // Update the store
            await this.dashboardStore.getSavedInfographics();
          }
        } catch (error) {
          console.error("Error deleting infographic:", error);
        } finally {
          // Set loading state to false regardless of success or failure
          this.deleteLoading = false;
        }
    },

    openInfographic() {
      this.dashboardStore.infographicsCreated = []
      this.$router.push(`/dashboard/editor/${this.infograph.uuid}`);
    },
  },
};
</script>

<style scoped>
.container {
  width: 225px;
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
  height: 200px;
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

.inline-edit-container {
  flex: 1;
  min-width: 0;
}

.title-input {
  width: 100%;
  font-size: 16px;
  font-weight: 500;
  padding: 2px 4px;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  outline: none;
  background: white;
}

.edit-button {
  padding: 4px;
  color: #666;
  border-radius: 4px;
  transition: background-color 0.2s;
  flex-shrink: 0;
}

.edit-button:hover {
  background-color: #f3f4f6;
}

.title-container:hover .edit-button {
  opacity: 1;
}

.actions-container {
  display: flex;
  gap: 8px;
  margin-top: auto;
}

.edit-btn {
  flex: 1;
}

.delete-btn {
  padding: 8px;
  color: #dc2626;
}

.delete-btn:hover:not([disabled]) {
  background-color: #fef2f2;
}

.delete-btn[disabled] {
  opacity: 0.7;
  cursor: not-allowed;
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

/* Spinner animation */
.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(220, 38, 38, 0.3);
  border-radius: 50%;
  border-top-color: #dc2626;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>