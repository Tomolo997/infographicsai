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
              ${{ pack.pricePerCredit }}/credit
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
import { useBillingStore } from "~/stores/billing";

definePageMeta({
  layout: "dashboard",
  middleware: "auth",
});

const billingStore = useBillingStore();
const isLoading = ref(false);

// Credit packs configuration
const creditPacks = ref([
  {
    id: "pack_10",
    credits: 10,
    price: 5,
    pricePerCredit: "0.50",
    stripePriceId: null, // Will be set after running the management command
  },
  {
    id: "pack_50",
    credits: 50,
    price: 25,
    pricePerCredit: "0.50",
    stripePriceId: null,
  },
  {
    id: "pack_100",
    credits: 100,
    price: 45,
    pricePerCredit: "0.45",
    stripePriceId: null,
  },
  {
    id: "pack_200",
    credits: 200,
    price: 89,
    pricePerCredit: "0.45",
    stripePriceId: null,
  },
  {
    id: "pack_custom",
    isCustom: true,
    credits: null,
    price: null,
  },
]);

// Fetch credit packs from API (with Stripe price IDs)
const fetchCreditPacks = async () => {
  try {
    const { $api } = useNuxtApp();
    const packs = await $api("/billing/credits/packs/");
    // Update credit packs with Stripe price IDs from API
    packs.forEach((apiPack) => {
      const localPack = creditPacks.value.find(
        (p) => p.credits === apiPack.credits
      );
      if (localPack) {
        localPack.stripePriceId = apiPack.stripe_price_id;
      }
    });
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
    const { $api } = useNuxtApp();

    // Try to create checkout session with price ID if available
    let response;
    if (pack.stripePriceId) {
      try {
        response = await $api("/billing/credits/checkout/", {
          method: "POST",
          body: {
            price_id: pack.stripePriceId,
            credits: pack.credits,
          },
        });
      } catch (error) {
        console.warn(
          "Checkout endpoint not available, using purchase endpoint"
        );
        // Fallback to purchase endpoint
        response = await billingStore.purchaseCredits(pack.credits);
      }
    } else {
      // Use purchaseCredits method with credit amount
      response = await billingStore.purchaseCredits(pack.credits);
    }

    // Redirect to checkout URL if provided
    if (response?.checkout_url) {
      window.location.href = response.checkout_url;
    } else if (response?.url) {
      // Alternative URL field
      window.location.href = response.url;
    } else if (response?.session_id) {
      // If we have a session ID, construct checkout URL
      // This assumes the backend provides a way to construct the URL
      // Or you can redirect to a backend endpoint that handles the redirect
      window.location.href = `/billing/credits/checkout/${response.session_id}`;
    } else {
      console.error("No checkout URL or session ID in response:", response);
      alert("Failed to initiate checkout. Please contact support.");
    }
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
});
</script>

<style scoped>
/* Add any custom styles if needed */
</style>
