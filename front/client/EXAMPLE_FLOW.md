# Video Generation Flow Example

## Complete HTTP Flow with Polling

This document shows the exact HTTP requests and responses during video generation.

## Step 1: Start Video Generation

**Request:**
```http
POST /api/transitions/create-and-generate/
Content-Type: application/json
Authorization: Token your-auth-token

{
  "front_image": "https://example.com/front.jpg",
  "tail_image": "https://example.com/tail.jpg",
  "prompt": "Dynamic video transition",
  "duration": 5,
  "transition_type": "ENERGETIC",
  "enable_subtitles": true,
  "subtitle_style": "default",
  "subtitle_position": "bottom",
  "subtitles": [
    {
      "startTime": 0,
      "endTime": 2.5,
      "text": "First subtitle"
    }
  ],
  "enable_music": true,
  "music_type": "ambient",
  "enable_voiceover": false
}
```

**Response (202 Accepted):**
```json
{
  "task_id": "f7c3e8d1-9a2b-4c5d-8e7f-1a2b3c4d5e6f",
  "status": "pending",
  "message": "Transition creation and video generation started"
}
```

## Step 2: Poll for Status (Automatic)

The client automatically starts polling every 2 seconds.

### Poll Attempt 1 (after 2 seconds)

**Request:**
```http
GET /api/transitions/task-status/f7c3e8d1-9a2b-4c5d-8e7f-1a2b3c4d5e6f/
Authorization: Token your-auth-token
```

**Response:**
```json
{
  "task_id": "f7c3e8d1-9a2b-4c5d-8e7f-1a2b3c4d5e6f",
  "state": "PENDING",
  "ready": false,
  "info": null
}
```

### Poll Attempt 2 (after 4 seconds)

**Request:**
```http
GET /api/transitions/task-status/f7c3e8d1-9a2b-4c5d-8e7f-1a2b3c4d5e6f/
Authorization: Token your-auth-token
```

**Response:**
```json
{
  "task_id": "f7c3e8d1-9a2b-4c5d-8e7f-1a2b3c4d5e6f",
  "state": "PROCESSING",
  "ready": false,
  "info": {
    "current": 1,
    "total": 100,
    "status": "Processing frames..."
  }
}
```

### Poll Attempt 3-N (continues every 2 seconds)

Continues polling until `ready: true`...

### Final Poll (when complete)

**Request:**
```http
GET /api/transitions/task-status/f7c3e8d1-9a2b-4c5d-8e7f-1a2b3c4d5e6f/
Authorization: Token your-auth-token
```

**Response (Success):**
```json
{
  "task_id": "f7c3e8d1-9a2b-4c5d-8e7f-1a2b3c4d5e6f",
  "state": "SUCCESS",
  "ready": true,
  "result": {
    "transition_id": 123,
    "generated_transition_id": 456,
    "video_url": "https://example.com/videos/generated_video.mp4",
    "thumbnail_url": "https://example.com/thumbnails/thumb.jpg",
    "duration": 5,
    "status": "completed",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

## Code Example Matching This Flow

```javascript
import { useDashboardVideoStore } from '~/stores/dashboardVideo'

const videoStore = useDashboardVideoStore()

// Set parameters
videoStore.setFrontImage('https://example.com/front.jpg')
videoStore.setTailImage('https://example.com/tail.jpg')
videoStore.setPrompt('Dynamic video transition')
videoStore.setDuration(5)
videoStore.setTransitionType('energetic')
videoStore.setEnableSubtitles(true)
videoStore.addSubtitle()
videoStore.subtitles[0].startTime = 0
videoStore.subtitles[0].endTime = 2.5
videoStore.subtitles[0].text = 'First subtitle'

