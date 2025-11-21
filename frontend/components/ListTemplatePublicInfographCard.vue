<template>
  <div>
    <!-- Card Component -->
    <div class="container cursor-pointer">
      <div class="preview-wrapper">
        <InfographicPreview
          :scale="4"
          v-if="infograph.content"
          :elements="parseContent(infograph.content.canvas_data).elements || []"
          :canvasWidth="infograph.width"
          :canvasHeight="infograph.height"
          :backgroundColor="infograph.background_color || '#ffffff'"
          :backgroundImage="parseContent(infograph.content).backgroundImage"
          :backgroundPatternUrl="
            parseContent(infograph.content).backgroundPatternUrl
          "
          :backgroundImageSettings="
            parseContent(infograph.content).backgroundImageSettings
          "
          :backgroundPatternSettings="
            parseContent(infograph.content).backgroundPatternSettings
          "
        />
      </div>

      <div class="info-section">
        <div class="actions-container">
          <Button @click="editInfographic" class="edit-btn"
            >Edit</Button
          >
        </div>
      </div>

      <div class="dimensions">
        {{ infograph.width }} x {{ infograph.height }}
      </div>
    </div>

    <!-- Modal for Full Image Preview -->
    <div v-if="showModal" class="modal-overlay" >
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">{{ infograph.title }}</h3>
          <button @click="showModal = false" class="close-button">
            <svg
              class="h-6 w-6"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
            >
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
            :scale="4"
            v-if="infograph.content && showLivePreview"
            :elements="
              parseContent(infograph.content.canvas_data).elements || []
            "
            :canvasWidth="infograph.width"
            :canvasHeight="infograph.height"
            :backgroundColor="infograph.background_color || '#ffffff'"
            :backgroundImage="parseContent(infograph.content).backgroundImage"
            :backgroundPatternUrl="
              parseContent(infograph.content).backgroundPatternUrl
            "
            :backgroundImageSettings="
              parseContent(infograph.content).backgroundImageSettings
            "
            :backgroundPatternSettings="
              parseContent(infograph.content).backgroundPatternSettings
            "
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
          <Button @click="editInfographic" class="edit-btn"
            >Edit</Button
          >
          <Button @click="() => (showModal = false)" class="cancel-btn"
            >Close</Button
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import InfographicPreview from "./InfographicPreview.vue";
import apiClient from "~/services/apiClient";
import { useDashboardStore } from "~/stores/dashboardStore";
import { useAuthStore } from '~/stores/auth';
import { useRouter } from 'vue-router';

export default {
  name: "ListTemplatePublicInfographCard",

  components: {
    InfographicPreview,
  },

  props: {
    infograph: {
      type: Object,
      required: true,
    },
    showLivePreview: {
      type: Boolean,
      default: true,
    },
  },

  setup() {
    const dashboardStore = useDashboardStore();
    const authStore = useAuthStore();
    const router = useRouter();
    
    return {
      dashboardStore,
      authStore,
      router
    };
  },

  data() {
    return {
      showModal: false,
      computedScale: {
        // Scale factors for different infographic widths
        "1000x500": 5, // For Infographic (800x2000)
        "800x2000": 3, // For Infographic Letter (1000x500)
        default: 0.2,
      },
    };
  },

  methods: {
    async subscribe(planId) {
      console.log("Subscribing to plan:", planId);
      try {
        const response = await apiClient.post(
          "/account/public-checkout-session/",
          {
            tier_id: planId,
            coupon_code: true,
          }
        );
        window.location.href = response.data.url;
      } catch (error) {
        console.error("Error subscribing:", error);
      } finally {
      }
    },
    
    async editInfographic() {
      // Check if user is authenticated
      if (!this.authStore.isAuthenticated()) {
        // Redirect to signup if not authenticated
        this.router.push('/signup');
        return;
      }
      
      try {
        if (this.infograph && this.infograph.uuid) {
          // If we have a valid UUID, redirect to editor
          window.location.href = `/dashboard/editor/${this.infograph.uuid}`;
        } 
      } catch (error) {
        console.error("Error redirecting to editor:", error);
      }
    },
    
    parseContent(contentString) {
      if (!contentString) return {};
      try {
        return typeof contentString === "string"
          ? JSON.parse(contentString)
          : contentString;
      } catch (e) {
        console.error("Error parsing infographic content:", e);
        return {};
      }
    },
  },
};
</script>

<style scoped>
.container {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
  transition: all 0.2s;
}

.preview-wrapper {
  flex: 1;
  width: 100%;
  overflow: hidden;
  margin-bottom: 16px;
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

.edit-btn {
  flex: 1;
}

.dimensions {
  position: absolute;
  top: 12px;
  right: 12px;
  font-size: 12px;
  color: #666;
  background-color: rgba(243, 244, 246, 0.7);
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
  max-height: 70vh;
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