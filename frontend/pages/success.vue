<template>
  <div class="success-container">
    <h1>Subscription Successful!</h1>
    <div class="success-message">
      <p>Thank you for subscribing to our service.</p>
      <p>Your subscription has been successfully processed.</p>
    </div>
    <div class="subscription-details">
      <h2>Subscription Details:</h2>
      <p><strong>Plan:</strong> {{ subscriptionPlan }}</p>
      <p><strong>Start Date:</strong> {{ startDate }}</p>
      <p><strong>Next Billing Date:</strong> {{ nextBillingDate }}</p>
    </div>
    <div class="next-steps">
      <h2>Next Steps:</h2>
      <ul>
        <li>Check your email for a confirmation of your subscription.</li>
        <li>Explore our features and start using our service.</li>
        <li>If you have any questions, please contact our support team.</li>
      </ul>
    </div>
    <router-link to="/dashboard" class="btn-primary">Go to Dashboard</router-link>
  </div>
</template>

<script>
export default {
  name: 'SubscriptionSuccess',
  data() {
    return {
      subscriptionPlan: 'Premium Plan', // This should be dynamically set based on the user's chosen plan
      startDate: new Date().toLocaleDateString(),
      nextBillingDate: new Date(new Date().setMonth(new Date().getMonth() + 1)).toLocaleDateString(),
    }
  },
  mounted() {
    // You might want to fetch the actual subscription details from your backend here
    // and update the data properties accordingly
  }
}
</script>

<style scoped>
.success-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

h1 {
  color: #4CAF50;
}

.success-message {
  margin-bottom: 20px;
}

.subscription-details, .next-steps {
  text-align: left;
  margin-bottom: 20px;
}

ul {
  padding-left: 20px;
}

.btn-primary {
  display: inline-block;
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background-color: #45a049;
}
</style>
