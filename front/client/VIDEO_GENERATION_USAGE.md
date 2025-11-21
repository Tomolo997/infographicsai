# Video Generation API Usage Guide

This guide explains how to use the video generation API with automatic polling.

## Overview

The video generation system consists of:

1. **`videoGenerationApi.js`** - API client functions with polling support
2. **`dashboardVideo.js` store** - Centralized state management with built-in generation
3. **Axios** - HTTP client for making requests

## Installation

Axios is already installed. If you need to reinstall:

```bash
npm install axios
```

## Basic Usage

### Method 1: Using the Store (Recommended)

The easiest way is to use the store's built-in `generateVideo()` method:

```javascript
import { useDashboardVideoStore } from '~/stores/dashboardVideo'

const videoStore = useDashboardVideoStore()

// Set your parameters (or use UI form)
videoStore.setFrontImage('https://example.com/front.jpg')
videoStore.setTailImage('https://example.com/tail.jpg')
videoStore.setPrompt('Dynamic video transition')
videoStore.setDuration(5)
videoStore.setTransitionType('energetic')

// Generate video with automatic polling
try {
  const result = await videoStore.generateVideo((status) => {
    console.log('Task state:', status.state)
    console.log('Task ID:', status.task_id)
    console.log('Ready:', status.ready)
  })
  
  console.log('Generated video:', result)
  // result contains: { video_url, transition_id, ... }
} catch (error) {
  console.error('Generation failed:', error.message)
}
```

### Method 2: Direct API Calls

For more control, use the API functions directly:

```javascript
import { 
  createAndGenerateVideoWithPolling,
  checkTaskStatus 
} from '~/client/videoGenerationApi'

const params = {
  frontImage: 'https://example.com/front.jpg',
  tailImage: 'https://example.com/tail.jpg',
  prompt: 'Dynamic transition',
  duration: 5,
  transitionType: 'energetic',
  enableSubtitles: true,
  subtitleStyle: 'default',
  // ... other params
}

// Generate with automatic polling
const result = await createAndGenerateVideoWithPolling(
  params,
  (status) => {
    console.log('Progress:', status)
  }
)
```

## API Endpoints

### 1. Create and Generate Video

**Endpoint:** `POST /api/transitions/create-and-generate/`

Creates a new transition and starts video generation.

```javascript
import { createAndGenerateVideo } from '~/client/videoGenerationApi'

const response = await createAndGenerateVideo({
  frontImage: 'https://...',
  tailImage: 'https://...',
  prompt: 'Cool transition',
  duration: 5,
  transitionType: 'energetic',
  enableSubtitles: false,
  // ... other params
})

// Returns: { task_id: 'abc-123', status: 'pending' }
```

### 2. Generate Video for Existing Transition

**Endpoint:** `POST /api/transitions/generate-video/`

Generates video for an existing transition.

```javascript
import { generateVideo } from '~/client/videoGenerationApi'

const response = await generateVideo(123) // transition_id

// Returns: { task_id: 'abc-123', transition_id: 123, status: 'pending' }
```

### 3. Check Task Status

**Endpoint:** `GET /api/transitions/task-status/{task_id}/`

Check the status of a running task.

```javascript
import { checkTaskStatus } from '~/client/videoGenerationApi'

const status = await checkTaskStatus('abc-123')

// Returns:
// {
//   task_id: 'abc-123',
//   state: 'PENDING' | 'PROCESSING' | 'SUCCESS' | 'FAILURE',
//   ready: false,
//   info: { ... } // or result/error if ready
// }
```

## Polling

The polling system automatically checks task status until completion:

```javascript
import { pollTaskStatus } from '~/client/videoGenerationApi'

const result = await pollTaskStatus(
  'task-id-here',
  (status) => {
    // Called on each poll
    console.log('Current state:', status.state)
  },
  2000,  // Poll interval in ms (default: 2000)
  150    // Max attempts (default: 150 = 5 minutes)
)
```

## Complete Example with Vue Component

