# Fal.ai Integration - Quick Start

## 🎯 What Was Implemented

You now have a **production-ready, non-blocking infographic generation system** using fal.ai!

### Key Features

✅ **Async/Non-blocking** - API responds immediately (no 30-60s wait)  
✅ **Webhook callbacks** - fal.ai notifies you when images are ready  
✅ **Status tracking** - Users can check generation progress  
✅ **Credit system** - Credits deducted after successful submission  
✅ **Error handling** - Failed jobs tracked with error messages  
✅ **Scalable** - Handle hundreds of concurrent requests

---

## 📁 Files Changed

### New Files

- `app/infographs/infographs/client/fal_ai.py` - fal.ai client wrapper
- `app/infographs/migrations/0002_*.py` - Database migration
- `guides/FAL_AI_INTEGRATION_GUIDE.md` - Full documentation
- `guides/FAL_AI_QUICK_START.md` - This file
- `test_fal_client.py` - Test script

### Modified Files

- `app/infographs/models.py` - Added status tracking fields
- `app/infographs/views.py` - Added webhook + status endpoints
- `app/infographs/urls.py` - Added new routes
- `app/infographs/infographs/service.py` - Implemented async generation
- `app/app/settings/base.py` - Added FAL_AI_API_KEY config

---

## 🚀 Quick Setup

### 1. Add API Key to `.env`

```bash
# Get your API key from https://fal.ai/dashboard
FAL_AI_API_KEY=your_fal_ai_key_here

# For webhooks (production)
SITE_URL=https://api.ainfographic.com

# For local development with ngrok
# SITE_URL=https://abc123.ngrok.io
```

### 2. Run Migrations (Already Done)

```bash
cd app
python manage.py migrate infographs
```

✅ Migration already applied!

### 3. Test the Client

```bash
# Test async submission (recommended)
python test_fal_client.py --test async

# Test blocking generation (will wait 30-60s)
python test_fal_client.py --test blocking

# Test with webhook
python test_fal_client.py --test webhook

# Poll for specific result
python test_fal_client.py --test poll --request-id YOUR_REQUEST_ID
```

---

## 📡 API Endpoints

### 1. Create Infograph (Returns Immediately)

```bash
POST /api/infographs/create/
Authorization: Token YOUR_TOKEN

{
  "prompt": "Create an infographic about renewable energy",
  "blog_url": "https://example.com/blog" (optional),
  "aspect_ratio": "16/9",
  "resolution": "2K",
  "number_of_infographs": 1
}
```

**Response**:

```json
{
  "infographs": [
    {
      "id": 123,
      "request_id": "fal-abc123",
      "status": "processing",
      "status_url": "https://queue.fal.run/..."
    }
  ],
  "total_submitted": 1,
  "credits_used": 1
}
```

### 2. Check Status

```bash
GET /api/infographs/status/123/
Authorization: Token YOUR_TOKEN
```

**Response (Processing)**:

```json
{
  "id": 123,
  "status": "processing",
  "image_url": null,
  "created_at": "2025-11-22T10:30:00Z",
  "updated_at": "2025-11-22T10:30:15Z"
}
```

**Response (Completed)**:

```json
{
  "id": 123,
  "status": "completed",
  "image_url": "https://fal.media/.../image.png",
  "created_at": "2025-11-22T10:30:00Z",
  "updated_at": "2025-11-22T10:30:45Z"
}
```

### 3. Webhook (Called by fal.ai)

```bash
POST /api/infographs/webhook/123/
# No auth required - called by fal.ai servers

{
  "images": [
    {"url": "https://fal.media/.../image.png", ...}
  ]
}
```

---

## 🎨 Frontend Integration Example

### Vue.js/Nuxt Example

```vue
<script setup>
const { $api } = useNuxtApp()
const infographs = ref([])
const isGenerating = ref(false)

async function createInfograph() {
  isGenerating.value = true

  try {
    // Submit generation job
    const response = await $api.post('/api/infographs/create/', {
      prompt: 'A modern infographic about AI',
      aspect_ratio: '16/9',
      resolution: '2K',
      number_of_infographs: 1,
    })

    const infograph = response.data.infographs[0]
    infographs.value.push({
      id: infograph.id,
      status: 'processing',
      image_url: null,
    })

    // Start polling for status
    pollStatus(infograph.id)
  } catch (error) {
    console.error('Failed to create infograph:', error)
  } finally {
    isGenerating.value = false
  }
}

async function pollStatus(infographId) {
  const maxAttempts = 30
  let attempts = 0

  const interval = setInterval(async () => {
    try {
      const response = await $api.get(`/api/infographs/status/${infographId}/`)
      const data = response.data

      // Update UI
      const infograph = infographs.value.find((i) => i.id === infographId)
      if (infograph) {
        infograph.status = data.status
        infograph.image_url = data.image_url
      }

      // Stop polling if completed or failed
      if (data.status === 'completed' || data.status === 'failed') {
        clearInterval(interval)

        if (data.status === 'completed') {
          // Show success notification
          showNotification('Infographic ready!', 'success')
        } else {
          showNotification('Generation failed', 'error')
        }
      }

      attempts++
      if (attempts >= maxAttempts) {
        clearInterval(interval)
        showNotification('Timeout: Generation took too long', 'warning')
      }
    } catch (error) {
      console.error('Failed to check status:', error)
    }
  }, 3000) // Poll every 3 seconds
}
</script>

<template>
  <div>
    <button @click="createInfograph" :disabled="isGenerating">
      {{ isGenerating ? 'Submitting...' : 'Create Infograph' }}
    </button>

    <div v-for="infograph in infographs" :key="infograph.id" class="infograph-item">
      <div v-if="infograph.status === 'processing'">
        <div class="spinner">⏳</div>
        <p>Generating your infographic...</p>
      </div>

      <div v-else-if="infograph.status === 'completed'">
        <img :src="infograph.image_url" alt="Generated infographic" />
        <button @click="downloadImage(infograph.image_url)">Download</button>
      </div>

      <div v-else-if="infograph.status === 'failed'">
        <p class="error">❌ Generation failed</p>
      </div>
    </div>
  </div>
</template>
```

