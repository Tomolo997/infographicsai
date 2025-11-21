export default defineNuxtPlugin(async () => {
  const authStore = useAuthStore()
  
  // Initialize auth state from cookie
  authStore.initializeAuth()
})