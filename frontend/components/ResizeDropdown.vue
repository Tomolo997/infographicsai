# Dropdown.vue
<template>
  <div class="relative">
    <slot name="trigger"></slot>
    
    <div v-if="localIsOpen" class="absolute z-50 min-w-[300px] w-full max-w-[1000px] mt-1 bg-white border border-gray-200 rounded-md shadow-lg max-h-[500px] overflow-y-auto">
      <div v-for="(category, idx) in items" :key="idx" class="p-2">
        <h3 class="text-xs font-semibold text-gray-500 px-3 py-2 border-b">
          {{ category.category }}
        </h3>
        <div class="grid grid-cols-1 gap-1">
          <button
            v-for="(item, itemIdx) in category.items"
            :key="itemIdx"
            class="flex items-center justify-between px-3 py-2 hover:bg-gray-50 rounded-md w-full text-left group"
            @click="selectSize(item)"
          >
            <div class="flex items-center gap-3">
              <div 
                class="relative w-8 h-8 border border-gray-200 rounded bg-gray-50 flex items-center justify-center"
                :style="{
                  aspectRatio: `${item.width}/${item.height}`,
                }"
              >
                <div class="absolute inset-0 flex items-center justify-center">
                  <div class="w-full h-full bg-blue-100 opacity-50"></div>
                </div>
              </div>
              <div>
                <div class="text-sm font-medium">{{ item.label }}</div>
                <div v-if="item.width && item.height" class="text-xs text-gray-500">{{ item.width }} x {{ item.height }}px</div>
              </div>
            </div>
            <div class="opacity-0 group-hover:opacity-100 text-xs text-blue-500">
              Select
            </div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    modelValue: String,
    items: {
      type: Array,
      required: true
    },
    placeholder: String,
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  
  emits: ['update:modelValue', 'update:isOpen'],
  
  data() {
    return {
      localIsOpen: false
    }
  },
  
  watch: {
    isOpen(newVal) {
      this.localIsOpen = newVal;
    },
    localIsOpen(newVal) {
      this.$emit('update:isOpen', newVal);
    }
  },
  
  methods: {
    selectSize(item) {
      this.$emit('update:modelValue', item.value)
      this.localIsOpen = false;
      this.$emit('update:isOpen', false);
    },
    
    toggleDropdown() {
      this.localIsOpen = !this.localIsOpen;
      this.$emit('update:isOpen', this.localIsOpen);
    }
  },
  
  created() {
    this.localIsOpen = this.isOpen;
  }
}
</script>