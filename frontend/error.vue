<template>
  <div class="flex flex-col items-center w-screen bg-white relative">
    <div
      class="flex flex-col inner-container items-center w-full xl:w-[1350px]"
    >
      <!-- Header -->

      <Header />
      <div class="error-page">
        <h1>{{ error.statusCode }}</h1>
        <h2>Oops! Something went wrong</h2>
        <p>{{ error.message }}</p>
        <NuxtLink to="/" class="home-button"> Go back to homepage </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ErrorPage",
  props: {
    error: {
      type: Object,
      default: null,
    },
  },
};
</script>

<style scoped>
.error-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  text-align: center;
  font-family: Arial, sans-serif;
  background-color: #f8f8f8;
}

h1 {
  font-size: 8rem;
  margin-bottom: 0;
  color: var(--primary-color);
}

h2 {
  font-size: 2rem;
  margin-top: 0;
  color: #34495e;
}

p {
  font-size: 1.2rem;
  color: #7f8c8d;
  margin-bottom: 2rem;
}

.home-button {
  padding: 10px 20px;
  font-size: 1rem;
  color: white;
  background-color: var(--primary-color);
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.home-button:hover {
  background-color: #2980b9;
}
</style>