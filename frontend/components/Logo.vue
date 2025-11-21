<template>
  <span
    :class="textSizeComputed"
    :style="{ width: computedWidth, height: computedHeight,}"
    class="logo-square font-mono flex justify-center items-center text-white"
  >
    AiG
  </span>
</template>

<script setup>
const props = defineProps({
  width: {
    type: String,
    default: "36px",
  },
  height: {
    type: String,
    default: "36px",
  },
  small: {
    type: Boolean,
    default: false,
  },
  big: {
    type: Boolean,
    default: false,
  },
  large: {
    type: Boolean,
    default: false,
  },
});

// Compute the actual width and height based on size props
const computedWidth = computed(() => {
  if (props.small) return "24px";
  if (props.big) return "48px";
  if (props.large) return "64px";
  return props.width;
});

const computedHeight = computed(() => {
  if (props.small) return "24px";
  if (props.big) return "48px";
  if (props.large) return "64px";
  return props.height;
});

// Compute the text size based on the logo size
const textSizeComputed = computed(() => {
  if (props.small) return "text-xs";
  if (props.big) return "text-base";
  if (props.large) return "text-xl";
  return "text-sm";
});

</script>


<style scoped>
.logo-square {
  width: 36px;
  height: 36px;
  background-color: #3e57da;
  border-radius: 2px;
      padding-top: 4px;
}
</style>