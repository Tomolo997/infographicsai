<template>
  <div class="min-h-screen p-6">
    <!-- Header Section -->
    <div class="flex items-start justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-primary mb-2">Feedback</h1>
        <p class="text-md text-text-secondary">
          Share your thoughts and help us improve
        </p>
      </div>
    </div>

    <!-- Feedback Form Card -->
    <div class="max-w-4xl">
      <div class="bg-card-bg border border-card-border rounded-lg p-6">
        <form @submit.prevent="handleSubmitFeedback" class="space-y-6">
          <!-- Feedback Type -->
          <div>
            <label
              for="feedback-type"
              class="block text-sm font-medium text-text-primary mb-2"
            >
              Feedback Type
            </label>
            <select
              id="feedback-type"
              v-model="feedbackForm.type"
              class="w-full px-4 py-3 bg-background-primary border border-card-border text-text-primary rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            >
              <option value="">Select feedback type</option>
              <option value="bug">Bug Report</option>
              <option value="feature">Feature Request</option>
              <option value="improvement">Improvement Suggestion</option>
              <option value="other">Other</option>
            </select>
          </div>

          <!-- Subject -->
          <div>
            <label
              for="subject"
              class="block text-sm font-medium text-text-primary mb-2"
            >
              Subject
            </label>
            <input
              id="subject"
              v-model="feedbackForm.subject"
              type="text"
              class="w-full px-4 py-3 bg-background-primary border border-card-border text-text-primary rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all placeholder:text-text-secondary"
              placeholder="Brief summary of your feedback"
              required
            />
          </div>

          <!-- Message -->
          <div>
            <label
              for="message"
              class="block text-sm font-medium text-text-primary mb-2"
            >
              Message
            </label>
            <textarea
              id="message"
              v-model="feedbackForm.message"
              rows="8"
              class="w-full px-4 py-3 bg-background-primary border border-card-border text-text-primary rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all placeholder:text-text-secondary resize-none"
              placeholder="Please provide detailed feedback about your experience, suggestions, or any issues you've encountered..."
              required
            ></textarea>
            <div class="mt-2 text-xs text-text-secondary">
              {{ feedbackForm.message.length }} / 2000 characters
            </div>
          </div>

          <!-- Rating (Optional) -->
          <div>
            <label class="block text-sm font-medium text-text-primary mb-2">
              Overall Experience (Optional)
            </label>
            <div class="flex items-center gap-2">
              <button
                v-for="rating in 5"
                :key="rating"
                type="button"
                @click="feedbackForm.rating = rating"
                :class="[
                  'w-10 h-10 rounded-lg border-2 transition-all',
                  feedbackForm.rating >= rating
                    ? 'border-primary-500 bg-primary-500/10 text-primary-500'
                    : 'border-card-border text-text-secondary hover:border-primary-500/50',
                ]"
              >
                <svg
                  class="w-5 h-5 mx-auto"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"
                  />
                </svg>
              </button>
              <span
                v-if="feedbackForm.rating"
                class="ml-2 text-sm text-text-secondary"
              >
                {{ getRatingLabel(feedbackForm.rating) }}
              </span>
            </div>
          </div>

          <!-- Contact Preference -->
          <div>
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                v-model="feedbackForm.allowContact"
                type="checkbox"
                class="w-4 h-4 text-primary-500 border-card-border rounded focus:ring-primary-500 focus:ring-2"
              />
              <span class="text-sm text-text-primary">
                Allow us to contact you about this feedback
              </span>
            </label>
          </div>

          <!-- Submit Button -->
          <div class="flex justify-end gap-3">
            <button
              type="button"
              @click="resetForm"
              class="inline-flex items-center gap-2 px-4 py-2 rounded-lg border border-card-border bg-card-bg hover:bg-background-secondary transition-colors text-sm font-medium text-text-primary"
            >
              Clear
            </button>
            <button
              type="submit"
              :disabled="isSubmitting || !canSubmit"
              class="inline-flex items-center gap-2 px-4 py-2 rounded-lg bg-primary-500 text-white hover:bg-primary-600 transition-colors text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="!isSubmitting">Submit Feedback</span>
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
                Submitting...
              </span>
            </button>
          </div>
        </form>
      </div>

      <!-- Success Message -->
      <div
        v-if="showSuccess"
        class="mt-6 bg-green-500/10 border border-green-500/30 rounded-lg p-4"
      >
        <div class="flex items-center gap-3">
          <svg
            class="w-5 h-5 text-green-500 flex-shrink-0"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M5 13l4 4L19 7"
            />
          </svg>
          <div>
            <h3 class="text-sm font-semibold text-green-500 mb-1">
              Thank you for your feedback!
            </h3>
            <p class="text-sm text-text-secondary">
              We appreciate you taking the time to share your thoughts with us.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

definePageMeta({
  layout: "dashboard",
  middleware: "auth",
});

// State
const isSubmitting = ref(false);
const showSuccess = ref(false);

// Feedback form
const feedbackForm = ref({
  type: "",
  subject: "",
  message: "",
  rating: 0,
  allowContact: false,
});

// Computed
const canSubmit = computed(() => {
  return (
    feedbackForm.value.subject.trim() &&
    feedbackForm.value.message.trim() &&
    feedbackForm.value.message.length <= 2000
  );
});

// Methods
const getRatingLabel = (rating) => {
  const labels = {
    1: "Poor",
    2: "Fair",
    3: "Good",
    4: "Very Good",
    5: "Excellent",
  };
  return labels[rating] || "";
};

const resetForm = () => {
  feedbackForm.value = {
    type: "",
    subject: "",
    message: "",
    rating: 0,
    allowContact: false,
  };
  showSuccess.value = false;
};

const handleSubmitFeedback = async () => {
  if (!canSubmit.value) return;

  try {
    isSubmitting.value = true;
    const { $api } = useNuxtApp();

    await $api("/feedback/submit/", {
      method: "POST",
      body: {
        type: feedbackForm.value.type || null,
        subject: feedbackForm.value.subject,
        message: feedbackForm.value.message,
        rating: feedbackForm.value.rating || null,
        allow_contact: feedbackForm.value.allowContact,
      },
    });

    // Show success message
    showSuccess.value = true;

    // Reset form after 3 seconds
    setTimeout(() => {
      resetForm();
    }, 3000);
  } catch (error) {
    console.error("Error submitting feedback:", error);
    alert(
      error.response?.data?.message ||
        "Failed to submit feedback. Please try again."
    );
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
/* Add any custom styles if needed */
</style>


