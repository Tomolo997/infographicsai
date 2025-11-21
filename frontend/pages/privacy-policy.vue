<template>
  <div class="flex flex-col items-center w-screen bg-white relative">
    <div
      class="flex flex-col inner-container items-center w-full xl:w-[1350px]"
    >
      <!-- Header -->

      <Header />
  <div class="privacy-policy">
    <h1>Privacy Policy</h1>
    <p>Last updated:  16 Sept 2024</p>
    <p>This Privacy Policy describes how your personal information is collected, used, and shared when you visit or make a purchase from  datagif.io.</p>

    <h2>1. Personal Information We Collect</h2>
    <p>When you visit the Site, we automatically collect certain information about your device, including information about your web browser, IP address, time zone, and some of the cookies that are installed on your device.</p>
    <p>Additionally, as you browse the Site, we collect information about the individual web pages or products that you view, what websites or search terms referred you to the Site, and information about how you interact with the Site.</p>

    <h2>2. How We Use Your Personal Information</h2>
    <p>We use the information that we collect generally to:</p>
    <ul>
      <li>Fulfill any orders placed through the Site (including processing your payment information, arranging for shipping, and providing you with invoices and/or order confirmations).</li>
      <li>Communicate with you;</li>
      <li>Screen our orders for potential risk or fraud; and</li>
      <li>When in line with the preferences you have shared with us, provide you with information or advertising relating to our products or services.</li>
    </ul>

    <h2>3. Sharing Your Personal Information</h2>
    <p>We share your Personal Information with third parties to help us use your Personal Information, as described above. For example, we use Google Analytics to help us understand how our customers use the Site.</p>
    <p>We may also share your Personal Information to comply with applicable laws and regulations, to respond to a subpoena, search warrant or other lawful request for information we receive, or to otherwise protect our rights.</p>

    <h2>4. Behavioral Advertising</h2>
    <p>We use your Personal Information to provide you with targeted advertisements or marketing communications we believe may be of interest to you.</p>

    <h2>5. Data Retention</h2>
    <p>When you place an order through the Site, we will maintain your Order Information for our records unless and until you ask us to delete this information.</p>

    <h2>6. Changes</h2>
    <p>We may update this privacy policy from time to time in order to reflect, for example, changes to our practices or for other operational, legal or regulatory reasons.</p>

    <h2>7. Contact Us</h2>
    <p>For more information about our privacy practices, if you have questions, or if you would like to make a complaint, please contact us by e-mail at <a href="mailto:hello@datagif.io">hello@datagif.io</a>  or by mail using the details provided below:</p>
    <p>Datagif<br></p>
  </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TermsAndConditions",
  // You can add any necessary component logic here
};
</script>

<style scoped>
.privacy-policy {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
    margin-top: 100px;
}

h1 {
  color: #333;
  border-bottom: 2px solid #333;
  padding-bottom: 10px;
}

h2 {
  color: #555;
  margin-top: 20px;
}

ul {
  padding-left: 20px;
}

p, li {
  line-height: 1.6;
  color: #666;
}
</style>