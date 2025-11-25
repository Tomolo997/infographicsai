import asyncio
from typing import Any, Dict, Optional

from django.conf import settings

import fal_client


class FalAI:
    """
    Async client for fal.ai image generation.
    
    Fal.ai Queue System:
    - Jobs are queued when submitted (non-blocking)
    - You receive a request_id immediately
    - Generation happens in background (30-60 seconds)
    - Results delivered via webhook or polling
    
    Webhook vs Subscribe:
    - subscribe(): Blocks until complete, gets progress updates (NOT recommended for production)
    - submit_async(): Returns immediately, webhook notified when done (RECOMMENDED)
    """
    
    def __init__(self):
        self.model = "fal-ai/nano-banana-pro"
        self.edit_model = "fal-ai/nano-banana-pro/edit"
    
    async def submit_generation(self, prompt: str, webhook_url: Optional[str] = None, **kwargs) -> Dict[str, str]:
        """
        Submit an infographic generation job (non-blocking).
        
        Args:
            prompt: The image generation prompt
            webhook_url: Optional URL where fal.ai will POST results when ready
            **kwargs: Additional arguments for the model
            
        Returns:
            Dict with 'request_id' and 'status_url' for checking progress
        """
        handler = await fal_client.submit_async(
            self.model,
            arguments={
                "prompt": prompt,
                **kwargs
            },
            webhook_url=webhook_url,
        )
        
        return {
            "request_id": handler.request_id,
            "status_url": f"https://queue.fal.run/fal-ai/nano-banana-pro/requests/{handler.request_id}/status"
        }
    
    def submit_generation_sync(
        self, 
        prompt: str, 
        webhook_url: Optional[str] = None,
        **kwargs
    ) -> Dict[str, str]:
        """
        Synchronous wrapper for submit_generation.
        Creates event loop if needed (for use in Django views).
        """
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(
            self.submit_generation(prompt, webhook_url, **kwargs)
        )
    
    async def get_result(self, request_id: str) -> Dict[str, Any]:
        """
        Poll for generation result by request_id.
        Use this if you didn't provide a webhook_url.
        
        Args:
            request_id: The request_id from submit_generation
            
        Returns:
            The generation result with image URL
        """
        result = await fal_client.result_async(
            self.model,
            request_id
        )
        return result
    
    def get_result_sync(self, request_id: str) -> Dict[str, Any]:
        """Synchronous wrapper for get_result."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.get_result(request_id))
    
    def generate_infographic_blocking(
        self, 
        prompt: str,
        on_progress_update=None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        BLOCKING generation with progress updates.
        Only use for testing or admin tools, NOT for production API endpoints!
        
        Args:
            prompt: The image generation prompt
            on_progress_update: Optional callback for progress logs
            **kwargs: Additional arguments for the model
            
        Returns:
            The complete generation result with image URL
        """
        def default_on_queue_update(update):
            if isinstance(update, fal_client.InProgress):
                logs = getattr(update, 'logs', None)
                if logs:
                    for log in logs:
                        print(f"[FAL.AI] {log['message']}")
                        if on_progress_update:
                            on_progress_update(log['message'])
        
        result = fal_client.subscribe(
            self.model,
            arguments={
                "prompt": prompt,
                **kwargs
            },
            with_logs=True,
            on_queue_update=default_on_queue_update,
        )
        
        return result
    
    async def submit_edit_generation(
        self, 
        prompt: str,
        image_urls: list,
        webhook_url: Optional[str] = None,
        **kwargs
    ) -> Dict[str, str]:
        """
        Submit an edit generation job using nano-banana-pro/edit (non-blocking).
        Uses template images to guide the generation.
        
        Args:
            prompt: The image generation prompt
            image_urls: List of template image URLs to use as reference
            webhook_url: Optional URL where fal.ai will POST results when ready
            **kwargs: Additional arguments for the model
            
        Returns:
            Dict with 'request_id' and 'status_url' for checking progress
        """
        handler = await fal_client.submit_async(
            self.edit_model,
            arguments={
                "prompt": prompt,
                "image_urls": image_urls,
                **kwargs
            },
            webhook_url=webhook_url,
        )
        
        return {
            "request_id": handler.request_id,
            "status_url": f"https://queue.fal.run/fal-ai/nano-banana-pro/edit/requests/{handler.request_id}/status"
        }
    
    def submit_edit_generation_sync(
        self, 
        prompt: str,
        image_urls: list,
        webhook_url: Optional[str] = None,
        **kwargs
    ) -> Dict[str, str]:
        """
        Synchronous wrapper for submit_edit_generation.
        Creates event loop if needed (for use in Django views).
        """
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(
            self.submit_edit_generation(prompt, image_urls, webhook_url, **kwargs)
        )