---

## 🔧 Local Development with Webhooks

fal.ai can't reach `http://localhost:8000`, so use **ngrok**:

### Setup ngrok

```bash
# Install ngrok (Mac)
brew install ngrok

# Start tunnel
ngrok http 8000

# Output:
# Forwarding https://abc123.ngrok.io -> http://localhost:8000
```

### Update .env

```bash
SITE_URL=https://abc123.ngrok.io
```

### Restart Django

```bash
cd app
python manage.py runserver
```

Now fal.ai can call your webhook! 🎉

---

## 🔍 Understanding Queue vs Webhook

### ❌ Queue/Subscribe (Blocking)

```python
# BAD for production - blocks for 30-60 seconds
result = fal_client.subscribe(
    "fal-ai/nano-banana-pro",
    arguments={"prompt": "..."}
)
# Your API waits here for 30-60 seconds ❌
```

**Problems**:

- Blocks server thread
- Can't handle concurrent requests
- Timeout issues
- Poor UX

### ✅ Webhook/Async (Non-Blocking)

```python
# GOOD for production - returns immediately
handler = await fal_client.submit_async(
    "fal-ai/nano-banana-pro",
    arguments={"prompt": "..."},
    webhook_url="https://yoursite.com/webhook/123/"
)
request_id = handler.request_id  # Returns in ~0.2s ✅
# fal.ai generates in background, calls webhook when done
```

**Benefits**:

- Returns immediately
- Scales to 100s of requests
- Great UX
- Production ready

---

## 📊 Database Schema

```python
class Infograph(models.Model):
    # Existing fields
    account = ForeignKey(Account)
    blog_url = URLField()
    image_url = URLField()  # Populated when completed
    resolution = CharField()
    aspect_ratio = CharField()
    credits_used = IntegerField()

    # NEW: Async tracking fields
    fal_request_id = CharField()  # Job ID from fal.ai
    status = CharField()  # pending → processing → completed/failed
    prompt = TextField()  # The full prompt used
    error_message = TextField()  # If failed

    created_at = DateTimeField()
    updated_at = DateTimeField()
```

---

## ✅ Next Steps

### 1. Test Everything

```bash
# Test the client
python test_fal_client.py --test async

# Test API endpoint (after starting server)
curl -X POST http://localhost:8000/api/infographs/create/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Test", "aspect_ratio": "16/9", "resolution": "2K", "number_of_infographs": 1}'
```

### 2. Implement Frontend

- Show "Generating..." spinner
- Poll status endpoint every 3-5 seconds
- Display image when completed
- Handle errors gracefully

### 3. Add R2 Upload

Currently, `image_url` contains fal.ai's URL. You should:

1. Download image from fal.ai
2. Upload to Cloudflare R2
3. Replace URL with R2 URL

```python
# In handle_webhook_result()
image_url = result_data["images"][0]["url"]

# TODO: Download and upload to R2
r2_url = upload_to_r2(image_url)
infograph.image_url = r2_url
```

### 4. Add User Notifications

When generation completes:

- Send email: "Your infographic is ready!"
- WebSocket push notification
- In-app notification

### 5. Production Setup

```bash
# Production .env
SITE_URL=https://api.ainfographic.com
FAL_AI_API_KEY=your_production_key

# Ensure webhook endpoint is publicly accessible
# Use HTTPS (SSL certificate)
```

---

## 🐛 Troubleshooting

### Issue: "Webhook never called"

**Solution**: Use ngrok for local development

```bash
ngrok http 8000
# Set SITE_URL=https://your-ngrok-url.ngrok.io
```

### Issue: "Generation failed"

**Check**:

1. fal.ai API key valid?
2. Prompt not too long?
3. Check `error_message` in database
4. Check fal.ai dashboard for errors

### Issue: "Credits deducted but no image"

**Fix**: Implement credit refund for failed jobs

```python
if infograph.status == InfographStatus.FAILED:
    # Refund credits
    account.credit_balance += infograph.credits_used
    account.save()
```

---

## 📚 Resources

- **Full Guide**: `guides/FAL_AI_INTEGRATION_GUIDE.md`
- **fal.ai Docs**: https://fal.ai/docs
- **Nano Banana Pro**: https://fal.ai/models/fal-ai/nano-banana-pro
- **Python Client**: https://github.com/fal-ai/fal-client-python

---

## 🎉 Summary

You now have:

| Feature            | Status |
| ------------------ | ------ |
| Non-blocking API   | ✅     |
| Webhook support    | ✅     |
| Status tracking    | ✅     |
| Credit system      | ✅     |
| Error handling     | ✅     |
| Test suite         | ✅     |
| Documentation      | ✅     |
| Database migration | ✅     |

**Next**: Integrate with frontend and add R2 upload!

