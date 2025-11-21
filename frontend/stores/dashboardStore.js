import { defineStore } from "pinia"
import apiClient, { setupCSRF } from "~/services/apiClient"
import { navigateTo } from "#app"

export const useDashboardStore = defineStore("dashboard", {
  state: () => ({
    infographWidht: 1024,
    infographHeight: 1024,
    isCreateInfographicModalOpen: false,
    selectedSize: "Infographic",
    infographicsSaved: [],
    infographicsCreated: [],
    isLoading: false,
  }),
  actions: {
    async createInfograph(templateName = null) {
      try {
        await setupCSRF()

        let endpoint = "/infos/create-infographic/"
        let data = {}

        // If a template name is provided, use the create-from-template endpoint
        if (templateName) {
          endpoint = "/infos/create-from-template/"
          data = { template_name: templateName }
        }

        const response = await apiClient.post(endpoint, data)

        if (response?.data?.infograph_id) {
          await navigateTo(response.data.redirect_url)
        }
      } catch (error) {
        // Handle specific error cases
        if (error.response) {
          console.error("Error creating infographic:", error.response.data)
        }
        throw error // Re-throw for additional handling if needed
      }
    },
    async duplicateInfograph(uuid) {
      try {
        await setupCSRF()

        const response = await apiClient.post(
          `/infos/infographic/${uuid}/duplicate/`
        )

        if (response?.data?.uuid) {
          await navigateTo(response.data.redirect_url)
          return response.data
        }
      } catch (error) {
        // Handle specific error cases
        if (error.response) {
          console.error("Error duplicating infographic:", error.response.data)
        }
        throw error // Re-throw for additional handling if needed
      }
    },
    removeToast(index) {
      this.toasts.splice(index, 1)
    },
    async getInfographics() {
      try {
        this.isLoading = true
        const response = await apiClient.get("/infos/list-infographics/")
        this.infographicsSaved = response.data
        this.error = null
      } catch (error) {
        this.error =
          error.response?.data?.error || "Failed to fetch infographics"
        this.infographicsSaved = []
      } finally {
        this.isLoading = false
      }
    },
    async getSavedInfographics() {
      try {
        this.isLoading = true
        const response = await apiClient.get("/infos/saved-infographics/")
        this.infographicsSaved = response.data
        this.error = null
      } catch (error) {
        this.error =
          error.response?.data?.error || "Failed to fetch infographics"
        this.infographicsSaved = []
      } finally {
        this.isLoading = false
      }
    },
    // New method to fetch only specific infographics by UUIDs
    async getNewInfographics(uuids) {
      if (!uuids || uuids.length === 0) {
        return []
      }

      try {
        this.isLoading = true
        // Convert the UUIDs array to a comma-separated string
        const uuidsParam = uuids.join(",")
        const response = await apiClient.get(
          `/infos/list-infographics/?uuids=${uuidsParam}`
        )

        // Update the store with only the new infographics
        this.infographicsCreated = response.data
        this.error = null
        return response.data
      } catch (error) {
        this.error =
          error.response?.data?.error || "Failed to fetch new infographics"
        return []
      } finally {
        this.isLoading = false
      }
    },
  },
})
