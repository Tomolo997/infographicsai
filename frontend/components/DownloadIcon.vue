
<template>
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    :width="size" 
    :height="size" 
    viewBox="0 0 24 24"
  >
    <path :fill="color" d="M5 20h14v-2H5zM19 9h-4V3H9v6H5l7 7z"></path>
  </svg>
</template>

<script>
export default {
  name: 'IcBaselineDownload',
  props: {
    size: {
      type: String,
      default: '1em'
    },
    color: {
      type: String,
      default: 'currentColor'
    }
  }
}
</script>