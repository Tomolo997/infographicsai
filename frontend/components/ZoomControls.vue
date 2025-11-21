<template>
  <div class="zoom-controls">
    <button 
      class="zoom-btn" 
      @click="$emit('zoom-out')"
      :disabled="zoom <= 0.1"
    >
      <span>-</span>
    </button>
    
    <div class="zoom-slider-container">
      <input
        type="range"
        :value="zoom"
        min="0.1"
        max="3"
        step="0.1"
        @input="handleSliderChange"
        class="zoom-slider"
      />
      <span class="zoom-percentage" @click="$emit('reset-zoom')">
        {{ Math.round(zoom * 100) }}%
      </span>
    </div>

    <button 
      class="zoom-btn" 
      @click="$emit('zoom-in')"
      :disabled="zoom >= 3"
    >
      <span>+</span>
    </button>
  </div>
</template>

<script>
export default {
  name: 'ZoomControls',
  props: {
    zoom: {
      type: Number,
      required: true
    }
  },
  methods: {
    handleSliderChange(event) {
      this.$emit('update-zoom', parseFloat(event.target.value));
    }
  }
}
</script>

<style scoped>

.zoom-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  background-color: white;
  color: #666;
  cursor: pointer;
  transition: all 0.2s ease;
}

.zoom-btn:hover:not(:disabled) {
  background-color: #f5f5f5;
}

.zoom-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.zoom-slider-container {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 150px;
}

.zoom-slider {
  flex: 1;
  height: 4px;
  -webkit-appearance: none;
  background: #e0e0e0;
  border-radius: 2px;
  outline: none;
}

.zoom-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #4a90e2;
  cursor: pointer;
  border: none;
}

.zoom-slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #4a90e2;
  cursor: pointer;
  border: none;
}

.zoom-percentage {
  min-width: 48px;
  text-align: center;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  user-select: none;
}

.zoom-percentage:hover {
  background-color: #f5f5f5;
}
</style>