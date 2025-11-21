# Transitions Video Generation - Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            YOUR APPLICATION                              │
│                                                                          │
│  ┌─────────────────┐        ┌──────────────────┐                       │
│  │   Frontend/API  │        │  Django Shell    │                       │
│  │   Request       │        │  Direct Call     │                       │
│  └────────┬────────┘        └────────┬─────────┘                       │
│           │                          │                                  │
│           ▼                          ▼                                  │
│  ┌──────────────────────────────────────────────────────┐              │
│  │         INTERFACE LAYER (views.py / service.py)      │              │
│  │                                                       │              │
│  │  REST API Endpoints        Service Functions         │              │
│  │  - /batch-generate/        - create_transition()     │              │
│  │  - /create-and-generate/   - generate_video()        │              │
│  │  - /task-status/<id>/      - create_and_generate()   │              │
│  └──────────────────┬───────────────────────────────────┘              │
│                     │                                                   │
└─────────────────────┼───────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         TASK QUEUE LAYER                                │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │                    CELERY (tasks.py)                          │      │
│  │                                                                │      │
│  │  ┌────────────────────────────────────────────────────────┐  │      │
│  │  │  generate_video_task()                                 │  │      │
│  │  │  - Single video generation                             │  │      │
│  │  └────────────────────────────────────────────────────────┘  │      │
│  │                                                                │      │
│  │  ┌────────────────────────────────────────────────────────┐  │      │
│  │  │  create_and_generate_video_task()                      │  │      │
│  │  │  - Create transition + generate video                  │  │      │
│  │  └────────────────────────────────────────────────────────┘  │      │
│  │                                                                │      │
│  │  ┌────────────────────────────────────────────────────────┐  │      │
│  │  │  batch_generate_videos_task() ⭐                       │  │      │
│  │  │  - Parallel generation for existing transitions        │  │      │
│  │  └────────────────────────────────────────────────────────┘  │      │
│  │                                                                │      │
│  │  ┌────────────────────────────────────────────────────────┐  │      │
│  │  │  batch_create_and_generate_task() ⭐                   │  │      │
│  │  │  - Parallel create + generate for multiple             │  │      │
│  │  └────────────────────────────────────────────────────────┘  │      │
│  └────────────────────────┬─────────────────────────────────────┘      │
│                           │                                             │
│                           ▼                                             │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │                   REDIS QUEUE                                 │      │
│  │                                                                │      │
│  │   [Task 1] [Task 2] [Task 3] ... [Task 10]                   │      │
│  └────────┬──────┬──────┬──────────────┬──────────────┬─────────┘      │
│           │      │      │              │              │                 │
└───────────┼──────┼──────┼──────────────┼──────────────┼─────────────────┘
            │      │      │              │              │
            ▼      ▼      ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        WORKER POOL                                       │
│                                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         ┌──────────┐        │
│  │ Worker 1 │  │ Worker 2 │  │ Worker 3 │   ...   │ Worker10 │        │
│  │          │  │          │  │          │         │          │        │
│  │ Task 1   │  │ Task 2   │  │ Task 3   │         │ Task 10  │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘         └────┬─────┘        │
│       │             │             │                     │               │
└───────┼─────────────┼─────────────┼─────────────────────┼───────────────┘
        │             │             │                     │
        ▼             ▼             ▼                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      VIDEO GENERATION LAYER                              │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │                     FAL CLIENT (client.py)                    │      │
