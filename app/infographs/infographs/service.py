from typing import Any, Dict, Optional

from django.conf import settings

from infographs.infographs.client.fal_ai import FalAI
from infographs.infographs.client.url_client import URLAnalyzer
from infographs.infographs.exceptions import NotEnoughCreditsException
from infographs.models import Infograph, InfographStatus

from account.models import Account


def create_infograph(
  account: Account,
  prompt: str,
  blog_url: str,
  aspect_ratio: str,
  resolution: str,
  number_of_infographs: int
) -> Dict[str, Any]:
    """
    Create infograph(s) and submit async generation jobs to fal.ai.
    
    Returns immediately with infograph IDs and status.
    Actual image generation happens in background.
    """
    credits_used = 1
    if resolution == "4K":
        credits_used += 1
    
    # Check if the account has enough credits
    total_credits_needed = credits_used * number_of_infographs
    if account.credit_balance < total_credits_needed:
        raise NotEnoughCreditsException(
            f"You need {total_credits_needed} credits but have {account.credit_balance}"
        )
    
    # Scrape the blog and get the content if URL provided
    blog_content = None
    if blog_url:
        blog_data = URLAnalyzer()._scrape_website(blog_url)
        blog_content = blog_data.get("content", "")
    
    # Build the enhanced prompt
    enhanced_prompt = _build_prompt(prompt, blog_content, aspect_ratio)
    
    # Initialize fal.ai client
    fal_client = FalAI()
    
    # Create webhook URL for receiving results
    webhook_base_url = getattr(settings, 'SITE_URL', 'http://localhost:8000')
    
    # Create infographs and submit generation jobs
    infographs = []
    for i in range(number_of_infographs):
        # Create infograph record with PENDING status
        infograph = Infograph.objects.create(
            account=account,
            blog_url=blog_url,
            blog_json={"content": blog_content} if blog_content else None,
            resolution=resolution,
            aspect_ratio=aspect_ratio,
            credits_used=credits_used,
            prompt=enhanced_prompt,
            status=InfographStatus.PENDING,
        )
        
        try:
            # Submit async generation job to fal.ai

            webhook_url = f"{webhook_base_url}/api/infographs/webhook/{infograph.id}/"
            print("webhook_url", webhook_url)
            result = fal_client.submit_generation_sync(
                prompt=enhanced_prompt,
                webhook_url=webhook_url,
                aspect_ratio=aspect_ratio,
            )
            
            # Update with request ID and mark as PROCESSING
            infograph.fal_request_id = result["request_id"]
            infograph.status = InfographStatus.PROCESSING
            infograph.save()
            
            infographs.append({
                "id": infograph.id,
                "request_id": result["request_id"],
                "status": infograph.status,
                "status_url": result.get("status_url"),
            })
            
        except Exception as e:
            # Mark as failed if submission fails
            infograph.status = InfographStatus.FAILED
            infograph.error_message = str(e)
            infograph.save()
            print("error", e)
            infographs.append({
                "id": infograph.id,
                "status": InfographStatus.FAILED,
                "error": str(e),
            })
    
    # Deduct credits only after successful submission
    account.credit_balance -= total_credits_needed
    account.save()
    
    return {
        "infographs": infographs,
        "total_submitted": len(infographs),
        "credits_used": total_credits_needed,
    }


def _build_prompt(user_prompt: str, blog_content: Optional[str], aspect_ratio: str) -> str:
    """Build enhanced prompt for infographic generation."""
    base_prompt = f"""Create a modern, professional infographic with the following specifications:

User Request: {user_prompt}
"""
    
    if blog_content:
        # Truncate content to avoid token limits
        truncated_content = blog_content[:1000] + "..." if len(blog_content) > 1000 else blog_content
        base_prompt += f"""

Blog Content Summary:
{truncated_content}

Extract key information from the blog and present it visually in the infographic."""
    
    return base_prompt


