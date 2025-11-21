
<template>
  <svg 
    xmlns="http://www.w3.org/2000/svg" 
    :width="size" 
    :height="size" 
    viewBox="0 0 24 24" 
    :fill="color"
  >
    <path d="M7.41 15.41L12 10.83l4.59 4.58L18 14l-6-6l-6 6l1.41 1.41Z"></path>
  </svg>
</template>

<script>
export default {
  name: 'MdiChevronUp',
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