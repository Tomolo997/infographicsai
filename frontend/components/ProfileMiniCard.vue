<template>
  <NuxtLink
    to="/dashboard/settings"
    class="profile-div flex items-center gap-3 px-2 py-1 w-full max-w-sm overflow-hidden"
  >
    <img
      v-if="userInfo?.profile_picture_url"
      :src="userInfo?.profile_picture_url"
      :alt="'Profile picture'"
      class="rounded-[1rem] w-10 h-10"
    />
    <div v-else class="rounded-[1rem] w-10 h-10 bg-gray-200 flex items-center justify-center">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        fill="currentColor"
        class="w-6 h-6 text-gray-500"
      >
        <path
          d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
        />
      </svg>
    </div>
    <div class="flex flex-col">
      <span class="text-sm font-medium">{{ userInfo?.email }}</span>
      <span class="text-xs text-gray-500">{{ userInfo?.subscription.tier }}</span>
    </div>
    <button class="ml-auto" @click="handleClick">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="20"
        height="20"
        viewBox="0 0 24 24"
        class="text-gray-500"
      ></svg>
    </button>
  </NuxtLink>
</template>

<script>
import { useAuthStore } from "@/stores/auth";

export default {
  setup() {
    const authStore = useAuthStore();
    const { getUser } = authStore;
    return {
      authStore,
      getUser,
    };
  },
  name: "ProfileCard",
  data() {
    return {
      userInfo: null,
      name: "tomaž Ovsenjak",
      email: "tomazovsenjak7@gmail.com",
      profileImage: "/api/placeholder/40/40",
    };
  },
  mounted() {
    this.userInfo = this.getUser();
  },
  methods: {
    handleClick() {
      this.$emit("click");
    },
  },
};
</script>

<style scoped>
.profile-div {
  border-radius: 8px;
  transition: background-color 0.3s ease, color 0.3s ease;
}
.profile-div:hover {
  background-color: rgba(43, 46, 64, 0.06);
}
</style>