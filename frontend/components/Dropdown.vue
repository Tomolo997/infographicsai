<template>
  <div class="dropdown-wrapper" ref="dropdownRef">
    <div class="dropdown-trigger" @click="toggleDropdown">
      <slot name="trigger"></slot>
    </div>
    <transition name="fade">
      <div v-if="isOpen" class="dropdown" :style="dropdownStyle">
        <div v-for="(item, index) in items" :key="index">
          <NuxtLink
            v-if="item.href"
            :to="item.href"
            class="dropdown-item"
            :style="item.customStyle"
            @click="selectItem(item)"
          >
            <component :is="item.icon" />
            {{ item.label }}
          </NuxtLink>
          <div v-else class="dropdown-item"    :style="item.customStyle" @click="handleItemClick(item)">
            <component :is="item.icon" />
            {{ item.label }}
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import { useAuthStore } from "@/stores/auth";
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
  },
  data() {
    return {
      isOpen: false,
      editorStore: useEditorStore(),
      authStore: useAuthStore()
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
    async logout() {
       await this.authStore.logout()
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
  },
};
</script>

<style scoped>
.dropdown-wrapper {
  position: relative;
}

.dropdown {
  width: max-content;
  min-width: 100%;
  position: absolute;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  z-index: 100;
  padding: 5px;
  overflow: scroll;
  max-height: 400px;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  font-size: 14px;
  font-weight: 300;
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