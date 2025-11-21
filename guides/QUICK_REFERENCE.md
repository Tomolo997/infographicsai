# Transitions Service - Quick Reference Card

## 🚀 Start Services

```bash
# Terminal 1: Redis (if not running)
redis-server

# Terminal 2: Celery Worker (10 parallel workers)
celery -A app worker -l info --concurrency=10

# Terminal 3: Django
python manage.py runserver

# Terminal 4: Flower (monitoring)
celery -A app flower
```

## 📝 Generate 10 Videos in Parallel

### Option 1: Python (Django Shell)

```python
from transitions.tasks import batch_create_and_generate_task

transitions = [
    {
        'account_id': 1,
        'front_image': f'https://example.com/img{i}.jpg',
        'tail_image': f'https://example.com/img{i+1}.jpg',
        'transition_type': 'ENERGETIC',
        'duration': 5,
        'prompt': f'Transition {i}'
    }
    for i in range(10)
]

result = batch_create_and_generate_task.delay(transitions)
print(f"Task ID: {result.id}")
```

### Option 2: REST API

```bash
curl -X POST http://localhost:8000/api/v1/transitions/batch-create-and-generate/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "transitions": [
      {
        "front_image": "https://...",
        "tail_image": "https://...",
        "transition_type": "ENERGETIC",
        "duration": 5,
        "prompt": "Transition 1"
      }
      // ... add 9 more
    ]
  }'
```

## 🔍 Check Task Status

### Python

```python
from celery.result import AsyncResult

task = AsyncResult('task-id-here')
print(task.state)  # PENDING, STARTED, SUCCESS, FAILURE
print(task.ready())  # True if complete
print(task.result)  # Get result
```

### REST API

```bash
curl http://localhost:8000/api/v1/transitions/task-status/TASK_ID/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## 📊 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/generate-video/` | POST | Generate video for existing transition |
| `/create-and-generate/` | POST | Create transition + generate video |
| `/batch-generate/` | POST | **Batch generate (parallel)** ⭐ |
| `/batch-create-and-generate/` | POST | **Batch create + generate** ⭐ |
| `/task-status/<task_id>/` | GET | Check task status |

## 🧪 Test Your Setup

```python
# In Django shell
from transitions.test_service import run_all_tests
run_all_tests()
```

## 📈 Monitor with Flower

```bash
celery -A app flower
# Visit: http://localhost:5555
```

## ⚙️ Configuration

### Increase Parallel Workers

```bash
# 20 parallel workers
celery -A app worker --concurrency=20 -l info

# Auto-scale (5-20 workers)
celery -A app worker --autoscale=20,5 -l info
```

### Check Active Workers

```bash
celery -A app inspect active
celery -A app inspect stats
```

## 🐛 Troubleshooting

### Celery Not Running

```bash
# Check Redis
redis-cli ping  # Should return: PONG

# Start Celery
celery -A app worker -l info --concurrency=10
```

### Check FAL_KEY

```bash
# In Django shell
import os
print(os.getenv('FAL_KEY'))
```

### View Celery Logs

```bash
celery -A app worker -l debug
```

## 📚 Full Documentation

- **Setup Guide**: `TRANSITIONS_SETUP_GUIDE.md`
- **Detailed Docs**: `app/transitions/README.md`
- **Examples**: `app/transitions/example_usage.py`
- **Tests**: `app/transitions/test_service.py`

## 🎯 Key Features

✅ **Synchronous service functions** for direct usage
✅ **Asynchronous Celery tasks** for background processing
✅ **Batch processing** - Generate 10+ videos in parallel
✅ **REST API endpoints** with proper error handling
✅ **Auto-retry** - Tasks retry up to 3 times on failure
✅ **Monitoring** - Track progress with Flower
✅ **Type hints** - Full type annotations for IDE support

## 💡 Pro Tips

1. **Always use batch tasks** when generating multiple videos
2. **Monitor with Flower** in production
3. **Set appropriate timeouts** (video generation takes 5-10 min)
4. **Configure concurrency** based on your server resources
5. **Use Redis persistence** in production

## 🔥 Quick Win

```python
# Generate 10 videos in ~10 minutes (instead of 100 minutes!)
from transitions.tasks import batch_create_and_generate_task

data = [{'account_id': 1, 'front_image': '...', 'tail_image': '...', 
         'transition_type': 'ENERGETIC', 'duration': 5, 
         'prompt': f'Video {i}'} for i in range(10)]

result = batch_create_and_generate_task.delay(data)
print(f"🎬 Generating 10 videos in parallel! Task: {result.id}")
```

