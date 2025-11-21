# Transitions Video Generation Setup Guide

## Overview

You now have a complete video generation system for transitions with support for **parallel processing of multiple videos** using Celery task queues.

## What Was Created

### 1. Service Functions (`app/transitions/service.py`)
- `create_transition()` - Create transition records
- `generate_transition_video()` - Generate video synchronously
- `create_and_generate_transition()` - Combined create + generate

### 2. Celery Tasks (`app/transitions/tasks.py`)
- `generate_video_task()` - Single async video generation
- `create_and_generate_video_task()` - Create transition + generate video async
- `batch_generate_videos_task()` - **Generate multiple videos in parallel** ⭐
- `batch_create_and_generate_task()` - **Create multiple + generate in parallel** ⭐

### 3. REST API Views (`app/transitions/views.py`)
- `POST /api/v1/transitions/generate-video/` - Single video generation
- `POST /api/v1/transitions/create-and-generate/` - Create and generate
- `POST /api/v1/transitions/batch-generate/` - **Batch generate (parallel)** ⭐
- `POST /api/v1/transitions/batch-create-and-generate/` - **Batch create + generate** ⭐
- `GET /api/v1/transitions/task-status/<task_id>/` - Check task status

### 4. Documentation
- `app/transitions/README.md` - Comprehensive documentation
- `app/transitions/example_usage.py` - Code examples

## Quick Start

### 1. Make Sure Celery is Running

```bash
# Terminal 1: Start Celery Worker with 10 concurrent workers
celery -A app worker -l info --concurrency=10

# Terminal 2: Start Django server
python manage.py runserver

# Terminal 3: (Optional) Start Flower for monitoring
pip install flower
celery -A app flower
# Then visit http://localhost:5555
```

### 2. Generate 10 Videos in Parallel (Python)

```python
from transitions.tasks import batch_create_and_generate_task

# Prepare 10 transitions
transitions_data = []
for i in range(10):
    transitions_data.append({
        'account_id': 1,  # Your account ID
        'front_image': f'https://example.com/image{i*2}.jpg',
        'tail_image': f'https://example.com/image{i*2+1}.jpg',
        'transition_type': 'ENERGETIC',
        'duration': 5,
        'prompt': f'Smooth transition number {i+1}',
        'name': f'Transition {i+1}'
    })

# Submit all 10 at once - they'll run in parallel!
result = batch_create_and_generate_task.delay(transitions_data)
print(f"Task group ID: {result.id}")
```

### 3. Generate 10 Videos in Parallel (REST API)

```bash
curl -X POST http://localhost:8000/api/v1/transitions/batch-create-and-generate/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "transitions": [
      {
        "front_image": "https://example.com/img1.jpg",
        "tail_image": "https://example.com/img2.jpg",
        "transition_type": "ENERGETIC",
        "duration": 5,
        "prompt": "Transition 1"
      },
      {
        "front_image": "https://example.com/img3.jpg",
        "tail_image": "https://example.com/img4.jpg",
        "transition_type": "CALM",
        "duration": 10,
        "prompt": "Transition 2"
      }
      // ... add up to 10 more
    ]
  }'
```

### 4. Check Task Status

```bash
curl http://localhost:8000/api/v1/transitions/task-status/TASK_ID/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## How Parallel Processing Works

### The Magic: Celery + Redis

1. **Celery Worker Pool**: When you run `celery -A app worker --concurrency=10`, Celery creates 10 worker processes
2. **Task Queue**: Tasks are queued in Redis
3. **Parallel Execution**: Up to 10 tasks run simultaneously (configurable)
4. **Auto-retry**: Failed tasks automatically retry up to 3 times

### Visual Flow

```
Your Request → batch_create_and_generate_task()
                          ↓
              Splits into 10 individual tasks
                          ↓
              Redis Queue (manages distribution)
                          ↓
         ┌────────────────┼────────────────┐
         ↓                ↓                ↓
    Worker 1         Worker 2    ...  Worker 10
    Task 1           Task 2           Task 10
    Video 1          Video 2          Video 10
         ↓                ↓                ↓
    5-10 mins        5-10 mins        5-10 mins
         ↓                ↓                ↓
    ✅ Done          ✅ Done          ✅ Done
