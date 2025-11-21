<template>
  <div class="editor flex justify-start">
    <CanvasEditor ref="canvasEditor" />
  </div>
</template>

<script>
import { useCanvasRef } from '~/composables/useCanvasRef'

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
    };
  },
  methods: {
    startChartAnimation() {
      this.$refs.chartComponent.startAnimation();
    },
    createChartGif() {
      this.$refs.chartComponent.createGif();
    },
    toggleChartClicks() {
      this.$refs.chartComponent.toggleChartClicks();
    },
  },
  async mounted() {},
};
</script>

<style scoped>
.editor {
  display: flex;
  height: calc(100vh - 80px);
}

.loading {
  font-size: 1.5rem;
  color: #333;
}
</style>