│  │                                                                │      │
│  │  - FalClient.generate_video()                                 │      │
│  │  - API: fal-ai/kling-video/v2.1/pro/image-to-video          │      │
│  └────────────────────────┬─────────────────────────────────────┘      │
│                           │                                             │
└───────────────────────────┼─────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        EXTERNAL API                                      │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │                      FAL.AI API                               │      │
│  │                                                                │      │
│  │  Input:  prompt + front_image + tail_image                   │      │
│  │  Output: video_url (5-10 minutes processing)                 │      │
│  └────────────────────────┬─────────────────────────────────────┘      │
│                           │                                             │
└───────────────────────────┼─────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                        DATABASE LAYER                                    │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────┐      │
│  │                 PostgreSQL (models.py)                        │      │
│  │                                                                │      │
│  │  ┌────────────────────────────────────────────────────────┐  │      │
│  │  │  Transition Model                                       │  │      │
│  │  │  - account, front_image, tail_image                    │  │      │
│  │  │  - transition_type, duration, prompt                   │  │      │
│  │  │  - video_url ← Updated after generation               │  │      │
│  │  │  - enable_subtitles, audio_url, subtitles             │  │      │
│  │  └────────────────────────────────────────────────────────┘  │      │
│  │                                                                │      │
│  │  ┌────────────────────────────────────────────────────────┐  │      │
│  │  │  GeneratedTransition Model                              │  │      │
│  │  │  - transitions (M2M), video_url, audio_url             │  │      │
│  │  └────────────────────────────────────────────────────────┘  │      │
│  └──────────────────────────────────────────────────────────────┘      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Data Flow - Single Video Generation

```
┌────────────┐
│   Client   │  POST /api/transitions/create-and-generate/
└──────┬─────┘
       │
       ▼
┌────────────────────────────────────────────────────┐
│  CreateAndGenerateVideoView                        │
│  1. Validate input                                 │
│  2. Submit task to Celery                          │
│  3. Return task_id immediately                     │
└──────┬─────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────┐
│  create_and_generate_video_task (Celery)           │
│  1. Create Transition record in DB                 │
│  2. Queue generate_video_task                      │
│  3. Return status                                  │
└──────┬─────────────────────────────────────────────┘
       │
       ▼
┌────────────────────────────────────────────────────┐
│  generate_video_task (Celery Worker)               │
│  1. Get Transition from DB                         │
│  2. Call FalClient.generate_video()                │
│  3. Wait for FAL API (5-10 minutes)                │
│  4. Save video_url to DB                           │
│  5. Return success/failure                         │
└──────┬─────────────────────────────────────────────┘
       │
       ▼
┌────────────┐
│  Complete  │  Transition.video_url is now set
└────────────┘
```

## Data Flow - Batch Processing (10 Videos in Parallel)

```
┌────────────┐
│   Client   │  POST /api/transitions/batch-create-and-generate/
└──────┬─────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│  BatchCreateAndGenerateView                                   │
│  1. Validate all 10 transitions data                         │
│  2. Submit batch task to Celery                              │
│  3. Return task_group_id immediately                         │
└──────┬───────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│  batch_create_and_generate_task                              │
│  1. Splits into 10 individual tasks                          │
│  2. Queues all tasks in Redis                                │
└──────┬───────────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│  REDIS QUEUE                                                  │
│  [Task1][Task2][Task3][Task4][Task5]...[Task10]             │
└──────┬───────────────────────────────────────────────────────┘
       │
       ├──────────────┬──────────────┬──────────────┬─────────┐
       ▼              ▼              ▼              ▼         ▼
   ┌────────┐    ┌────────┐    ┌────────┐    ┌────────┐  ...
   │Worker 1│    │Worker 2│    │Worker 3│    │Worker10│
   │        │    │        │    │        │    │        │
   │ Task 1 │    │ Task 2 │    │ Task 3 │    │ Task 10│
   └───┬────┘    └───┬────┘    └───┬────┘    └───┬────┘
       │             │             │              │
       │             │             │              │
       ▼             ▼             ▼              ▼
   ┌────────────────────────────────────────────────────┐
   │  ALL WORKERS RUN IN PARALLEL                       │
   │                                                     │
   │  Each:                                              │
   │  1. Create Transition in DB                        │
   │  2. Call FalClient.generate_video()                │
   │  3. Wait for FAL API (5-10 min)                    │
   │  4. Save video_url to DB                           │
   └─────────────────────┬──────────────────────────────┘
                         │
                         ▼
                   ┌────────────┐
                   │  Complete  │  10 videos in ~10 minutes
                   │   10 URLs  │  (instead of 100 minutes!)
                   └────────────┘
```

