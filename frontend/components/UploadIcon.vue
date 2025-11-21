
<template>
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    :width="size" 
    :height="size" 
    viewBox="0 0 24 24"
    :fill="color"
  >
    <path d="M9 16v-6H5l7-7l7 7h-4v6H9m-4 4v-2h14v2H5Z"></path>
  </svg>
</template>

<script>
export default {
  name: 'MdiUpload',
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