```vue
<template>
  <div>
    <button @click="generate" :disabled="isGenerating">
      {{ isGenerating ? 'Generating...' : 'Generate Video' }}
    </button>
    
    <div v-if="progress">
      Task State: {{ progress.state }}
    </div>
    
    <video v-if="videoUrl" :src="videoUrl" controls />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useDashboardVideoStore } from '~/stores/dashboardVideo'

const videoStore = useDashboardVideoStore()
const isGenerating = ref(false)
const progress = ref(null)
const videoUrl = ref(null)

const generate = async () => {
  isGenerating.value = true
  
  try {
    const result = await videoStore.generateVideo((status) => {
      progress.value = status
    })
    
    videoUrl.value = result.video_url
    alert('Video generated successfully!')
  } catch (error) {
    alert(`Failed: ${error.message}`)
  } finally {
    isGenerating.value = false
  }
}
</script>
```

## Batch Operations

### Batch Generate Multiple Videos

```javascript
import { batchGenerateVideos } from '~/client/videoGenerationApi'

const response = await batchGenerateVideos([1, 2, 3, 4, 5])

// Returns: { task_group_id: 'abc', total: 5, status: 'pending' }

// Then poll for status
const status = await checkTaskStatus(response.task_group_id)
```

### Batch Create and Generate

```javascript
import { batchCreateAndGenerate } from '~/client/videoGenerationApi'

const transitions = [
  { frontImage: '...', tailImage: '...', prompt: '...', duration: 5, transitionType: 'energetic' },
  { frontImage: '...', tailImage: '...', prompt: '...', duration: 5, transitionType: 'calm' },
]

const response = await batchCreateAndGenerate(transitions)
```

## Error Handling

```javascript
try {
  const result = await videoStore.generateVideo()
  console.log('Success:', result)
} catch (error) {
  if (error.message.includes('timeout')) {
    console.error('Generation took too long')
  } else if (error.message.includes('Task failed')) {
    console.error('Backend processing error')
  } else {
    console.error('Network or API error:', error)
  }
}
```

## Store State

The store tracks generation state automatically:

```javascript
const videoStore = useDashboardVideoStore()

// Check state
console.log(videoStore.isGenerating)       // boolean
console.log(videoStore.generationProgress) // current task status
console.log(videoStore.generationError)    // error message if failed
console.log(videoStore.taskId)             // current task ID
console.log(videoStore.generatedResult)    // final result

// Reset state
videoStore.resetGenerationState()
```

## Parameter Mapping

Frontend parameters are automatically mapped to backend format:

| Frontend | Backend | Required |
|----------|---------|----------|
| `frontImage` | `front_image` | ✅ |
| `tailImage` | `tail_image` | ✅ |
| `prompt` | `prompt` | ✅ |
| `duration` | `duration` | ✅ |
| `transitionType` | `transition_type` | ✅ |
| `enableSubtitles` | `enable_subtitles` | ❌ |
| `subtitleStyle` | `subtitle_style` | ❌ |
| `subtitlePosition` | `subtitle_position` | ❌ |
| `subtitles` | `subtitles` | ❌ |
| `enableMusic` | `enable_music` | ❌ |
| `musicType` | `music_type` | ❌ |
| `enableVoiceover` | `enable_voiceover` | ❌ |
| `voiceType` | `voice_type` | ❌ |
| `voiceoverText` | `voiceover_text` | ❌ |

## Customizing Poll Intervals

```javascript
import { pollTaskStatus } from '~/client/videoGenerationApi'

// Poll every 5 seconds for up to 10 minutes
const result = await pollTaskStatus(
  taskId,
  onProgress,
  5000,  // 5 seconds
  120    // 120 attempts = 10 minutes
)
```

## Tips

1. **Always handle errors** - Network issues, timeouts, and processing failures can occur
2. **Show progress** - Use the progress callback to update UI
3. **Set reasonable timeouts** - Default is 5 minutes (150 attempts × 2s)
4. **Use the store** - It handles state management automatically
5. **Check `canGenerate`** - Validates required fields before API call

## Troubleshooting

**"Cannot generate: missing required fields"**
- Ensure `frontImage`, `tailImage`, `prompt`, and `duration > 0` are set

**"Task polling timeout"**
- Video generation took longer than expected
- Increase `maxAttempts` parameter
- Check backend logs for processing issues

**Network errors**
- Check API endpoint configuration in `apiClient.js`
- Verify authentication token is valid
- Check CORS settings if accessing from different domain

