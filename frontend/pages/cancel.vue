<template>
  <div class="cancel-container">
    <h1>Subscription Not Completed</h1>
    <p>You have cancelled the subscription process.</p>
    <p>If you have any questions or need assistance, please contact our support team.</p>
    <router-link to="/">Return to Home</router-link>
  </div>
</template>

<script>
export default {
  name: 'CancelSubscription',
  
  data() {
    return {
      message: 'Your subscription has been successfully cancelled.'
    };
  }
};
</script>

<style scoped>
.cancel-container {
  text-align: center;
  margin-top: 50px;
}

.cancel-container h1 {
  font-size: 2em;
  margin-bottom: 20px;
}

.cancel-container p {
  font-size: 1.2em;
  margin-bottom: 20px;
}

.cancel-container a {
  color: #42b983;
  text-decoration: none;
  font-weight: bold;
}
</style>