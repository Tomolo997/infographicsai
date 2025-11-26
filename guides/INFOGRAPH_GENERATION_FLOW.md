# Infograph Generation & Real-time Status Updates

## Overview

This document explains how the infograph generation system works with real-time status updates, ensuring users get immediate feedback without needing to reload the page.

---

## 1. Dashboard Page Flow (`/dashboard/index.vue`)

### When User Clicks "Generate"

#### Step 1: Initial Request (POST `/infographs/create/`)

```javascript
{
  prompt: "user prompt",
  blog_url: "optional URL",
  aspect_ratio: "9:16",
  resolution: "2K",
  number_of_infographs: 1
}
```

#### Step 2: Server Response (201 Created)

```javascript
{
  infographs: [
    {
      id: 123,
      request_id: "fal-request-id",
      status: "processing",
      status_url: "optional"
    }
  ],
  total_submitted: 1,
  credits_used: 1
}
```

#### Step 3: Frontend Initializes Results

- Results array is populated with infograph IDs
- Status is set to "processing"
- Small cards are displayed showing loading state

#### Step 4: Polling Starts Automatically

- For each infograph, polling begins immediately
- **Interval: Every 3 seconds**
- Endpoint: `GET /infographs/status/{id}/`

#### Step 5: Status Check Response

```javascript
{
  id: 123,
  status: "processing" | "completed" | "failed",
  image_url: "https://...",  // null if still processing
  created_at: "2025-11-23T...",
  updated_at: "2025-11-23T...",
  request_id: "fal-request-id"  // only if processing
}
```

#### Step 6: UI Updates in Real-Time

- If **processing**: Shows spinner + "Generating your infographic..."
- If **completed**: Displays the generated image with hover preview
- If **failed**: Shows error message with retry option
- **Polling stops** when status is "completed" or "failed"

---

## 2. Saved Page Flow (`/dashboard/saved/`)

### On Page Load

#### Step 1: Fetch All Infographs

```javascript
GET /infographs/list/
```

Response:

```javascript
[
  {
    id: 123,
    status: "completed",
    image_url: "https://...",
    aspect_ratio: "9:16",
    resolution: "2K",
    blog_url: "...",
    created_at: "...",
    ...
  },
  {
    id: 124,
    status: "processing",  // 👈 Still generating
    image_url: null,
    ...
  }
]
```

#### Step 2: Automatic Polling for Processing Infographs

- Frontend identifies all infographs with status "processing" or "pending"
- Starts polling for each one automatically
- **Interval: Every 5 seconds** (slightly slower than dashboard to reduce load)

#### Step 3: Visual Indicators

- **Status Badge**: Shows current status (completed/processing/failed)
- **Live Indicator**: Small pulsing blue dot appears for infographs being polled
- **Tooltip**: "Checking for updates..."

#### Step 4: Real-time Updates

- When status changes to "completed":
  - Image appears automatically
  - Status badge updates to green
  - Polling stops
  - Blue indicator disappears

---

## 3. Backend Architecture

### Endpoint: `POST /infographs/create/`

**Purpose**: Create infograph(s) and submit to fal.ai for generation

**Process**:

1. Validate user has enough credits
2. Scrape blog content if URL provided
3. Build enhanced prompt
4. For each infograph:
   - Create database record with status "PENDING"
   - Submit async job to fal.ai
   - Update status to "PROCESSING"
   - Store fal.ai request_id
