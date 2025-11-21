<template>
  <div class="editor-section">
    <label>{{ label }}</label>
    <textarea v-model="localContent" @input="updateContent"></textarea>
  </div>
</template>

<script>
export default {
  name: "EditorSection",
  props: {
    label: {
      type: String,
      required: true,
    },
    modelValue: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      localContent: this.modelValue,
    };
  },
  methods: {
    updateContent() {
      this.$emit('update:modelValue', this.localContent);
    },
  },
  watch: {
    modelValue(newValue) {
      this.localContent = newValue;
    },
  },
};
</script>

<style scoped>
.editor-section {
  margin-bottom: 20px;
}
.editor-section label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}
.editor-section textarea {
  width: 100%;
  height: 60px;
  padding: 5px;
  resize: vertical;
}
</style>