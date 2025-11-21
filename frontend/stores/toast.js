// src/stores/toast.js
import { defineStore } from "pinia"

export const useToastStore = defineStore("toast", {
  state: () => ({
    toasts: [],
    defaultDuration: 3000,
  }),

  actions: {
    addToast({ type = "info", message, duration = null }) {
      const id = Date.now()
      const toast = {
        id,
        type,
        message,
        duration: duration || this.defaultDuration,
      }

      this.toasts.push(toast)

      // Set timeout to remove toast
      setTimeout(() => {
        this.removeToast(id)
      }, toast.duration)
    },

    removeToast(id) {
      const index = this.toasts.findIndex((toast) => toast.id === id)
      if (index > -1) {
        this.toasts.splice(index, 1)
      }
    },

    // Convenience methods for different toast types
    success(message, duration) {
      this.addToast({
        type: "success",
        message,
        duration,
      })
    },

    error(message, duration) {
      this.addToast({
        type: "error",
        message,
        duration,
      })
    },

    warning(message, duration) {
      this.addToast({
        type: "warning",
        message,
        duration,
      })
    },

    info(message, duration) {
      this.addToast({
        type: "info",
        message,
        duration,
      })
    },

    // Clear all toasts
    clearAll() {
      this.toasts = []
    },
  },
})