// Generate with polling (automatic)
try {
  const result = await videoStore.generateVideo((status) => {
    console.log('Poll response:', status)
    // Logs each poll response:
    // { task_id: '...', state: 'PENDING', ready: false }
    // { task_id: '...', state: 'PROCESSING', ready: false, info: {...} }
    // { task_id: '...', state: 'SUCCESS', ready: true, result: {...} }
  })
  
  console.log('Final result:', result)
  // {
  //   transition_id: 123,
  //   video_url: 'https://...',
  //   ...
  // }
  
} catch (error) {
  console.error('Error:', error.message)
}
```

## Timeline

```
Time    Event                        HTTP Request
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
0s      User clicks Generate        POST /api/transitions/create-and-generate/
        → Returns task_id           202 Accepted
        
2s      Auto poll #1                GET /api/transitions/task-status/{id}/
        → State: PENDING            200 OK
        
4s      Auto poll #2                GET /api/transitions/task-status/{id}/
        → State: PROCESSING         200 OK
        
6s      Auto poll #3                GET /api/transitions/task-status/{id}/
        → State: PROCESSING         200 OK
        
...     Continue polling...
        
60s     Auto poll #30               GET /api/transitions/task-status/{id}/
        → State: SUCCESS            200 OK
        → ready: true
        → Polling stops
        → Promise resolves
```

## Error Scenarios

### Scenario 1: Task Failure

**Final Poll Response:**
```json
{
  "task_id": "f7c3e8d1-9a2b-4c5d-8e7f-1a2b3c4d5e6f",
  "state": "FAILURE",
  "ready": true,
  "error": "Failed to process video: Invalid image format"
}
```

**JavaScript catches:**
```javascript
catch (error) {
  // error.message = "Failed to process video: Invalid image format"
}
```

### Scenario 2: Timeout

If polling exceeds max attempts (default 150 = 5 minutes):

**JavaScript catches:**
```javascript
catch (error) {
  // error.message = "Task polling timeout - maximum attempts reached"
}
```

### Scenario 3: Network Error

**JavaScript catches:**
```javascript
catch (error) {
  // error.message = "Network Error" or "Request failed with status 500"
}
```

## Using Raw API Functions

If you want to manually control the flow:

```javascript
import { 
  createAndGenerateVideo, 
  checkTaskStatus 
} from '~/client/videoGenerationApi'

// Step 1: Start generation
const { task_id } = await createAndGenerateVideo(params)

// Step 2: Manual polling
const pollManually = async () => {
  while (true) {
    await new Promise(resolve => setTimeout(resolve, 2000)) // Wait 2s
    
    const status = await checkTaskStatus(task_id)
    console.log('Status:', status)
    
    if (status.ready) {
      if (status.state === 'SUCCESS') {
        return status.result
      } else {
        throw new Error(status.error)
      }
    }
  }
}

const result = await pollManually()
```

## Using Automatic Polling Function

```javascript
import { 
  createAndGenerateVideo, 
  pollTaskStatus 
} from '~/client/videoGenerationApi'

// Step 1: Start generation
const { task_id } = await createAndGenerateVideo(params)

// Step 2: Auto poll
const result = await pollTaskStatus(
  task_id,
  (status) => console.log('Progress:', status),
  2000,  // poll every 2 seconds
  150    // max 150 attempts
)
```

## Best Practices

1. **Always use polling** - Don't expect immediate results
2. **Show progress** - Use the status callback to update UI
3. **Handle all states** - PENDING, PROCESSING, SUCCESS, FAILURE
4. **Set reasonable timeouts** - Video generation can take 1-5 minutes
5. **Catch errors** - Network, timeout, and processing errors can occur
6. **Store task_id** - In case user refreshes page, you can resume polling

## Resume Polling After Page Refresh

```javascript
// Save task_id to localStorage when generation starts
localStorage.setItem('currentTaskId', task_id)

// On page load, check if there's a pending task
const pendingTaskId = localStorage.getItem('currentTaskId')
if (pendingTaskId) {
  try {
    const result = await pollTaskStatus(pendingTaskId)
    console.log('Resumed and completed:', result)
    localStorage.removeItem('currentTaskId')
  } catch (error) {
    console.error('Resumed task failed:', error)
  }
}
```