```

**Time Savings:**
- Sequential (1 at a time): 10 videos × 10 minutes = **100 minutes** ⏰
- Parallel (10 at once): 10 videos = **~10 minutes** ⚡

## Configuration

### Increase Concurrency for More Parallel Jobs

```bash
# Run up to 20 videos in parallel
celery -A app worker -l info --concurrency=20

# Or use autoscaling (min 5, max 20 workers)
celery -A app worker -l info --autoscale=20,5
```

### Add to settings.py (optional optimizations)

```python
# Better for parallel processing
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_PREFETCH_MULTIPLIER = 1

# Prevent tasks from hanging
CELERY_TASK_TIME_LIMIT = 900  # 15 minutes hard limit
CELERY_TASK_SOFT_TIME_LIMIT = 600  # 10 minutes soft limit
```

## Testing

### Test Single Video Generation

```python
# Django shell
python manage.py shell

>>> from transitions.tasks import create_and_generate_video_task
>>> from account.models import Account
>>> account = Account.objects.first()
>>> result = create_and_generate_video_task.delay(
...     account_id=account.id,
...     front_image="https://example.com/img1.jpg",
...     tail_image="https://example.com/img2.jpg",
...     transition_type="ENERGETIC",
...     duration=5,
...     prompt="Test transition"
... )
>>> print(f"Task ID: {result.id}")
```

### Test Batch Processing

```python
>>> from transitions.tasks import batch_generate_videos_task
>>> # Assuming you have transitions with IDs 1-10
>>> result = batch_generate_videos_task.delay([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
>>> print(f"Task group ID: {result.id}")
```

## Monitoring

### Using Flower (Web UI)

```bash
# Install
pip install flower

# Run
celery -A app flower

# Open browser
http://localhost:5555
```

Features:
- See active tasks
- Monitor worker status
- View task history
- Retry failed tasks

### Using Django Shell

```python
from celery.result import AsyncResult

# Check task status
task = AsyncResult('your-task-id')
print(f"State: {task.state}")
print(f"Ready: {task.ready()}")

if task.ready():
    print(f"Result: {task.result}")
```

## Troubleshooting

### Issue: Tasks Not Running in Parallel

**Solution:**
```bash
# Check worker info
celery -A app inspect active

# Make sure you have enough workers
celery -A app worker --concurrency=10 -l info
```

### Issue: Redis Connection Failed

**Solution:**
```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG

# If not running, start it
redis-server
```

### Issue: Tasks Failing with FAL_KEY Error

**Solution:**
```bash
# Make sure FAL_KEY is in your .env file
echo "FAL_KEY=your-key-here" >> app/.env
```

### Issue: Videos Taking Too Long

This is normal! Video generation takes 5-10 minutes per video. That's why parallel processing is important.

**Tips:**
- Always use batch tasks for multiple videos
- Set appropriate concurrency (10-20 workers)
- Monitor with Flower
- Use proper timeouts in your code

## Production Recommendations

1. **Use Supervisor** to keep Celery running
2. **Enable Flower** for monitoring
3. **Set up logging** to track video generation
4. **Use Redis persistence** to prevent data loss
5. **Configure autoscaling** based on load
6. **Set task time limits** to prevent hanging

## Next Steps

1. ✅ Start Celery worker: `celery -A app worker --concurrency=10 -l info`
2. ✅ Test single video generation
3. ✅ Test batch processing with 2-3 videos
4. ✅ Scale up to 10+ videos in parallel
5. ✅ Set up Flower for monitoring
6. ✅ Integrate into your frontend application

## Need Help?

- Check `app/transitions/README.md` for detailed documentation
- See `app/transitions/example_usage.py` for code examples
- Visit Celery docs: https://docs.celeryq.dev/
- Visit Flower docs: https://flower.readthedocs.io/

## Summary

You now have:
- ✅ Service functions for direct usage
- ✅ Celery tasks for async processing
- ✅ **Batch processing for 10+ videos in parallel** ⭐
- ✅ REST API endpoints
- ✅ Complete documentation and examples
- ✅ Monitoring with Flower

**The key feature you asked about:** You can now run **10 video generation requests in parallel** using `batch_generate_videos_task()` or the `/batch-generate/` endpoint!

