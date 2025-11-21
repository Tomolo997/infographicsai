<template>
  <div
    class="p-4 h-full bg-card-bg border border-card-border rounded-lg flex flex-col space-between"
  >
    <!-- Tab Selector -->
    <div class="tab-selector">
      <button
        v-for="tab in tabs"
        :key="tab.value"
        @click="activeTab = tab.value"
        :class="[
          'tab-button',
          activeTab === tab.value ? 'tab-active' : 'tab-inactive',
        ]"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- Tab Content -->
    <div class="tab-content">
      <!-- Basic Tab -->
      <div v-show="activeTab === 'basic'" class="space-y-3">
        <!-- Prompt -->
        <div class="space-y-2">
          <label class="block text-card-text-primary text-xs font-medium">
            Prompt
          </label>
          <textarea
            v-model="videoStore.prompt"
            placeholder="Enter your prompt here..."
            class="w-full h-20 px-3 py-2 text-sm bg-card-bg border border-card-border rounded-lg text-card-text-primary placeholder-card-text-secondary focus:outline-none focus:border-primary-500 transition-colors resize-none"
          />
        </div>

        <!-- Duration -->
        <div class="space-y-2">
          <label class="block text-card-text-primary text-xs font-medium">
            Duration (seconds)
          </label>
          <input
            v-model.number="videoStore.duration"
            type="number"
            min="1"
            max="60"
            step="0.5"
            placeholder="5"
            class="w-full px-3 py-2 text-sm bg-card-bg border border-card-border rounded-lg text-card-text-primary placeholder-card-text-secondary focus:outline-none focus:border-primary-500 transition-colors"
          />
        </div>

        <!-- Transition Type -->
        <div class="space-y-2">
          <label class="block text-card-text-primary text-xs font-medium">
            Transition Type
          </label>
          <select
            v-model="videoStore.transitionType"
            class="w-full px-3 py-2 text-sm bg-card-bg border border-card-border rounded-lg text-card-text-primary focus:outline-none focus:border-primary-500 transition-colors cursor-pointer"
          >
            <option value="">Select transition</option>
            <option value="fade">Fade</option>
            <option value="slide">Slide</option>
            <option value="zoom">Zoom</option>
            <option value="wipe">Wipe</option>
            <option value="morph">Morph</option>
            <option value="blur">Blur</option>
            <option value="rotate">Rotate</option>
          </select>
        </div>
      </div>

      <!-- Subtitle Tab -->
      <div v-show="activeTab === 'subtitle'" class="space-y-3">
        <!-- Enable Subtitles -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-card-text-primary text-xs font-medium">
              Enable Subtitles
            </span>
            <button
              type="button"
              @click="
                videoStore.setEnableSubtitles(!videoStore.enableSubtitles)
              "
              :class="[
                'toggle-switch',
                videoStore.enableSubtitles ? 'toggle-on' : 'toggle-off',
              ]"
            >
              <span
                :class="[
                  'toggle-thumb',
                  videoStore.enableSubtitles
                    ? 'toggle-thumb-on'
                    : 'toggle-thumb-off',
                ]"
              ></span>
            </button>
          </div>
        </div>

        <div v-if="videoStore.enableSubtitles" class="space-y-3">
          <!-- Subtitle Style -->
          <div class="space-y-2">
            <label class="block text-card-text-primary text-xs font-medium">
              Subtitle Style
            </label>
            <select
              v-model="videoStore.subtitleStyle"
              class="w-full px-3 py-2 text-sm bg-card-bg border border-card-border rounded-lg text-card-text-primary focus:outline-none focus:border-primary-500 transition-colors cursor-pointer"
            >
              <option value="default">Default</option>
              <option value="bold">Bold</option>
              <option value="animated">Animated</option>
              <option value="minimal">Minimal</option>
            </select>
          </div>

          <!-- Subtitle Position -->
          <div class="space-y-2">
            <label class="block text-card-text-primary text-xs font-medium">
              Position
            </label>
            <select
              v-model="videoStore.subtitlePosition"
              class="w-full px-3 py-2 text-sm bg-card-bg border border-card-border rounded-lg text-card-text-primary focus:outline-none focus:border-primary-500 transition-colors cursor-pointer"
            >
              <option value="bottom">Bottom</option>
              <option value="center">Center</option>
              <option value="top">Top</option>
            </select>
          </div>

          <!-- Add Subtitle Button -->
          <button
            @click="addSubtitle"
            type="button"
            class="w-full px-3 py-2 text-xs font-medium bg-card-bg border border-card-border rounded-lg text-card-text-primary hover:border-primary-500 transition-all flex items-center justify-center gap-2"
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
            Add Subtitle
          </button>

          <!-- Subtitle List -->
          <div v-if="videoStore.subtitles.length > 0" class="space-y-2">
            <div class="flex items-center justify-between mb-2">
              <span class="text-card-text-primary text-xs font-medium">
                Subtitles ({{ videoStore.subtitles.length }})
              </span>
            </div>

            <div
              v-for="(subtitle, index) in videoStore.subtitles"
              :key="subtitle.id"
              class="subtitle-item"
            >
              <div class="subtitle-header">
                <span class="subtitle-number">#{{ index + 1 }}</span>
                <button
                  @click="removeSubtitle(index)"
                  type="button"
                  class="remove-btn"
                  title="Remove subtitle"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    class="w-3 h-3"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M6 18L18 6M6 6l12 12"
                    />
                  </svg>
                </button>
              </div>

              <div class="subtitle-content">
                <!-- Time inputs -->
                <div class="time-inputs">
                  <div class="time-input-group">
                    <label class="time-label">Start</label>
                    <input
                      v-model.number="subtitle.startTime"
                      type="number"
                      min="0"
                      step="0.1"
                      placeholder="0.0"
                      class="time-input"
                    />
                    <span class="time-unit">s</span>
                  </div>
                  <div class="time-input-group">
                    <label class="time-label">End</label>
                    <input
                      v-model.number="subtitle.endTime"
                      type="number"
                      min="0"
                      step="0.1"
                      placeholder="0.0"
                      class="time-input"
                    />
                    <span class="time-unit">s</span>
                  </div>
                </div>

                <!-- Subtitle text -->
                <textarea
                  v-model="subtitle.text"
                  placeholder="Enter subtitle text..."
                  class="subtitle-textarea"
                  rows="2"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Audio Tab -->
      <div v-show="activeTab === 'audio'" class="space-y-3">
        <!-- Enable Background Music -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-card-text-primary text-xs font-medium">
              Enable Background Music
            </span>
            <button
              type="button"
              @click="videoStore.setEnableMusic(!videoStore.enableMusic)"
              :class="[
                'toggle-switch',
                videoStore.enableMusic ? 'toggle-on' : 'toggle-off',
              ]"
            >
              <span
                :class="[
                  'toggle-thumb',
                  videoStore.enableMusic
                    ? 'toggle-thumb-on'
                    : 'toggle-thumb-off',
                ]"
              ></span>
            </button>
          </div>
        </div>

        <!-- Music Type -->
        <div v-if="videoStore.enableMusic" class="space-y-2">
          <label class="block text-card-text-primary text-xs font-medium">
            Music Type
          </label>
          <select
            v-model="videoStore.musicType"
            class="w-full px-3 py-2 text-sm bg-card-bg border border-card-border rounded-lg text-card-text-primary focus:outline-none focus:border-primary-500 transition-colors cursor-pointer"
          >
            <option value="ambient">Ambient</option>
            <option value="upbeat">Upbeat</option>
            <option value="cinematic">Cinematic</option>
            <option value="calm">Calm</option>
            <option value="energetic">Energetic</option>
          </select>
        </div>

        <!-- Music Volume -->

        <!-- Enable Voiceover -->
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-card-text-primary text-xs font-medium">
              Enable Voiceover
            </span>
            <button
              type="button"
              @click="
                videoStore.setEnableVoiceover(!videoStore.enableVoiceover)
              "
              :class="[
                'toggle-switch',
                videoStore.enableVoiceover ? 'toggle-on' : 'toggle-off',
              ]"
            >
              <span
                :class="[
                  'toggle-thumb',
                  videoStore.enableVoiceover
                    ? 'toggle-thumb-on'
                    : 'toggle-thumb-off',
                ]"
              ></span>
            </button>
          </div>
        </div>

        <!-- Voice Type -->
        <div v-if="videoStore.enableVoiceover" class="space-y-2">
          <label class="block text-card-text-primary text-xs font-medium">
            Voice Type
          </label>
          <select
            v-model="videoStore.voiceType"
            class="w-full px-3 py-2 text-sm bg-card-bg border border-card-border rounded-lg text-card-text-primary focus:outline-none focus:border-primary-500 transition-colors cursor-pointer"
          >
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="neutral">Neutral</option>
          </select>
        </div>

        <!-- Voiceover Text -->
        <div v-if="videoStore.enableVoiceover" class="space-y-2">
          <label class="block text-card-text-primary text-xs font-medium">
            Voiceover Script
          </label>
          <textarea
            v-model="videoStore.voiceoverText"
            placeholder="Enter voiceover script..."
            class="w-full h-20 px-3 py-2 text-sm bg-card-bg border border-card-border rounded-lg text-card-text-primary placeholder-card-text-secondary focus:outline-none focus:border-primary-500 transition-colors resize-none"
          />
        </div>
      </div>
    </div>

    <!-- Generate Button (Always Visible) -->
    <button
      @click="handleGenerate"
      :disabled="!videoStore.canGenerate"
      :class="[
        'w-full px-4 py-2.5 text-sm font-medium rounded-lg transition-all duration-200 mt-auto flex items-center justify-center',
        videoStore.canGenerate
          ? 'bg-gradient-to-r from-primary-500 to-[#d88a0a] text-white hover:shadow-lg hover:shadow-primary-500/30 hover:scale-[1.02] active:scale-[0.98]'
          : 'bg-card-border text-card-text-secondary cursor-not-allowed',
      ]"
    >
      <span
        v-if="!videoStore.isGenerating"
        class="flex items-center justify-center gap-2"
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
            d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
          />
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        Generate
      </span>
      <span v-else class="flex items-center justify-center gap-2">
        <svg
          class="animate-spin w-4 h-4"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            class="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            stroke-width="4"
          ></circle>
          <path
            class="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
        Generating...
      </span>
    </button>
  </div>
