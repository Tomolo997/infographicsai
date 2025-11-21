<!-- AuthHandler.vue -->
<template>
  <div>Authenticating...</div>
</template>

<script>
import apiClient from '~/services/apiClient';
import { useToastStore } from '~/stores/toast';

export default {
    setup() {
       useHead({
      title: 'Verify | Ainfographic',
      meta: [
        { name: 'description', content: 'This is the verify page of Ainfographic.' },
        { property: 'og:title', content: 'Verify | Ainfographic' },
        { property: 'og:description', content: 'This is the verify page of Ainfographic.' },
        { property: 'og:image', content: 'https://images.ainfographic.com/opengraph.png' },
        { property: 'og:url', content: 'https://ainfographic.com/verify-magic-link' },
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:title', content: 'Verify | Ainfographic' },
        { name: 'twitter:description', content: 'This is the verify page of Ainfographic.' },
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
  mounted() {
    const token = this.$route.query.token;
    if (token) {
      this.verifyMagicLink(token);
    }
  },
  methods: {
    async verifyMagicLink(token) {
      try {
        // Use apiClient instead of fetch for proper CSRF token handling
        const response = await apiClient.post('/account/verify-magic-link/', { token });
        
        // Handle successful authentication
        const data = response.data;
        if (data.token) {
          // Store the token in localStorage
          localStorage.setItem("token", data.token);
          this.$router.push("/dashboard");
        } else {
          this.toastStore.addToast({ message: data.error, type: 'error' });
        }
      } catch (error) {
        console.error('Error verifying magic link:', error);
        this.toastStore.addToast({ 
          message: error.response?.data?.error || 'Failed to verify magic link', 
          type: 'error' 
        });
      }
    },
  },
};
</script>