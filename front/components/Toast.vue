<template>
  <Teleport to="body">
    <TransitionGroup
      name="toast"
      tag="div"
      class="fixed top-4 left-1/2 transform -translate-x-1/2 z-50 pointer-events-none flex flex-col items-center gap-3"
    >
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="[
          'pointer-events-auto w-full max-w-md bg-card-bg border rounded-lg shadow-2xl p-4 flex items-start gap-3',
          getToastStyles(toast.type),
        ]"
      >
        <!-- Icon -->
        <div :class="['flex-shrink-0', getIconColor(toast.type)]">
          <!-- Success Icon -->
          <svg
            v-if="toast.type === 'success'"
            xmlns="http://www.w3.org/2000/svg"
            class="w-5 h-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
              clip-rule="evenodd"
            />
          </svg>
          <!-- Error Icon -->
          <svg
            v-else-if="toast.type === 'error'"
            xmlns="http://www.w3.org/2000/svg"
            class="w-5 h-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
              clip-rule="evenodd"
            />
          </svg>
          <!-- Warning Icon -->
          <svg
            v-else-if="toast.type === 'warning'"
            xmlns="http://www.w3.org/2000/svg"
            class="w-5 h-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fill-rule="evenodd"
              d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
              clip-rule="evenodd"
            />
          </svg>
        </div>

        <!-- Message -->
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-text-primary">
            {{ toast.message }}
          </p>
        </div>

        <!-- Close button -->
        <button
          type="button"
          class="flex-shrink-0 text-text-secondary hover:text-text-primary transition-colors p-1 rounded-md hover:bg-white/5"
          @click="removeToast(toast.id)"
          aria-label="Close toast"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-4 w-4"
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
    </TransitionGroup>
  </Teleport>
</template>

<script setup>
import { computed } from 'vue'
import { useToastStore } from '~/stores/toast'

const toastStore = useToastStore()

const toasts = computed(() => toastStore.toasts)

const removeToast = (id) => {
  toastStore.remove(id)
}

const getToastStyles = (type) => {
  const styles = {
    success: 'border-green-200 bg-card-bg',
    error: 'border-red-200 bg-card-bg',
    warning: 'border-yellow-200 bg-card-bg',
  }
  return styles[type] || styles.success
}

const getIconColor = (type) => {
  const colors = {
    success: 'text-green-600',
    error: 'text-red-600',
    warning: 'text-yellow-600',
  }
  return colors[type] || colors.success
}
</script>

<style scoped>
/* Toast enter/leave transitions */
.toast-enter-active {
  transition: all 0.3s ease-out;
}

.toast-leave-active {
  transition: all 0.2s ease-in;
}

.toast-enter-from {
  opacity: 0;
  transform: translateY(-20px) scale(0.95);
}

.toast-enter-to {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.toast-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.toast-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

/* Move transition for reordering */
.toast-move {
  transition: transform 0.3s ease;
}
</style>

