<template>
  <div class="min-h-screen p-6">
    <!-- Header Section -->
    <div class="flex items-start justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-primary mb-2">Settings</h1>
        <p class="text-md text-text-secondary">
          Manage your account settings and preferences
        </p>
      </div>
    </div>

    <!-- Settings Grid -->
    <div class="w-full space-y-6">
      <!-- Credits Balance Card -->
      <div class="bg-card-bg border border-card-border rounded-lg p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold text-text-primary">
            Credits Balance
          </h2>
          <button
            @click="navigateTo('/dashboard/credits')"
            class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-primary-500 text-white hover:bg-primary-600 transition-colors text-sm font-medium"
          >
            <svg
              class="w-4 h-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              stroke-width="2"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                d="M12 4v16m8-8H4"
              />
            </svg>
            Buy Credits
          </button>
        </div>
        <div class="flex items-center gap-4">
          <div class="flex-1">
            <div class="text-4xl font-bold text-primary mb-1">
              {{ creditBalance }}
            </div>
            <div class="text-sm text-text-secondary">Available credits</div>
          </div>
          <!-- <div class="text-right">
            <div class="text-sm text-text-secondary mb-1">Last updated</div>
            <div class="text-sm font-medium text-text-primary">
              {{ formatDate(user.value?.last_updated) }}
            </div> -->
          <!-- </div> -->
        </div>
      </div>

      <!-- <div class="bg-card-bg border border-card-border rounded-lg p-6">
        <h2 class="text-lg font-semibold text-text-primary mb-4">
          Change Password
        </h2>
        <form @submit.prevent="handlePasswordChange" class="space-y-4">
          <div>
            <label
              for="current-password"
              class="block text-sm font-medium text-text-primary mb-2"
            >
              Current Password
            </label>
            <div class="relative">
              <input
                id="current-password"
                v-model="passwordForm.currentPassword"
                :type="showCurrentPassword ? 'text' : 'password'"
                class="w-full px-4 py-3 pr-12 bg-background-primary border border-card-border text-text-primary rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all placeholder:text-text-secondary"
                placeholder="Enter current password"
              />
              <button
                type="button"
                @click="showCurrentPassword = !showCurrentPassword"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-text-secondary hover:text-text-primary transition-colors"
              >
                <svg
                  v-if="!showCurrentPassword"
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                  />
                </svg>
                <svg
                  v-else
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                  />
                </svg>
              </button>
            </div>
          </div>

          <div>
            <label
              for="new-password"
              class="block text-sm font-medium text-text-primary mb-2"
            >
              New Password
            </label>
            <div class="relative">
              <input
                id="new-password"
                v-model="passwordForm.newPassword"
                :type="showNewPassword ? 'text' : 'password'"
                class="w-full px-4 py-3 pr-12 bg-background-primary border border-card-border text-text-primary rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all placeholder:text-text-secondary"
                placeholder="Enter new password"
              />
              <button
                type="button"
                @click="showNewPassword = !showNewPassword"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-text-secondary hover:text-text-primary transition-colors"
              >
                <svg
                  v-if="!showNewPassword"
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                  />
                </svg>
                <svg
                  v-else
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                  />
                </svg>
              </button>
            </div>
          </div>

          <div>
            <label
              for="confirm-password"
              class="block text-sm font-medium text-text-primary mb-2"
            >
              Confirm New Password
            </label>
            <div class="relative">
              <input
                id="confirm-password"
                v-model="passwordForm.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                class="w-full px-4 py-3 pr-12 bg-background-primary border border-card-border text-text-primary rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all placeholder:text-text-secondary"
                placeholder="Confirm new password"
              />
              <button
                type="button"
                @click="showConfirmPassword = !showConfirmPassword"
                class="absolute right-4 top-1/2 -translate-y-1/2 text-text-secondary hover:text-text-primary transition-colors"
              >
                <svg
                  v-if="!showConfirmPassword"
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                  />
                </svg>
                <svg
                  v-else
                  class="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
                  />
                </svg>
              </button>
            </div>
          </div>

          <div class="flex justify-end">
            <button
              type="submit"
              :disabled="isChangingPassword"
              class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-primary-500 text-white hover:bg-primary-600 transition-colors text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="!isChangingPassword">Change Password</span>
              <span v-else class="inline-flex items-center gap-2">
                <svg
                  class="w-4 h-4 animate-spin"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    class="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    stroke-width="4"
                  ></circle>
                  <path
                    class="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Changing...
              </span>
            </button>
          </div>
        </form>
      </div> -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import apiClient from "~/client/apiClient";
import { useToastStore } from "~/stores/toast";
import { useAuthStore } from "~/stores/auth";
definePageMeta({
  layout: "dashboard",
  middleware: "auth",
});

const toastStore = useToastStore();
const authStore = useAuthStore();
const user = computed(() => authStore.user);
// State
const creditBalance = ref(0);

// Methods
const formatDate = (date) => {
  if (!date) return "";
  return new Date(date).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
};

const handlePasswordChange = async () => {
  // Validate passwords
  if (!passwordForm.value.currentPassword) {
    alert("Please enter your current password");
    return;
  }
  if (!passwordForm.value.newPassword) {
    alert("Please enter a new password");
    return;
  }
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    alert("New passwords do not match");
    return;
  }
  if (passwordForm.value.newPassword.length < 8) {
    alert("New password must be at least 8 characters long");
    return;
  }

  try {
    isChangingPassword.value = true;
    const { $api } = useNuxtApp();
    await $api("/account/password/change/", {
      method: "POST",
      body: {
        current_password: passwordForm.value.currentPassword,
        new_password: passwordForm.value.newPassword,
      },
    });
    alert("Password changed successfully!");
    // Reset form
    passwordForm.value = {
      currentPassword: "",
      newPassword: "",
      confirmPassword: "",
    };
  } catch (error) {
    console.error("Error changing password:", error);
    alert(
      error.response?.data?.message ||
        "Failed to change password. Please try again."
    );
  } finally {
    isChangingPassword.value = false;
  }
};

// Fetch user data and credit balance on mount
onMounted(async () => {
  creditBalance.value = user.value?.credit_balance || 0;
});
</script>

<style scoped>
/* Add any custom styles if needed */
</style>