## Component Responsibilities

### 1. Views (views.py) - API Layer
- Validate incoming requests
- Submit tasks to Celery
- Return task IDs immediately (non-blocking)
- Provide task status endpoints

### 2. Service (service.py) - Business Logic
- Direct Python functions for simple use cases
- Create transitions
- Generate videos synchronously
- Used when you don't need async processing

### 3. Tasks (tasks.py) - Async Processing ⭐
- **Core of parallel processing**
- Individual tasks: `generate_video_task`, `create_and_generate_video_task`
- Batch tasks: `batch_generate_videos_task`, `batch_create_and_generate_task`
- Auto-retry on failure (up to 3 times)
- Celery manages distribution across workers

### 4. Client (client.py) - External API
- Interface to FAL.AI API
- Handles video generation requests
- Manages timeouts and errors
- Returns video URLs

### 5. Models (models.py) - Data Layer
- `Transition`: Individual transition records
- `GeneratedTransition`: Combined transitions
- Store all metadata and video URLs

### 6. Celery Workers - Execution Layer
- Run tasks in parallel
- Configurable concurrency (1-50+ workers)
- Managed by Celery + Redis

## Scaling Strategy

### Current: 10 Parallel Videos
```bash
celery -A app worker --concurrency=10 -l info
```

### Scale to 20 Parallel Videos
```bash
celery -A app worker --concurrency=20 -l info
```

### Multi-Server Scaling
```
Server 1: celery -A app worker --concurrency=10 --hostname=worker1@%h
Server 2: celery -A app worker --concurrency=10 --hostname=worker2@%h
Server 3: celery -A app worker --concurrency=10 --hostname=worker3@%h

Total: 30 parallel videos across 3 servers!
```

## Monitoring Stack

```
┌─────────────────────────────────────────────┐
│              Flower (Web UI)                │
│        http://localhost:5555                │
│                                             │
│  - Active tasks                             │
│  - Worker status                            │
│  - Task history                             │
│  - Retry failed tasks                       │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│          Celery Inspect API                 │
│  celery -A app inspect active               │
│  celery -A app inspect stats                │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────────┐
│          Task Status Endpoint               │
│  GET /api/transitions/task-status/<id>/     │
└─────────────────────────────────────────────┘
```

## Error Handling Flow

```
Task Execution
     │
     ▼
[Try Execute]
     │
     ├─── SUCCESS ──→ Save video_url ──→ Return success
     │
     └─── FAILURE
            │
            ▼
       [Retry 1]
            │
            ├─── SUCCESS ──→ Save video_url ──→ Return success
            │
            └─── FAILURE
                   │
                   ▼
              [Retry 2]
                   │
                   ├─── SUCCESS ──→ Save video_url ──→ Return success
                   │
                   └─── FAILURE
                          │
                          ▼
                     [Retry 3]
                          │
                          ├─── SUCCESS ──→ Save video_url ──→ Return success
                          │
                          └─── FAILURE ──→ Return error (Max retries exceeded)
```

## Summary

This architecture provides:

✅ **Scalability**: Handle 10, 20, 50+ parallel videos
✅ **Reliability**: Auto-retry, error handling, monitoring
✅ **Flexibility**: Use sync functions OR async tasks
✅ **Performance**: 10x faster with parallel processing
✅ **Monitoring**: Flower UI + task status API
✅ **Production-Ready**: Battle-tested tech stack (Celery + Redis)

**Key Innovation**: The batch tasks (`batch_generate_videos_task` and `batch_create_and_generate_task`) enable true parallel processing, answering your core question: "How to run 10 requests in parallel with a queue?"

