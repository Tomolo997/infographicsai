<template>
  <div class="editor flex justify-start">
    <CanvasEditor ref="canvasEditor" :loading="loading" />
  </div>
</template>

<script>
import { useCanvasRef } from "~/composables/useCanvasRef";
import { useEditorStore } from "~/stores/editorStore";

export default {
  components: {},
  setup() {
    definePageMeta({
      layout: "editor",
    });

    const { setCanvasEditor } = useCanvasRef();
    const canvasEditor = ref(null);

    onMounted(() => {
      setCanvasEditor(canvasEditor.value);
    });

    return {
      canvasEditor,
    };
  },
  name: "Editor",
  data() {
    return {
      userInfo: null,
      loading: true,
      error: null,
      editorStore: useEditorStore(),
    };
  },
  methods: {
    async loadInfographic() {
      try {
        this.loading = true;
        this.error = null;
        const uuid = this.$route.params.uuid;
        
        // Check if UUID is valid or exists
        if (!uuid || uuid === 'none') {
          console.warn('Invalid or missing UUID parameter');
          // Redirect to dashboard instead of trying to load a non-existent infographic
          navigateTo('/dashboard');
          return;
        }
        
        this.editorStore.infographId = uuid;
        await this.editorStore.loadInfographic(uuid);
      } catch (error) {
        console.error("Failed to load infographic:", error);
        this.error = error.message || "Failed to load infographic";
        // On error, you might want to redirect to dashboard as well
        // Uncomment the line below if you want this behavior
        // navigateTo('/dashboard');
      } finally {
        this.loading = false;
        
        // Check for auto-save parameter and trigger it
        if (this.$route.query.autoSave === "true") {
          this.triggerAutoSave();
        }
      }
    },
    
    async triggerAutoSave() {
      setTimeout(async () => {
        try {
          if (this.canvasEditor) {
            const previewBlob = await this.canvasEditor.generatePreviewImage();
            await this.editorStore.saveInfographicsAdmin(previewBlob);
          } else {
            console.error("CanvasEditor not available for auto-save");
          }
        } catch (error) {
          console.error("Auto-save failed:", error);
        }
      }, 5000); // Wait 5 seconds for canvas to fully load
    },
  },
  async mounted() {
    await this.loadInfographic();
  },
};
</script>

<style scoped>
.editor {
  display: flex;
  height: calc(100vh - 80px);
}

.loading,
.error {
  font-size: 1.5rem;
  color: #333;
  width: 100%;
  text-align: center;
}

.error {
  color: #dc2626;
}
</style>