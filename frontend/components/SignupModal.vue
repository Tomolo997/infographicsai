<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h2 class="modal-title">Sign up to continue</h2>
        <button class="close-button" @click="closeModal">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      <div class="modal-body">
        <p class="modal-message">Create a free account to generate your first infographic</p>
        <a :href="googleAuthLink" class="google-button">
          <svg class="google-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M12.24 10.285V14.4h6.806c-.275 1.765-2.056 5.174-6.806 5.174-4.095 0-7.439-3.389-7.439-7.574s3.345-7.574 7.439-7.574c2.33 0 3.891.989 4.785 1.849l3.254-3.138C18.189 1.186 15.479 0 12.24 0c-6.635 0-12 5.365-12 12s5.365 12 12 12c6.926 0 11.52-4.869 11.52-11.726 0-.788-.085-1.39-.189-1.989H12.24z" fill="currentColor" />
          </svg>
          Continue with Google
        </a>
      </div>
      <div class="modal-footer">
        <p class="login-text">Already have an account? <NuxtLink to="/login" class="login-link">Sign in</NuxtLink></p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SignupModal',
  props: {
    isOpen: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    googleAuthLink() {
      const frontendUrl = process.env.NODE_ENV === 'production' ? 'https://ainfographic.com' : 'http://localhost:8000';
      const clientId = "522967994175-ls6959hdgt560ql25a3kuthilpq0eeom.apps.googleusercontent.com";
      const redirectUri = frontendUrl + "/api/account/google/callback/public/";
      const scope = "profile email";
      const responseType = "code";
      const state = "random_string";

      return `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=${responseType}&scope=${scope}&state=${state}`;
    }
  },
  methods: {
    closeModal() {
      this.$emit('close');
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal-content {
  background-color: white;
  border-radius: 12px;
  width: 90%;
  max-width: 400px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.modal-header {
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e5e7eb;
}

.modal-title {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
}

.close-button {
  background: transparent;
  border: none;
  color: #6b7280;
  cursor: pointer;
}

.modal-body {
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.modal-message {
  font-size: 16px;
  color: #4b5563;
  text-align: center;
  margin-bottom: 8px;
}

.google-button {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 16px;
  background-color: white;
  color: #374151;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
}

.google-button:hover {
  background-color: #f9fafb;
  border-color: #9ca3af;
}

.google-icon {
  width: 18px;
  height: 18px;
  margin-right: 12px;
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  color: #6b7280;
  font-size: 14px;
  margin: 8px 0;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid #e5e7eb;
}

.divider span {
  padding: 0 10px;
}

.signup-link {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 12px 16px;
  background-color: #3e57da;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
}

.signup-link:hover {
  background-color: #364fc7;
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #e5e7eb;
  text-align: center;
}

.login-text {
  font-size: 14px;
  color: #6b7280;
}

.login-link {
  color: #3e57da;
  font-weight: 500;
  text-decoration: none;
}

.login-link:hover {
  text-decoration: underline;
}
</style> 