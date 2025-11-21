<!-- Start Generation Here -->
<template>
  <div class="generation-prompt">
    <h2>Generate Infographic</h2>
  </div>
</template>

<script>
export default {
  async setup() {
    definePageMeta({
      layout: "dashboard",
    });
  },
  data() {
    return {
      formData: {
        url: "",
        language: "",
      },
      responseMessage: "",
    };
  },
  methods: {
    async generateInfographic() {
      try {
        const response = await this.$http.post(
          "/api/generate-info/",
          this.formData
        );
        this.responseMessage = response.data.message;
      } catch (error) {
        this.responseMessage =
          error.response.data.error || "An error occurred.";
      }
    },
  },
};
</script>

<style scoped>
.generation-prompt {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.generation-prompt h2 {
  text-align: center;
}
.generation-prompt form {
  display: flex;
  flex-direction: column;
}
.generation-prompt label {
  margin-bottom: 5px;
}
.generation-prompt input {
  margin-bottom: 15px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.generation-prompt button {
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.generation-prompt .response-message {
  margin-top: 20px;
  text-align: center;
}
</style>
<!-- End Generation Here -->
