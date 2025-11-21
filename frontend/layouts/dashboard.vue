<template>
    <div class="app-layout w-full">
    <LeftSideBar></LeftSideBar>
    <div class="w-full overflow-y-auto">
      <Navigation></Navigation>
      <slot></slot>
    </div>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const route = useRoute();
const authStore = useAuthStore();

const { fetchUser, isAuthenticated } = authStore;
const tokenFromQuery = route.query?.token;

if (tokenFromQuery) {
  authStore.setToken(tokenFromQuery);
  await fetchUser();
} else {
  // await fetchUser();
  if (!isAuthenticated()) {
     await fetchUser();
  }
}
</script>
<style scoped>
.app-layout {
    display: flex;
    flex-direction: row;
    height: 100vh;
    background-repeat: repeat;
    background-size: 100px 100px; /* Adjust this value to match the size of your SVG */
}

.page-content {
    flex: 1;
    overflow-y: auto;
    max-height: 100vh;
}

</style>
