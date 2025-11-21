<template>
  <div class="px-8 py-4">
    <div class="flex gap-[5px] flex-col">
      <div class="flex justify-start items-center">
        <span class="text-sm font-semibold flex justify-center items-center"
          >Give feedback</span
        >
      </div>
      <div class="h-[1px] w-full bg-grayBackgroundLight"></div>
    </div>
    
    <div class="mt-6 max-w-2xl">
      <p class="text-sm text-gray-600 mb-4">
        We'd love to hear your thoughts about our product. Your feedback helps us improve!
      </p>
      
      <form @submit.prevent="submitFeedback" class="flex flex-col gap-4">
        <div>
          <label for="title" class="block text-sm font-medium text-gray-700 mb-1">Title</label>
          <input
            id="title"
            v-model="feedbackTitle"
            type="text"
            class="border border-lineColor rounded-md w-full px-3 py-2 outline-primary text-sm"
            placeholder="Brief summary of your feedback"
            required
          />
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="category" class="block text-sm font-medium text-gray-700 mb-1">Category</label>
            <select
              id="category"
              v-model="feedbackCategory"
              class="border border-lineColor rounded-md w-full px-3 py-2 outline-primary text-sm"
              required
            >
              <option value="general">General Feedback</option>
              <option value="usability">Usability</option>
              <option value="feature">Feature Request</option>
              <option value="bug">Bug Report</option>
              <option value="other">Other</option>
            </select>
          </div>
          
          <div>
            <label for="rating" class="block text-sm font-medium text-gray-700 mb-1">Rating (1-5)</label>
            <div class="flex items-center">
              <div class="flex">
                <button 
                  v-for="i in 5" 
                  :key="i"
                  type="button"
                  @click="feedbackRating = i"
                  class="text-2xl focus:outline-none"
                  :class="{ 'text-yellow-400': i <= feedbackRating, 'text-gray-300': i > feedbackRating }"
                >
                  ★
                </button>
              </div>
              <span v-if="feedbackRating" class="ml-2 text-sm text-gray-600">{{ feedbackRating }}/5</span>
            </div>
          </div>
        </div>
        
        <div>
          <label for="feedback" class="block text-sm font-medium text-gray-700 mb-1">Your feedback</label>
          <textarea
            id="feedback"
            v-model="feedbackText"
            rows="5"
            class="border border-lineColor rounded-md w-full px-3 py-2 outline-primary text-sm"
            placeholder="Tell us what you think about our product..."
            required
          ></textarea>
        </div>
        
        <div class="flex items-center gap-3 mt-2">
          <button
            type="submit"
            class="bg-primary hover:bg-primary-dark text-white px-4 py-2 rounded-md text-sm font-medium flex items-center"
            :disabled="isSubmitting"
          >
            <span v-if="isSubmitting">Submitting...</span>
            <span v-else>Submit feedback</span>
          </button>
          
          <span v-if="submitStatus" class="text-sm" :class="submitStatusClass">
            {{ submitStatus }}
          </span>
        </div>
      </form>
      
      <!-- Feedback History Section - Only show if user has previous feedback -->
      <div v-if="previousFeedback.length > 0" class="mt-10">
        <h3 class="text-sm font-semibold mb-3">Your Previous Feedback</h3>
        <div class="h-[1px] w-full bg-grayBackgroundLight mb-4"></div>
        
        <div v-for="feedback in previousFeedback" :key="feedback.id" class="mb-4 p-4 border border-lineColor rounded-md">
          <div class="flex justify-between">
            <h4 class="font-medium">{{ feedback.title }}</h4>
            <span class="text-xs text-gray-500">{{ new Date(feedback.created_at).toLocaleDateString() }}</span>
          </div>
          <div class="flex items-center mt-1 text-sm text-gray-700">
            <span class="bg-gray-100 rounded-md px-2 py-1 text-xs">{{ getCategoryLabel(feedback.category) }}</span>
            <span v-if="feedback.rating" class="ml-2 text-yellow-500">
              {{ '★'.repeat(feedback.rating) }}<span class="text-gray-300">{{ '★'.repeat(5 - feedback.rating) }}</span>
            </span>
          </div>
          <p class="mt-2 text-sm text-gray-600">{{ feedback.text }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from "@/stores/auth";
import { useRoute, useRouter } from "vue-router";
import apiClient from "@/services/apiClient";

export default {
  name: "GiveFeedback",
  async setup() {
    definePageMeta({
      layout: "dashboard",
    });
    const route = useRoute();
    const router = useRouter();
    const authStore = useAuthStore();
    const { user, logout, getUser, fetchUser, isAuthenticated } = authStore;
    const tokenFromQuery = route.query?.token;
    if (tokenFromQuery) {
      authStore.setToken(tokenFromQuery);
      await fetchUser();
    } else {
      if (!isAuthenticated()) {
        await fetchUser();
      }
    }
    return {
      user,
      logout,
      getUser,
      fetchUser,
    };
  },
  data() {
    return {
      feedbackTitle: "",
      feedbackText: "",
      feedbackCategory: "general",
      feedbackRating: 0,
      isSubmitting: false,
      submitStatus: "",
      submitStatusClass: "",
      previousFeedback: [],
    };
  },
  async mounted() {
    this.userInfo = this.getUser();
    await this.fetchPreviousFeedback();
  },
  methods: {
    async submitFeedback() {
      this.isSubmitting = true;
      this.submitStatus = "";
      
      try {
        const response = await apiClient.post("/account/suggest/", {
          title: this.feedbackTitle,
          suggestion: this.feedbackText,
          category: this.feedbackCategory,
          rating: this.feedbackRating || null
        });
        
        this.submitStatus = "Thank you for your feedback!";
        this.submitStatusClass = "text-green-600";
        
        // Clear the form
        this.feedbackTitle = "";
        this.feedbackText = "";
        this.feedbackCategory = "general";
        this.feedbackRating = 0;
        
        // Refresh the feedback history
        await this.fetchPreviousFeedback();
        
        setTimeout(() => {
          this.submitStatus = "";
        }, 5000);
        
      } catch (error) {
        console.error("Error submitting feedback:", error);
        this.submitStatus = error.response?.data?.error || "Failed to submit feedback. Please try again.";
        this.submitStatusClass = "text-red-600";
      } finally {
        this.isSubmitting = false;
      }
    },
    
    async fetchPreviousFeedback() {
      try {
        const response = await apiClient.get("/account/suggest/");
        this.previousFeedback = response.data;
      } catch (error) {
        console.error("Error fetching feedback history:", error);
      }
    },
    
    getCategoryLabel(category) {
      const categories = {
        'general': 'General Feedback',
        'usability': 'Usability',
        'feature': 'Feature Request',
        'bug': 'Bug Report',
        'other': 'Other'
      };
      return categories[category] || category;
    }
  },
};
</script>

<style scoped>
/* Any additional styles can go here */
</style>