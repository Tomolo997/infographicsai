<template>
  <div class="px-8 py-4">
    <div class="flex gap-[5px] flex-col">
      <div class="flex justify-start items-center">
        <span class="text-sm font-semibold flex justify-center items-center"
          >Settings</span
        >
      </div>
      <div class="h-[1px] w-full bg-grayBackgroundLight"></div>

      <!-- Profile Section -->
      <div class="mt-6">
        <h2 class="text-lg font-semibold mb-4">Profile</h2>
        <div class="flex flex-col space-y-4">
          <!-- Profile Picture Display -->
          <div class="flex items-center space-x-4">
            <div class="profile-picture-container">
              <img
                v-if="userProfilePicture && !previewUrl"
                :src="userProfilePicture"
                alt="Profile"
                class="profile-picture"
              />
              <img
                v-else-if="previewUrl"
                :src="previewUrl"
                alt="Preview"
                class="profile-picture preview"
              />
              <div v-else class="profile-picture-placeholder">
                <svg
                  class="placeholder-icon"
                  fill="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
                  />
                </svg>
              </div>
            </div>

            <!-- Upload Controls -->
            <div class="flex flex-col space-y-2">
              <input
                type="file"
                id="profile-picture"
                class="file-input"
                @change="handleFileUpload"
                accept="image/*"
              />
              <label
                for="profile-picture"
                :class="[
                  'file-upload-label',
                  { 'opacity-50 cursor-not-allowed': isUploading },
                ]"
                :disabled="isUploading"
              >
                <svg
                  v-if="!isUploading"
                  class="upload-icon"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                  />
                </svg>
                <span v-if="isUploading" class="spinner"></span>
                {{ isUploading ? "Uploading..." : "Choose Picture" }}
              </label>
            </div>
          </div>

          <!-- Preview Controls -->
          <div v-if="previewUrl" class="flex space-x-2">
            <button
              @click="uploadProfilePicture"
              :disabled="isUploading"
              class="btn btn-primary"
            >
              {{ isUploading ? "Uploading..." : "Save Picture" }}
            </button>
            <button
              @click="cancelUpload"
              :disabled="isUploading"
              class="btn btn-secondary"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>

      <!-- Subscription Section -->
      <div class="mt-8">
        <h2 class="text-lg font-semibold mb-4">Subscription</h2>

        <!-- Current Subscription Info -->
        <div
          v-if="subscriptionInfo && subscriptionInfo.tier_name !== 'Free'"
          class="bg-white rounded-lg shadow p-6 mb-6"
        >
          <div class="flex justify-between items-center mb-4">
            <div>
              <h3 class="text-xl font-semibold">
                {{ subscriptionInfo.tier_name }}
              </h3>
              <p class="text-gray-600">Status: {{ subscriptionInfo.status }}</p>
            </div>
            <div class="text-right">
              <p class="text-sm text-gray-600">
               
                <div v-if="subscriptionInfo.downloads_remaining === 999999"> Downloads: Unlimited</div>
                <div v-else>
                  Downloads: {{ subscriptionInfo.downloads_remaining }} /
                  {{ subscriptionInfo.monthly_download_limit }}
                </div>
              </p>
              <p class="text-sm text-gray-600">
                AI Credits this month: {{ subscriptionInfo.credits_remaining }} /
                {{ subscriptionInfo.ai_credits }}
              </p>
            </div>
          </div>

          <!-- Subscription Actions -->
          <div class="flex gap-4 mt-4">
            <button
              v-if="subscriptionInfo.status === 'active'"
              @click="cancelSubscription"
              class="btn btn-secondary"
            >
              Cancel Subscription
            </button>
            <button
              v-if="subscriptionInfo.status === 'canceling'"
              @click="reactivateSubscription"
              class="btn btn-primary"
            >
              Reactivate Subscription
            </button>
            <button
              v-if="availableUpgrades.length > 0 && subscriptionInfo.status !== 'canceling'"
              @click="showUpgradeModal = true"
              class="btn btn-primary"
            >
              Upgrade Plan
            </button>
          </div>
        </div>

        <!-- Subscribe Section (if no active subscription) -->
        <div v-else class="bg-white rounded-lg shadow p-6">
          <h3 class="text-xl font-semibold mb-4">Choose a Plan</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div
              v-for="plan in availableUpgrades"
              :key="plan.id"
              class="border rounded-lg p-6 hover:shadow-lg transition-shadow"
            >
              <h4 class="text-lg font-semibold">{{ plan.name }}</h4>
              <p class="text-2xl font-bold my-4">
                ${{ plan.price }}<span class="text-sm text-gray-600">{{ plan.name === 'Lifetime' ? ' one-time' : '/month' }}</span>
              </p>
              <ul class="space-y-2 mb-6">
                <li>{{ plan.monthly_download_limit === 999999 ? 'Unlimited' : plan.monthly_download_limit }} Downloads/month</li>
                <li>{{ plan.ai_credits }} AI Credits</li>
              </ul>
              <button
                @click="subscribe(plan.id)"
                class="btn btn-primary w-full"
              >
                {{ plan.name === 'Lifetime' ? 'Get Lifetime' : 'Subscribe' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Upgrade Modal -->
    <Transition name="modal">
      <div
        v-if="showUpgradeModal"
        class="modal-overlay"
        @click.self="showUpgradeModal = false"
      >
        <div class="modal-content">
          <h3 class="text-xl font-semibold mb-4">Upgrade Your Plan</h3>
          <div class="space-y-4">
            <div
              v-for="tier in availableUpgrades"
              :key="tier.id"
              class="credit-pack cursor-pointer hover:bg-gray-50"
              @click="upgradeTo(tier.id)"
            >
              <div>
                <h4 class="font-semibold">{{ tier.name }}</h4>
                <p class="text-sm text-gray-600">{{ tier.description }}</p>
              </div>
              <p class="font-semibold">${{ tier.price }}{{ tier.name.toLowerCase() !== 'lifetime' ? '/month' : '' }}</p>
            </div>
          </div>
          <div class="mt-6 flex justify-end">
            <button @click="showUpgradeModal = false" class="btn btn-secondary">
              Cancel
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script>
import { useAuthStore } from "@/stores/auth";
import { useRoute, useRouter } from "vue-router";
import apiClient from "@/services/apiClient";
import { useToastStore } from "~/stores/toast";

export default {
  name: "settings",
  async setup() {
    definePageMeta({
      layout: "dashboard",
    });
    const toastStore = useToastStore();
    const authStore = useAuthStore();
    const { user, logout, getUser, fetchUser } = authStore;
    const router = useRouter();
    const route = useRoute();
    return {
      logout,
      getUser,
      fetchUser,
      user,
      router,
      route,
      toastStore,
    };
  },
  data() {
    return {
      userInfo: null,
      selectedFile: null,
      userProfilePicture: null,
      previewUrl: null,
      isProcessing: false,
      showBuyCreditsModal: false,
      showUpgradeModal: false,
      creditPacks: [],
      subscriptionInfo: null,
      isEverythingLoading: false,
      availableUpgrades: [],
      isUploading: false,
      subscriptionPlans: {
        basic: { id: 10 }, // Replace with your actual tier IDs
        premium: { id: 11 },
        lifetime: { id: 12 },
      },
    };
  },
  async mounted() {
    try {
      this.isEverythingLoading = true;
      await this.fetchSubscriptionStatus();
      this.userInfo = this.getUser();
      this.userProfilePicture = this.userInfo?.profile_picture_url;
      this.isEverythingLoading = false;
      if (this.route.query.session_id) {
        this.handleStripeRedirect();
      }
    } catch (error) {
      this.isEverythingLoading = false;
    }
  },
  methods: {
    async fetchSubscriptionStatus() {
      try {
        const response = await apiClient.get("/account/subscription-status/");
        console.log(response.data);
        this.subscriptionInfo = response.data.subscription;
        if (
          response.data.has_subscription &&
          !this.subscriptionInfo.is_lifetime
        ) {
          await this.fetchAvailableUpgrades();
        }
      } catch (error) {
        this.toastStore.error("Failed to fetch subscription status");
      }
    },
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (!file) return;

      // Validate file type
      if (!file.type.startsWith("image/")) {
        this.toastStore.error("Please select an image file");
        return;
      }

      // Validate file size (5MB limit)
      const maxSize = 5 * 1024 * 1024; // 5MB in bytes
      if (file.size > maxSize) {
        this.toastStore.error("File size should not exceed 5MB");
        return;
      }

      this.selectedFile = file;
      this.createPreview(file);
    },

    createPreview(file) {
      // Revoke previous preview URL to prevent memory leaks
      if (this.previewUrl) {
        URL.revokeObjectURL(this.previewUrl);
      }

      // Create new preview URL
      this.previewUrl = URL.createObjectURL(file);
    },
    cancelUpload() {
      // Clear preview and selected file
      if (this.previewUrl) {
        URL.revokeObjectURL(this.previewUrl);
      }
      this.previewUrl = null;
      this.selectedFile = null;

      // Reset the file input
      const fileInput = document.getElementById("profile-picture");
      if (fileInput) fileInput.value = "";
    },

    async uploadProfilePicture() {
      if (!this.selectedFile) return;

      this.isUploading = true;
      const formData = new FormData();
      formData.append("file", this.selectedFile);

      try {
        const response = await apiClient.post(
          "/account/upload-profile-picture/",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        );

        this.userProfilePicture = response.data.profile_picture_url;
        this.toastStore.success("Profile picture updated successfully");

        // Clear the preview and selected file
        URL.revokeObjectURL(this.previewUrl);
        this.previewUrl = null;
        this.selectedFile = null;

        // Reset the file input
        const fileInput = document.getElementById("profile-picture");
        if (fileInput) fileInput.value = "";
      } catch (error) {
        this.toastStore.error(
          error.response?.data?.error || "Failed to upload profile picture"
        );
      } finally {
        this.isUploading = false;
      }
    },

    async fetchAvailableUpgrades() {
      try {
        const response = await apiClient.get("/account/available-upgrades/");
        this.availableUpgrades = response.data.available_upgrades;

      } catch (error) {
        this.toastStore.error("Failed to fetch available upgrades");
      }
    },

    async subscribe(planId) {
      this.isProcessing = true;
      try {
        const response = await apiClient.post(
          "/account/create-checkout-session/",
          {
            tier_id: planId,
          }
        );
        window.location.href = response.data.url;
      } catch (error) {
        this.toastStore.error("Failed to initiate subscription");
      } finally {
        this.isProcessing = false;
      }
    },

    async upgradeTo(tierId) {
      this.isProcessing = true;
      try {
        const response = await apiClient.post(
          "/account/upgrade-subscription/",
          {
            tier_id: tierId,
          }
        );
        window.location.href = response.data.url;
      } catch (error) {
        this.toastStore.error("Failed to initiate upgrade");
      } finally {
        this.isProcessing = false;
        this.showUpgradeModal = false;
      }
    },

    async cancelSubscription() {
      if (!confirm("Are you sure you want to cancel your subscription?"))
        return;

      try {
        await apiClient.post("/account/cancel-subscription/");
        this.toastStore.success(
          "Subscription will be canceled at the end of the billing period"
        );
        await this.fetchSubscriptionStatus();
      } catch (error) {
        this.toastStore.error("Failed to cancel subscription");
      }
    },

    async reactivateSubscription() {
      try {
        await apiClient.post("/account/reactivate-subscription/");
        this.toastStore.success("Subscription reactivated successfully");
        await this.fetchSubscriptionStatus();
      } catch (error) {
        this.toastStore.error("Failed to reactivate subscription");
      }
    },

    async handleStripeRedirect() {
      // Handle successful Stripe redirect
      this.toastStore.success("Payment processed successfully!");
      await this.fetchSubscriptionStatus();
      // Remove query parameter
      this.router.replace({ query: {} });
    },

    // ... your existing methods ...
  },
  beforeUnmount() {
    // Clean up any preview URLs when component is destroyed
    if (this.previewUrl) {
      URL.revokeObjectURL(this.previewUrl);
    }
  },
};
</script>

<style scoped>
.profile-picture-container {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #e5e7eb;
  position: relative;
}

.profile-picture {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: all 0.3s ease;
}

.profile-picture.preview {
  opacity: 0.8;
}

.profile-picture-placeholder {
  width: 100%;
  height: 100%;
  background-color: #e5e7eb;
  display: flex;
  justify-content: center;
  align-items: center;
}

.placeholder-icon {
  width: 48px;
  height: 48px;
  color: #9ca3af;
}

.file-upload-label {
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  background-color: #4f46e5;
  color: white;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.875rem;
}

.file-upload-label:hover:not(:disabled) {
  background-color: #4338ca;
}

.file-upload-label:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.upload-icon {
  width: 20px;
  height: 20px;
  margin-right: 0.5rem;
}

.spinner {
  width: 20px;
  height: 20px;
  margin-right: 0.5rem;
  border: 2px solid #ffffff;
  border-top: 2px solid transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.file-input {
  display: none;
}

.btn {
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-primary {
  background-color: #4f46e5;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background-color: #4338ca;
}

.btn-secondary {
  background-color: #6b7280;
  color: white;
}

.btn-secondary:hover:not(:disabled) {
  background-color: #4b5563;
}

.profile-container {
  font-family: "Inter", sans-serif;
}

.file-input {
  display: none;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  padding: 2rem;
  border-radius: 0.5rem;
  max-width: 28rem;
  width: 100%;
}

.credit-pack {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
}

/* Modal transition */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s;
}
.modal-enter,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}
</style>