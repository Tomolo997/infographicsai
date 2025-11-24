import json

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import requests
from infographs.api import service as infographs_api_service
from infographs.infographs import service as infographs_service
from infographs.infographs.exceptions import NotEnoughCreditsException
from infographs.models import Infograph, Template
from infographs.serializers import InfographSerializer
from marshmallow import ValidationError
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.

class InfographListAPIView(generics.ListAPIView):
    queryset = Infograph.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Filter by authenticated user
        infographs = self.get_queryset().filter(account=request.user.account).order_by('-created_at')
        serializer = InfographSerializer(infographs, many=True)
        return Response(serializer.data)


class InfographCreateAPIView(generics.CreateAPIView):
    """
    Create infograph generation job(s).
    Returns immediately with job IDs - generation happens asynchronously.
    """
    queryset = Infograph.objects.all()
    serializer_class = InfographSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data = {
            "account": request.user.account,
            "prompt": request.data.get("prompt"),
            "blog_url": request.data.get("blog_url") or None,
            "aspect_ratio": request.data.get("aspect_ratio"),
            "resolution": request.data.get("resolution"),
            "number_of_infographs": request.data.get("number_of_infographs") or 1,
            "type": request.data.get("type") or "infograph",
        }
        
        try:
            result = infographs_api_service.create_infograph(**data)
            return Response(result, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(
                {"message": "Invalid data", "errors": e.messages}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except NotEnoughCreditsException as e:
            return Response(
                {"message": "Not enough credits"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"message": "Error creating infograph", "error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InfographCreateFromPDFAPIView(APIView):
    """
    Create infograph generation job(s) from PDF upload.
    Returns immediately with job IDs - generation happens asynchronously.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Get PDF file from request
        pdf_file = request.FILES.get("pdf_file")
        
        if not pdf_file:
            return Response(
                {"message": "No PDF file provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate file type
        if not pdf_file.name.endswith('.pdf'):
            return Response(
                {"message": "File must be a PDF"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get other parameters
        data = {
            "account": request.user.account,
            "prompt": request.data.get("prompt", ""),
            "pdf_file": pdf_file,
            "aspect_ratio": request.data.get("aspect_ratio", "9:16"),
            "resolution": request.data.get("resolution", "2K"),
            "number_of_infographs": int(request.data.get("number_of_infographs", 1)),
            "type": request.data.get("type", "infograph"),
        }
        
        try:
            result = infographs_service.create_infograph_from_pdf(**data)
            return Response(result, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(
                {"message": "Invalid data", "errors": e.messages}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except NotEnoughCreditsException as e:
            return Response(
                {"message": "Not enough credits"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"message": "Error creating infograph from PDF", "error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InfographStatusAPIView(APIView):
    """
    Check the status of an infograph generation job.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, infograph_id):
        try:
            # Ensure user owns this infograph
            infograph = Infograph.objects.get(
                id=infograph_id, 
                account=request.user.account
            )
            
            status_data = infographs_service.get_infograph_status(infograph_id)
            return Response(status_data, status=status.HTTP_200_OK)
            
        except Infograph.DoesNotExist:
            return Response(
                {"message": "Infograph not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": "Error fetching status", "error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InfographDeleteAPIView(generics.DestroyAPIView):
    """
    Delete an infograph.
    """
    queryset = Infograph.objects.all()
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        try:
            # Ensure user owns this infograph
            infograph = Infograph.objects.get(
                id=pk,
                account=request.user.account
            )
            infograph.delete()
            
            return Response(
                {"message": "Infograph deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
            
        except Infograph.DoesNotExist:
            return Response(
                {"message": "Infograph not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": "Error deleting infograph", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@method_decorator(csrf_exempt, name='dispatch')
class InfographWebhookAPIView(APIView):
    """
    Webhook endpoint for fal.ai to POST results when generation completes.
    
    This endpoint is called by fal.ai servers, not by users, so:
    - No authentication required (fal.ai doesn't send auth headers)
    - CSRF exempt
    - Should validate the request came from fal.ai (optional: check IP/signature)
    """
    permission_classes = [AllowAny]
    
    def post(self, request, infograph_id):
        try:
            # Log the webhook received
            print(f"[WEBHOOK] Received webhook for infograph {infograph_id}")
            print(f"[WEBHOOK] Data: {request.data}")
            
            # Process the result
            infograph = infographs_service.handle_webhook_result(
                infograph_id=infograph_id,
                result_data=request.data
            )
            
            return Response({
                "message": "Webhook processed successfully",
                "infograph_id": infograph.id,
                "status": infograph.status
            }, status=status.HTTP_200_OK)
            
        except Infograph.DoesNotExist:
            return Response(
                {"message": "Infograph not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"[WEBHOOK ERROR] {str(e)}")
            return Response(
                {"message": "Error processing webhook", "error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InfographDownloadAPIView(APIView):
    """
    Proxy endpoint to download infograph images with proper CORS headers.
    This bypasses CORS restrictions by fetching the image server-side.
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, infograph_id):
        try:
            # Ensure user owns this infograph
            infograph = Infograph.objects.get(
                id=infograph_id,
                account=request.user.account
            )
            
            # Check if image URL exists
            if not infograph.image_url:
                return Response(
                    {"message": "Image not available yet"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Fetch the image from the external URL
            try:
                image_response = requests.get(
                    infograph.image_url,
                    timeout=30,
                    stream=True
                )
                image_response.raise_for_status()
                
                # Get content type from response or default to image/png
                content_type = image_response.headers.get('Content-Type', 'image/png')
                
                # Create Django HttpResponse with proper CORS headers
                response = HttpResponse(
                    image_response.content,
                    content_type=content_type
                )
                
                # Add CORS headers to allow frontend to download
                response['Access-Control-Allow-Origin'] = '*'
                response['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
                response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
                
                # Add content disposition for download
                filename = f"infograph-{infograph_id}.png"
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                
                return response
                
            except requests.exceptions.RequestException as e:
                return Response(
                    {"message": "Failed to fetch image", "error": str(e)}, 
                    status=status.HTTP_502_BAD_GATEWAY
                )
            
        except Infograph.DoesNotExist:
            return Response(
                {"message": "Infograph not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"message": "Error downloading infograph", "error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )