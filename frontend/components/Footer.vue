<template>
  <footer class="footer-section">
    <div class="footer-container">
      <div class="footer-left">
        <div class="footer-logo">
          <Logo></Logo>
          <span class="footer-logo-text">Ainfographic</span>
        </div>
        <p class="footer-description">
          Turn any URL or content into shareable infographics for social
          media, blogs, and marketing.
        </p>
      </div>

      <div class="footer-right">
        <div class="footer-column">
          <h4 class="footer-column-title">Product</h4>
          <ul class="footer-links">
            <li>
              <NuxtLink to="/#features" class="footer-link">Features</NuxtLink>
            </li>
            <li>
              <NuxtLink to="/#templates" class="footer-link">Templates</NuxtLink>
            </li>
            <li>
              <NuxtLink to="/#pricing" class="footer-link">Pricing</NuxtLink>
            </li>
          </ul>
        </div>

        <div class="footer-column">
          <h4 class="footer-column-title">Resources</h4>
          <ul class="footer-links">
            <li>
              <NuxtLink to="/blog" class="footer-link">Blog</NuxtLink>
            </li>
            <li>
              <NuxtLink to="/blog/instagram-post-sizes-complete-guide-2025" class="footer-link">Instagram Post Sizes Guide</NuxtLink>
            </li>
          </ul>
        </div>

        <div class="footer-column">
          <h4 class="footer-column-title">Company</h4>
          <ul class="footer-links">
            <li>
              <a href="mailto:tomazovsenjak7@gmail.com" class="footer-link">Contact</a>
            </li>
          </ul>
        </div>

        <div class="footer-column">
          <h4 class="footer-column-title">Legal</h4>
          <ul class="footer-links">
            <li>
              <NuxtLink to="/terms-and-conditions" class="footer-link">Terms of Service</NuxtLink>
            </li>
            <li>
              <NuxtLink to="/privacy" class="footer-link">Privacy Policy</NuxtLink>
            </li>
            <li>
              <NuxtLink to="/#faq" class="footer-link">FAQ</NuxtLink>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="footer-bottom">
      <p class="footer-copyright">
        © {{ new Date().getFullYear() }} Ainfographic. All rights reserved.
      </p>
      <div class="footer-legal">
        <NuxtLink to="/terms-and-conditions" class="footer-legal-link">Terms of Service</NuxtLink>
        <NuxtLink to="/privacy" class="footer-legal-link">Privacy Policy</NuxtLink>
      </div>
    </div>
  </footer>
</template>

<script setup>
import Logo from '~/components/Logo.vue'
</script>

<style scoped>
.footer-section {
  background-color: #f9fafb;
  padding-top: 80px;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
  display: flex;
  flex-wrap: wrap;
  gap: 60px;
}

.footer-left {
  flex: 1 1 300px;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.footer-logo-text {
  font-size: 18px;
  font-weight: 700;
  color: #111827;
}

.footer-description {
  font-size: 16px;
  color: #6b7280;
  line-height: 1.6;
}

.footer-right {
  flex: 2 1 600px;
  display: flex;
  justify-content: space-between;
  gap: 40px;
}

.footer-column {
  flex: 1;
}

.footer-column-title {
  font-size: 16px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 20px;
}

.footer-links {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.footer-link {
  display: block;
  font-size: 14px;
  color: #6b7280;
  margin-bottom: 12px;
  transition: color 0.2s ease;
}

.footer-link:hover {
  color: var(--primary-color, #4f46e5);
}

.footer-bottom {
  max-width: 1200px;
  margin: 60px auto 0;
  padding: 20px 16px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.footer-copyright {
  font-size: 14px;
  color: #9ca3af;
  margin: 0;
}

.footer-legal {
  display: flex;
  gap: 20px;
}

.footer-legal-link {
  font-size: 14px;
  color: #6b7280;
  transition: color 0.2s ease;
}

.footer-legal-link:hover {
  color: var(--primary-color, #4f46e5);
}

@media (max-width: 767px) {
  .footer-container {
    flex-direction: column;
    gap: 40px;
  }
  
  .footer-right {
    flex-direction: column;
    gap: 30px;
  }
  
  .footer-bottom {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style> 