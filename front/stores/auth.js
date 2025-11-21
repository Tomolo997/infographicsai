import { defineStore } from 'pinia'
import apiClient from '~/client/apiClient'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    isAuthenticated: false,
    loading: false,
  }),

  getters: {
    isLoggedIn: (state) => state.isAuthenticated,
    currentUser: (state) => state.user,
  },

  actions: {
    async login(credentials) {
      this.loading = true
      try {
        const response = await apiClient.post('/account/api-token-auth/', {
          username: credentials.email,
          password: credentials.password,
        })

        this.token = response.data.token
        this.user = {
          id: response.data.user_id,
          email: response.data.email,
        }
        this.isAuthenticated = true

        if (typeof window !== 'undefined') {
          localStorage.setItem('token', response.data.token)
        }

        const tokenCookie = useCookie('auth-token', {
          maxAge: 60 * 60 * 24 * 7,
        })
        tokenCookie.value = response.data.token

        await navigateTo('/dashboard')
        return response.data
      } catch (error) {
        console.error('Login error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async register(userData) {
      this.loading = true
      try {
        const response = await apiClient.post('/account/signup/', {
          email: userData.email,
          password1: userData.password1,
          password2: userData.password2,
        })

        return {
          success: true,
          message: 'Account created successfully! Please check your email.',
          email: userData.email,
          user: response.data,
        }
      } catch (error) {
        console.error('Registration error:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async logout() {
      try {
        await apiClient.post('/account/logout/')
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.user = null
        this.token = null
        this.isAuthenticated = false

        if (typeof window !== 'undefined') {
          localStorage.removeItem('token')
        }

        const tokenCookie = useCookie('auth-token')
        tokenCookie.value = null

        await navigateTo('/')
      }
    },

    async fetchUser() {
      if (!this.token) {
        console.log('no token')
        if (typeof window !== 'undefined') {
          const storedToken = localStorage.getItem('token')
          if (storedToken) {
            this.token = storedToken
          } else {
            return null
          }
        } else {
          return null
        }
      }

      try {
        const response = await apiClient.get('/account/me/')
        this.user = response.data
        this.isAuthenticated = true
        return response.data
      } catch (error) {
        console.error('Failed to fetch user:', error)
        if (error.response?.status === 401 || error.response?.status === 403) {
          this.logout()
        }
        throw error
      }
    },

    initializeAuth() {
      const tokenCookie = useCookie('auth-token')
      if (tokenCookie.value) {
        this.token = tokenCookie.value

        if (typeof window !== 'undefined') {
          localStorage.setItem('token', tokenCookie.value)
        }

        this.fetchUser()
      } else if (typeof window !== 'undefined') {
        const storedToken = localStorage.getItem('token')
        if (storedToken) {
          this.token = storedToken
          tokenCookie.value = storedToken
          this.fetchUser()
        }
      }
    },
  },
})
