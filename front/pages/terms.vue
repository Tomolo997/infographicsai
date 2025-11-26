<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="prose prose-lg max-w-none">
      <h1 class="text-4xl font-bold text-gray-900 mb-8">Terms of Service</h1>
      
      <p class="text-gray-600 mb-8">
        <strong>Last updated:</strong> {{ lastUpdated }}
      </p>

      <div class="space-y-8">
        <section>
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">1. Acceptance of Terms</h2>
          <p class="text-gray-700 leading-relaxed">
            By accessing and using SaaS MVP ("the Service"), you accept and agree to be bound by the terms and provision of this agreement. 
            If you do not agree to abide by the above, please do not use this service.
          </p>
        </section>

        <section>
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">2. Description of Service</h2>
          <p class="text-gray-700 leading-relaxed">
            SaaS MVP provides a platform for building and deploying Software as a Service applications. The Service includes 
            authentication, billing, user management, and other tools necessary for SaaS development.
          </p>
        </section>

        <section>
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">3. User Accounts</h2>
          <p class="text-gray-700 leading-relaxed mb-4">
            To access certain features of the Service, you must register for an account. You agree to:
          </p>
          <ul class="list-disc pl-6 text-gray-700 space-y-2">
            <li>Provide accurate, current, and complete information during registration</li>
            <li>Maintain and promptly update your account information</li>
            <li>Maintain the security of your password and account</li>
            <li>Accept all risks of unauthorized access to your account</li>
          </ul>
        </section>

        <section>
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">4. Acceptable Use</h2>
          <p class="text-gray-700 leading-relaxed mb-4">
            You agree not to use the Service to:
          </p>
          <ul class="list-disc pl-6 text-gray-700 space-y-2">
            <li>Violate any laws or regulations</li>
            <li>Infringe upon the rights of others</li>
            <li>Distribute spam, malware, or other harmful content</li>
            <li>Attempt to gain unauthorized access to our systems</li>
            <li>Use the Service for any illegal or unauthorized purpose</li>
          </ul>
        </section>

        <section>
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">5. Billing and Payments</h2>
          <p class="text-gray-700 leading-relaxed mb-4">
            Payment terms for paid services include:
          </p>
          <ul class="list-disc pl-6 text-gray-700 space-y-2">
            <li>Subscription fees are billed in advance on a monthly or annual basis</li>
            <li>All fees are non-refundable except as required by law</li>
            <li>You authorize us to charge your payment method for all fees</li>
            <li>We may change our fees with 30 days notice</li>
          </ul>
        </section>

        <section>
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">6. Privacy Policy</h2>
          <p class="text-gray-700 leading-relaxed">
            Your privacy is important to us. Our Privacy Policy explains how we collect, use, and protect your information 
            when you use our Service. By using our Service, you agree to the collection and use of information in accordance 
            with our Privacy Policy.
          </p>
        </section>

        <section>
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">7. Intellectual Property</h2>
          <p class="text-gray-700 leading-relaxed">
            The Service and its original content, features, and functionality are and will remain the exclusive property of 
            SaaS MVP and its licensors. The Service is protected by copyright, trademark, and other laws.
          </p>
        </section>

        <section>
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">8. Termination</h2>
          <p class="text-gray-700 leading-relaxed">
            We may terminate or suspend your account and bar access to the Service immediately, without prior notice or liability, 
            under our sole discretion, for any reason whatsoever and without limitation, including but not limited to a breach 
            of the Terms.
          </p>
        </section>

        <section>
          <h2 class="text-2xl font-semibated text-gray-900 mb-4">9. Disclaimer of Warranties</h2>
          <p class="text-gray-700 leading-relaxed">
            The information on this service is provided on an "as is" basis. To the fullest extent permitted by law, 
            this Company excludes all representations, warranties, conditions and terms.
          </p>
        </section>

        <section>
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">10. Limitation of Liability</h2>
          <p class="text-gray-700 leading-relaxed">
            In no event shall SaaS MVP, nor its directors, employees, partners, agents, suppliers, or affiliates, be liable 
            for any indirect, incidental, special, consequential, or punitive damages, including without limitation, loss of 
            profits, data, use, goodwill, or other intangible losses.
          </p>
        </section>

        <section>
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">11. Changes to Terms</h2>
          <p class="text-gray-700 leading-relaxed">
            We reserve the right, at our sole discretion, to modify or replace these Terms at any time. If a revision is 
            material, we will provide at least 30 days notice prior to any new terms taking effect.
          </p>
        </section>

        <section>
          <h2 class="text-2xl font-semibold text-gray-900 mb-4">12. Contact Information</h2>
          <p class="text-gray-700 leading-relaxed">
            If you have any questions about these Terms of Service, please contact us at:
          </p>
          <div class="mt-4 p-4 bg-gray-50 rounded-lg">
            <p class="text-gray-700">
              <strong>Email:</strong> legal@saasmvp.com<br>
              <strong>Address:</strong> 123 Business St, Tech City, TC 12345
            </p>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
useSeoMeta({
  title: 'Terms of Service - Ainfographic',
  description: 'Terms of Service for Ainfographic platform. Learn about our terms and conditions for using our service.'
})

const lastUpdated = ref('January 1, 2024')
</script>