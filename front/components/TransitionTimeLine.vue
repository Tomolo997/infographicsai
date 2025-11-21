<template>
  <div class="timeline-container">
    <div class="dock-wrapper">
      <!-- Timeline Header -->
      <div class="timeline-header">
        <div class="timeline-info">
          <span class="duration-text">{{ formatTime(currentTime) }}</span>
          <span class="separator">/</span>
          <span class="total-duration">{{ formatTime(totalDuration) }}</span>
        </div>
        <div class="timeline-controls">
          <button
            @click="addSegment"
            class="add-segment-btn"
            title="Add Segment"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              class="w-4 h-4"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 4v16m8-8H4"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Timeline Track -->
      <div class="timeline-track" ref="timelineTrack" @click="handleTrackClick">
        <!-- Playhead -->
        <div
          class="playhead"
          :style="{ left: playheadPosition + '%' }"
          @mousedown="startDraggingPlayhead"
        >
          <div class="playhead-line"></div>
          <div class="playhead-handle"></div>
        </div>

        <!-- Video Segments -->
        <div class="segments-container">
          <div
            v-for="(segment, index) in segments"
            :key="segment.id"
            class="segment"
            :class="{
              selected: selectedSegment?.id === segment.id,
              hovered: hoveredSegment?.id === segment.id,
            }"
            :style="getSegmentStyle(segment)"
            @click.stop="selectSegment(segment)"
            @mouseenter="hoveredSegment = segment"
            @mouseleave="hoveredSegment = null"
          >
            <!-- Segment Preview -->
            <div class="segment-preview">
              <img
                v-if="segment.frontImage"
                :src="segment.frontImage"
                alt="Front"
                class="preview-image front"
              />
              <img
                v-if="segment.tailImage"
                :src="segment.tailImage"
                alt="Tail"
                class="preview-image tail"
              />
              <div
                v-if="!segment.frontImage && !segment.tailImage"
                class="preview-placeholder"
              >
                <span class="placeholder-text">{{ index + 1 }}</span>
              </div>
            </div>

            <!-- Segment Duration -->
            <div class="segment-duration">{{ segment.duration }}s</div>

            <!-- Transition Indicator -->
          </div>
        </div>

        <!-- Time Markers -->
        <div class="time-markers">
          <div
            v-for="marker in timeMarkers"
            :key="marker.time"
            class="time-marker"
            :style="{ left: marker.position + '%' }"
          >
            <span class="marker-label">{{ formatTime(marker.time) }}</span>
          </div>
        </div>
      </div>

      <!-- Transition Picker Popup -->
      <transition name="fade-up">
        <div
          v-if="showTransitionPicker"
          class="transition-picker"
          :style="transitionPickerStyle"
        >
          <div class="picker-header">
            <span class="picker-title">Select Transition</span>
            <button @click="showTransitionPicker = false" class="close-btn">
              ×
            </button>
          </div>
          <div class="transition-options">
            <div
              v-for="transition in availableTransitions"
              :key="transition.type"
              class="transition-option"
              :class="{
                selected:
                  selectedTransitionSegment?.transitionType === transition.type,
              }"
              @click="applyTransition(transition.type)"
            >
              <div class="option-icon">
                {{ transition.icon }}
              </div>
              <div class="option-info">
                <div class="option-name">{{ transition.name }}</div>
                <div class="option-desc">{{ transition.description }}</div>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    videoDuration: {
      type: Number,
      default: 5, // Default 5 seconds
    },
  },
  data() {
    return {
      segments: [
        {
          id: 1,
          startTime: 0,
          duration: 5,
          frontImage: null,
          tailImage: null,
          transitionType: null,
        },
        {
          id: 2,
          startTime: 5,
          duration: 5,
          frontImage: null,
          tailImage: null,
          transitionType: null,
        },
      ],
      currentTime: 0,
      selectedSegment: null,
      hoveredSegment: null,
      isDraggingPlayhead: false,
      isResizing: false,
      resizingSegment: null,
      showTransitionPicker: false,
      selectedTransitionSegment: null,
      transitionPickerIndex: null,
      transitionPickerStyle: {},
      availableTransitions: [
        {
          type: "fade",
          name: "Fade",
          icon: "⚡",
          description: "Smooth fade transition",
        },
        {
          type: "slide",
          name: "Slide",
          icon: "➡️",
          description: "Slide from side",
        },
        {
          type: "zoom",
          name: "Zoom",
          icon: "🔍",
          description: "Zoom in/out effect",
        },
        {
          type: "wipe",
          name: "Wipe",
          icon: "🌊",
          description: "Wipe across screen",
        },
        {
          type: "morph",
          name: "Morph",
          icon: "✨",
          description: "Morphing transition",
        },
        {
          type: "blur",
          name: "Blur",
          icon: "💫",
          description: "Blur effect",
        },
      ],
    };
  },
  computed: {
    totalDuration() {
      return this.segments.reduce((sum, seg) => sum + seg.duration, 0);
    },
    playheadPosition() {
      return (this.currentTime / this.totalDuration) * 100;
    },
    timeMarkers() {
      const markers = [];
      const interval = 1; // 1 second intervals
      for (let i = 0; i <= Math.ceil(this.totalDuration); i += interval) {
        markers.push({
          time: i,
          position: (i / this.totalDuration) * 100,
        });
      }
      return markers;
    },
  },
  mounted() {
    document.addEventListener("mousemove", this.handleMouseMove);
    document.addEventListener("mouseup", this.handleMouseUp);
  },
  beforeUnmount() {
    document.removeEventListener("mousemove", this.handleMouseMove);
    document.removeEventListener("mouseup", this.handleMouseUp);
  },
  methods: {
    formatTime(seconds) {
      const mins = Math.floor(seconds / 60);
      const secs = Math.floor(seconds % 60);
      return `${mins}:${secs.toString().padStart(2, "0")}`;
    },
    getSegmentStyle(segment) {
      const startPercent = (segment.startTime / this.totalDuration) * 100;
      const widthPercent = (segment.duration / this.totalDuration) * 100;
      return {
        left: startPercent + "%",
        width: widthPercent + "%",
      };
    },
    selectSegment(segment) {
      this.selectedSegment = segment;
      this.$emit("segment-selected", segment);
    },
    addSegment() {
      const lastSegment = this.segments[this.segments.length - 1];
      const newSegment = {
        id: Date.now(),
        startTime: lastSegment.startTime + lastSegment.duration,
        duration: 2,
        frontImage: null,
        tailImage: null,
        transitionType: null,
      };
      this.segments.push(newSegment);
    },
    handleTrackClick(event) {
      if (this.isDraggingPlayhead || this.isResizing) return;
      const rect = this.$refs.timelineTrack.getBoundingClientRect();
      const clickX = event.clientX - rect.left;
      const percentage = clickX / rect.width;
      this.currentTime = Math.max(
        0,
        Math.min(this.totalDuration, percentage * this.totalDuration)
      );
    },
    startDraggingPlayhead(event) {
      this.isDraggingPlayhead = true;
      event.preventDefault();
    },
    startResizing(segment, event) {
      this.isResizing = true;
      this.resizingSegment = segment;
      event.preventDefault();
    },
    handleMouseMove(event) {
      if (this.isDraggingPlayhead) {
        const rect = this.$refs.timelineTrack.getBoundingClientRect();
        const clickX = event.clientX - rect.left;
        const percentage = Math.max(0, Math.min(1, clickX / rect.width));
        this.currentTime = percentage * this.totalDuration;
      } else if (this.isResizing && this.resizingSegment) {
        const rect = this.$refs.timelineTrack.getBoundingClientRect();
        const clickX = event.clientX - rect.left;
        const percentage = Math.max(0, Math.min(1, clickX / rect.width));
        const newEndTime = percentage * this.totalDuration;
        const minDuration = 0.5;
        const newDuration = Math.max(
          minDuration,
          newEndTime - this.resizingSegment.startTime
        );
        this.resizingSegment.duration = newDuration;

        // Update subsequent segments
        const index = this.segments.findIndex(
          (s) => s.id === this.resizingSegment.id
        );
        if (index < this.segments.length - 1) {
          this.segments[index + 1].startTime =
            this.resizingSegment.startTime + newDuration;
        }
      }
    },
    handleMouseUp() {
      this.isDraggingPlayhead = false;
      this.isResizing = false;
      this.resizingSegment = null;
    },
    openTransitionPicker(segment, index) {
      this.selectedTransitionSegment = segment;
      this.transitionPickerIndex = index;
      this.showTransitionPicker = true;

      // Position the picker near the transition indicator
      const segmentPercent = (segment.startTime / this.totalDuration) * 100;
      this.transitionPickerStyle = {
        left: `${Math.min(segmentPercent + 10, 70)}%`,
      };
    },
    applyTransition(transitionType) {
      if (this.selectedTransitionSegment) {
        this.selectedTransitionSegment.transitionType = transitionType;
        this.$emit("transition-applied", {
          segment: this.selectedTransitionSegment,
          transition: transitionType,
        });
      }
      this.showTransitionPicker = false;
    },
    updateSegmentData(segmentId, data) {
      const segment = this.segments.find((s) => s.id === segmentId);
      if (segment) {
        Object.assign(segment, data);
      }
    },
  },
};
</script>

