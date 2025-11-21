<template>
  <div class="file-upload-container" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleDrop">
    <div class="file-upload-area">
      <CloudUploadOutlineIcon class="text-primary" size="60"/>
      <p class="upload-text ">Click to select or drag and drop (supports .CSV)</p>
      <button class="choose-file-btn" @click.stop="triggerFileInput">
        <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        Choose file
      </button>
      <input
        type="file"
        ref="fileInput"
        @change="handleFileChange"
        accept=".csv"
        style="display: none;"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: 'Upload',
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    handleFileChange(event) {
      const file = event.target.files[0];
      this.processFile(file);
    },
    handleDrop(event) {
      const file = event.dataTransfer.files[0];
      this.processFile(file);
    },
    processFile(file) {
      if (file && file.name.endsWith('.csv')) {
        this.$emit('file-selected', file);
      } else {
        alert('Please select a CSV file.');
      }
    }
  }
};
</script>

<style scoped>
.file-upload-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  cursor: pointer;
  margin-top: 2rem;
}

.file-upload-area {
  border: 2px dashed var(--primary-color);
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  background-color: #f9fafb;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 17rem;
}

.file-upload-container:hover .file-upload-area {
  border-color: var(--primary-color);
  background-color: #eef2ff;
}

.cloud-icon {
  width: 48px;
  height: 48px;
  margin-bottom: 1rem;
  color: var(--primary-color);
}

.upload-text {
  margin-bottom: 1rem;
  color: var(--primary-color);
}

.choose-file-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 1rem 2rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.choose-file-btn:hover {
  background-color: #4f46e5;
}

.search-icon {
  width: 18px;
  height: 18px;
  margin-right: 0.5rem;
}
</style>