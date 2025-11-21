<template>
  <div class="input-container">
    <label :for="id" class="input-label">{{ title }}</label>
    <select
      :id="id"
      v-model="selectedValue"
      class="dropdown-input"
      :placeholder="placeholder"
    >
      <option v-for="option in options" :key="option.value" :value="option.value">
        {{ option.text }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  name: 'DropdownInput',
  props: {
    title: {
      type: String,
      default: 'Select an option'
    },
    placeholder: {
      type: String,
      default: 'Choose...'
    },
    options: {
      type: Array,
      required: true,
      validator: (value) => value.every(option => 'value' in option && 'text' in option)
    },
    modelValue: {
      type: [String, Number],
      default: ''
    }
  },
  computed: {
    selectedValue: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit('update:modelValue', value);
      }
    },
    id() {
      return `dropdown-input-${this._uid}`;
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

.dropdown-input {
  width: 100%;
  padding: 10px;
  font-size:var(--font-size-smaller);
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f8f8f8;
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
  background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%23808080%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E");
  background-repeat: no-repeat;
  background-position: right 10px top 50%;
  background-size: 12px auto;
}

.dropdown-input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
}


.placeholder {
  color: #999;
}

</style>