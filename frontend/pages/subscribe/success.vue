<template>
  <div class="subscription-success-container">
    <div class="success-state">
      <div class="success-icon">✓</div>
      <h2>Subscription Successful!</h2>
      <p>Your payment was processed successfully.</p>
      
      <!-- For new users -->
      <div v-if="!isLoggedIn" class="message-box">
        <h3>Check your email</h3>
        <p>We've sent you a login link to access your new account. Please check your email inbox and click the login link to get started.</p>
        <p class="note">If you don't see the email, please check your spam folder.</p>
      </div>
      
      <!-- For existing users who are already logged in -->
      <div v-else class="message-box">
        <h3>Your subscription is now active</h3>
        <p>Your account has been updated with your new subscription benefits.</p>
      </div>
      
      <div class="button-container">
        <NuxtLink v-if="isLoggedIn" to="/dashboard" class="primary-button">
          Go to Dashboard
        </NuxtLink>
        <NuxtLink v-else to="/login" class="secondary-button">
          Login
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

useHead({
  title: 'Subscription Success | Ainfographic',
  meta: [
    { name: 'description', content: 'Your subscription to Ainfographic was successful!' },
  ],
  link: [
    { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }
  ]
});

const isLoggedIn = ref(false);

onMounted(() => {
  // Check if user is already logged in
  const token = localStorage.getItem('token');
  isLoggedIn.value = !!token;
});
</script>

<style scoped>
.subscription-success-container {
  max-width: 600px;
  margin: 50px auto;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  background-color: white;
  text-align: center;
}

.success-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.success-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px;
  height: 60px;
  border-radius: 50%;
  margin-bottom: 20px;
  font-size: 32px;
  background-color: #d1fae5;
  color: #059669;
}

h2 {
  font-size: 24px;
  margin-bottom: 16px;
  color: #111827;
}

p {
  color: #4b5563;
  margin-bottom: 10px;
}

.message-box {
  background-color: #f9fafb;
  border-radius: 8px;
  padding: 20px;
  margin: 20px 0;
  text-align: left;
}

.message-box h3 {
  font-size: 18px;
  margin-bottom: 10px;
  color: #111827;
}

.note {
  font-size: 14px;
  color: #6b7280;
  font-style: italic;
}

.button-container {
  margin-top: 20px;
}

.primary-button, .secondary-button {
  display: inline-block;
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s ease;
}

.primary-button {
  background-color: var(--primary-color, #4f46e5);
  color: white;
}

.primary-button:hover {
  background-color: var(--primary-hover, #4338ca);
}

.secondary-button {
  background-color: white;
  color: var(--primary-color, #4f46e5);
  border: 1px solid var(--primary-color, #4f46e5);
}

.secondary-button:hover {
  background-color: #f9fafb;
}
</style>