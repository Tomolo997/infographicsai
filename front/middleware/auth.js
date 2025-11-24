export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore()
  const tokenCookie = useCookie('auth-token')

  // Allow access if there's a token in query params (from OAuth redirect)
  if (to.query.token) {
    return
  }

  // Check if user is not logged in and has no valid token
  if (!authStore.isLoggedIn && !tokenCookie.value) {
    return navigateTo('/login')
  }
})
