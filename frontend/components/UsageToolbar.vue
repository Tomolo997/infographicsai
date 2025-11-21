<template>
  <div class="usage-stats p-4 rounded-lg">
    <div class="usage-section">
      <div class="text-sm text-[rgba(5,5,6,0.6)] mb-2 font-light">
        Usage (remaining)
      </div>

      <div class="stat-container mb-3">
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center gap-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
            >
              <path
                fill="currentColor"
                d="m12 16l-5-5l1.4-1.45l2.6 2.6V4h2v8.15l2.6-2.6L17 11zm-6 4q-.825 0-1.412-.587T4 18v-3h2v3h12v-3h2v3q0 .825-.587 1.413T18 20z"
              />
            </svg>
            <span class="text-[rgba(5,5,6,0.96)] text-[13px] font-light"
              >Downloads</span
            >
          </div>
          <span class="text-[rgba(5,5,6,0.96)] text-[13px] font-light">
            <div v-if="userInfo?.downloads.remaining === 999999">Unlimited</div>
            <div v-else>
              {{ userInfo?.downloads.remaining }} of
              {{ userInfo?.downloads?.limit }}
            </div>
          </span>
        </div>
        <div class="progress-bar">
          <div
            class="progress-fill"
            :style="{
              width: `${
                (userInfo?.downloads.remaining / userInfo?.downloads.limit) *
                100
              }%`,
            }"
          ></div>
        </div>
      </div>

      <div class="stat-container mb-3">
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center gap-2">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
            >
              <path
                fill="currentColor"
                d="M8.4 21q-2.275 0-3.838-1.562T3 15.6q0-.95.325-1.85t.925-1.625L7.8 7.85L5.375 3h13.25L16.2 7.85l3.55 4.275q.6.725.925 1.625T21 15.6q0 2.275-1.575 3.838T15.6 21zm3.6-5q-.825 0-1.412-.587T10 14t.588-1.412T12 12t1.413.588T14 14t-.587 1.413T12 16M9.625 7h4.75l1-2h-6.75zM8.4 19h7.2q1.425 0 2.413-.987T19 15.6q0-.6-.213-1.162t-.587-1.013L14.525 9H9.5l-3.7 4.4q-.375.45-.587 1.025T5 15.6q0 1.425.988 2.413T8.4 19"
              />
            </svg>
            <span class="text-[rgba(5,5,6,0.96)] text-[13px] font-light"
              >Credits</span
            >
          </div>
          <span class="text-[rgba(5,5,6,0.96)] text-[13px] font-light"
            >{{ userInfo?.credits.current }} of
            {{ userInfo?.credits?.total }}</span
          >
        </div>
        <div class="progress-bar">
          <div
            class="progress-fill"
            :style="{
              width: `${
                (userInfo?.credits.current / userInfo?.credits?.total) * 100
              }%`,
            }"
          ></div>
        </div>
      </div>

      <div class="text-xs text-[rgba(5,5,6,0.6)] mt-3 font-light">
        {{ trialSubscriptionText }}
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from "@/stores/auth";
export default {
  setup() {
    const authStore = useAuthStore();
    return {
      authStore,
    };
  },
  name: "UsageStats",
  data() {
    return {
      userInfo: null,
    };
  },
  mounted() {
    this.userInfo = this.authStore.getUser();
  },
  computed: {
    trialSubscriptionText() {
      const date = new Date(this.userInfo?.subscription?.end_date);
      const day = date.getDate();
      const month = date.toLocaleString("en-US", { month: "short" });
      const year = date.getFullYear();
      if (this.userInfo?.subscription.is_lifetime) {
        return "Lifetime subscription - AI credits renew every 30 days";
      }
      if (this.userInfo?.subscription.tier === "Free") {
        return "Free trial";
      }
      if (this.userInfo?.subscription.status === "canceling") {
        return `Your subscription ends on ${day} ${month} ${year}`;
      }

      if (this.userInfo?.subscription.status === "active") {
        return `Your subscription renews ${day} ${month} ${year}`;
      }

    },
  },
  methods: {
    upgradeToPro() {
      this.$emit("upgrade");
    },
  },
};
</script>

<style scoped>
.usage-stats {
}

.stat-container {
  padding: 4px 0;
}

.progress-bar {
  width: 100%;
  height: 4px;
  background-color: rgba(43, 46, 64, 0.06);
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #3e57da;
  border-radius: 2px;
  transition: width 0.3s ease;
}

.button {
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
  border: none;
  padding: 8px 16px;
  font-weight: 300;
  display: flex;
  justify-content: center;
  align-items: center;
}

.button--secondary {
  background-color: #3e57da;
  color: white;
}

.button--secondary:hover:not(:disabled) {
  background-color: #3a4fbb;
}
</style>