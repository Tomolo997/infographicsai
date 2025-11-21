<template>
  <div class="sidebar">
    <nav>
      <div class="generate-button">
        <Button
          type="primary"
          :square="true"
          @click="navigateTo('/dashboard')"
        >
      <CircleEditOutlineIcon />
      </Button>
      </div>
      <ul>
        <li
          v-for="(item, index) in menuItems"
          :key="index"
          :class="{ active: currentRoute === item.route }"
          @click="navigateTo(item.route)"
        >
          <Icon :name="item.icon" />
        </li>
      </ul>
    </nav>
    <div class="bottom-menu">
      <Button
        type="secondary"
        @click="navigateTo('/dashboard/settings')"
        :square="true"
      >
    <CogOutlineIcon />
    </Button>
      <Button
        :square="true"
        type="secondary"
        @click="logout"
      >
      <LogoutIcon />
    </Button>
    </div>
    <Modal
      @close="generateInfoGraphicsModalOpen = false"
      :is-open="generateInfoGraphicsModalOpen"
      title="Generate Infographics with AI"
      sub-title="Transform your blog post into stunning infographics with just a click."
    >
      <div class="modal-wrapper">
        <form @submit="generateBlog" class="generate-form">
          <URLInput placeholder="www.aiinfographics.com" />
          <DropdownInput
            v-model="selectedLanguage"
            title="Select a Language"
            placeholder="Choose a language..."
            :options="languageOptions"
          />
          <div class="modal-button-wrapper">
            <Button icon="tabler:activity">Generate</Button>
          </div>
        </form>
      </div>
    </Modal>
  </div>
</template>

<script>
import { useAuthStore } from "@/stores/auth";
import apiClient from "@/services/apiClient";
import { useRouter } from "vue-router";
export default {
  async setup() {
    //
    const authStore = useAuthStore();
    const { isAuthenticated, logout } = authStore;

    const router = useRouter();

    return {
      logout,
      isAuthenticated,
      router,
    };
  },
  data() {
    return {
      generateInfoGraphicsModalOpen: false,
      menuItems: [
      ],
      currentRoute: "/dashboard", // Set this based on your routing logic
      selectedLanguage: "english",
      languageOptions: [
        { value: "english", text: "English" },
        { value: "spanish", text: "Español" },
        { value: "french", text: "Français" },
        { value: "german", text: "Deutsch" },
        { value: "italian", text: "Italiano" },
        { value: "portuguese", text: "Português" },
      ],
    };
  },
  mounted() {
    this.currentRoute = this.$route.path;
  },
  methods: {
    generateBlog(e) {
      e.preventDefault();
    },
    navigateTo(route) {
      // Implement your navigation logic here
      this.currentRoute = route;
      this.router.push(route);
      // You might want to use Vue Router's this.$router.push(route)
    },
    logout() {
      apiClient
        .post("/account/logout/")
        .then((response) => {
          this.someData = response.data;
          localStorage.removeItem("token");
          this.$router.push('/login');
        })
        .catch((error) => {
          console.error("There was an error!", error);
        });
    },
  },
};
</script>

<style scoped>
.sidebar {
  width: 55px;
  background-color: white;
  padding: 2rem 5px;
  box-shadow: 2px 0 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  overflow-y: auto;
  border-right: 1px solid var(--border-color-primary);
}

.sidebar nav ul {
  list-style-type: none;
  padding: 0;
  margin-top: 1rem;
}

.sidebar nav li {
  padding: var(--spacing-small) var(--spacing-medium);
  margin-bottom: 0.5rem;
  cursor: pointer;
  font-size: var(--font-size-smaller);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 2px;
  color: var(--primary-color);
  font-weight: 600;
  border: 1px solid #efe5fd;
  border-radius: var(--border-radius);
}

.sidebar nav li:hover {
  background-color: #f1f5f9;
}

.sidebar nav li.active {
  background-color: var(--primary-color);
  color: white;
}
.bottom-menu {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.generate-button button {
  width: 100%;
}

.modal-title {
  font-size: var(--font-size-large);
  color: var(--primary-color);
  margin-bottom: 1rem;
  text-align: center;
}

.modal-description {
  font-size: var(--font-size-small);
  color: var(--text-color);
  margin-bottom: 1.5rem;
  text-align: center;
}

.url-input-container {
  margin-bottom: 1.5rem;
}

.url-field {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius);
  font-size: var(--font-size-small);
}

.url-field:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 2px rgba(var(--primary-color-rgb), 0.2);
}

.generate-button-container {
  display: flex;
  justify-content: center;
}

.generate-btn {
  padding: 0.75rem 1.5rem;
  font-size: var(--font-size-small);
  font-weight: 600;
}

.generate-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.modal-wrapper {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.modal-button-wrapper {
  display: flex;
  width: 100%;
  margin-top: 12px;
}

.modal-button-wrapper button {
  width: 100%;
}
.generate-form {
  display: flex;
  flex-direction: column;
  gap: 5px;
}
</style>