<template>
  <div class="text-element-preview" 
    :style="{
      fontSize: `${element.fontSize}px`,
      fontFamily: element.fontFamily,
      fontWeight: element.fontWeight,
      fontStyle: element.fontStyle,
      color: element.color,
      textAlign: element.textAlign,
      lineHeight: element.lineHeight,
      textDecoration: element.textDecoration,
      padding: `${element.padding}px`,
      width: '100%',
      height: '100%',
      overflow: 'visible',
      wordBreak: 'break-word',
      userSelect: 'none',
    }">
    {{ element.content }}
  </div>
</template>

<script>
export default {
  name: "TextElementPreview",
  props: {
    element: {
      type: Object,
      required: true
    },
    preview: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.text-element-preview {
  position: relative;
  pointer-events: none;
}
</style>