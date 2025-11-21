<template>
  <div class="free-trial-container">
    <div class="background-shapes">
      <!-- SVG shapes would go here to mimic the background design -->
    </div>
    <div class="content">
      <h2 class="title">Start Creating for Free Today</h2>
      <p class="subtitle text-gray-300">Your first 5 animated graphs are on us - no credit card required.</p>
      <a href="/signup" class="cta-button">Get 5 free credits</a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FreeTrialCTA',
  // Add any necessary component logic here
}
</script>

<style scoped>
.free-trial-container {
    height: 300px;
  background-color: #274370;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #ffffff;
  padding: 2rem;
  text-align: center;
  overflow: hidden;
  width: 100%;
  margin-top: 5rem;

  border-radius: 10px;
}

.content {
  z-index: 2;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.title {
  font-size: 40px;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 22px;
  margin-bottom: 1.5rem;
}

.cta-button {
  background-color: #5271ff;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.cta-button:hover {
  background-color: #4060ff;
}

/* Add responsive styles as needed */
@media (max-width: 768px) {
  .title {
    font-size: 1.5rem;
  }
  
  .subtitle {
    font-size: 0.9rem;
  }
}
</style>