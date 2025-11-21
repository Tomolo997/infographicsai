<template>
  <div class="dropdown-wrapper" ref="dropdownRef">
    <div class="dropdown-trigger" @click="toggleDropdown">
      <slot name="trigger"></slot>
    </div>
    <transition name="fade">
      <div v-if="isOpen" class="dropdown" :style="dropdownStyle">
        <div>
          <div class="text-[12px] py-3 px-3">{{ title }}</div>
          <div class="w-full h-[1px] bg-gray-200"></div>
        </div>
        <div class="p-2">
          <!-- Basic Shapes -->
          <div class="mb-2">
            <div class="text-xs text-gray-500 mb-1 px-2">Basic Shapes</div>
            <div :class="[`grid grid-cols-${gridCols} gap-2`]">
              <div
                v-for="shape in basicShapes"
                :key="shape.type"
                class="shape-item"
                @click="selectShape(shape)"
              >
                <div
                  class="shape-preview"
                  :innerHTML="getShapePreview(shape.type)"
                ></div>
                <div class="shape-name text-xs mt-1">{{ shape.label }}</div>
              </div>
            </div>
          </div>

          <div class="mb-2">
            <div class="text-xs text-gray-500 mb-1 px-2">Lines</div>
            <div :class="[`grid grid-cols-${gridCols} gap-2`]">
              <div
                v-for="shape in lineShapes"
                :key="shape.type"
                class="shape-item"
                @click="selectShape(shape)"
              >
                <div
                  class="shape-preview"
                  :innerHTML="shape.type === 'line' ? getShapePreview(shape.type).replace('stroke-width=\'0\'', 'stroke-width=\'4\'') : getShapePreview(shape.type)"
                ></div>
                <div class="shape-name text-xs mt-1">{{ shape.label }}</div>
              </div>
            </div>
          </div>

          <!-- Special Shapes -->
          <div>
            <div class="text-xs text-gray-500 mb-1 px-2">Special Shapes</div>
            <div :class="[`grid grid-cols-${gridCols} gap-2`]">
              <div
                v-for="shape in specialShapes"
                :key="shape.type"
                class="shape-item"
                @click="selectShape(shape)"
              >
                <div
                  class="shape-preview"
                  :innerHTML="getShapePreview(shape.type)"
                ></div>
                <div class="shape-name text-xs mt-1">{{ shape.label }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { useEditorStore } from "@/stores/editorStore";

export default {
  name: "ShapeDropdown",

  props: {
    title: {
      type: String,
      default: "Add Shape",
    },
    positionTop: {
      type: String,
      default: "105%",
    },
    positionLeft: {
      type: String,
      default: "0",
    },
    gridCols: {
      type: [Number, String],
      default: 4,
    },
  },

  data() {
    return {
      isOpen: false,
      basicShapes: [
        { type: "square", label: "Square" },
        { type: "circle", label: "Circle" },
        { type: "rectangle", label: "Rectangle" },
        { type: "triangle", label: "Triangle" },
        { type: "pentagon", label: "Pentagon" },
        { type: "hexagon", label: "Hexagon" },
        { type: "octagon", label: "Octagon" },
        { type: "star", label: "Star" },
        { type: "starburst", label: "Starburst" },
      ],
      lineShapes: [
        { type: "line", label: "Line", isLine: true },
        // { type: "arrow", label: "Arrow", isLine: true },
      ],
      specialShapes: [
        { type: "cloud", label: "Cloud" },
        { type: "heart", label: "Heart" },
        { type: "message", label: "Message" },
      ],
      editorStore: useEditorStore(),
    };
  },

  computed: {
    dropdownStyle() {
      return {
        top: this.positionTop,
        left: this.positionLeft,
      };
    },
  },

  methods: {
    toggleDropdown() {
      this.isOpen = !this.isOpen;
    },

    closeDropdown(event) {
      if (
        this.$refs.dropdownRef &&
        !this.$refs.dropdownRef.contains(event.target)
      ) {
        this.isOpen = false;
      }
    },

    getShapePreview(type) {
      return this.editorStore.svgShapes[type] || "";
    },

    selectShape(shape) {
      // Add the shape
      const shapeId = this.editorStore.addShapeElement(shape.type);

      // Apply specific settings for lines

      this.$emit("shape-selected", shapeId);
      this.isOpen = false;
    },
  },

  mounted() {
    document.addEventListener("click", this.closeDropdown);
  },

  beforeUnmount() {
    document.removeEventListener("click", this.closeDropdown);
  },
};
</script>

<style scoped>
.dropdown-wrapper {
  position: relative;
  display: inline-block;
}

.dropdown {
  width: 320px;
  position: absolute;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.shape-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 8px;
  cursor: pointer;
  border-radius: 4px;
  color: #050506f5;
}

.shape-item:hover {
  background-color: #f2f2f4;
}

.shape-preview {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.shape-preview :deep(svg) {
  width: 100%;
  height: 100%;
  color: #3e57da;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>