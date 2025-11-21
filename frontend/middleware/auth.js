export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore()


  // If the route requires auth and the user is not authenticated
  if (to.meta.requiresAuth && !authStore.isAuthenticated()) {
    // Redirect to login page
    return navigateTo("/login")
  }
})
