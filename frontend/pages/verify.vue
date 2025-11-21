<template>
  <div class="verification">
    <div v-if="loading">Verifying your account...</div>
    <div v-if="success">Your account has been successfully verified!</div>
    <div v-if="error">
      There was an error verifying your account. Please try again.
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      loading: true,
      success: false,
      error: false,
    };
  },
  async mounted() {
    const uid = this.$route.query.uid;
    const token = this.$route.query.token;

    if (!uid || !token) {
      this.error = true;
      this.loading = false;
      return;
    }

    try {
      const baseUrl = process.env.NODE_ENV === 'production' ? 'https://ainfographic.com/api' : 'http://127.0.0.1:8000/api';
      const response = await fetch(baseUrl + 
        `/account/verify/${uid}/${token}/`
      );

      if (response.status === 200) {
        this.success = true;
      } else {
        this.error = true;
      }
    } catch (e) {
      this.error = true;
    } finally {
      this.loading = false;
    }
  },
};
</script>

<style scoped>
.verification {
  text-align: center;
  margin-top: 50px;
}
</style>
