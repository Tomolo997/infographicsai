<template>
  <div class="editor-container">
    <div
      ref="editor"
      contenteditable="true"
      class="editor"
      @input="handleInput"
      @focus="showDropdown"
      @keyup="updateActiveFormats"
      @mouseup="updateActiveFormats"
      :placeholder="placeholder"
      :class="{
        'indirect-editor': indirectEdit,
        'direct-editor': !indirectEdit,
      }"
    ></div>
    <div class="edit-icon"></div>
    <div v-if="isDropdownVisible" class="formatting-dropdown">
      <button
        @mousedown.prevent="applyFormatting('bold')"
        :class="{ active: activeFormats.bold }"
      >
        <strong>B</strong>
      </button>
      <button
        @mousedown.prevent="applyFormatting('italic')"
        :class="{ active: activeFormats.italic }"
      >
        <i>I</i>
      </button>
      <button
        @mousedown.prevent="applyFormatting('underline')"
        :class="{ active: activeFormats.underline }"
      >
        <u>U</u>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "TextEditor",
  props: {
    modelValue: {
      type: String,
      default: "",
    },
    placeholder: {
      type: String,
      default: "Enter text here",
    },
    indirectEdit: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["update:modelValue", "input"],
  data() {
    return {
      isDropdownVisible: false,
      activeFormats: {
        bold: false,
        italic: false,
        underline: false,
      },
    };
  },
  mounted() {
    this.$refs.editor.innerHTML = this.modelValue;
    document.addEventListener("click", this.handleOutsideClick);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.handleOutsideClick);
  },
  watch: {
    modelValue(newValue) {
      if (this.$refs.editor.innerHTML !== newValue) {
        this.$refs.editor.innerHTML = newValue;
      }
    },
  },
  methods: {
    handleInput(event) {
      const newValue = event.target.innerHTML;
      this.$emit("update:modelValue", newValue);
      this.$emit("input", newValue);
    },
    showDropdown() {
      this.isDropdownVisible = true;
      this.updateActiveFormats();
    },
    handleOutsideClick(event) {
      if (!this.$el.contains(event.target)) {
        this.isDropdownVisible = false;
      }
    },
    applyFormatting(format) {
      document.execCommand(format, false, null);
      this.$refs.editor.focus();
      this.handleInput({ target: this.$refs.editor });
      this.updateActiveFormats();
    },
    updateActiveFormats() {
      this.activeFormats.bold = document.queryCommandState("bold");
      this.activeFormats.italic = document.queryCommandState("italic");
      this.activeFormats.underline = document.queryCommandState("underline");
    },
  },
};
</script>

<style scoped>
.editor-container {
  position: relative;
}
.editor {
  border-radius: 8px;
  font-size: 18px;
  text-align: start;
  line-height: 1.5;
  outline: none;
  width: 100%;
  max-width: 100%;
  overflow-wrap: break-word;
  word-wrap: break-word;
}

.editor:focus {
  outline: none;
}
.editor:empty::before {
  content: attr(placeholder);
  color: #888;
}

.formatting-dropdown {
  position: absolute;
  top: 90%;
  left: 0;
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  margin-top: 5px;
  z-index: 100;
  display: flex;
  justify-content: center;
  gap: 4px;
}
.formatting-dropdown button {
  background: none;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  cursor: pointer;
  width: 25px;
  height: 25px;
}
.formatting-dropdown button:hover {
  background: #f0f0f0;
}
.formatting-dropdown button.active {
  background-color: #e0e0e0;
  border-color: #bdbdbd;
}
</style>