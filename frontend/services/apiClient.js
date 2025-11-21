// src/services/apiClient.js
import axios from "axios"
const isProduction = process.env.NODE_ENV === "production"
const baseURL = isProduction ? "https://ainfographic.com/api" : "/api" // Changed this to relative URL

const apiClient = axios.create({
  baseURL: baseURL,
  headers: {
    "Content-Type": "application/json",
    "X-CSRFToken": getCookie("csrf_token"),
  },
  withCredentials: true,
})

// Function to get cookie by name
function getCookie(name) {
  if (typeof document === 'undefined') {
    return null;
  }
  
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  
  if (parts.length === 2) {
    return parts.pop().split(';').shift();
  }
  
  return null;
}


// Rest of your interceptor code stays the same
apiClient.interceptors.request.use(
  (config) => {
    if (typeof window !== "undefined") {
      const token = localStorage.getItem("token")
      if (token) {
        config.headers.Authorization = `Token ${token}`
      }
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor to handle CSRF token issues
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    
    // If the error is due to CSRF token issues (403 Forbidden) and we haven't tried to refresh the token yet
    if (error.response && error.response.status === 403 && !originalRequest._retry) {
      originalRequest._retry = true // Mark that we've tried to refresh the token
      
      try {
        // Refresh the CSRF token
        const response = await apiClient.get('/infos/get-csrf/')
        apiClient.defaults.headers['X-CSRFToken'] = response.data.csrf_token
        // Also set the CSRF token in cookies for forms that might need it
        document.cookie = `csrf_token=${response.data.csrf_token}; path=/; SameSite=Lax`;
        
        // Retry the original request with the new token
        return apiClient(originalRequest)
      } catch (refreshError) {
        console.error('Failed to refresh CSRF token:', refreshError)
        return Promise.reject(error)
      }
    }
    
    return Promise.reject(error)
  }
)

// Get CSRF token and set it for all future requests
export async function setupCSRF() {
  // Check if CSRF token is already set
  if (apiClient.defaults.headers['X-CSRFToken']) {
    return // Token already set, no need to fetch again
  }
  
  try {
    const response = await apiClient.get('/infos/get-csrf/')
    apiClient.defaults.headers['X-CSRFToken'] = response.data.csrf_token
  } catch (error) {
    console.error('Error fetching CSRF token:', error)
    // Still allow the application to function even if CSRF token fetch fails
  }
}

// Force refresh the CSRF token
export async function refreshCSRFToken() {
  try {
    const response = await apiClient.get('/infos/get-csrf/')
    apiClient.defaults.headers['X-CSRFToken'] = response.data.csrf_token
    return true
  } catch (error) {
    console.error('Error refreshing CSRF token:', error)
    return false
  }
}

export const getProxyUrl = (path) => {
  return isProduction
    ? `https://ainfographic.com/api/icons/media-proxy/${path}`
    : `http://localhost:8000/api/icons/media-proxy/${path}`
}


export default apiClient
