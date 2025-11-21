<template>
  <div class="dropdown-wrapper" ref="dropdownRef">
    <div class="dropdown-trigger" @click="toggleDropdown">
      <slot name="trigger"></slot>
    </div>
    <transition name="fade">
      <div v-if="isOpen" class="dropdown" :style="dropdownStyle">
         <div>
          <div class="text-[12px] py-3 px-3">{{ title }}</div>
          <div class="w-full h-[1px] bg-gray-200"></div>
        </div>
        <div v-for="(item, index) in items" :key="index">
          <NuxtLink
            v-if="item.href"
            :to="item.href"
            class="dropdown-item"
            @click="selectItem(item)"
          >
            <component :is="item.icon" />
            {{ item.label }}
          </NuxtLink>
          <div v-else class="dropdown-item" :class="item.class" @click="handleItemClick(item)">
            <component :is="item.icon" />
            {{ item.label }}
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { useEditorStore } from "@/stores/editorStore";

import { markRaw } from "vue";
export default {
  name: "SimpleDropdown",
  props: {
    items: {
      type: Array,
      required: true,
    },
    positionTop: {
      type: String,
      default: "105%",
    },
    positionLeft: {
      type: String,
      default: "0",
    },
    modelValue: {
      type: [String, Number, Object],
      default: null,
    },
    placeholder: {
      type: String,
      default: "Select an option",
    },
        title: {
      type: String,
      default: "Add text",
    },
  },
  data() {
    return {
      isOpen: false,
          editorStore: useEditorStore(),
    };
  },
  methods: {
    toggleDropdown() {
      this.isOpen = !this.isOpen;
    },
    closeDropdown(event) {
      if (
        this.$refs.dropdownRef &&
        !this.$refs.dropdownRef.contains(event.target)
      ) {
        this.isOpen = false;
      }
    },
    logout() {
    },
    selectItem(item) {
      this.selectedItem = item;
      this.$emit(
        "update:modelValue",
        item.value !== undefined ? item.value : item.label
      );
      this.isOpen = false;
    },
    handleItemClick(item) {
      if (item.action === "logout") {
        this.logout();
      } else {
        this.selectItem(item);
        this.$emit('titleSizeSelected', item.value);
      }
      this.isOpen = false;
    },
  },
  computed: {
    dropdownStyle() {
      return {
        top: this.positionTop,
        left: this.positionLeft,
      };
    },
    processedItems() {
      return this.items.map((item) => ({
        ...item,
        icon: item.icon ? markRaw(item.icon) : null,
      }));
    },
  },
  mounted() {
    document.addEventListener("click", this.closeDropdown);
  },
  beforeUnmount() {
    document.removeEventListener("click", this.closeDropdown);
  },
  watch: {
    modelValue: {
      immediate: true,
      handler(newValue) {
        this.selectedItem =
          this.items.find(
            (item) =>
              (item.value !== undefined && item.value === newValue) ||
              (item.value === undefined && item.label === newValue)
          ) || null;
      },
    },
    isOpen: {
      handler(opened){
        if(!opened){
          this.editorStore.selectedNavigationDesign = null
        }

      }
    }
  },
};
</script>

<style scoped>
.dropdown-wrapper {
  position: relative;
}

.dropdown {
  width: 300px;
  position: absolute;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  z-index: 100;
  padding: 5px;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  color: #050506f5;
  cursor: pointer;
  border-radius: 8px;
}

.dropdown-item:hover {
  background-color: #f2f2f4;
}

.dropdown-item svg {
  margin-right: 8px;
  width: 16px;
  height: 16px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>