<style scoped>
.timeline-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  pointer-events: none;
  z-index: 50;
}

.dock-wrapper {
  width: 100%;
  pointer-events: auto;
  min-height: 140px;
  padding: 16px;
  background: rgba(23, 23, 23, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid #2e2e2e;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 4px;
}

.timeline-info {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
}

.duration-text {
  color: #ba7408;
  font-weight: 600;
}

.separator {
  color: #999999;
}

.total-duration {
  color: #999999;
}

.timeline-controls {
  display: flex;
  gap: 8px;
}

.add-segment-btn {
  width: 28px;
  height: 28px;
  background: linear-gradient(135deg, #ba7408 0%, #d88a0a 100%);
  border: none;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: white;
  transition: all 0.2s ease;
}

.add-segment-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(186, 116, 8, 0.4);
}

.timeline-track {
  position: relative;
  height: 80px;
  background: #121212;
  border-radius: 12px;
  overflow: visible;
  cursor: pointer;
}

.segments-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
}

.segment {
  position: absolute;
  height: 100%;
  background: rgba(23, 23, 23, 0.9);
  border: 2px solid #2e2e2e;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.segment:hover,
.segment.hovered {
  border-color: #ba7408;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(186, 116, 8, 0.3);
}

.segment.selected {
  border-color: #ba7408;
  box-shadow: 0 0 0 3px rgba(186, 116, 8, 0.2);
}

.segment-preview {
  width: 100%;
  height: 100%;
  display: flex;
  position: relative;
}

.preview-image {
  width: 50%;
  height: 100%;
  object-fit: cover;
}

.preview-image.front {
  border-right: 1px solid #2e2e2e;
}

.preview-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(
    135deg,
    rgba(186, 116, 8, 0.1) 0%,
    rgba(216, 138, 10, 0.1) 100%
  );
}

