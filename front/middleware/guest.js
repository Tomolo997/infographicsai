export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore()
  const tokenCookie = useCookie('auth-token')

  // Check if user is logged in via store or has a valid token
  if (authStore.isLoggedIn || tokenCookie.value) {
    return navigateTo('/dashboard')
  }
})
