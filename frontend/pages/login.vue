<template>
  <div>
<div class="flex items-center justify-center p-12">
  <div class="mx-auto w-[350px] bg-white">
    <div class="mb-8 space-y-1 flex flex-col justify-center align-center">
      <h1 class="text-center text-3xl text-gray-700 font-bold">Login to Ainfographic.com</h1>
      <h4 class="text-center text-sm text-gray-700">Or <nuxt-link class="text-primary" to="/signup">create an account</nuxt-link></h4>
    </div>
    <form @submit.prevent="handleLogin">
      <div class="mb-2">
        <label for="email" class="mb-3 block text-base font-medium text-gray-700">Email Address</label>
        <input type="email" name="email" id="email" placeholder="Enter your email" class="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-indigo-500 focus:shadow-md" v-model="email" required />
      </div>
      <div class="mt-8">
        <button class="hover:shadow-form w-full rounded-md bg-primary py-3 px-8 text-center text-base font-semibold text-white outline-none flex items-center justify-center" :disabled="isLoading">
          <svg v-if="isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ isLoading ? 'Sending...' : 'Login with magic link' }}
        </button>
      </div>
      <div class="my-4 flex items-center justify-center">
        <div class="flex items-center justify-center w-full">
          <div class="border-t border-gray-300 flex-grow"></div>
          <span class="mx-4 text-gray-500">or</span>
          <div class="border-t border-gray-300 flex-grow"></div>
        </div>
      </div>
      <div class="mb-2">
        <a :href="googleAuthLink" class="flex items-center justify-center w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-indigo-500 focus:shadow-md">
          <GoogleIcon alt="Google" class="mr-2 h-5 w-5 text-gray-500" />
        </a>
      </div>
    </form>
  </div>
</div>
</div>
</template>

<script>
import { useToastStore } from "~/stores/toast";
import apiClient from "~/services/apiClient";

export default {
  setup() {
     useHead({
      title: 'Login | Ainfographic',
      meta: [
        { name: 'description', content: 'This is the dashboard of Ainfographic.' },
        { property: 'og:title', content: 'Dashboard | Ainfographic' },
        { property: 'og:description', content: 'This is the dashboard of Ainfographic.' },
        { property: 'og:image', content: 'https://images.ainfographic.com/opengraph.png' },
        { property: 'og:url', content: 'https://ainfographic.com/login' },
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:title', content: 'Login | Ainfographic' },
        { name: 'twitter:description', content: 'This is the dashboard of Ainfographic.' },
        { name: 'twitter:image', content: 'https://images.ainfographic.com/opengraph.png' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.svg' }
      ]
    });
    const toastStore = useToastStore();
    definePageMeta({
      layout: 'auth'
    })
    return {
      toastStore
    };
  },
  data() {
    return {
      email: "",
      password: "",
      isLoading: false,
    };
  },
  computed: {
    googleAuthLink() {
      const frontendUrl = process.env.NODE_ENV === 'production' ? 'https://ainfographic.com' : 'http://localhost:8000';
      const clientId =
         "522967994175-ls6959hdgt560ql25a3kuthilpq0eeom.apps.googleusercontent.com";
      const redirectUri = frontendUrl + "/api/account/google/callback/";
      const scope = "profile email";
      const responseType = "code";
      const state = "random_string"; // You can use a random string or CSRF token for security

      return `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=${responseType}&scope=${scope}&state=${state}`;
    },
  },
  methods: {
    handleLogin(e) {
      e.preventDefault();
      this.isLoading = true;
      // Use apiClient which has CSRF token support
      apiClient.post("/account/login-magic-link/", {
        email: this.email,
      })
        .then((response) => {
          if (response.data.message === 'Magic link sent') {
            this.toastStore.addToast({ message: 'Magic link sent to your email', type: 'success' });
          } else {
            this.toastStore.addToast({ message: response.data.error, type: 'error' });
            console.error("Login failed:", response.data.error);
          }
        })
        .catch((error) => {
          if (error.response && error.response.data && error.response.data.error) {
            this.toastStore.addToast({ message: error.response.data.error, type: 'error' });
          } else {
            this.toastStore.addToast({ message: 'An error occurred during login', type: 'error' });
          }
          console.error("Error:", error);
        })
        .finally(() => {
          this.isLoading = false;
        });
    },
    checkAuthentication() {
      const token = localStorage.getItem("token");
   
    },
  },
  mounted() {
    this.checkAuthentication();
  },
};
//http://127.0.0.1:8000/api/account/api-token-auth/
</script>