.placeholder-text {
  font-size: 24px;
  font-weight: 600;
  color: #ba7408;
}

.segment-duration {
  position: absolute;
  top: 4px;
  left: 4px;
  background: rgba(0, 0, 0, 0.7);
  color: #f2f2f2;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 4px;
  font-weight: 600;
}

.transition-indicator {
  position: absolute;
  right: -16px;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  cursor: pointer;
}

.transition-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #ba7408 0%, #d88a0a 100%);
  border: 2px solid #171717;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(186, 116, 8, 0.4);
  transition: all 0.2s ease;
}

.transition-indicator:hover .transition-icon {
  transform: scale(1.2);
  box-shadow: 0 4px 12px rgba(186, 116, 8, 0.6);
}

.transition-type {
  font-size: 14px;
  font-weight: 600;
  color: white;
}

.resize-handle {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 8px;
  background: transparent;
  cursor: ew-resize;
  z-index: 5;
}

.resize-handle:hover {
  background: rgba(186, 116, 8, 0.3);
}

.playhead {
  position: absolute;
  top: 0;
  bottom: 0;
  width: 2px;
  z-index: 20;
  pointer-events: none;
}

.playhead-line {
  width: 2px;
  height: 100%;
  background: #ba7408;
  box-shadow: 0 0 8px rgba(186, 116, 8, 0.6);
}

.playhead-handle {
  position: absolute;
  top: -6px;
  left: 50%;
  transform: translateX(-50%);
  width: 12px;
  height: 12px;
  background: #ba7408;
  border: 2px solid #171717;
  border-radius: 50%;
  cursor: grab;
  pointer-events: auto;
  box-shadow: 0 2px 8px rgba(186, 116, 8, 0.4);
}

.playhead-handle:active {
  cursor: grabbing;
}

.time-markers {
  position: absolute;
  bottom: -20px;
  left: 0;
  right: 0;
  height: 20px;
  pointer-events: none;
}

.time-marker {
  position: absolute;
  transform: translateX(-50%);
}

.marker-label {
  font-size: 10px;
  color: #666;
}

.transition-picker {
  position: absolute;
  bottom: calc(100% + 12px);
  background: rgba(23, 23, 23, 0.98);
  backdrop-filter: blur(20px);
  border: 1px solid #2e2e2e;
  border-radius: 12px;
  padding: 12px;
  min-width: 280px;
  max-width: 320px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6);
  z-index: 100;
}

.picker-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #2e2e2e;
}

.picker-title {
  font-size: 13px;
  font-weight: 600;
  color: #f2f2f2;
}

.close-btn {
  background: none;
  border: none;
  color: #999;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.2s ease;
}

.close-btn:hover {
  color: #f2f2f2;
}

.transition-options {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.transition-option {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px;
  background: rgba(23, 23, 23, 0.5);
  border: 1px solid transparent;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.transition-option:hover {
  background: rgba(186, 116, 8, 0.1);
  border-color: #ba7408;
}

.transition-option.selected {
  background: rgba(186, 116, 8, 0.2);
  border-color: #ba7408;
}

.option-icon {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #ba7408 0%, #d88a0a 100%);
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.option-info {
  flex: 1;
}

.option-name {
  font-size: 13px;
  font-weight: 600;
  color: #f2f2f2;
  margin-bottom: 2px;
}

.option-desc {
  font-size: 11px;
  color: #999;
}

/* Fade Up Transition */
.fade-up-enter-active,
.fade-up-leave-active {
  transition: all 0.3s ease;
}

.fade-up-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-up-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .dock-wrapper {
    padding: 12px;
  }

  .timeline-track {
    height: 60px;
  }

  .transition-picker {
    min-width: 240px;
    max-width: calc(100vw - 40px);
  }
}
</style>
