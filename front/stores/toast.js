import { defineStore } from 'pinia'

export const useToastStore = defineStore('toast', {
  state: () => ({
    toasts: [],
  }),

  actions: {
    show(message, type = 'success', duration = 5000) {
      const id = Date.now() + Math.random()
      const toast = {
        id,
        message,
        type, // 'success', 'error', 'warning'
        duration,
      }

      this.toasts.push(toast)

      // Auto remove after duration
      if (duration > 0) {
        setTimeout(() => {
          this.remove(id)
        }, duration)
      }

      return id
    },

    success(message, duration = 5000) {
      return this.show(message, 'success', duration)
    },

    error(message, duration = 5000) {
      return this.show(message, 'error', duration)
    },

    warning(message, duration = 5000) {
      return this.show(message, 'warning', duration)
    },

    remove(id) {
      const index = this.toasts.findIndex((toast) => toast.id === id)
      if (index > -1) {
        this.toasts.splice(index, 1)
      }
    },

    clear() {
      this.toasts = []
    },
  },
})

