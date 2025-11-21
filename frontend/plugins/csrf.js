// plugins/csrf.js
import apiClient, { setupCSRF } from '~/services/apiClient'

export default defineNuxtPlugin(async () => {
  // Only run on client-side
  if (process.client) {
    try {
      // Set up CSRF token when the app initializes
      await setupCSRF()
    } catch (error) {
      console.error('Failed to set up CSRF token:', error)
    }
  }
}) 