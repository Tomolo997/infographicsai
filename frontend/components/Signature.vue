<!-- Start Generation Here -->
<template>
  <div class="signature-container">
    <div class="signature">
      <p>Best regards,</p>
      <p>{{ authorName }}</p>
      <p>{{ authorTitle }}</p>
      <p>{{ authorCompany }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    authorName: {
      type: String,
      required: true,
    },
    authorTitle: {
      type: String,
      required: true,
    },
    authorCompany: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
.signature-container {
  margin-top: 20px;
  font-family: Arial, sans-serif;
  font-size: 14px;
  color: #333;
}

.signature {
  border-top: 1px solid #ccc;
  padding-top: 10px;
}
</style>
<!-- End Generation Here -->
