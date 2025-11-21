// DownloadDropdown.vue
<template>
  <div class="relative inline-block">
    <Dropdown
      v-model="selectedFormat"
      :items="downloadFormats"
      position-top="110%"
      position-left="-16px"
      :disabled="isDownloading"
    >
      <template #trigger>
        <Button 
          variant="secondary" 
          class="flex w-[100px] z-30 items-center gap-2"
          :disabled="isDownloading"
        >
          <span class="flex items-center gap-2">
            <span v-if="isDownloading" class="animate-spin">
              <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </span>
           <span @click="deselectElement" v-else>Download</span>
          </span>
        </Button>
      </template>
    </Dropdown>
  </div>
</template>

<script>
import { ref, watch } from 'vue';
import { useCanvasRef } from '~/composables/useCanvasRef';
import { useEditorStore } from '~/stores/editorStore';

export default {
  name: 'DownloadDropdown',
  setup() {
    const store = useEditorStore();
    const { canvasEditor } = useCanvasRef();
    const selectedFormat = ref('png');
    const isDownloading = ref(false);

    const downloadFormats = [
      { label: 'JPEG Image', value: 'jpg' },
      { label: 'WebP Image', value: 'webp' },
      { label: 'PNG Image', value: 'png' },
    ];

    watch(selectedFormat, async (newFormat) => {
      console.log("Downloading infographic");
      if (newFormat && !isDownloading.value) {
        try {
          isDownloading.value = true;
          await canvasEditor.value?.downloadCanvas(newFormat);
        } finally {
          isDownloading.value = false;
          selectedFormat.value = null; // Reset selection after download
        }
      }
    });


    return {
      selectedFormat,
      downloadFormats,
      isDownloading,
      store,
    };
  },
  methods: {
    deselectElement() {
      this.store.clearSelection();
    },
  },
};
</script>