<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="isOpen"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        @click.self="handleBackdropClick"
      >
        <!-- Blurred backdrop -->
        <div
          class="absolute inset-0 bg-black/60 backdrop-blur-sm"
          @click="handleBackdropClick"
        ></div>

        <!-- Modal card -->
        <div
          :class="[
            'relative w-full bg-card-bg border border-card-border rounded-lg shadow-2xl overflow-hidden',
            maxWidth
              ? maxWidth
              : layout === 'two-column'
              ? 'max-w-4xl'
              : 'max-w-md',
          ]"
          role="dialog"
          aria-modal="true"
          :aria-labelledby="titleId"
        >
          <!-- Single Column Layout -->
          <template v-if="layout === 'single-column'">
            <!-- Header -->
            <div class="flex items-start justify-between p-6 pb-4">
              <div class="flex-1">
                <h2
                  :id="titleId"
                  class="text-xl font-semibold text-text-primary mb-1"
                >
                  {{ title }}
                </h2>
                <p v-if="subtitle" class="text-sm text-text-secondary">
                  {{ subtitle }}
                </p>
              </div>

              <!-- Close button -->
              <button
                type="button"
                class="ml-4 text-text-secondary hover:text-text-primary transition-colors p-1 rounded-md hover:bg-white/5"
                @click="closeModal"
                aria-label="Close modal"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>

            <!-- Divider -->
            <div class="border-t border-card-border"></div>

            <!-- Body -->
            <div class="p-6 text-text-primary">
              <slot name="body">
                <!-- Default body content -->
              </slot>
            </div>

            <!-- CTA / Footer -->
            <div v-if="$slots.cta" class="p-6 pt-0">
              <slot name="cta">
                <!-- CTA buttons go here -->
              </slot>
            </div>
          </template>

          <!-- Two Column Layout -->
          <template v-else-if="layout === 'two-column'">
            <div class="flex flex-col md:flex-row">
              <!-- Left Column -->
              <div
                class="md:w-1/2 p-6 border-b md:border-b-0 md:border-r border-card-border"
              >
                <div class="flex items-start justify-between mb-4">
                  <div class="flex-1">
                    <h2
                      :id="titleId"
                      class="text-xl font-semibold text-text-primary mb-1"
                    >
                      {{ title }}
                    </h2>
                    <p v-if="subtitle" class="text-sm text-text-secondary">
                      {{ subtitle }}
                    </p>
                  </div>

                  <!-- Close button -->
                  <button
                    type="button"
                    class="ml-4 text-text-secondary hover:text-text-primary transition-colors p-1 rounded-md hover:bg-white/5"
                    @click="closeModal"
                    aria-label="Close modal"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      class="h-5 w-5"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      stroke-width="2"
                    >
                      <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                </div>

                <!-- Divider -->
                <div class="border-t border-card-border mb-4"></div>

                <!-- Left Body -->
                <div class="text-text-primary">
                  <slot name="left">
                    <!-- Left column content -->
                  </slot>
                </div>
              </div>

              <!-- Right Column -->
              <div class="md:w-1/2 p-6 flex flex-col">
                <!-- Right Body -->
                <div class="flex-1 text-text-primary">
                  <slot name="right">
                    <!-- Right column content -->
                  </slot>
                </div>

                <!-- CTA / Footer -->
                <div v-if="$slots.cta" class="mt-6">
                  <slot name="cta">
                    <!-- CTA buttons go here -->
                  </slot>
                </div>
              </div>
            </div>
          </template>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script>
export default {
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    title: {
      type: String,
      required: true,
    },
    subtitle: {
      type: String,
      default: "",
    },
    layout: {
      type: String,
      default: "single-column",
      validator: (value) => ["single-column", "two-column"].includes(value),
    },
    closeOnBackdropClick: {
      type: Boolean,
      default: true,
    },
    maxWidth: {
      type: String,
      default: "",
    },
  },
  emits: ["close"],
  computed: {
    titleId() {
      return `modal-title-${Math.random().toString(36).substr(2, 9)}`;
    },
  },
  watch: {
    isOpen(newValue) {
      if (newValue) {
        document.body.style.overflow = "hidden";
      } else {
        document.body.style.overflow = "";
      }
    },
  },
  beforeUnmount() {
    document.body.style.overflow = "";
  },
  methods: {
    closeModal() {
      this.$emit("close");
    },
    handleBackdropClick() {
      if (this.closeOnBackdropClick) {
        this.closeModal();
      }
    },
  },
};
</script>

<style scoped>
/* Modal transition effects */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-active .relative,
.modal-leave-active .relative {
  transition: transform 0.2s ease, opacity 0.2s ease;
}

.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.95);
  opacity: 0;
}
</style>

