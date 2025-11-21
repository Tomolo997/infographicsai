<template>
  <ClientOnly>
    <div class="main-container">
      <div class="w-full max-w-6xl">
        <div
          class="w-full mt-16 h-[400px] shadow-sm bg-card-bg border border-card-border rounded-lg flex"
        >
          <div class="w-1/2 p-6 flex justify-center flex-col space-y-4">
            <h1 class="text-4xl font-bold leading-tight">
              Welcome back, {{ user?.email }} 👋
            </h1>
            <p class="text-xl text-text-secondary">
              Create infographs with the help our AI and automation.
            </p>
            <div class="flex items-center gap-4">
              <button @click="handleCreateVideo" class="btn-primary">
                Create Infograph
              </button>
              <button @click="handleTutorial" class="btn-secondary">
                Tutorials
              </button>
            </div>
          </div>
          <div class="w-1/2 p-6">
            <img
              src="https://www.pexels.com/download/video/34577544/"
              alt="Evolution Video"
              class="w-full h-full object-cover"
            />
          </div>
        </div>
      </div>
    </div>
    <Modal
      :isOpen="showCreateVideoModal"
      title="Create Infograph"
      subtitle="Choose how you want to create your infograph"
      layout="single-column"
      maxWidth="max-w-5xl"
      @close="showCreateVideoModal = false"
    >
      <template #body>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- Option 1: Create from Scratch -->
          <div
            class="flex flex-col border border-card-border rounded-lg p-4 bg-background-primary hover:border-primary-500 transition-colors"
          >
            <h3 class="text-lg font-semibold text-text-primary mb-2">
              Create from Scratch
            </h3>
            <p class="text-sm text-text-secondary mb-4">
              Start with a blank canvas and build your infograph from the ground
              up
            </p>

            <!-- Video Preview Space -->
            <div
              class="w-full h-32 bg-background-primary rounded-lg border border-card-border overflow-hidden mb-4 flex-grow"
            >
              <div
                class="w-full h-full flex items-center justify-center text-text-secondary"
              >
                <svg
                  class="w-12 h-12 opacity-50"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 4v16m8-8H4"
                  />
                </svg>
              </div>
            </div>

            <button
              @click="handleCreateFromScratch"
              class="w-full btn-primary text-sm py-2"
            >
              Start Creating
            </button>
          </div>

          <!-- Option 2: Create from Templates -->
          <div
            class="flex flex-col border border-card-border rounded-lg p-4 bg-background-primary hover:border-primary-500 transition-colors"
          >
            <h3 class="text-lg font-semibold text-text-primary mb-2">
              Create from Templates
            </h3>
            <p class="text-sm text-text-secondary mb-4">
              Choose from our library of professionally designed templates
            </p>

            <!-- Video Preview Space -->
            <div
              class="w-full h-32 bg-background-primary rounded-lg border border-card-border overflow-hidden mb-4 flex-grow"
            >
              <div
                class="w-full h-full flex items-center justify-center text-text-secondary"
              >
                <svg
                  class="w-12 h-12 opacity-50"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M4 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1H5a1 1 0 01-1-1v-3zM14 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1h-4a1 1 0 01-1-1v-3z"
                  />
                </svg>
              </div>
            </div>

            <button
              @click="handleCreateFromTemplates"
              class="w-full btn-primary text-sm py-2"
            >
              Browse Templates
            </button>
          </div>

          <!-- Option 3: Create from Your Own Template -->
          <div
            class="flex flex-col border border-card-border rounded-lg p-4 bg-background-primary hover:border-primary-500 transition-colors"
          >
            <h3 class="text-lg font-semibold text-text-primary mb-2">
              Use Your Template
            </h3>
            <p class="text-sm text-text-secondary mb-4">
              Upload and use your own custom template design
            </p>

            <!-- Video Preview Space -->
            <div
              class="w-full h-32 bg-background-primary rounded-lg border border-card-border overflow-hidden mb-4 flex-grow"
            >
              <div
                class="w-full h-full flex items-center justify-center text-text-secondary"
              >
                <svg
                  class="w-12 h-12 opacity-50"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                  />
                </svg>
              </div>
            </div>

            <button
              @click="handleUploadTemplate"
              class="w-full btn-primary text-sm py-2"
            >
              Upload Template
            </button>
          </div>
        </div>
      </template>
    </Modal>
  </ClientOnly>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "~/stores/auth";
const authStore = useAuthStore();
const route = useRoute();

const user = ref(null);
onMounted(async () => {
  // Check if token is in query params (from Google OAuth redirect)
  const token = route.query.token;

  if (token) {
    try {
      // Store token
      if (typeof window !== "undefined") {
        localStorage.setItem("token", token);
      }

      const tokenCookie = useCookie("auth-token", {
        maxAge: 60 * 60 * 24 * 7,
      });
      tokenCookie.value = token;

      // Update auth store
      authStore.token = token;
      authStore.isAuthenticated = true;

      // Fetch user data
      await authStore.fetchUser();

      // Clean up URL by removing token query param
      navigateTo("/dashboard", { replace: true });
    } catch (err) {
      console.error("Token authentication error:", err);
      // If token is invalid, redirect to login
      navigateTo("/login");
    }
  }

  user.value = authStore.user;
});

console.log("🚀 Dashboard script is loading...");

definePageMeta({
  layout: "dashboard",
  middleware: "auth",
});

const showCreateVideoModal = ref(false);
const clickCount = ref(0);

const handleCreateVideo = () => {
  showCreateVideoModal.value = true;
};

const handleTutorial = () => {
  clickCount.value++;
};

const handleCreateFromScratch = () => {
  showCreateVideoModal.value = false;
  navigateTo("/dashboard/create");
};

const handleCreateFromTemplates = () => {
  showCreateVideoModal.value = false;
  navigateTo("/dashboard/create/templates");
};

const handleUploadTemplate = () => {
  showCreateVideoModal.value = false;
  navigateTo("/dashboard/create?type=own-templates");
};
</script>

<style scoped>
.main-container {
  display: flex;
  justify-content: center;
  align-items: start;
  min-height: calc(100vh - 100px);
  overflow: auto;
  padding: 20px;
  display: flex;
  gap: 20px;
}
</style>