</template>

<script>
import { useDashboardVideoStore } from "~/stores/dashboardVideo";

export default {
  setup() {
    const videoStore = useDashboardVideoStore();
    return { videoStore };
  },
  data() {
    return {
      activeTab: "basic",
      tabs: [
        { label: "General", value: "basic" },
        { label: "Subtitle", value: "subtitle" },
        { label: "Audio", value: "audio" },
      ],
    };
  },
  methods: {
    addSubtitle() {
      this.videoStore.addSubtitle();
    },
    removeSubtitle(index) {
      this.videoStore.removeSubtitle(index);
    },
    async handleGenerate() {
      if (!this.videoStore.canGenerate) return;

      try {
        // Generate video with polling
        const result = await this.videoStore.generateVideo((status) => {
          console.log("Generation progress:", status);
          // You can emit progress events here if needed
          this.$emit("progress", status);
        });

        console.log("Video generated successfully:", result);

        // Emit success event
        this.$emit("generate", result);

        // Show success message (you can replace with toast notification)
        alert("Video generated successfully!");
      } catch (error) {
        console.error("Video generation failed:", error);

        // Emit error event
        this.$emit("error", error);

        // Show error message
        alert(`Video generation failed: ${error.message}`);
      }
    },
  },
};
</script>

<style scoped>
.tab-selector {
  display: flex;
  gap: 4px;
  padding: 4px;
  background: #121212;
  border-radius: 8px;
  margin-bottom: 8px;
}

