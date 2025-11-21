// src/stores/auth.js
import { defineStore } from "pinia"
import apiClient from "@/services/apiClient"
import { ref } from "vue"
import { useRouter } from "vue-router"

export const useAuthStore = defineStore("auth", () => {
  const user = ref(null)
  const token = ref(null)
  const router = useRouter()
  const subscriptionInfo = ref(null)

  // Initialize token from localStorage if it exists
  if (typeof window !== "undefined") {
    token.value = localStorage.getItem("token") || ""
    if (token.value) {
      apiClient.defaults.headers.common[
        "Authorization"
      ] = `Token ${token.value}`
    }
  }

  const setUser = (userData) => {
    user.value = userData
  }

  const getUser = () => {
    return user.value
  }

  const isAuthenticated = () => {
    return !!user.value
  }

  const setToken = (tokenData) => {
    token.value = tokenData
    if (typeof window !== "undefined") {
      localStorage.setItem("token", tokenData)
    }
    apiClient.defaults.headers.common["Authorization"] = `Token ${tokenData}`
  }

  const login = async (credentials) => {
    try {
      const response = await apiClient.post(
        "/account/api-token-auth/",
        credentials
      )
      setToken(response.data.token)
      await fetchUser()
    } catch (error) {
      console.error("Error logging in:", error)
    }
  }

  const fetchUser = async () => {
    try {
        const response = await apiClient.get("/account/me/")
        setUser(response.data)
    } catch (error) {
      console.error("Error fetching user:", error)
   

        if (typeof window !== "undefined") {
          if (window.location.pathname !== "/") {
            window.location.href = "/login"
          }
        }
    }
  }

  const logout = async () => {
    try {
      await apiClient.post("/account/logout/")
      token.value = ""
      user.value = null
      if (typeof window !== "undefined") {
        localStorage.removeItem("token")
      }
      delete apiClient.defaults.headers.common["Authorization"]
      window.location.href = "/login"
    } catch (error) {
      console.error("Error logging out:", error)
    }
  }

  return {
    user,
    token,
    login,
    logout,
    fetchUser,
    getUser,
    setUser,
    setToken,
    isAuthenticated,
  }
})
