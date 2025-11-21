<!-- src/components/Toast.vue -->
<template>
  <div class="fixed top-4 inset-x-0 mx-auto z-50 flex flex-col items-center gap-3 max-w-xs">
    <TransitionGroup name="toast">
      <div
        v-for="toast in toastStore.toasts"
        :key="toast.id"
        class="relative flex items-center px-3 py-2 rounded-lg shadow-md max-w-xs transform transition-all duration-300 border-2"
        :class="[toastTypeClasses[toast.type]]"
      >
        <!-- Icon container -->
        <div class="mr-2">
          <!-- Success icon -->
          <div v-if="toast.type === 'success'" class="bg-green-500 rounded-full p-1.5">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
          </div>
          
          <!-- Info icon -->
          <div v-if="toast.type === 'info'" class="bg-blue-500 rounded-full p-1.5">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          
          <!-- Warning icon -->
          <div v-if="toast.type === 'warning'" class="bg-yellow-500 rounded-full p-1.5">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          
          <!-- Error icon -->
          <div v-if="toast.type === 'error'" class="bg-red-500 rounded-full p-1.5">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </div>
        </div>
        
        <!-- Message -->
        <div class="flex-1">
          <div class="font-semibold text-[13px] text-black">
            {{ toastTitles[toast.type] }}
          </div>
          <div class="text-[13px] text-gray-700 font-light">{{ toast.message }}</div>
        </div>
        
        <!-- Close button -->
        <button 
          @click="toastStore.removeToast(toast.id)"
          class="absolute top-2 right-2 text-gray-400 hover:text-gray-600"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </TransitionGroup>
  </div>
</template>

<script>
import { useToastStore } from '../stores/toast'

export default {
  name: 'Toast',
  
  setup() {
    const toastStore = useToastStore()
    return { toastStore }
  },
  
  data() {
    return {
      toastTypeClasses: {
        success: 'bg-green-50 border-green-200',
        error: 'bg-red-50 border-red-200',
        warning: 'bg-yellow-50 border-yellow-200',
        info: 'bg-blue-50 border-blue-200'
      },
      textColorClasses: {
        success: 'text-green-600',
        error: 'text-red-600',
        warning: 'text-yellow-600',
        info: 'text-blue-600'
      },
      toastTitles: {
        success: 'Congratulations!',
        error: 'Something went wrong!',
        warning: 'Warning!',
        info: 'Did you know?'
      }
    }
  }
}
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateY(-30px);
}

.toast-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}
</style>