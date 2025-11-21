<template>
  <button
    :class="[
      'button py-2 px-4',
      `button--${variant}`,
      `button--weight-${fontWeight}`,
      { 'button--disabled': disabled },
      alignStyle,
      fontSize,
      addedStyle
    ]"
    :disabled="disabled"
    @click="$emit('click')"
  >
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: "Button",
  props: {
    fontSize: {
      type: String,
      default: "text-[12px]",
    },
    alignStyle: {
      type: String,
      default: "justify-center items-center",
    },
    addedStyle:{
        type: String,
      default: "",
    },
    variant: {
      type: String,
      default: "primary",
      validator: (value) =>
        [
          "primary",
          "secondary",
          "secondary-light",
          "secondary-white",
          "primary-inherit",
        ].includes(value),
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    fontWeight: {
      type: String,
      default: "light",
      validator: (value) => ["light", "regular", "semibold"].includes(value),
    },
  },
  emits: ["click"],
};
</script>

<style scoped>
.button {
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
  border: none;
  font-weight: 300; /* Light as base */
  display: flex;
}

.button--weight-light {
  font-weight: 300;
}

.button--weight-regular {
  font-weight: 400;
}

.button--weight-semibold {
  font-weight: 600;
}

.button--primary {
  background-color: rgba(43, 46, 64, 0.06);
  color: rgba(5, 5, 6, 0.96);
}

.button--primary-inherit {
  background-color: inherit;
  text-align: start;
  color: rgba(5, 5, 6, 0.96);
}
.button--primary-inherit-selected {
  background-color: inherit;
  text-align: start;
  color: #3e57da;
}
.button--primary-inherit:hover {
  background-color: rgba(43, 46, 64, 0.06);
}

.button--primary:hover:not(:disabled) {
  background-color: rgba(4, 4, 6, 0.12);
}

.button--primary.button--disabled {
  background-color: rgba(43, 46, 64, 0.02);
  color: rgba(43, 46, 64, 0.2);
  cursor: not-allowed;
}

.button--secondary {
  background-color: #3e57da;
  color: white;
}

.button--secondary:hover:not(:disabled) {
  background-color: #3a4fbb;
}

.button--secondary-light {
  background-color: rgba(61, 91, 251, 0.13);
  color: #3e57da;
}

.button--secondary-white {
  background-color: white;
  color: #3e57da;
}

.button--disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>