<template>
  <nav
    class="navigation w-full bg-white items-center flex gap-6 justify-end p-3"
  >
    <div>
      <Button
         @click="navigateTo('/dashboard')"
        variant="secondary"
        >New Infograph</Button
      >
    </div>
    <div class="h-[24px] w-[1px] bg-grayBackgroundLight"></div>
    <div>
      <Button @click="navigateTo('/dashboard/give-feedback')" variant="primary"
        >
        <span class="mr-2">

       <svg
          xmlns="http://www.w3.org/2000/svg"
          width="17"
          height="17"
          viewBox="0 0 24 24"
        >
          <path
            fill="currentColor"
            d="M22 1h-7a2.44 2.44 0 0 0-2.41 2l-.92 5.05a2.44 2.44 0 0 0 .53 2a2.47 2.47 0 0 0 1.88.88H17l-.25.66a3.26 3.26 0 0 0 3 4.41a1 1 0 0 0 .92-.59l2.24-5.06A1 1 0 0 0 23 10V2a1 1 0 0 0-1-1m-1 8.73l-1.83 4.13a1.3 1.3 0 0 1-.45-.4a1.23 1.23 0 0 1-.14-1.16l.38-1a1.68 1.68 0 0 0-.2-1.58A1.7 1.7 0 0 0 17.35 9h-3.29a.46.46 0 0 1-.35-.16a.5.5 0 0 1-.09-.37l.92-5A.44.44 0 0 1 15 3h6ZM9.94 13.05H7.05l.25-.66A3.26 3.26 0 0 0 4.25 8a1 1 0 0 0-.92.59l-2.24 5.06a1 1 0 0 0-.09.4v8a1 1 0 0 0 1 1h7a2.44 2.44 0 0 0 2.41-2l.92-5a2.44 2.44 0 0 0-.53-2a2.47 2.47 0 0 0-1.86-1m-.48 7.58A.44.44 0 0 1 9 21H3v-6.73l1.83-4.13a1.3 1.3 0 0 1 .45.4a1.23 1.23 0 0 1 .14 1.16l-.38 1a1.68 1.68 0 0 0 .2 1.58a1.7 1.7 0 0 0 1.41.74h3.29a.46.46 0 0 1 .35.16a.5.5 0 0 1 .09.37Z"
          />
        </svg>
        </span>

        Feedback</Button
      >
    </div>
    <div class="w-[32px] h-[32px] rounded-sm relative">
      <!-- this should be an profile picture -->
      <Dropdown
        :items="dropdownItems"
        position-top="110%"
        position-left="-80px"
      >
        <template #trigger>
          <img
                class="rounded-md"
            src="../assets/images/logo.svg"
            @click="accountModalOpen = true"
            alt=""
          />
        </template>
      </Dropdown>
    </div>
    <CreateInfographicModal
      :isOpen="dashboardStore.isCreateInfographicModalOpen"
      @close="dashboardStore.isCreateInfographicModalOpen = false"
    />
  </nav>
</template>
<script>
import { markRaw } from "vue";
import CogOutlineIcon from "./CogOutlineIcon.vue";
import LogoutIcon from "./LogoutIcon.vue";
import AccountIcon from "./AccountIcon.vue";

import { useDashboardStore } from "@/stores/dashboardStore";

export default {
  setup() {
    const dashboardStore = useDashboardStore();
    return {
      dashboardStore,
    };
  },
  name: "Navigation",
  data() {
    return {
      accountModalOpen: false,
      dropdownItems: [
        {
          label: "Settings",
          icon: markRaw(CogOutlineIcon),
          href: "/dashboard/settings",
        },
        { label: "Logout", icon: markRaw(LogoutIcon), action: "logout" },
      ],
      isCreateInfographicModalOpen: false,
    };
  },
  methods: {
    openCSVFile() {
      this.$emit("open-csv-file");
    },
    handleConfirm() {
      this.isModalCsvOpen = false;
      // A
    },
  },
};
</script>

<style scoped>
.navigation {
  height: 64px;
}

.user-menu {
  display: flex;
  gap: 5px;
}

.logo-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 5px;
}

.logo-wrapper img {
  width: 120px;
}

.logo-wrapper h1 {
  font-size: var(--font-size-large);
  color: var(--primary-color);
  margin: 0;
  font-weight: bold;
}
</style>