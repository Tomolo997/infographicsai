<template>
  <div class="min-h-screen p-6">
    <!-- Header Section -->
    <div class="flex items-start justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-primary mb-2">Credits</h1>
        <p class="text-md text-text-secondary">
          Purchase credits to create amazing infographics
        </p>
      </div>
    </div>

    <!-- Credits Grid -->
    <div
      class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 max-w-7xl"
    >
      <div
        v-for="pack in creditPacks"
        :key="pack.id"
        @click="handlePurchase(pack)"
        :class="[
          'group cursor-pointer rounded-lg border transition-all duration-300 bg-card-bg',
          pack.isCustom
            ? 'border-card-border hover:shadow-md'
            : 'border-card-border hover:shadow-lg',
        ]"
      >
        <!-- Pack Content -->
        <div class="p-4">
          <!-- Credits Count -->
          <div class="text-center mb-3">
            <div
              v-if="!pack.isCustom"
              class="text-2xl font-bold text-primary mb-1"
            >
              {{ pack.credits }}
            </div>
            <div v-else class="text-xl font-bold text-text-primary mb-1">
              Custom
            </div>
            <div class="text-xs text-text-secondary">
              {{ pack.isCustom ? "Bulk pricing" : "Credits" }}
            </div>
          </div>

          <!-- Price -->
          <div class="text-center mb-3">
            <div
              v-if="!pack.isCustom"
              class="text-2xl font-bold text-text-primary"
            >
              ${{ pack.price }}
            </div>
            <div v-else class="text-sm font-semibold text-text-primary">
              Contact us
            </div>
            <div
              v-if="!pack.isCustom"
              class="text-xs text-text-secondary mt-0.5"
            >
              ${{ pack.price_per_credit }}/credit
            </div>
          </div>

          <!-- CTA Button -->
          <button
            :class="[
              'w-full py-2 rounded-md text-sm font-medium transition-colors',
              pack.isCustom
                ? 'border border-primary-500 text-primary-500 hover:bg-primary-500/10'
                : 'bg-primary-500 text-white',
            ]"
            :disabled="isLoading"
          >
            <span v-if="!isLoading">
              {{ pack.isCustom ? "Contact" : "Purchase" }}
            </span>
            <span v-else class="inline-flex items-center gap-1">
              <svg class="w-3 h-3 animate-spin" fill="none" viewBox="0 0 24 24">
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
              <span class="text-xs">Processing</span>
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import apiClient from "~/client/apiClient";
import { useToastStore } from "~/stores/toast";
import { useRoute } from "vue-router";
definePageMeta({
  layout: "dashboard",
  middleware: "auth",
});

const isLoading = ref(false);
const toastStore = useToastStore();
const route = useRoute();
// Credit packs configuration
const creditPacks = ref([]);

// Fetch credit packs from API (with Stripe price IDs)
const fetchCreditPacks = async () => {
  try {
    const packs = await apiClient.get("/account/credit-packs/");

    creditPacks.value = packs.data;
  } catch (error) {
    console.error("Error fetching credit packs:", error);
    // Continue with default packs if API fails
  }
};

// Handle purchase
const handlePurchase = async (pack) => {
  if (pack.isCustom) {
    // Handle custom pack - open email client
    window.open(
      "mailto:support@ainfographic.com?subject=Custom Credit Pack Inquiry",
      "_blank"
    );
    return;
  }

  try {
    isLoading.value = true;

    // Try to create checkout session with price ID if available
    let response;
    response = await apiClient.post("/account/purchase-credits/", {
      price_id: pack.stripe_price_id,
    });
    window.open(response.data.checkout_url, "_blank");
    return;
  } catch (error) {
    console.error("Error purchasing credits:", error);
    alert(
      error.response?.data?.message ||
        "Failed to initiate purchase. Please try again."
    );
  } finally {
    isLoading.value = false;
  }
};

// Fetch credit packs on mount
onMounted(() => {
  fetchCreditPacks();
  if (route.query.success) {
    toastStore.success("Credits purchased successfully");
  }
  if (route.query.canceled) {
    toastStore.error("Purchase canceled");
  }
});
</script>

<style scoped>
/* Add any custom styles if needed */
</style>