.tab-button {
  flex: 1;
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 500;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.tab-active {
  background: linear-gradient(135deg, #ba7408 0%, #d88a0a 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(186, 116, 8, 0.3);
}

.tab-inactive {
  background: transparent;
  color: #999999;
}

.tab-inactive:hover {
  background: rgba(186, 116, 8, 0.1);
  color: #f2f2f2;
}

.tab-content {
  min-height: 200px;
  max-height: calc(100vh - 200px);
  overflow-y: auto;
  padding-right: 4px;
}

/* Custom scrollbar */
.tab-content::-webkit-scrollbar {
  width: 6px;
}

.tab-content::-webkit-scrollbar-track {
  background: #121212;
  border-radius: 3px;
}

.tab-content::-webkit-scrollbar-thumb {
  background: #2e2e2e;
  border-radius: 3px;
}

.tab-content::-webkit-scrollbar-thumb:hover {
  background: #ba7408;
}

/* Custom range slider */
.slider::-webkit-slider-thumb {
  appearance: none;
  width: 16px;
  height: 16px;
  background: linear-gradient(135deg, #ba7408 0%, #d88a0a 100%);
  border-radius: 50%;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  background: linear-gradient(135deg, #ba7408 0%, #d88a0a 100%);
  border-radius: 50%;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider::-webkit-slider-runnable-track {
  background: linear-gradient(
    to right,
    #ba7408 0%,
    #ba7408 var(--value, 50%),
    #2e2e2e var(--value, 50%),
    #2e2e2e 100%
  );
  border-radius: 4px;
}

/* Toggle Switch Styles */
.toggle-switch {
  position: relative;
  width: 44px;
  height: 24px;
  border-radius: 12px;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  flex-shrink: 0;
}

.toggle-off {
  background: #2e2e2e;
}

.toggle-on {
  background: linear-gradient(135deg, #ba7408 0%, #d88a0a 100%);
}

.toggle-thumb {
  position: absolute;
  top: 2px;
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.toggle-thumb-off {
  left: 2px;
}

.toggle-thumb-on {
  left: 22px;
}

.toggle-switch:hover {
  opacity: 0.9;
}

.toggle-switch:active .toggle-thumb {
  width: 24px;
}

/* Subtitle Item Styles */
.subtitle-item {
  background: #121212;
  border: 1px solid #2e2e2e;
  border-radius: 8px;
  padding: 12px;
  transition: all 0.2s ease;
}

.subtitle-item:hover {
  border-color: #ba7408;
}

.subtitle-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.subtitle-number {
  font-size: 11px;
  font-weight: 600;
  color: #ba7408;
  padding: 2px 8px;
  background: rgba(186, 116, 8, 0.1);
  border-radius: 4px;
}

.remove-btn {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  border: none;
  color: #999999;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.remove-btn:hover {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.subtitle-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.time-inputs {
  display: flex;
  gap: 8px;
}

.time-input-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.time-label {
  font-size: 10px;
  font-weight: 500;
  color: #999999;
  text-transform: uppercase;
}

.time-input {
  width: 100%;
  padding: 6px 8px;
  font-size: 12px;
  background: #171717;
  border: 1px solid #2e2e2e;
  border-radius: 6px;
  color: #f2f2f2;
  outline: none;
  transition: border-color 0.2s ease;
}

.time-input:focus {
  border-color: #ba7408;
}

.time-unit {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 11px;
  color: #999999;
  pointer-events: none;
}

.time-input-group {
  position: relative;
}

.subtitle-textarea {
  width: 100%;
  padding: 8px;
  font-size: 12px;
  background: #171717;
  border: 1px solid #2e2e2e;
  border-radius: 6px;
  color: #f2f2f2;
  resize: none;
  outline: none;
  transition: border-color 0.2s ease;
  font-family: inherit;
}

.subtitle-textarea:focus {
  border-color: #ba7408;
}

.subtitle-textarea::placeholder {
  color: #666666;
}
</style>