def _get_image_size(aspect_ratio: str, resolution: str) -> str:
    """
    Map aspect ratio and resolution to image dimensions.
    fal.ai typically accepts: square, portrait, landscape, or specific dimensions
    """
    
    size_map = {
        ("9/16", "1K"): "9:",
        ("9/16", "2K"): "portrait_4_3",
        ("9/16", "4K"): "portrait_4_3",
        ("1/1", "1K"): "square",
        ("1/1", "2K"): "square_hd",
        ("1/1", "4K"): "square_hd",
        ("16/9", "1K"): "landscape_4_3",
        ("16/9", "2K"): "landscape_16_9",
        ("16/9", "4K"): "landscape_16_9",

    }
    
    return size_map.get((aspect_ratio, resolution), "square_hd")


def handle_webhook_result(infograph_id: int, result_data: Dict[str, Any]) -> Infograph:
    """
    Handle webhook callback from fal.ai when generation completes.
    
    Args:
        infograph_id: The infograph database ID
        result_data: The result from fal.ai
    """
    try:
        infograph = Infograph.objects.get(id=infograph_id)
        print("results", result_data)
        # Extract status, error, and payload
        fal_status = result_data.get("status")
        fal_error = result_data.get("error")
        payload = result_data.get("payload", {})

        # Default to None
        image_url = None

        # Extract image URL from payload if available
        if "images" in payload and payload["images"]:
            image_url = payload["images"][0].get("url")

        # Mark status based on received data
        if fal_status == "OK" and image_url:
            infograph.image_url = image_url
            infograph.status = InfographStatus.COMPLETED
            infograph.error_message = None
            infograph.save()
            return infograph

        # Mark as failed if error or image is not available
        infograph.status = InfographStatus.FAILED
        if fal_error:
            infograph.error_message = str(fal_error)
        else:
            infograph.error_message = "No image generated from fal.ai response"
        infograph.save()
        return infograph
        # Check if generation was successful
        if "url" in result_data and len(result_data["url"]) > 0:
            # TODO: Upload to R2 storage and replace URL
            infograph.image_url = result_data["url"]
            infograph.status = InfographStatus.COMPLETED
            infograph.save()
                
            # TODO: Send notification to user (email/websocket)
            return infograph
        
        # If we got here, something went wrong
        infograph.status = InfographStatus.FAILED
        infograph.error_message = "No image URL in response"
        infograph.save()
        
    except Infograph.DoesNotExist:
        raise ValueError(f"Infograph {infograph_id} not found")
    except Exception as e:
        # Mark as failed on any error
        infograph.status = InfographStatus.FAILED
        infograph.error_message = str(e)
        infograph.save()
    
    return infograph


def get_infograph_status(infograph_id: int) -> Dict[str, Any]:
    """
    Get the current status of an infograph generation.
    Can optionally poll fal.ai if still processing.
    """
    infograph = Infograph.objects.get(id=infograph_id)
    
    response = {
        "id": infograph.id,
        "status": infograph.status,
        "image_url": infograph.image_url,
        "created_at": infograph.created_at.isoformat(),
        "updated_at": infograph.updated_at.isoformat(),
    }
    
    # If still processing and we have a request_id, we could poll fal.ai
    if infograph.status == InfographStatus.PROCESSING and infograph.fal_request_id:
        response["request_id"] = infograph.fal_request_id
        
        # Optional: Poll fal.ai for status
        # fal_client = FalAI()
        # try:
        #     result = fal_client.get_result_sync(infograph.fal_request_id)
        #     if result:
        #         handle_webhook_result(infograph_id, result)
        #         response["status"] = InfographStatus.COMPLETED
        #         response["image_url"] = infograph.image_url
        # except:
        #     pass  # Still processing
    
    if infograph.status == InfographStatus.FAILED:
        response["error"] = infograph.error_message
    
    return response

    

    
    
    