<template>
  <div class="flex flex-col items-center w-screen bg-white relative">
    <div
      class="flex flex-col inner-container items-center w-full xl:w-[1350px]"
    >
      <!-- Header -->

      <Header />
      <div class="terms-and-conditions">
        <h1>Terms and Conditions</h1>
        <p>
          Welcome to our website. If you continue to browse and use this
          website, you are agreeing to comply with and be bound by the following
          terms and conditions of use.
        </p>

        <h2>1. Terms of Use</h2>
        <p>
          By using our website, you agree to these terms of use. If you disagree
          with any part of these terms, please do not use our website.
        </p>

        <h2>2. Use License</h2>
        <p>
          Permission is granted to temporarily download one copy of the
          materials (information or software) on our website for personal,
          non-commercial transitory viewing only. This is the grant of a
          license, not a transfer of title, and under this license you may not:
        </p>
        <ul>
          <li>modify or copy the materials;</li>
          <li>
            use the materials for any commercial purpose, or for any public
            display (commercial or non-commercial);
          </li>
          <li>
            attempt to decompile or reverse engineer any software contained on
            our website;
          </li>
          <li>
            remove any copyright or other proprietary notations from the
            materials; or
          </li>
          <li>
            transfer the materials to another person or "mirror" the materials
            on any other server.
          </li>
        </ul>

        <h2>3. Disclaimer</h2>
        <p>
          The materials on our website are provided on an 'as is' basis. We make
          no warranties, expressed or implied, and hereby disclaim and negate
          all other warranties including, without limitation, implied warranties
          or conditions of merchantability, fitness for a particular purpose, or
          non-infringement of intellectual property or other violation of
          rights.
        </p>

        <h2>4. Limitations</h2>
        <p>
          In no event shall we or our suppliers be liable for any damages
          (including, without limitation, damages for loss of data or profit, or
          due to business interruption) arising out of the use or inability to
          use the materials on our website, even if we or an authorized
          representative has been notified orally or in writing of the
          possibility of such damage.
        </p>

        <h2>5. Accuracy of Materials</h2>
        <p>
          The materials appearing on our website could include technical,
          typographical, or photographic errors. We do not warrant that any of
          the materials on our website are accurate, complete or current. We may
          make changes to the materials contained on our website at any time
          without notice.
        </p>

        <h2>6. Links</h2>
        <p>
          We have not reviewed all of the sites linked to our website and are
          not responsible for the contents of any such linked site. The
          inclusion of any link does not imply endorsement by us of the site.
          Use of any such linked website is at the user's own risk.
        </p>

        <h2>7. Modifications</h2>
        <p>
          We may revise these terms of service for our website at any time
          without notice. By using this website you are agreeing to be bound by
          the then current version of these terms of service.
        </p>

        <h2>8. Governing Law</h2>
        <p>
          These terms and conditions are governed by and construed in accordance
          with the laws of United States of America and you irrevocably submit to the
          exclusive jurisdiction of the courts in that State or location.
        </p>
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
.terms-and-conditions {
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

p,
li {
  line-height: 1.6;
  color: #666;
}
</style>