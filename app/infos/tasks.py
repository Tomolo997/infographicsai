# tasks.py
import os
os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"
import time
import logging
from django.conf import settings
from django.utils import timezone
from datetime import datetime, time
from infos.models import InfoGraph

# Configure Celery if you're using it
from app.celery import app

logger = logging.getLogger(__name__)


@app.task
def cleanup_unsaved_infographs():
    """
    Daily task to clean up unsaved infographs that were created today.
    This task should be scheduled to run at the end of each day.
    """
    today = timezone.now().date()
    # Make timezone-aware datetimes
    today_start = timezone.make_aware(datetime.combine(today, time.min))
    today_end = timezone.make_aware(datetime.combine(today, time.max))

    # Find and delete unsaved infographs created today
    unsaved_infographs = InfoGraph.objects.filter(
        created_at__range=(today_start, today_end),
        is_saved=False
    )
    
    count = unsaved_infographs.count()
    unsaved_infographs.delete()
    
    logger.info(f"Cleaned up {count} unsaved infographs from {today}")
    return count
