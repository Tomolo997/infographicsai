<template>
  <div class="infographic-preview-container">
    <div class="infographic-preview-wrapper">
      <div class="infographic-preview-centering-wrapper">
        <div
          class="infographic-preview"
          :style="{
            width: `${(canvasWidth / 10) * scale}px`,
            height: `${(canvasHeight / 10) * scale}px`,
            backgroundColor: `${backgroundPatternUrl ? 'transparent' : backgroundColor}`,
            backgroundImage: backgroundUrl ? `url(${backgroundUrl})` : 'none',
            backgroundSize: backgroundSize,
            backgroundPosition: backgroundPosition,
            backgroundRepeat: `${backgroundPatternUrl ? 'repeat' : 'no-repeat'}`,
            backgroundBlendMode: 'normal',
            opacity: backgroundPatternOpacity,
          }"
        >
          <!-- Canvas Content -->
          <div class="infographic-preview-content">
            <!-- Render all elements -->
            <div
              v-for="element in elements"
              :key="element.id"
              class="infographic-preview-element"
              :style="{
                position: 'absolute',
                left: `${(element.x / 10) * scale}px`,
                top: `${(element.y / 10) * scale}px`,
                width: `${(element.width / 10) * scale}px`,
                height: `${(element.height / 10) * scale}px`,
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
                :preview="true"
              />
              <ShapesElementPreview
                v-else-if="element.type === 'shape'"
                :element="getScaledElement(element)"
                :isDragging="false"
                :preview="true"
              />
              <MediaElementPreview
                v-else-if="element.type === 'media'"
                :element="getScaledElement(element)"
                :isDragging="false"
                :preview="true"
              />
              <IconElementPreview
                v-else-if="element.type === 'graphic'"
                :element="getScaledElement(element)"
                :isDragging="false"
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
import TextElementPreview from "./TextElementPreview.vue";
import ShapesElementPreview from "./ShapesElementPreview.vue";
import MediaElementPreview from "./MediaElementPreview.vue";
import IconElementPreview from "./IconElementPreview.vue";

export default {
  name: "InfographicPreview",
  components: {
    TextElementPreview,
    ShapesElementPreview,
    MediaElementPreview,
    IconElementPreview,
  },

  props: {
    elements: {
      type: Array,
      required: true,
    },
    canvasWidth: {
      type: Number,
      required: true,
    },
    canvasHeight: {
      type: Number,
      required: true,
    },
    backgroundColor: {
      type: String,
      default: "#ffffff"
    },
    backgroundImage: {
      type: String,
      default: null
    },
    backgroundPatternUrl: {
      type: String,
      default: null
    },
    backgroundImageSettings: {
      type: Object,
      default: () => ({
        scale: 1,
        position: "center",
        positionX: "50%",
        positionY: "50%"
      })
    },
    backgroundPatternSettings: {
      type: Object,
      default: () => ({
        size: "auto",
        opacity: 1
      })
    },
    scale: {
      type: Number,
      default: 1,
      validator: value => value > 0 && value <= 10
    }
  },

  computed: {
    backgroundUrl() {
      if (this.backgroundImage) {
        return this.backgroundImage;
      }
      if (this.backgroundPatternUrl) {
        return this.backgroundPatternUrl;
      }
      return null;
    },
    backgroundSize() {
      if (this.backgroundImage) {
        return this.backgroundImageSettings.scale === 1
          ? "cover"
          : `${this.backgroundImageSettings.scale * 100}%`;
      } else if (this.backgroundPatternUrl) {
        if (this.backgroundPatternSettings.size === "repeat") {
          return "auto";
        } else if (this.backgroundPatternSettings.size === "contain") {
          return "contain";
        } else {
          return this.backgroundPatternSettings.size;
        }
      }
      return "cover";
    },
    backgroundPosition() {
      if (this.backgroundImage) {
        return this.backgroundImageSettings.position === "custom"
          ? `${this.backgroundImageSettings.positionX} ${this.backgroundImageSettings.positionY}`
          : this.backgroundImageSettings.position;
      }
      return "center";
    },
    backgroundPatternOpacity() {
      return this.backgroundPatternSettings?.opacity || 1;
    }
  },

  methods: {
    getScaledElement(element) {
      // Create a copy of the element with scaled dimensions for preview
      const scaledElement = { ...element };
      scaledElement.fontSize = element.fontSize ? (element.fontSize / 10) * this.scale : undefined;
      // Add any other scaling needed for specific element types
      return scaledElement;
    }
  }
}
</script>

<style scoped>
.infographic-preview-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.infographic-preview-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.infographic-preview-centering-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

.infographic-preview {
  position: relative;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.infographic-preview-content {
  position: relative;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.infographic-preview-element {
  position: absolute;
  pointer-events: none;
}
</style> 