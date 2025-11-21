<template>
  <transition name="modal-fade">
    <div v-if="isOpen" class="modal-overlay" @click.self="closeModal">
      <div :class="['modal-content', widthSize]">
        <button class="modal-close" @click="closeModal">
          <svg
            width="14"
            height="14"
            viewBox="0 0 14 14"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M13.7 0.3C13.3 -0.1 12.7 -0.1 12.3 0.3L7 5.6L1.7 0.3C1.3 -0.1 0.7 -0.1 0.3 0.3C-0.1 0.7 -0.1 1.3 0.3 1.7L5.6 7L0.3 12.3C-0.1 12.7 -0.1 13.3 0.3 13.7C0.5 13.9 0.7 14 1 14C1.3 14 1.5 13.9 1.7 13.7L7 8.4L12.3 13.7C12.5 13.9 12.8 14 13 14C13.2 14 13.5 13.9 13.7 13.7C14.1 13.3 14.1 12.7 13.7 12.3L8.4 7L13.7 1.7C14.1 1.3 14.1 0.7 13.7 0.3Z"
              fill="black"
            />
          </svg>
        </button>
        <h1 :class="['title', `text-3xl`, 'pl-4 pt-1 pb-2']">{{ title }}</h1>
        <h3 v-if="subTitle" class="text-sm sub-title">
          {{ subTitle }}
        </h3>

        <slot></slot>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: "Modal",
  props: {
    isOpen: {
      type: Boolean,
      default: false,
    },
    title: {
      type: String,
      default: "",
    },
    subTitle: {
      type: String,
      default: "",
    },
    size: {
      type: String,
      default: "medium",
      validator(value) {
        return ["small", "medium", "large", "full-screen"].includes(value);
      },
    },
    titleSize: {
      type: String,
      default: "20px",
    },
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
  },
  computed: {
    subTitleSize() {
      switch (this.size) {
        case "small":
          return "text-xs";
        case "medium":
          return "text-xs";
        case "large":
          return "text-base";
        case "full-screen":
          return "text-xs";
        default:
          return "text-sm";
      }
    },
    widthSize() {
      switch (this.size) {
        case "small":
          return "w-1/4";
        case "medium":
          return "w-1/2";
        case "large":
          return "w-3/4";
        case "full-screen":
          return "w-full";
        default:
          return "w-1/2";
      }
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #fff;
  padding: 14px 10px;
  padding-bottom: 0px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  max-width: 90%;
  height: 90%;
  overflow-y: auto;
  position: relative;
}

.modal-close {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  background: none;
  border: none;
  cursor: pointer;
  color: #999;
}

.modal-close:hover {
  color: #333;
}

.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s;
}

.modal-fade-enter,
.modal-fade-leave-to {
  opacity: 0;
}

.icon-close {
  width: 15px;
  height: 15px;
}
.title {
  text-align: start;
  color: var(--text-color);
  font-weight: 600;
}

.sub-title {
  color: var(--text-color);
  line-height: 1.4;
  opacity: 0.8;
  margin-left: 1rem;
  margin-bottom: 0.5rem;
}
</style>
