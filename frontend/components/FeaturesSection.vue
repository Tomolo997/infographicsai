<template>
  <div class="features-section">
    <h2 class="section-title">Snappa saves you time every step of the way</h2>
    
    <div class="features-container">
      <div class="feature-item">
        <h3 class="feature-title">Start with the perfect image dimensions</h3>
        <p class="feature-description">
          The perfect sized image is always one click away. Image dimensions for social media, 
          display ads, blogs, emails, and infographics are available as clickable presets.
        </p>
      </div>
      
      <div class="feature-item">
        <h3 class="feature-title">Get a head start with pre-made templates</h3>
        <p class="feature-description">
          Don't start from scratch or stare at a blank screen ever again. Choose from thousands 
          of pre-made templates that look professional and earn you more attention, clicks, and customers.
        </p>
        <a href="#templates" class="feature-link">View our design templates</a>
      </div>
      
      <div class="feature-item">
        <h3 class="feature-title">Find free high-res stock photos inside Snappa</h3>
        <p class="feature-description">
          Get access to 5,000,000+ free, high-resolution, and totally not cheesy stock photos. 
          You don't need to scour multiple stock libraries, worry about usage rights, or pay for 
          the best background images anymore.
        </p>
      </div>
      
      <div class="feature-item">
        <h3 class="feature-title">Add text, graphics, and effects in seconds</h3>
        <p class="feature-description">
          Create whatever you've imagined in seconds. Choose from 200+ fonts, 100,000+ vectors 
          and shapes, and play with photo effects until your graphic is perfect—no design experience required.
        </p>
      </div>
      
      <div class="feature-item">
        <h3 class="feature-title">Remove image backgrounds with just one click</h3>
        <p class="feature-description">
          Removing backgrounds from images used to be difficult and time consuming. Now you just 
          click a button, wait a second, and then pick your jaw up off the floor after seeing your 
          background vanish like magic.
        </p>
        <a href="#background-removal" class="feature-link">Learn more about removing backgrounds</a>
      </div>
      
      <div class="feature-item">
        <h3 class="feature-title">Resize your best graphics in a flash</h3>
        <p class="feature-description">
          Never make the same stunning graphic more than once. In one click, you can turn your 
          Twitter header into a Facebook cover, your Instagram post into a Pinterest pin, or a 
          Facebook ad into a billboard ad.
        </p>
        <a href="#resize" class="feature-link">Learn more about resizing images</a>
      </div>
      
      <div class="feature-item">
        <h3 class="feature-title">Schedule and share your graphics instantly</h3>
        <p class="feature-description">
          Share your graphics to Facebook, Twitter, and other popular social media platforms 
          without leaving Snappa. Save even more time when you connect your Buffer account and 
          pre-schedule your posts.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FeaturesSection'
}
</script>

<style scoped>
.features-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 20px;
}

.section-title {
  font-size: 32px;
  font-weight: 700;
  color: #333;
  text-align: center;
  margin-bottom: 50px;
}

.features-container {
  display: flex;
  flex-direction: column;
  gap: 50px;
}

.feature-item {
  display: flex;
  flex-direction: column;
  max-width: 800px;
  margin: 0 auto;
}

.feature-title {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin-bottom: 16px;
}

.feature-description {
  font-size: 16px;
  line-height: 1.6;
  color: #555;
  margin-bottom: 16px;
}

.feature-link {
  color: #4d61fc;
  font-size: 16px;
  font-weight: 600;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  margin-top: 4px;
  transition: color 0.2s ease;
}

.feature-link:hover {
  color: #3a4eca;
}

.feature-link::after {
  content: "→";
  margin-left: 6px;
  transition: transform 0.3s ease;
}

.feature-link:hover::after {
  transform: translateX(5px);
}

@media (max-width: 768px) {
  .section-title {
    font-size: 28px;
  }
  
  .feature-title {
    font-size: 20px;
  }
  
  .feature-description {
    font-size: 15px;
  }
}

@media (max-width: 480px) {
  .section-title {
    font-size: 24px;
  }
  
  .feature-title {
    font-size: 18px;
  }
  
  .features-container {
    gap: 40px;
  }
}
</style>