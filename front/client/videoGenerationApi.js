/**
 * Video Generation API Service
 *
 * Handles video generation requests and polling for status updates
 */

import apiClient from './apiClient'

/**
 * Create a transition and generate video
 * @param {Object} params - Video generation parameters
 * @returns {Promise<{task_id: string, status: string}>}
 */
export async function createAndGenerateVideo(params) {
  const {
    frontImage,
    tailImage,
    prompt,
    duration,
    transitionType,
    enableSubtitles,
    subtitleStyle,
    subtitlePosition,
    subtitles,
    enableMusic,
    musicType,
    enableVoiceover,
    voiceType,
    voiceoverText,
  } = params

  // Map frontend params to backend API format
  const requestData = {
    front_image: frontImage,
    tail_image: tailImage,
    prompt: prompt,
    duration: duration,
    transition_type: transitionType.toUpperCase() || 'ENERGETIC',
    enable_subtitles: enableSubtitles,
    subtitle_style: subtitleStyle,
    subtitle_position: subtitlePosition,
    subtitles: subtitles,
    enable_music: enableMusic,
    music_type: musicType,
    enable_voiceover: enableVoiceover,
    voice_type: voiceType,
    voiceover_text: voiceoverText,
  }

  const response = await apiClient.post('/transitions/create-and-generate/', requestData)
  return response.data
}

/**
 * Generate video for an existing transition
 * @param {number} transitionId - The transition ID
 * @returns {Promise<{task_id: string, transition_id: number, status: string}>}
 */
export async function generateVideo(transitionId) {
  const response = await apiClient.post('/transitions/generate-video/', {
    transition_id: transitionId,
  })
  return response.data
}

/**
 * Check the status of a Celery task
 * @param {string} taskId - The task ID
 * @returns {Promise<{task_id: string, state: string, result: any, ready: boolean}>}
 */
export async function checkTaskStatus(taskId) {
  const response = await apiClient.get(`/transitions/task-status/${taskId}/`)
  return response.data
}

/**
 * Poll task status until completion
 * @param {string} taskId - The task ID
 * @param {Function} onProgress - Callback for progress updates
 * @param {number} pollInterval - Polling interval in ms (default: 2000)
 * @param {number} maxAttempts - Maximum polling attempts (default: 150, 5 minutes at 2s intervals)
 * @returns {Promise<any>} - The task result
 */
export async function pollTaskStatus(taskId, onProgress = null, pollInterval = 2000, maxAttempts = 150) {
  let attempts = 0

  return new Promise((resolve, reject) => {
    const poll = async () => {
      try {
        attempts++

        if (attempts > maxAttempts) {
          reject(new Error('Task polling timeout - maximum attempts reached'))
          return
        }

        const status = await checkTaskStatus(taskId)

        // Call progress callback if provided
        if (onProgress) {
          onProgress(status)
        }

        // Check if task is complete
        if (status.ready) {
          if (status.state === 'SUCCESS') {
            resolve(status.result)
          } else if (status.state === 'FAILURE') {
            reject(new Error(status.error || 'Task failed'))
          } else {
            reject(new Error(`Task completed with unexpected state: ${status.state}`))
          }
        } else {
          // Task still running, continue polling
          setTimeout(poll, pollInterval)
        }
      } catch (error) {
        reject(error)
      }
    }

    // Start polling
    poll()
  })
}

/**
 * Create and generate video with automatic polling
 * @param {Object} params - Video generation parameters
 * @param {Function} onProgress - Callback for progress updates
 * @returns {Promise<any>} - The generation result
 */
export async function createAndGenerateVideoWithPolling(params, onProgress = null) {
  // Start the video generation
  const response = await createAndGenerateVideo(params)
  
  // Check if running in sync mode (no task_id or sync_mode flag)
  if (!response.task_id || response.sync_mode) {
    // Task completed synchronously, return result immediately
    console.log('Video generation completed synchronously (Redis/Celery not available)')
    
    // Call progress callback with completion status if provided
    if (onProgress) {
      onProgress({
        task_id: null,
        state: 'SUCCESS',
        ready: true,
        transition_id: response.transition_id,
        video_url: response.video_url
      })
    }
    
    return {
      success: response.success,
      transition_id: response.transition_id,
      video_url: response.video_url,
      sync_mode: true
    }
  }

  // Async mode: Poll until completion
  const result = await pollTaskStatus(response.task_id, onProgress)

  return result
}

/**
 * Generate video with automatic polling
 * @param {number} transitionId - The transition ID
 * @param {Function} onProgress - Callback for progress updates
 * @returns {Promise<any>} - The generation result
 */
export async function generateVideoWithPolling(transitionId, onProgress = null) {
  // Start the video generation
  const response = await generateVideo(transitionId)
  
  // Check if running in sync mode (no task_id or sync_mode flag)
  if (!response.task_id || response.sync_mode) {
    // Task completed synchronously, return result immediately
    console.log('Video generation completed synchronously (Redis/Celery not available)')
    
    // Call progress callback with completion status if provided
    if (onProgress) {
      onProgress({
        task_id: null,
        state: 'SUCCESS',
        ready: true,
        transition_id: response.transition_id,
        video_url: response.video_url
      })
    }
    
    return {
      success: response.success,
      transition_id: response.transition_id,
      video_url: response.video_url,
      sync_mode: true
    }
  }

  // Async mode: Poll until completion
  const result = await pollTaskStatus(response.task_id, onProgress)

  return result
}

/**
 * Batch generate videos
 * @param {Array<number>} transitionIds - Array of transition IDs
 * @returns {Promise<{task_group_id: string, total: number}>}
 */
export async function batchGenerateVideos(transitionIds) {
  const response = await apiClient.post('/transitions/batch-generate/', {
    transition_ids: transitionIds,
  })
  return response.data
}

/**
 * Batch create and generate videos
 * @param {Array<Object>} transitions - Array of transition parameters
 * @returns {Promise<{task_group_id: string, total: number}>}
 */
export async function batchCreateAndGenerate(transitions) {
  const response = await apiClient.post('/transitions/batch-create-and-generate/', {
    transitions: transitions,
  })
  return response.data
}

/**
 * Get all transitions for the authenticated user
 * @returns {Promise<Array>} - Array of transitions
 */
export async function getTransitions() {
  const response = await apiClient.get('/transitions/list/')
  return response.data
}

/**
 * Get a single transition by ID
 * @param {number} transitionId - The transition ID
 * @returns {Promise<Object>} - The transition object
 */
export async function getTransition(transitionId) {
  const response = await apiClient.get(`/transitions/get/${transitionId}/`)
  return response.data
}

/**
 * Update a transition
 * @param {number} transitionId - The transition ID
 * @param {Object} data - The updated transition data
 * @returns {Promise<Object>} - The updated transition
 */
export async function updateTransition(transitionId, data) {
  const response = await apiClient.patch(`/transitions/update/${transitionId}/`, data)
  return response.data
}

/**
 * Delete a transition
 * @param {number} transitionId - The transition ID
 * @returns {Promise<void>}
 */
export async function deleteTransition(transitionId) {
  const response = await apiClient.delete(`/transitions/delete/${transitionId}/`)
  return response.data
}

export default {
  createAndGenerateVideo,
  generateVideo,
  checkTaskStatus,
  pollTaskStatus,
  createAndGenerateVideoWithPolling,
  generateVideoWithPolling,
  batchGenerateVideos,
  batchCreateAndGenerate,
  getTransitions,
  getTransition,
  updateTransition,
  deleteTransition,
}
