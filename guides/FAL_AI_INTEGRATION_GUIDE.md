# Fal.ai Async Infographic Generation Guide

## Overview

This guide explains how the fal.ai integration works for non-blocking infographic generation. The system uses **webhooks** to handle long-running image generation jobs (30-60 seconds) without blocking your API.

---

## 🏗️ Architecture

### How it Works: Queue vs Webhook

#### ❌ **Queue/Subscribe (Blocking - NOT USED)**

```python
result = fal_client.subscribe(
    "fal-ai/nano-banana-pro",
    arguments={"prompt": "..."},
    with_logs=True,
    on_queue_update=callback
)
```

- **Blocks** your API for 30-60 seconds waiting for result
- Provides real-time progress updates
- **Problem**: Can't handle many concurrent requests
- **Use case**: Admin tools, testing only

#### ✅ **Webhook/Submit Async (Non-Blocking - RECOMMENDED)**

```python
handler = await fal_client.submit_async(
    "fal-ai/nano-banana-pro",
    arguments={"prompt": "..."},
    webhook_url="https://your-site.com/api/infographs/webhook/123/"
)
# Returns immediately with request_id
```

- **Returns immediately** with `request_id`
- fal.ai processes in background
- fal.ai **calls your webhook** when done
- **Perfect for**: Production, high-volume apps

---

## 📊 Database Schema

The `Infograph` model now tracks async generation:

```python
class Infograph(models.Model):
    # ... existing fields ...

    # Async generation tracking
    fal_request_id = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, choices=InfographStatus.choices)
    prompt = models.TextField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
```

### Status Flow

```
PENDING → PROCESSING → COMPLETED
                     ↘ FAILED
```

---

## 🔄 API Flow

### 1. **Create Infograph** (User Request)

**Endpoint**: `POST /api/infographs/create/`

**Request**:

```json
{
  "prompt": "Create an infographic about climate change",
  "blog_url": "https://example.com/blog-post",
  "aspect_ratio": "16/9",
  "resolution": "2K",
  "number_of_infographs": 1
}
```

**Response** (Immediate):

```json
{
  "infographs": [
    {
      "id": 123,
      "request_id": "fal-request-abc123",
      "status": "processing",
      "status_url": "https://queue.fal.run/..."
    }
  ],
  "total_submitted": 1,
  "credits_used": 1
}
```

**What happens**:

1. ✅ Credits are checked and deducted
2. ✅ Blog URL is scraped (if provided)
3. ✅ Enhanced prompt is built
4. ✅ Job submitted to fal.ai with webhook URL
5. ✅ Database record created with `status=PROCESSING`
6. ✅ User receives response immediately (doesn't wait 30-60s!)

---

### 2. **Check Status** (User Polls)

**Endpoint**: `GET /api/infographs/status/<infograph_id>/`

**Response**:

```json
{
  "id": 123,
  "status": "processing", // or "completed", "failed"
  "image_url": null, // populated when completed
  "created_at": "2025-11-22T10:30:00Z",
  "updated_at": "2025-11-22T10:30:15Z"
}
```

**When completed**:

```json
{
  "id": 123,
  "status": "completed",
  "image_url": "https://images.ainfographic.com/abc123.png",
  "created_at": "2025-11-22T10:30:00Z",
  "updated_at": "2025-11-22T10:30:45Z"
}
```

---

### 3. **Webhook Callback** (fal.ai → Your Server)

**Endpoint**: `POST /api/infographs/webhook/<infograph_id>/`

**This endpoint is called by fal.ai servers** when generation completes.

**fal.ai sends**:

```json
{
  "images": [
    {
      "url": "https://fal.media/files/.../image.png",
      "width": 1920,
      "height": 1080,
      "content_type": "image/png"
    }
  ],
  "seed": 12345,
  "has_nsfw_concepts": [false],
  "prompt": "..."
}
```

**What happens**:

1. ✅ Webhook receives result
2. ✅ Image URL extracted
3. ✅ Status updated to `COMPLETED`
4. ✅ TODO: Upload image to R2 storage
5. ✅ TODO: Notify user (email/websocket)

---

## 🔧 Configuration

### Environment Variables

Add to your `.env` file:

```bash
# Fal.ai API Key
FAL_AI_API_KEY=your_fal_ai_api_key_here

# Site URL (for webhook URLs)
# Development
SITE_URL=http://localhost:8000

# Production
SITE_URL=https://api.ainfographic.com
```

### Important Notes

1. **Webhooks in Development**:

   - fal.ai cannot call `http://localhost:8000` (not publicly accessible)
   - Solutions:
     - Use **ngrok**: `ngrok http 8000` → Get public URL
     - Use **status polling** instead of webhooks
     - Deploy to staging server

2. **Webhooks in Production**:
   - Ensure your domain is publicly accessible
   - SSL/HTTPS required for production
   - Set `SITE_URL=https://api.ainfographic.com`

---

## 🧪 Testing

### Test 1: Create Infograph

```bash
curl -X POST http://localhost:8000/api/infographs/create/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A modern infographic about AI",
    "aspect_ratio": "16/9",
    "resolution": "2K",
    "number_of_infographs": 1
  }'
```

### Test 2: Check Status

```bash
curl http://localhost:8000/api/infographs/status/123/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Test 3: Simulate Webhook (Local Testing)

```bash
curl -X POST http://localhost:8000/api/infographs/webhook/123/ \
  -H "Content-Type: application/json" \
  -d '{
    "images": [
      {
        "url": "https://example.com/test.png",
        "width": 1920,
        "height": 1080
      }
    ]
  }'
