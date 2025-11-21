<template>
  <div class="input-container">
    <label :for="id" class="input-label">{{ title }}</label>
    <input
      :type="'url'"
      :id="id"
      v-model="inputValue"
      class="url-input"
      :placeholder="placeholder"
    />
  </div>
</template>

<script>
export default {
  name: 'URLInput',
  props: {
    title: {
      type: String,
      default: 'Url'
    },
    placeholder: {
      type: String,
      default: 'https://www.example.com'
    },
    modelValue: {
      type: String,
      default: ''
    }
  },
  computed: {
    inputValue: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit('update:modelValue', value);
      }
    },
    id() {
      return `url-input-${this._uid}`;
    }
  }
}
</script>

<style scoped>
.input-container {
  font-family: Arial, sans-serif;
  width: 100%;
  max-width: 400px;
}

.input-label {
  display: block;
  font-size: var(--font-size-smaller);
  margin-bottom: 2px;
  color: #333;
}

.url-input {
  width: 100%;
  padding: 10px;
  font-size: var(--font-size-small);
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f8f8f8;
}

.url-input::placeholder {
  color: #999;
}

.url-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}
</style>