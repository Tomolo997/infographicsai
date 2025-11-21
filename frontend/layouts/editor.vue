<template>
  <div class="app-layout w-full">
    <EditorLeftSideBar></EditorLeftSideBar>
    <div class="w-full justify-end">
      <EditorNavigation></EditorNavigation>
      <div class="h-[1px] w-full bg-grayBackground"></div>

      <div
        class="absolute top-24 flex justify-between gap-4 items-center right-5 z-10 bg-grayBackgroundLight p-2 rounded-lg"
      >
        <div
          v-if="store.selectedElement?.id"
          class="relative cursor-pointer"
          @click="toggleElementLock"
        >
          <svg
            v-if="store.selectedElement?.locked"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            class="text-primary"
          >
            <path
              fill="currentColor"
              d="M12 17a2 2 0 0 0 2-2a2 2 0 0 0-2-2a2 2 0 0 0-2 2a2 2 0 0 0 2 2m6-9a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V10a2 2 0 0 1 2-2h1V6a5 5 0 0 1 5-5a5 5 0 0 1 5 5v2h1m-6-5a3 3 0 0 0-3 3v2h6V6a3 3 0 0 0-3-3Z"
            />
          </svg>
          <svg
            v-else
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="M12 17q.825 0 1.413-.587T14 15t-.587-1.412T12 13t-1.412.588T10 15t.588 1.413T12 17m-6 5q-.825 0-1.412-.587T4 20V10q0-.825.588-1.412T6 8h7V6q0-2.075 1.463-3.537T18 1t3.538 1.463T23 6h-2q0-1.25-.875-2.125T18 3t-2.125.875T15 6v2h3q.825 0 1.413.588T20 10v10q0 .825-.587 1.413T18 22z"
            />
          </svg>
        </div>
        <button
          @click="bringElementToFront"
          class="justify-center rounded-md text-sm font-light flex items-center gap-1"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <g fill="currentColor">
              <path
                d="M12.305 3.315a.75.75 0 0 0-.61 0l-9 4a.75.75 0 0 0 0 1.37l9 4a.75.75 0 0 0 .61 0l9-4a.75.75 0 0 0 0-1.37z"
              />
              <path
                d="M3.305 11.315a.75.75 0 0 0-.61 1.37l9 4a.75.75 0 0 0 .61 0l9-4a.75.75 0 0 0-.61-1.37L12 15.179z"
              />
              <path
                d="M3.305 15.315a.75.75 0 0 0-.61 1.37l9 4a.75.75 0 0 0 .61 0l9-4a.75.75 0 0 0-.61-1.37L12 19.179z"
              />
            </g>
          </svg>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="18"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="m12 2l7 7l-1.4 1.425l-4.6-4.6V13h-2V5.825l-4.6 4.575L5 9zm1 13v3h-2v-3zm0 5v2h-2v-2z"
            />
          </svg>
        </button>
        <button
          @click="bringElementToBack"
          class="justify-center rounded-md text-sm font-light flex items-center gap-1"
          title="Bring to Back"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <g fill="currentColor">
              <path
                d="M12.305 3.315a.75.75 0 0 0-.61 0l-9 4a.75.75 0 0 0 0 1.37l9 4a.75.75 0 0 0 .61 0l9-4a.75.75 0 0 0 0-1.37z"
              />
              <path
                d="M3.305 11.315a.75.75 0 0 0-.61 1.37l9 4a.75.75 0 0 0 .61 0l9-4a.75.75 0 0 0-.61-1.37L12 15.179z"
              />
              <path
                d="M3.305 15.315a.75.75 0 0 0-.61 1.37l9 4a.75.75 0 0 0 .61 0l9-4a.75.75 0 0 0-.61-1.37L12 19.179z"
              />
            </g>
          </svg>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="18"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="m12 22l-7-7l1.4-1.425l4.6 4.6V11h2v7.175l4.6-4.575L19 15zM11 9V6h2v3zm0-5V2h2v2z"
            />
          </svg>
        </button>

        <!-- Add this button here (with matching styling) -->
        <button
          v-if="store.backgroundImage"
          @click="toggleBackgroundRepositioning"
          class="justify-center rounded-md text-sm font-light flex items-center gap-1"
          title="Reposition background"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="9" cy="9" r="2"></circle>
            <path d="M21 15l-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path>
          </svg>
          <span class="hidden sm:inline">Reposition</span>
        </button>

        <svg
          class="cursor-pointer"
          @click="handleUndo"
          :class="{
            'cursor-pointer': canUndo,
            'cursor-not-allowed opacity-30': !canUndo,
          }"
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
        >
          <path
            fill="currentColor"
            d="M7 19v-2h7.1q1.575 0 2.738-1T18 13.5T16.838 11T14.1 10H7.8l2.6 2.6L9 14L4 9l5-5l1.4 1.4L7.8 8h6.3q2.425 0 4.163 1.575T20 13.5t-1.737 3.925T14.1 19z"
          />
        </svg>
        <svg
          class="cursor-pointer"
          @click="handleRedo"
          :class="{
            'cursor-pointer': canRedo,
            'cursor-not-allowed opacity-30': !canRedo,
          }"
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
        >
          <path
            fill="currentColor"
            d="M9.9 19q-2.425 0-4.163-1.575T4 13.5t1.738-3.925T9.9 8h6.3l-2.6-2.6L15 4l5 5l-5 5l-1.4-1.4l2.6-2.6H9.9q-1.575 0-2.738 1T6 13.5T7.163 16T9.9 17H17v2z"
          />
        </svg>
        <!-- Save with loading state -->
        <div class="relative">
          <svg
            @click="handleSave"
            class="cursor-pointer"
            :class="{ 'opacity-0': isSaving }"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="M21 7v12q0 .825-.587 1.413T19 21H5q-.825 0-1.412-.587T3 19V5q0-.825.588-1.412T5 3h12zm-9 11q1.25 0 2.125-.875T15 15t-.875-2.125T12 12t-2.125.875T9 15t.875 2.125T12 18m-6-8h9V6H6z"
            />
          </svg>
          <!-- Loading spinner -->
          <svg
            v-if="isSaving"
            class="animate-spin absolute top-0 left-0"
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <path
              fill="currentColor"
              d="M12,4V2A10,10 0 0,0 2,12H4A8,8 0 0,1 12,4Z"
            />
          </svg>
        </div>

        <!-- Lock/Unlock Element button - only show when an element is selected -->
      </div>
      <SideEditor class="absolute top-40 right-5" />
      <slot></slot>
    </div>
  </div>
