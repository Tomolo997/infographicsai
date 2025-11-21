<template>
  <div class="preview-canvas-container">
    <div ref="canvasWrapper" class="preview-canvas-wrapper">
      <div class="preview-canvas-centering-wrapper" ref="canvasCenteringWrapper">
        <div
          class="preview-canvas"
          :style="{
            width: `${canvasWidth / 10}px`,
            height: `${canvasHeight / 10}px`,
            backgroundColor: `${store.backgroundPatternUrl ? 'transparent' : store.backgroundColorCanvas}`,
            backgroundImage: backgroundUrl ? `url(${backgroundUrl})` : 'none',
            backgroundSize: backgroundSize,
            backgroundPosition: backgroundPosition,
            backgroundRepeat: `${store.backgroundPatternUrl ? 'repeat' : 'no-repeat'}`,
            backgroundBlendMode: 'normal',
            opacity: store.backgroundPatternSettings.opacity,
          }"
        >
          <!-- Canvas Content -->
          <div class="preview-canvas-content">
            <!-- Render all elements -->
            <div
              v-for="element in store.elements"
              :key="element.id"
              class="preview-canvas-element"
              :style="{
                position: 'absolute',
                left: `${element.x / 10}px`,
                top: `${element.y / 10}px`,
                width: `${element.width / 10}px`,
                height: `${element.height / 10}px`,
                transform: `rotate(${element.rotation || 0}deg)`,
                textAlign: element.textAlign,
                background: 'transparent',
                pointerEvents: 'none',
              }"
            >
              <!-- Element components -->
              <TextElementPreview
                v-if="element.type === 'text'"
                :element="getScaledElement(element)"
                :isDragging="false"
                :ref="`textElement-${element.id}`"
                :preview="true"
              />
              <ShapesElementPreview
                v-else-if="element.type === 'shape'"
                :element="getScaledElement(element)"
                :isDragging="false"
                :ref="`shapeElement-${element.id}`"
                :preview="true"
              />
              <MediaElementPreview
                v-else-if="element.type === 'media'"
                :element="getScaledElement(element)"
                :isDragging="false"
                :ref="`mediaElement-${element.id}`"
                :preview="true"
              />
              <IconElementPreview
                v-else-if="element.type === 'graphic'"
                :element="getScaledElement(element)"
                :isDragging="false"
                :ref="`graphicElement-${element.id}`"
                :preview="true"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useEditorStore } from "@/stores/editorStore";
import TextElement from "./TextElement.vue";
import ShapesElement from "./ShapesElement.vue";
import MediaElement from "./MediaElement.vue";
import IconElement from "./IconElement.vue";
import apiClient from "@/services/apiClient";

export default {
  name: "PreviewCanvasEditor",
  components: {
    TextElement,
    ShapesElement,
    MediaElement,
    IconElement,
  },

  setup() {
    const store = useEditorStore();
    return { store };
  },

  props: {
    uuid: {
      type: String,
      required: true,
    }
  },

  data() {
    return {
      loaded: false
    };
  },

  computed: {
    canvasWidth() {
      return this.store.canvasWidth;
    },
    canvasHeight() {
      return this.store.canvasHeight;
    },
    backgroundUrl() {
      if (this.store.backgroundImage) {
        return this.store.backgroundImage;
      }
      if (this.store.backgroundPatternUrl) {
        return this.store.backgroundPatternUrl;
      }
      return null;
    },
    backgroundSize() {
      if (this.store.backgroundImage) {
        return this.store.backgroundImageSettings.scale === 1
          ? "cover"
          : `${this.store.backgroundImageSettings.scale * 100}%`;
      } else if (this.store.backgroundPatternUrl) {
        if (this.store.backgroundPatternSettings.size === "repeat") {
          return "auto";
        } else if (this.store.backgroundPatternSettings.size === "contain") {
          return "contain";
        } else {
          return this.store.backgroundPatternSettings.size;
        }
      }
      return "cover";
    },
    backgroundPosition() {
      if (this.store.backgroundImage) {
        return this.store.backgroundImageSettings.position === "custom"
          ? `${this.store.backgroundImageSettings.positionX} ${this.store.backgroundImageSettings.positionY}`
          : this.store.backgroundImageSettings.position;
      }
      return "center";
    }
  },

  methods: {
    getScaledElement(element) {
      // Create a copy of the element with scaled dimensions for preview
      const scaledElement = { ...element };
      scaledElement.fontSize = element.fontSize ? element.fontSize / 10 : undefined;
      // Add any other scaling needed for specific element types
      return scaledElement;
    },
    
    async loadPreview() {
      // Load the infographic data using the UUID
      try {
        const response = await this.store.loadInfographic(this.uuid);
        if (response.status === 200) {
          this.loaded = true;
        }
      } catch (error) {
        console.error('Failed to load preview:', error);
      }
    }
  },

  mounted() {
    if (this.uuid) {
      this.loadPreview();
    }
  }
}
</script>

<style scoped>
.preview-canvas-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.preview-canvas-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.preview-canvas-centering-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

.preview-canvas {
  position: relative;
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.preview-canvas-content {
  position: relative;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.preview-canvas-element {
  position: absolute;
  pointer-events: none;
}
</style> 