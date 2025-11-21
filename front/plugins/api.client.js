export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  
  const api = $fetch.create({
    baseURL: config.public.apiBase,
    onRequest({ request, options }) {
      const tokenCookie = useCookie('auth-token')
      if (tokenCookie.value) {
        options.headers = {
          ...options.headers,
          Authorization: `Token ${tokenCookie.value}`
        }
      }
    },
    onResponseError({ response }) {
      if (response.status === 401) {
        // Clear auth and redirect to login
        const tokenCookie = useCookie('auth-token')
        tokenCookie.value = null
        
        const authStore = useAuthStore()
        authStore.user = null
        authStore.token = null
        authStore.isAuthenticated = false
        
        navigateTo('/login')
      }
    }
  })

  return {
    provide: {
      api
    }
  }
})