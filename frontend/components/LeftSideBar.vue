<template>
  <div
    class="left-sidebar w-[240px] flex flex-col min-w-[240px] bg-grayBackground"
  >
    <UpgradeSideBar :tier="userInfo?.subscription?.tier" :can-upgrade="canUpgrade"> </UpgradeSideBar>
    <ul class="w-full flex flex-col gap-3 mt-8">
      <li class="w-full px-6 mb-6">
        <Button
          v-if="!canUpgrade"
          alignStyle="justify-start items-center"
          fontSize="text-[12px]"
          addedStyle="w-full"
          variant="primary"
          @click="navigateTo('/dashboard/settings')"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            class="mr-2"
          >
            <path fill="#3e57da" d="M11 15H6l7-14v8h5l-7 14z" />
          </svg>
          Unlock more features</Button
        >
      </li>
      <li class="w-full px-6">
        <Button
          alignStyle="justify-start items-center"
          fontSize="text-[14px]"
          @click="navigateTo('/dashboard')"
          addedStyle="w-full"
          variant="secondary"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="mr-2"
            width="16"
            height="16"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              fill-rule="evenodd"
              d="M15.635 2.124c.327-.832 1.503-.832 1.83 0l.428 1.09l1.084.429c.83.328.83 1.504 0 1.832l-1.084.43l-.428 1.089c-.327.832-1.503.832-1.83 0l-.428-1.09l-1.085-.429c-.83-.328-.83-1.504 0-1.832l1.085-.43zm.915.406l.415 1.055c.1.254.3.455.553.556l1.057.418l-1.057.419a.98.98 0 0 0-.553.555l-.415 1.055l-.415-1.055a.98.98 0 0 0-.554-.555l-1.057-.419l1.057-.418a.98.98 0 0 0 .554-.556zm-13.236.784a3.633 3.633 0 0 1 5.139 0l12.233 12.233a3.633 3.633 0 0 1-5.139 5.139L3.314 8.453a3.633 3.633 0 0 1 0-5.139m4.078 1.06a2.133 2.133 0 1 0-3.017 3.018L5.96 8.978l3.017-3.017zm9.216 15.251L7.022 10.04l3.017-3.017l9.586 9.586a2.133 2.133 0 1 1-3.017 3.017m4.724-10.679c-.327-.833-1.503-.833-1.83 0l-.155.393l-.391.155c-.83.328-.83 1.504 0 1.832l.391.155l.155.394c.327.832 1.503.832 1.83 0l.154-.394l.392-.155c.83-.328.83-1.504 0-1.832l-.392-.155zm-.915.405l-.141.36c-.1.253-.3.455-.554.555l-.364.144l.364.144c.254.1.454.302.554.555l.14.36l.142-.36c.1-.253.3-.454.554-.555l.364-.144l-.364-.144a.98.98 0 0 1-.554-.555zM4.668 15.124c.327-.832 1.503-.832 1.83 0l.155.394l.39.154c.83.329.83 1.505 0 1.833l-.39.155l-.155.393c-.327.833-1.503.833-1.83 0l-.155-.393l-.391-.155c-.83-.328-.83-1.504 0-1.832l.391-.155zm.774.765l.14-.36l.142.36c.1.254.3.455.554.556l.364.144l-.364.144a.98.98 0 0 0-.554.555l-.141.36l-.141-.36a.98.98 0 0 0-.554-.555l-.364-.144l.364-.144a.98.98 0 0 0 .554-.556"
              clip-rule="evenodd"
            />
          </svg>
          New Infograph</Button
        >
      </li>
      <li class="w-full px-6">
        <Button
          :font-size="'text-[15px]'"
          alignStyle="items-center"
          @click="navigateTo('/dashboard/templates')"
          class="w-full flex gap-2"
          :variant="
            isSelected('/dashboard/templates')
              ? 'secondary-light'
              : 'primary-inherit'
          "
        >
          <span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="18"
              height="18"
              viewBox="0 0 24 24"
            >
              <path
                fill="currentColor"
                d="M2 2h20v20H2zm2 2v4h16V4zm16 6h-9v10h9zM9 20V10H4v10z"
              />
            </svg>
          </span>
          Templates</Button
        >
      </li>
      <li class="w-full px-6">
        <Button
          :font-size="'text-[15px]'"
          alignStyle="items-center"
          @click="navigateTo('/dashboard/saved')"
          class="w-full flex gap-2"
          :variant="
            isSelected('/dashboard/saved')
              ? 'secondary-light'
              : 'primary-inherit'
          "
        >
          <span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
            >
              <path
                fill="currentColor"
                d="M20 7.423v10.962q0 .69-.462 1.153T18.384 20H5.616q-.691 0-1.153-.462T4 18.384V5.616q0-.691.463-1.153T5.616 4h10.961zm-8.004 9.115q.831 0 1.417-.582T14 14.543t-.582-1.418t-1.413-.586t-1.419.581T10 14.535t.582 1.418t1.414.587M6.769 9.77h7.423v-3H6.77z"
              />
            </svg>
          </span>
          Saved</Button
        >
      </li>
    </ul>
    <ul class="mt-auto p-2">
      <UsageToolbar />
      <div class="w-full mb-4 flex justify-center"></div>

      <ProfileMiniCard @click="handleProfileClick" />
    </ul>
  </div>
</template>

<script>
import { useRoute, useRouter } from "vue-router";
import { useDashboardStore } from "@/stores/dashboardStore";
import { useAuthStore } from "@/stores/auth";
export default {
  setup() {
    const dashboardStore = useDashboardStore();
    const authStore = useAuthStore();
    const route = useRoute();
    const rounter = useRouter();
    return {
      route,
      dashboardStore,
      authStore,
      rounter,
    };
  },
  data() {
    return {
      selectedPath: "",
      userInfo: "",
    };
  },
  mounted() {
    this.userInfo = this.authStore.getUser();
  },
  computed: {
    currentPath() {},
    canUpgrade(){
      return this.userInfo?.subscription?.tier !== 'Premium Monthly' || !this.userInfo?.subscription?.is_lifetime
    }
  },
  methods: {
    isSelected(path) {
      return path === this.route.path;
    },
    handleProfileClick() {
      // Handle click event
    },
  },
};
</script>


<style scoped>
</style>