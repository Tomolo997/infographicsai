import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

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
        infographs = self.get_queryset().filter(account=request.user.account)
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