</template>

<script>
import { useEditorStore } from "@/stores/editorStore";
import { useFontStore } from "@/stores/fontStore";
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useCanvasRef } from "~/composables/useCanvasRef";
import { useToastStore } from "@/stores/toast";

export default {
  async setup() {
    useHead({
      title: "Dashboard | Ainfographic",
      meta: [
        {
          name: "description",
          content: "This is the dashboard of Ainfographic.",
        },
        { property: "og:title", content: "Dashboard | Ainfographic" },
        {
          property: "og:description",
          content: "This is the dashboard of Ainfographic.",
        },
        {
          property: "og:image",
          content: "https://images.ainfographic.com/opengraph.png",
        },
        { property: "og:url", content: "https://ainfographic.com/dashboard" },
        { name: "twitter:card", content: "summary_large_image" },
        { name: "twitter:title", content: "Dashboard | Ainfographic" },
        {
          name: "twitter:description",
          content: "This is the dashboard of Ainfographic.",
        },
        {
          name: "twitter:image",
          content: "https://images.ainfographic.com/opengraph.png",
        },
      ],
      link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.svg" }],
    });

    const route = useRoute();
    const authStore = useAuthStore();

    const { fetchUser, isAuthenticated } = authStore;
    const tokenFromQuery = route.query?.token;

    const { canvasEditor } = useCanvasRef();

    const handleGeneratePreviewImage = async () => {
      const yea = await canvasEditor.value?.generatePreviewImage();
      return yea;
    };

    const store = useEditorStore();
    const fontStore = useFontStore();
    const isSaving = ref(false);
    const toastStore = useToastStore();

    // Load fonts when component mounts
    onMounted(async () => {
      try {
        if (route.query?.adminMode === "true") {
        } else {
          await fetchUser();
        }
        await fontStore.loadFonts();
        // Load icons
      } catch (error) {
        console.error("Failed to load fonts:", error);
      }
    });
    return {
      store,
      fontStore,
      isSaving,
      route,
      handleGeneratePreviewImage,
      toastStore
    };
  },
  computed: {
    canUndo() {
      return this.store.history.past.length > 0;
    },
    canRedo() {
      return this.store.history.future.length > 0;
    },
    fontsLoading() {
      return this.fontStore?.isLoading;
    },
  },
  methods: {
    toggleBackgroundRepositioning() {
      const { canvasEditor } = useCanvasRef();
      if (canvasEditor.value) {
        canvasEditor.value.toggleBackgroundRepositioning();
      }
    },
    bringElementToFront() {
      if (this.store.selectedElement?.id) {
        this.store.bringToFront(this.store.selectedElement.id);
      }
    },
    bringElementToBack() {
      if (this.store.selectedElement?.id) {
        this.store.bringToBack(this.store.selectedElement.id);
      }
    },
    async handleSave() {
      if (this.isSaving) return;

      this.isSaving = true;
      try {
        // Get reference to CanvasEditor component

        // Call generatePreviewImage() method from CanvasEditor
        const previewBlob = await this.handleGeneratePreviewImage();

        // Pass the preview blob to saveInfographic
        const result = await this.store.saveInfographic(previewBlob);
        if (result.uuid && this.route.path == "/dashboard/editor") {
          window.location.href = `/dashboard/editor/${result.uuid}`;
        }
        this.toastStore.addToast({
          title: "Infographic saved",
          message: 'Infographic saved successfully',
          type: "success",
        });
      } catch (error) {
        this.toastStore.addToast({
          title: "Save failed",
          message: 'Please try again',
          type: "error",
        });
      } finally {
        this.isSaving = false;
      }
    },
    handleUndo() {
      if (this.canUndo) {
        this.store.undo();
      }
    },
    handleRedo() {
      if (this.canRedo) {
        this.store.redo();
      }
    },
    toggleElementLock() {
      if (this.store.selectedElement?.id) {
        this.store.toggleElementLock(this.store.selectedElement.id);
      }
    },
  },
};
</script>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: row;
  height: 100vh;
  background-repeat: repeat;
  background-size: 100px 100px;
}

.page-content {
  flex: 1;
  overflow-y: auto;
  max-height: 100vh;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>