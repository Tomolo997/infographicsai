# GuideLines.vue
<template>
  <div class="alignment-guides">
    <!-- Vertical center guide -->
    <div
      v-show="showCenterGuideX"
      class="guide vertical"
      :style="{ left: `${centerGuideX}px` }"
    ></div>

    <!-- Horizontal center guide -->
    <div
      v-show="showCenterGuideY"
      class="guide horizontal"
      :style="{ top: `${centerGuideY}px` }"
    ></div>
  </div>
</template>

<script>
import { defineComponent, ref, watch } from 'vue';

export default defineComponent({
  name: 'GuideLines',

  props: {
    // Currently dragging element
    element: {
      type: Object,
      required: true
    },
    // Other elements on canvas
    otherElements: {
      type: Array,
      required: true
    }
  },

  setup(props) {
    const THRESHOLD = 5;
    const showCenterGuideX = ref(false);
    const showCenterGuideY = ref(false);
    const centerGuideX = ref(0);
    const centerGuideY = ref(0);

    const checkAlignment = () => {
      // Calculate center of current element
      const elementCenterX = props.element.x + props.element.width / 2;
      const elementCenterY = props.element.y + props.element.height / 2;

      // Reset guides
      showCenterGuideX.value = false;
      showCenterGuideY.value = false;

      // Check alignment with other elements
      props.otherElements.forEach(other => {
        if (other.id === props.element.id) return;

        const otherCenterX = other.x + other.width / 2;
        const otherCenterY = other.y + other.height / 2;

        // Check horizontal center alignment
        if (Math.abs(elementCenterX - otherCenterX) < THRESHOLD) {
          showCenterGuideX.value = true;
          centerGuideX.value = otherCenterX;
        }

        // Check vertical center alignment
        if (Math.abs(elementCenterY - otherCenterY) < THRESHOLD) {
          showCenterGuideY.value = true;
          centerGuideY.value = otherCenterY;
        }
      });
    };

    // Watch for changes in element position
    watch(() => [props.element.x, props.element.y], checkAlignment, { immediate: true });

    return {
      showCenterGuideX,
      showCenterGuideY,
      centerGuideX,
      centerGuideY
    };
  }
});
</script>

<style scoped>
.alignment-guides {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 1000;
}

.guide {
  position: absolute;
  background-color: #4a90e2;
  pointer-events: none;
}

.guide.vertical {
  width: 1px;
  height: 100%;
  transform: translateX(-50%);
}

.guide.horizontal {
  height: 1px;
  width: 100%;
  transform: translateY(-50%);
}
</style>