5. Deduct credits from user account
6. Return infograph IDs immediately (don't wait for generation)

### Endpoint: `GET /infographs/status/{id}/`

**Purpose**: Check current status of an infograph

**Returns**:

- Current status from database
- Image URL if completed
- Error message if failed
- Request ID if still processing

**Note**: This endpoint is polled by the frontend, but primarily relies on webhooks for updates.

### Endpoint: `POST /infographs/webhook/{id}/`

**Purpose**: Receive completion callback from fal.ai

**Process**:

1. Receive webhook from fal.ai with generation results
2. Extract image URL from payload
3. Download image and upload to R2 storage
4. Update database record:
   - Status → "COMPLETED"
   - image_url → R2 URL
5. Frontend polling will pick up this change on next check

---

## 4. Key Features

### ✅ No Page Reload Required

- Users see updates in real-time
- Polling automatically stops when generation completes

### ✅ Multiple Infographs

- Can generate 1-4 infographs simultaneously
- Each one is tracked and polled independently

### ✅ Visual Feedback

- **Dashboard**:
  - Loading skeleton during generation
  - Spinner with progress message
  - Image preview on completion
- **Saved Page**:
  - Status badges (green/blue/red)
  - Live polling indicator (pulsing dot)
  - Automatic image updates

### ✅ Error Handling

- Failed generations show error state
- Polling stops on failure
- User can retry from scratch

### ✅ Resource Management

- Polling intervals stored in Map
- Cleaned up on component unmount
- Prevents memory leaks

---

## 5. Polling Configuration

| Location                         | Interval  | When to Poll                      |
| -------------------------------- | --------- | --------------------------------- |
| Dashboard (`/dashboard/`)        | 3 seconds | Immediately after creation        |
| Saved Page (`/dashboard/saved/`) | 5 seconds | On page load for processing items |

**Why different intervals?**

- Dashboard: User just created, expects fast feedback → 3s
- Saved Page: Historical view, less urgent → 5s (reduces server load)

---

## 6. User Experience Flow

### Creating Infographs

1. User enters prompt and settings
2. Clicks "Generate"
3. **Immediately sees loading cards** (no waiting)
4. Cards update automatically when ready (30-60 seconds)
5. Can click to preview, download, or edit

### Viewing Saved Infographs

1. User navigates to "Saved" page
2. Sees all infographs, including those still processing
3. **Processing items show live indicator**
4. Images appear automatically when ready
5. No need to refresh page

---

## 7. Code Examples

### Starting Polling (Dashboard)

```javascript
// After API returns infograph IDs
response.data.infographs.forEach((infograph) => {
  startPollingStatus(infograph.id)
})
```

### Polling Function

```javascript
const startPollingStatus = (infographId) => {
  // Initial check
  checkInfographStatus(infographId)

  // Poll every 3 seconds
  const interval = setInterval(() => {
    checkInfographStatus(infographId)
  }, 3000)

  pollingIntervals.value.set(infographId, interval)
}
```

### Status Check

```javascript
const checkInfographStatus = async (infographId) => {
  const response = await apiClient.get(`/infographs/status/${infographId}/`)

  // Update UI
  const index = results.value.findIndex((r) => r.id === infographId)
  results.value[index].status = response.data.status
  results.value[index].image = response.data.image_url

  // Stop if done
  if (response.data.status === 'completed' || response.data.status === 'failed') {
    clearInterval(pollingIntervals.value.get(infographId))
    pollingIntervals.value.delete(infographId)
  }
}
```

### Cleanup on Unmount

```javascript
onBeforeUnmount(() => {
  pollingIntervals.value.forEach((interval) => clearInterval(interval))
  pollingIntervals.value.clear()
})
```

---

## 8. Status States

| Status       | Description                     | Visible on Dashboard | Visible on Saved | Polling Active |
| ------------ | ------------------------------- | -------------------- | ---------------- | -------------- |
| `pending`    | Just created, not yet submitted | ✅ (rare)            | ✅               | ✅             |
| `processing` | Submitted to fal.ai, generating | ✅                   | ✅               | ✅             |
| `completed`  | Image ready, uploaded to R2     | ✅                   | ✅               | ❌             |
| `failed`     | Error during generation         | ✅                   | ✅               | ❌             |

---

## 9. Performance Considerations

### Polling Strategy

- Uses efficient `Map` data structure for interval tracking
- Stops polling immediately when generation completes
- Cleans up on component unmount to prevent memory leaks

### Network Efficiency

- Lightweight status endpoint (only returns necessary data)
- Polling intervals balanced between responsiveness and load
- Webhooks handle primary updates (polling is backup)

### User Experience

- Immediate feedback (no blank screens)
- Progressive enhancement (updates appear as ready)
- No manual refresh needed

---

## 10. Future Improvements

### Potential Enhancements

- [ ] WebSocket connections for instant updates (eliminate polling)
- [ ] Progress percentage from fal.ai
- [ ] Desktop notifications when generation completes
- [ ] Retry failed generations with one click
- [ ] Batch operations (delete/download multiple)

---

## Summary

The system provides a **seamless, real-time experience** where:

1. Users get immediate visual feedback
2. Status updates appear automatically
3. No page reloads required
4. Multiple infographs tracked independently
5. Clean resource management (no memory leaks)

Both the **Dashboard** and **Saved** pages use polling to keep users informed of generation progress without any manual intervention.

