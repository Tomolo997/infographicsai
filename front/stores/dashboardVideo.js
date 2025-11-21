/**
 * Dashboard Video Store
 *
 * This is the single source of truth for all video creation parameters.
 * It manages:
 * - Front and tail images from TransitionCreator
 * - All form parameters from EvolutionForm (prompt, duration, transitions, subtitles, audio settings)
 * - Video generation state
 *
 * Usage:
 * ```js
 * import { useDashboardVideoStore } from '~/stores/dashboardVideo'
 *
 * const videoStore = useDashboardVideoStore()
 *
 * // Get all params at once
 * const allParams = videoStore.getAllParams
 *
 * // Generate video with polling
 * await videoStore.generateVideo((status) => {
 *   console.log('Task status:', status)
 * })
 * ```
 */

import { defineStore } from 'pinia'
import { createAndGenerateVideoWithPolling } from '~/client/videoGenerationApi'
import { uploadImageFromDataURL, deleteImage } from '~/client/imageUploadApi'

export const useDashboardVideoStore = defineStore('dashboardVideo', {
  state: () => ({
    // Images (data URLs for preview)
    frontImage: null,
    tailImage: null,
    previewVideo: null,

    // Uploaded image URLs (actual R2 URLs)
    frontImageUrl: null,
    tailImageUrl: null,
    frontImageFilename: null,
    tailImageFilename: null,

    // Upload state
    isUploadingFront: false,
    isUploadingTail: false,
    uploadError: null,

    // Basic/General settings
    prompt: '',
    duration: 5,
    transitionType: '',

    // Subtitle settings
    enableSubtitles: true,
    subtitleStyle: 'default',
    subtitlePosition: 'bottom',
    subtitles: [],

    // Audio settings
    enableMusic: true,
    musicType: 'ambient',
    musicVolume: 50,
    enableVoiceover: false,
    voiceType: 'male',
    voiceoverText: '',

    // Generation state
    isGenerating: false,
    generationProgress: null,
    generationError: null,
    taskId: null,
    generatedResult: null,
  }),

  getters: {
    canGenerate: (state) => {
      return state.frontImageUrl && state.tailImageUrl && state.prompt.trim().length > 0 && state.duration > 0
    },

    getAllParams: (state) => {
      return {
        frontImage: state.frontImageUrl, // Use uploaded URL, not data URL
        tailImage: state.tailImageUrl, // Use uploaded URL, not data URL
        prompt: state.prompt,
        duration: state.duration,
        transitionType: state.transitionType,
        enableSubtitles: state.enableSubtitles,
        subtitleStyle: state.subtitleStyle,
        subtitlePosition: state.subtitlePosition,
        subtitles: state.subtitles,
        enableMusic: state.enableMusic,
        musicType: state.musicType,
        musicVolume: state.musicVolume,
        enableVoiceover: state.enableVoiceover,
        voiceType: state.voiceType,
        voiceoverText: state.voiceoverText,
      }
    },

    isUploading: (state) => {
      return state.isUploadingFront || state.isUploadingTail
    },
  },

  actions: {
    // Image actions (for preview only)
    setFrontImage(imageData) {
      this.frontImage = imageData
    },

    setTailImage(imageData) {
      this.tailImage = imageData
    },

    setPreviewVideo(videoUrl) {
      this.previewVideo = videoUrl
    },

    // Upload image and get R2 URL
    async uploadFrontImage(imageDataUrl) {
      if (!imageDataUrl) return

      this.isUploadingFront = true
      this.uploadError = null

      try {
        // Delete old image if exists
        if (this.frontImageFilename) {
          await deleteImage(this.frontImageFilename).catch(() => {
            // Ignore deletion errors
          })
        }

        // Upload new image
        const result = await uploadImageFromDataURL(imageDataUrl, 'front')

        this.frontImageUrl = result.url
        this.frontImageFilename = result.filename
        this.isUploadingFront = false
        console.log(result, 'RESULT')
        return result
      } catch (error) {
        this.uploadError = error.message || 'Failed to upload front image'
        this.isUploadingFront = false
        throw error
      }
    },

    async uploadTailImage(imageDataUrl) {
      if (!imageDataUrl) return

      this.isUploadingTail = true
      this.uploadError = null

      try {
        // Delete old image if exists
        if (this.tailImageFilename) {
          await deleteImage(this.tailImageFilename).catch(() => {
            // Ignore deletion errors
          })
        }

        // Upload new image
        const result = await uploadImageFromDataURL(imageDataUrl, 'tail')

        this.tailImageUrl = result.url
        this.tailImageFilename = result.filename
        this.isUploadingTail = false

        return result
      } catch (error) {
        this.uploadError = error.message || 'Failed to upload tail image'
        this.isUploadingTail = false
        throw error
      }
    },

    // Upload both images at once
    async uploadBothImages() {
      const promises = []

      if (this.frontImage && !this.frontImageUrl) {
        promises.push(this.uploadFrontImage(this.frontImage))
      }

      if (this.tailImage && !this.tailImageUrl) {
        promises.push(this.uploadTailImage(this.tailImage))
      }

      if (promises.length === 0) {
        return // Nothing to upload
      }

      try {
        await Promise.all(promises)
      } catch (error) {
        throw new Error('Failed to upload images: ' + error.message)
      }
    },

    // Basic settings actions
    setPrompt(prompt) {
      this.prompt = prompt
    },

    setDuration(duration) {
      this.duration = duration
    },

    setTransitionType(type) {
      this.transitionType = type
    },

    // Subtitle actions
    setEnableSubtitles(enabled) {
      this.enableSubtitles = enabled
    },

    setSubtitleStyle(style) {
      this.subtitleStyle = style
    },

    setSubtitlePosition(position) {
      this.subtitlePosition = position
    },

    addSubtitle() {
      const newSubtitle = {
        id: Date.now(),
        startTime: 0,
        endTime: 0,
        text: '',
      }
      this.subtitles.push(newSubtitle)
    },

    removeSubtitle(index) {
      this.subtitles.splice(index, 1)
    },

    updateSubtitle(index, field, value) {
      if (this.subtitles[index]) {
        this.subtitles[index][field] = value
      }
    },

    // Audio actions
    setEnableMusic(enabled) {
      this.enableMusic = enabled
    },

    setMusicType(type) {
      this.musicType = type
    },

    setMusicVolume(volume) {
      this.musicVolume = volume
    },

    setEnableVoiceover(enabled) {
      this.enableVoiceover = enabled
    },

    setVoiceType(type) {
      this.voiceType = type
    },

    setVoiceoverText(text) {
      this.voiceoverText = text
    },

    // Generation actions
    setIsGenerating(generating) {
      this.isGenerating = generating
    },

    // Generate video with polling
    async generateVideo(onProgress = null) {
      // First, upload images if not already uploaded
      if (!this.frontImageUrl || !this.tailImageUrl) {
        try {
          await this.uploadBothImages()
        } catch (error) {
          throw new Error('Failed to upload images: ' + error.message)
        }
      }

      if (!this.canGenerate) {
        throw new Error('Cannot generate: missing required fields')
      }

      this.isGenerating = true
      this.generationError = null
      this.generationProgress = null
      this.taskId = null
      this.generatedResult = null

      try {
        // Progress callback that updates store state
        const progressCallback = (status) => {
          this.generationProgress = status
          this.taskId = status.task_id

          // Also call user-provided callback if exists
          if (onProgress) {
            onProgress(status)
          }
        }

        // Call API with polling
        const result = await createAndGenerateVideoWithPolling(this.getAllParams, progressCallback)

        this.generatedResult = result
        this.isGenerating = false

        return result
      } catch (error) {
        this.generationError = error.message || 'Video generation failed'
        this.isGenerating = false
        throw error
      }
    },

    // Reset generation state
    resetGenerationState() {
      this.isGenerating = false
      this.generationProgress = null
      this.generationError = null
      this.taskId = null
      this.generatedResult = null
    },

    // Reset all
    resetAll() {
      this.frontImage = null
      this.tailImage = null
      this.previewVideo = null
      this.frontImageUrl = null
      this.tailImageUrl = null
      this.frontImageFilename = null
      this.tailImageFilename = null
      this.isUploadingFront = false
      this.isUploadingTail = false
      this.uploadError = null
      this.prompt = ''
      this.duration = 5
      this.transitionType = ''
      this.enableSubtitles = true
      this.subtitleStyle = 'default'
      this.subtitlePosition = 'bottom'
      this.subtitles = []
      this.enableMusic = true
      this.musicType = 'ambient'
      this.musicVolume = 50
      this.enableVoiceover = false
      this.voiceType = 'male'
      this.voiceoverText = ''
      this.resetGenerationState()
    },
  },
})

export default useDashboardVideoStore
