
<template>
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    :width="size" 
    :height="size" 
    viewBox="0 0 24 24" 
    :fill="color"
  >
    <path d="M7.41 8.58L12 13.17l4.59-4.59L18 10l-6 6l-6-6l1.41-1.42Z"></path>
  </svg>
</template>

<script>
export default {
  name: 'MdiChevronDown',
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