<template>
  <div class="upgrade-sidebar mt-2" ref="sidebarRef">
    <div class="main-content" @click="toggleDropdown">
      <!-- plan first letter-->
      <div class="content">
        <!-- plan -->
        <h2 class="title">{{ tier }}</h2>
        <div class="subtitle">
          <NuxtLink
              v-if="!canUpgrade"
            class="w-fit text-[10px] rounded-md text-primary p-0.5 px-4 bg-primaryLight"
          >
            Upgrade
          </NuxtLink>
        </div>
      </div>
      <div class="chevron">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <polyline
            :points="isOpen ? '18 15 12 9 6 15' : '6 9 12 15 18 9'"
          ></polyline>
        </svg>
      </div>
    </div>
    <div v-if="isOpen" class="dropdown">
      <NuxtLink to="/dashboard/settings" class="dropdown-item">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <circle cx="12" cy="12" r="3"></circle>
          <path
            d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"
          ></path>
        </svg>
        Settings
      </NuxtLink>
      <!-- <div class="dropdown-item">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        Add workspace
      </div> -->
      <NuxtLink to="/dashboard/templates" class="dropdown-item">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="3" y1="9" x2="21" y2="9"></line>
          <line x1="9" y1="21" x2="9" y2="9"></line>
        </svg>
        Templates
      </NuxtLink>
      <NuxtLink to="/dashboard/give-feedback" class="dropdown-item">
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
        Give Feedback
      </NuxtLink>
      <NuxtLink v-if="!canUpgrade" to="/dashboard/settings" class="dropdown-item">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="18"
          height="18"
          viewBox="0 0 24 24"
        >
          <path fill="#3e57da" d="M11 15H6l7-14v8h5l-7 14z" />
        </svg>
        Upgrade
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

const isOpen = ref(false);
const sidebarRef = ref(null);

const toggleDropdown = () => {
  isOpen.value = !isOpen.value;
};
const props = defineProps({
  canUpgrade: {
    type: Boolean,
    default: false
  },
  tier: {
    type: String,
    default: 'Basic'
  }
});


const closeDropdown = (event) => {
  if (sidebarRef.value && !sidebarRef.value.contains(event.target)) {
    isOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener("click", closeDropdown);
});

onUnmounted(() => {
  document.removeEventListener("click", closeDropdown);
});
</script>

<style scoped>
.upgrade-sidebar {
  background-color: inherit;
  border-radius: 8px;
  width: 240px;
  position: relative;
}

.main-content {
  display: flex;
  align-items: center;
  margin: 12px;
  padding: 4px;
  border-radius: 8px;
  transition: all 0.3s;
  cursor: pointer;
}

.main-content:hover {
  background-color: #2b2e400e;
}

.icon {
  background-color: #e0e0e0;
  color: #666;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: bold;
  margin-right: 12px;
}

.content {
  flex-grow: 1;
}

.title {
  margin: 0;
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.subtitle {
  font-size: 12px;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.1px;
}

.chevron {
  color: #999;
  cursor: pointer;
}

.dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: #ffffff;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  z-index: 10;
  padding: 5px;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  font-size: 14px;
  font-weight: 300;
  color: #050506f5;
  cursor: pointer;
  border-radius: 8px;
}

.dropdown-item:hover {
  background-color: #f2f2f4;
}

.dropdown-item svg {
  margin-right: 8px;
}
</style>