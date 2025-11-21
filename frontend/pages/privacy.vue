<template>
  <div class="privacy-page">
    <Header />
    <div class="privacy-container mt-[120px]">
      <div class="section-container">
        <div class="section-header">
          <h1 class="section-title">Privacy Policy</h1>
          <p class="section-subtitle">Last Updated: {{ new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' }) }}</p>
        </div>
        
        <div class="privacy-content">
          <div class="privacy-section">
            <h2 class="privacy-heading">1. Introduction</h2>
            <p>At Ainfographic, we take your privacy seriously. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our website, services, and applications (the "Service"). Please read this Privacy Policy carefully. By continuing to use our Service, you consent to the practices described in this policy.</p>
          </div>
          
          <div class="privacy-section">
            <h2 class="privacy-heading">2. Information We Collect</h2>
            <p>We may collect several types of information from and about users of our Service, including:</p>
            <ul class="privacy-list">
              <li><strong>Personal Information:</strong> Name, email address, telephone number, billing information, and any other information you provide when creating an account, subscribing to our Service, or contacting us.</li>
              <li><strong>Usage Data:</strong> Information about how you access and use our Service, including your IP address, browser type, device information, pages visited, time spent on those pages, and other diagnostic data.</li>
              <li><strong>Content:</strong> Any content you upload to our Service for infographic creation, including text, URLs, and images.</li>
              <li><strong>Cookies and Tracking Technologies:</strong> We use cookies and similar tracking technologies to track activity on our Service and to hold certain information to enhance your experience.</li>
            </ul>
          </div>
          
          <div class="privacy-section">
            <h2 class="privacy-heading">3. How We Use Your Information</h2>
            <p>We may use the information we collect for various purposes, including to:</p>
            <ul class="privacy-list">
              <li>Provide, maintain, and improve our Service</li>
              <li>Process and complete transactions</li>
              <li>Send you technical notices, updates, security alerts, and administrative messages</li>
              <li>Respond to your comments, questions, and requests</li>
              <li>Understand user preferences to enhance the user experience</li>
              <li>Develop new products, services, features, and functionality</li>
              <li>Monitor usage patterns and analyze trends</li>
              <li>Prevent fraudulent transactions and monitor against theft</li>
              <li>Comply with legal obligations</li>
            </ul>
          </div>
          
          <div class="privacy-section">
            <h2 class="privacy-heading">4. Sharing of Your Information</h2>
            <p>We may share your information with:</p>
            <ul class="privacy-list">
              <li><strong>Service Providers:</strong> Third-party vendors and service providers who perform services on our behalf, such as payment processing, data analysis, email delivery, hosting services, and customer service.</li>
              <li><strong>Business Transfers:</strong> If we are involved in a merger, acquisition, or sale of all or a portion of our assets, your information may be transferred as part of that transaction.</li>
              <li><strong>Legal Requirements:</strong> If required to do so by law or in response to valid requests by public authorities (e.g., a court or government agency).</li>
              <li><strong>With Your Consent:</strong> We may share your information for any other purpose with your consent.</li>
            </ul>
          </div>
          
          <div class="privacy-section">
            <h2 class="privacy-heading">5. Data Security</h2>
            <p>We implement appropriate technical and organizational measures to protect the security of your personal information. However, please be aware that no method of transmission over the Internet or method of electronic storage is 100% secure, and we cannot guarantee absolute security.</p>
          </div>
          
          <div class="privacy-section">
            <h2 class="privacy-heading">6. Your Data Protection Rights</h2>
            <p>Depending on your location, you may have certain rights regarding your personal information, including:</p>
            <ul class="privacy-list">
              <li>The right to access, update, or delete the information we have on you</li>
              <li>The right to rectification (to have your information corrected if it's inaccurate)</li>
              <li>The right to object to our processing of your personal information</li>
              <li>The right to restriction (to request that we restrict the processing of your personal information)</li>
              <li>The right to data portability (to request a copy of your data in a structured, machine-readable format)</li>
              <li>The right to withdraw consent at any time, where we relied on your consent to process your personal information</li>
            </ul>
            <p>To exercise any of these rights, please contact us at privacy@ainfographic.com.</p>
          </div>
          
          <div class="privacy-section">
            <h2 class="privacy-heading">7. Children's Privacy</h2>
            <p>Our Service is not intended for children under the age of 13. We do not knowingly collect personal information from children under 13. If you are a parent or guardian and you are aware that your child has provided us with personal information, please contact us so that we can take necessary actions.</p>
          </div>
          
          <div class="privacy-section">
            <h2 class="privacy-heading">8. Changes to This Privacy Policy</h2>
            <p>We may update our Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page and updating the "Last Updated" date. You are advised to review this Privacy Policy periodically for any changes.</p>
          </div>
          
          <div class="privacy-section">
            <h2 class="privacy-heading">9. Contact Us</h2>
            <p>If you have any questions about this Privacy Policy, please contact us at privacy@ainfographic.com.</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Footer -->
    <footer class="footer-section">
      <div class="footer-container">
        <div class="footer-left">
          <div class="footer-logo">
            <Logo></Logo>
            <span class="footer-logo-text">Ainfographic</span>
          </div>
          <p class="footer-description">
            Turn any URL or content into shareable infographics for social media, blogs, and marketing.
          </p>
        </div>
        
        <div class="footer-right">
          <div class="footer-column">
            <h4 class="footer-column-title">Product</h4>
            <ul class="footer-links">
              <li><NuxtLink to="/features" class="footer-link">Features</NuxtLink></li>
              <li><NuxtLink to="/templates" class="footer-link">Templates</NuxtLink></li>
              <li><NuxtLink to="/#pricing" class="footer-link">Pricing</NuxtLink></li>
            </ul>
          </div>
          
          <div class="footer-column">
            <h4 class="footer-column-title">Company</h4>
            <ul class="footer-links">
              <li><NuxtLink to="/about" class="footer-link">About Us</NuxtLink></li>
              <li><NuxtLink to="/contact" class="footer-link">Contact</NuxtLink></li>
              <li><NuxtLink to="/careers" class="footer-link">Careers</NuxtLink></li>
            </ul>
          </div>
          
          <div class="footer-column">
            <h4 class="footer-column-title">Legal</h4>
            <ul class="footer-links">
              <li><NuxtLink to="/terms-and-conditions" class="footer-link">Terms of Service</NuxtLink></li>
              <li><NuxtLink to="/privacy" class="footer-link">Privacy Policy</NuxtLink></li>
              <li><NuxtLink to="/#faq" class="footer-link">FAQ</NuxtLink></li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="footer-bottom">
        <p class="footer-copyright">© {{ new Date().getFullYear() }} Ainfographic. All rights reserved.</p>
        <div class="footer-legal">
          <NuxtLink to="/terms-and-conditions" class="footer-legal-link">Terms of Service</NuxtLink>
          <NuxtLink to="/privacy" class="footer-legal-link">Privacy Policy</NuxtLink>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
useHead({
  title: 'Privacy Policy - Ainfographic',
  meta: [
    { name: 'description', content: 'Privacy Policy for Ainfographic - Turn blog posts into scroll-stopping infographics' },
    { property: 'og:title', content: 'Privacy Policy - Ainfographic' },
    { property: 'og:description', content: 'Privacy Policy for Ainfographic - Turn blog posts into scroll-stopping infographics' },
  ],
});
</script>

<style scoped>
.privacy-page {
  background-color: #f9fafb;
}

.privacy-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 16px 80px;
}

.section-container {
  padding: 0;
}

.section-header {
  text-align: center;
  margin-bottom: 60px;
}

.section-title {
  font-size: 36px;
  font-weight: 700;
  color: #111827;
  margin-bottom: 16px;
}

.section-subtitle {
  font-size: 18px;
  color: #6b7280;
}

.privacy-content {
  background-color: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.privacy-section {
  margin-bottom: 30px;
}

.privacy-heading {
  font-size: 20px;
  font-weight: 600;
  color: #111827;
  margin-bottom: 16px;
}

.privacy-section p {
  font-size: 16px;
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 16px;
}

.privacy-list {
  padding-left: 20px;
  margin-bottom: 16px;
}

.privacy-list li {
  font-size: 16px;
  color: #4b5563;
  line-height: 1.6;
  margin-bottom: 8px;
}

/* Footer Section */
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

@media (max-width: 768px) {
  .privacy-content {
    padding: 30px 20px;
  }
  
  .section-title {
    font-size: 28px;
  }
  
  .privacy-heading {
    font-size: 18px;
  }
  
  .footer-container {
    flex-direction: column;
    gap: 40px;
  }
  
  .footer-right {
    flex-direction: column;
    gap: 30px;
  }
}
</style> 