```

---

## 🔌 Using ngrok for Local Development

Since fal.ai can't reach localhost, use ngrok:

```bash
# Install ngrok (if not installed)
brew install ngrok

# Start ngrok tunnel
ngrok http 8000

# You'll get output like:
# Forwarding   https://abc123.ngrok.io -> http://localhost:8000
```

Update your `.env`:

```bash
SITE_URL=https://abc123.ngrok.io
```

Now fal.ai can call your webhook!

---

## 📝 Code Examples

### FalAI Client Usage

```python
from infographs.infographs.client.fal_ai import FalAI

# Initialize client
client = FalAI()

# Submit async job (recommended)
result = client.submit_generation_sync(
    prompt="A beautiful infographic",
    webhook_url="https://yoursite.com/webhook/123/"
)
# Returns: {"request_id": "...", "status_url": "..."}

# Check result later (if no webhook)
result = client.get_result_sync(request_id="...")

# Blocking generation (NOT recommended for production)
result = client.generate_infographic_blocking(
    prompt="A beautiful infographic",
    on_progress_update=lambda msg: print(msg)
)
```

---

## 🚀 Next Steps / TODOs

1. **Upload to R2 Storage**

   - Download image from fal.ai URL
   - Upload to Cloudflare R2
   - Replace `image_url` with R2 URL

2. **User Notifications**

   - Send email when completed: "Your infographic is ready!"
   - WebSocket real-time updates
   - Push notifications (mobile)

3. **Frontend Integration**

   - Create infograph → Show "Processing..." UI
   - Poll status endpoint every 5 seconds
   - Display image when completed
   - Show error message if failed

4. **Error Handling**

   - Retry failed jobs
   - Handle webhook timeout (fal.ai timeout)
   - Refund credits on permanent failure

5. **Monitoring**
   - Track generation time metrics
   - Monitor webhook reliability
   - Alert on high failure rates

---

## 🐛 Troubleshooting

### Problem: Webhook never called

**Solutions**:

- Check `SITE_URL` is publicly accessible
- Use ngrok for local development
- Check fal.ai dashboard for webhook logs
- Use status polling as fallback

### Problem: Image generation fails

**Check**:

- Prompt is not too long (token limit)
- fal.ai API key is valid
- Account has sufficient fal.ai credits
- Check `error_message` field in database

### Problem: Credits deducted but no image

**Solution**:

- Check infograph status in database
- Look for `error_message`
- Implement credit refund logic for failures

---

## 📚 Resources

- [fal.ai Python Client Docs](https://fal.ai/docs/model-endpoints/client-libraries/python)
- [fal.ai Nano Banana Pro Model](https://fal.ai/models/fal-ai/nano-banana-pro)
- [Webhooks vs Polling Guide](https://requestbin.com/blog/working-with-webhooks/)

---

## Summary

| Aspect              | Implementation                          |
| ------------------- | --------------------------------------- |
| **Job Submission**  | Async via `submit_generation_sync()`    |
| **Status Tracking** | Database `status` field                 |
| **Result Delivery** | Webhook callback                        |
| **User Experience** | Immediate response, poll for status     |
| **Scalability**     | Can handle 100s of concurrent requests  |
| **Blocking Time**   | ~0.2s (submission only, not generation) |
