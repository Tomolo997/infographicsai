<template>
  <div>
    <!-- Button to open the repositioning modal -->
    <button 
      @click="openRepositioningModal" 
      class="reposition-btn"
      v-if="editorStore.backgroundImage"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 3H3v18h18V3z"></path>
        <path d="M21 11H3"></path>
        <path d="M11 3v18"></path>
      </svg>
      Reposition & scale background
    </button>

    <!-- Modal backdrop -->
    <div v-if="isModalOpen" class="modal-backdrop" @click="closeModal">
      <!-- Modal container (stop propagation to prevent closing when clicking inside) -->
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h3>Reposition & scale background</h3>
          <button class="close-btn" @click="closeModal">×</button>
        </div>
        <div class="modal-body">
          <div class="instruction">Click and drag the background to reposition</div>
          
          <!-- Image preview and repositioning area -->
          <div 
            class="preview-container" 
            ref="previewContainer"
            @mousedown="startDrag"
          >
            <div class="preview-image-wrapper">
              <img 
                :src="editorStore.backgroundImage" 
                class="preview-image"
                :style="previewImageStyle"
                @load="onImageLoad"
                ref="previewImage"
              />
            </div>
          </div>
          
          <!-- Scale control -->
          <div class="scale-control">
            <div class="control-label">Scale: {{ Math.round(scale * 100) }}%</div>
            <input 
              type="range" 
              min="50" 
              max="200" 
              v-model.number="scale" 
              class="scale-slider" 
              step="1"
            />
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="closeModal">Cancel</button>
          <button class="apply-btn" @click="applyChanges">Apply</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useEditorStore } from "@/stores/editorStore";

export default {
  name: "BackgroundPositioner",
  setup() {
    const editorStore = useEditorStore();
    return { editorStore };
  },
  data() {
    return {
      isModalOpen: false,
      positionX: 50, // center (%)
      positionY: 50, // center (%)
      scale: 1,
      isDragging: false,
      dragStart: { x: 0, y: 0 },
      positionStart: { x: 50, y: 50 },
      imageLoaded: false,
      imageSize: { width: 0, height: 0 },
      containerSize: { width: 0, height: 0 }
    };
  },
  computed: {
    previewImageStyle() {
      return {
        transform: `translate(-${this.positionX}%, -${this.positionY}%)`,
        width: `${this.scale * 100}%`,
        height: 'auto'
      };
    }
  },
  methods: {
    openRepositioningModal() {
      this.isModalOpen = true;
      
      // Initialize with current settings
      const settings = this.editorStore.backgroundImageSettings;
      this.positionX = parseFloat(settings.positionX) || 50;
      this.positionY = parseFloat(settings.positionY) || 50;
      this.scale = settings.scale || 1;
      
      // Add global event listeners
      setTimeout(() => {
        window.addEventListener('mousemove', this.handleDrag);
        window.addEventListener('mouseup', this.stopDrag);
      }, 100);
    },
    
    closeModal() {
      this.isModalOpen = false;
      this.removeGlobalListeners();
    },
    
    removeGlobalListeners() {
      window.removeEventListener('mousemove', this.handleDrag);
      window.removeEventListener('mouseup', this.stopDrag);
    },
    
    onImageLoad(e) {
      this.imageLoaded = true;
      this.imageSize = {
        width: e.target.naturalWidth,
        height: e.target.naturalHeight
      };
      
      if (this.$refs.previewContainer) {
        const rect = this.$refs.previewContainer.getBoundingClientRect();
        this.containerSize = {
          width: rect.width,
          height: rect.height
        };
      }
    },
    
    startDrag(e) {
      if (!this.imageLoaded) return;
      
      this.isDragging = true;
      this.dragStart = {
        x: e.clientX,
        y: e.clientY
      };
      this.positionStart = {
        x: this.positionX,
        y: this.positionY
      };
      
      // Change cursor during drag
      document.body.style.cursor = 'grabbing';
    },
    
    handleDrag(e) {
      if (!this.isDragging) return;
      
      const container = this.$refs.previewContainer;
      if (!container) return;
      
      const rect = container.getBoundingClientRect();
      
      // Calculate delta as percentage of container size
      const deltaXPercent = ((e.clientX - this.dragStart.x) / rect.width) * 100;
      const deltaYPercent = ((e.clientY - this.dragStart.y) / rect.height) * 100;
      
      // Invert movement direction for more intuitive repositioning 
      // (when you drag right, image moves left)
      this.positionX = Math.max(0, Math.min(100, this.positionStart.x - deltaXPercent));
      this.positionY = Math.max(0, Math.min(100, this.positionStart.y - deltaYPercent));
    },
    
    stopDrag() {
      this.isDragging = false;
      document.body.style.cursor = 'default';
    },
    
    applyChanges() {
      // Update the background image position in the store
      this.editorStore.repositionBackgroundImage(
        this.positionX,
        this.positionY,
        this.scale
      );
      
      this.closeModal();
    }
  },
  beforeUnmount() {
    this.removeGlobalListeners();
  }
}
</script>

<style scoped>
.reposition-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.reposition-btn:hover {
  background-color: #f5f5f5;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-container {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  width: 500px;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.modal-body {
  padding: 16px;
  overflow-y: auto;
}

.instruction {
  font-size: 14px;
  color: #666;
  margin-bottom: 12px;
}

.preview-container {
  position: relative;
  width: 100%;
  height: 300px;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
  cursor: grab;
  background-color: #f5f5f5;
  background-image: linear-gradient(45deg, #e0e0e0 25%, transparent 25%), 
    linear-gradient(-45deg, #e0e0e0 25%, transparent 25%), 
    linear-gradient(45deg, transparent 75%, #e0e0e0 75%), 
    linear-gradient(-45deg, transparent 75%, #e0e0e0 75%);
  background-size: 20px 20px;
  background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
}

.preview-container:active {
  cursor: grabbing;
}

.preview-image-wrapper {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.preview-image {
  position: absolute;
  top: 50%;
  left: 50%;
  max-width: none;
  transform-origin: center;
  pointer-events: none; /* Prevents image from intercepting mouse events */
}

.scale-control {
  margin-top: 16px;
}

.control-label {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  margin-bottom: 8px;
}

.scale-slider {
  width: 100%;
  height: 6px;
  -webkit-appearance: none;
  background: #eee;
  border-radius: 3px;
  outline: none;
}

.scale-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #3B82F6;
  cursor: pointer;
}

.scale-slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #3B82F6;
  cursor: pointer;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px;
  border-top: 1px solid #eee;
}

.cancel-btn {
  padding: 8px 16px;
  background: none;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.apply-btn {
  padding: 8px 16px;
  background-color: #3B82F6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.apply-btn:hover {
  background-color: #2563EB;
}
</style>