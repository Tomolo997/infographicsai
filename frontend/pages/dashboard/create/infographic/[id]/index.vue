<template>
  <div class="create-infographic">
    <div class="sidebar">
      <h2>Sidebar Title</h2>
      <ul>
        <li><a href="#section1">Section 1</a></li>
        <li><a href="#section2">Section 2</a></li>
        <li><a href="#section3">Section 3</a></li>
      </ul>
    </div>
    <div v-if="blogContent && blogContent.title" class="editable-blog-content">
      <NewTemplate
        :main-title="blogContent.title"
        :content="blogContent.sections"
      ></NewTemplate>
    </div>
    <div v-else-if="isLoading" class="loading-message">
      Loading blog content...
    </div>
    </div>
</template>

<script>
import apiClient from "@/services/apiClient";

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
      blogContent: null,
      isLoading: false,
    };
  },
  mounted() {
    this.getInfographic();
  },
  methods: {
    async getInfographic() {
      this.isLoading = true;
      try {
        const response = await apiClient.get(
          `/infos/infographic/${this.$route.params.id}/`
        );
        this.blogContent = response.data.content;
        if (this.blogContent && this.blogContent.sections) {
          this.blogContent.sections.forEach((section) => {
            this.$set(section, "editing", false);
          });
        }
      } catch (error) {
        this.responseMessage =
          error.response?.data?.error || "An error occurred.";
      } finally {
        this.isLoading = false;
      }
    },
    toggleEdit(index) {
      this.$set(
        this.blogContent.sections[index],
        "editing",
        !this.blogContent.sections[index].editing
      );
    },
    submitForm() {
      // Implement form submission logic here
    },
  },
};
</script>

<style scoped>
.create-infographic {
  display: flex;
  margin: auto;
  width: 100%;

}
.create-infographic h1,
.create-infographic h2 {
  text-align: center;
}
.create-infographic form {
  display: flex;
  flex-direction: column;
}
.create-infographic label {
  margin-bottom: 5px;
}
.create-infographic input {
  margin-bottom: 15px;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.create-infographic button {
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.section {
  margin-bottom: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  padding: 15px;
}
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.edit-button {
  background-color: #007bff;
  border: none;
  color: white;
  padding: 5px 10px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 14px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 4px;
}
.section-content {
  white-space: pre-wrap;
}
.section-edit {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  resize: vertical;
}
.loading-message,
.response-message {
  text-align: center;
  padding: 20px;
  font-style: italic;
  color: #666;
}

.sidebar {
  width: 250px;
  padding: 20px;
  background-color: #f4f4f4;
  border-right: 1px solid #ddd;
  height: 100%;
  overflow-y: auto;
}
.sidebar h2 {
  font-size: 1.5em;
  margin-bottom: 15px;
}
.sidebar ul {
  list-style-type: none;
  padding: 0;
}
.sidebar li {
  margin: 10px 0;
}
.sidebar a {
  text-decoration: none;
  color: #333;
  transition: color 0.3s;
}
.sidebar a:hover {
  color: #007bff;
}
.editable-blog-content{
  width: 100%;
}
</style>