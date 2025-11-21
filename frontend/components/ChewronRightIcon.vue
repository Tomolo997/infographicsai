
<template>
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    :width="size" 
    :height="size" 
    viewBox="0 0 24 24" 
    :fill="color"
  >
    <path d="M8.59 16.58L13.17 12L8.59 7.41L10 6l6 6l-6 6l-1.41-1.42Z"></path>
  </svg>
</template>

<script>
export default {
  name: 'MdiChevronRight',
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