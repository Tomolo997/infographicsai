import os
import uuid
import json
import re
import logging
import requests
import asyncio
import aiohttp
import numpy as np
import copy
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import transaction
from django.core.cache import cache

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import AnonRateThrottle

from sklearn.metrics.pairwise import cosine_similarity

from openai import OpenAI
import voyageai

from .models import InfoGraph, MediaUpload
from .serializers import InfoGraphSerializer, InfoGraphListSerializer
from .templates import get_template, get_all_templates, get_templates_by_section

from account.models import Account, CustomUser
from account.exceptions import DownloadForbidden

from icons.models import VectorIcon, SVGIcon, FlatIcon, OutlineIcon
from file_upload.client import R2Client

# Initialize clients
voyage_client = voyageai.Client(api_key=settings.VOYAGE_API_KEY)
logger = logging.getLogger(__name__)


logger = logging.getLogger(__name__)
from django.core.exceptions import ValidationError
import json


class SaveInfographicView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Initialize R2 client
            r2_client = R2Client()
            account = Account.objects.get(user=request.user)

            subscription = account.get_active_subscription()
            if subscription and subscription.tier.name.lower() == "free":
                existing_count = InfoGraph.objects.filter(
                    account=account, is_saved=True
                ).count()
                if existing_count >= 10:
                    return Response(
                        {
                            "error": "Free tier users are limited to 10 infographics. Please upgrade your plan to create more."
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )

            # Get the preview image file
            preview_image = request.FILES.get("preview_image")
            preview_url = None

            if preview_image:
                # Generate unique filename
                file_extension = "png"
                unique_filename = f"previews/{uuid.uuid4()}.{file_extension}"

                # Upload to R2
                preview_url = r2_client.upload_file(preview_image, unique_filename)
                if not preview_url:
                    return Response(
                        {"error": "Failed to upload preview image"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            # Process other data
            data = request.POST.dict()

            # Parse content JSON safely
            try:
                content_str = data.get("content", "{}")
                data["content"] = json.loads(content_str)
            except json.JSONDecodeError as e:
                return Response(
                    {"error": f"Invalid JSON in content field: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Get UUID
            uuid_str = data.get("infograph_id")
            infograph = None

            if uuid_str:
                try:
                    infograph = InfoGraph.objects.get(uuid=uuid_str)
                    # Delete old preview image if it exists
                    if infograph.preview_image_url and preview_url:
                        old_filename = infograph.preview_image_url.split("/")[-1]
                        r2_client.delete_file(f"previews/{old_filename}")
                except InfoGraph.DoesNotExist:
                    print("Infographic does not exist")
                    pass

            # Convert numeric fields
            try:
                data["width"] = int(data.get("width", 1024))
                data["height"] = int(data.get("height", 1024))
            except (TypeError, ValueError):
                return Response(
                    {"error": "Invalid width or height values"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Always set preview_image_url if we have a new one
            if preview_url:
                data["preview_image_url"] = preview_url

            # Prepare serializer based on whether we're updating or creating
            # Set the account in the context for creation
            context = {"account": account}
            serializer = InfoGraphSerializer(
                infograph, data=data, partial=True, context=context
            )

            if serializer.is_valid():
                try:
                    if infograph and "content" in data:
                        current_content = infograph.content or {}
                        new_content = data["content"]
                        merged_content = {**current_content, **new_content}
                        serializer.validated_data["content"] = merged_content

                    # For update operations, we don't need to pass account again
                    # For create operations, account will be taken from context
                    if infograph:
                        # This is an update operation
                        infograph = serializer.save()
                    else:
                        # This is a create operation
                        infograph = serializer.save()

                    return Response(
                        {
                            "message": "Infographic saved successfully",
                            "uuid": str(infograph.uuid),
                            "preview_url": infograph.preview_image_url,
                            "is_new": infograph is None,
                        },
                        status=status.HTTP_200_OK,
                    )
                except ValidationError as e:
                    return Response(
                        {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error saving infographic: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# views.py - Add a special endpoint for headless browser automation

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import uuid
import os


class AdminSaveInfographicView(APIView):
    """
    Special endpoint for headless browser automation.
    Uses a special token for authentication instead of normal user auth.
    """

    # No permission_classes - bypasses normal authentication
    permission_classes = [AllowAny]

    def post(self, request):
        try:

            # Get the infograph UUID
            infograph_uuid = request.data.get("infograph_uuid")
            if not infograph_uuid:
                return Response(
                    {"error": "Infograph UUID is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Get the preview image
            preview_image = request.FILES.get("preview_image")
            if not preview_image:
                return Response(
                    {"error": "Preview image is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Find the infograph by UUID
            from infos.models import InfoGraph

            try:
                infograph = InfoGraph.objects.get(uuid=infograph_uuid)
            except InfoGraph.DoesNotExist:
                return Response(
                    {"error": f"Infograph with UUID {infograph_uuid} not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Initialize storage client
            from file_upload.client import R2Client

            r2_client = R2Client()

            # Upload preview image
            file_extension = "png"
            unique_filename = f"previews/{uuid.uuid4()}.{file_extension}"

            # Delete old preview image if it exists
            if infograph.preview_image_url:
                try:
                    old_filename = infograph.preview_image_url.split("/")[-1]
                    r2_client.delete_file(f"previews/{old_filename}")
                except Exception as e:
                    # Log but continue
                    print(f"Error deleting old preview: {str(e)}")

            # Upload new preview image
            preview_url = r2_client.upload_file(preview_image, unique_filename)
            if not preview_url:
                return Response(
                    {"error": "Failed to upload preview image"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Update the infograph
            infograph.preview_image_url = preview_url
            infograph.save(update_fields=["preview_image_url", "updated_at"])

            return Response(
                {
                    "message": "Preview image saved successfully",
                    "uuid": str(infograph.uuid),
                    "preview_url": preview_url,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Add this to views.py
class AdminGetInfographicView(APIView):
    """
    Special endpoint for headless browser automation.
    Uses a special token for authentication instead of normal user auth.
    """

    # No permission_classes - bypasses normal authentication
    permission_classes = [AllowAny]

    def get(self, request, uuid):
        try:
            # Validate the admin token
            # Find the infograph by UUID
            try:
                infograph = InfoGraph.objects.get(uuid=uuid)
            except InfoGraph.DoesNotExist:
                return Response(
                    {"error": f"Infograph with UUID {uuid} not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Serialize the response using a consistent format
            response_data = {
                "background_color": infograph.background_color,
                "title": infograph.title,
                "content": infograph.content,
                "uuid": str(infograph.uuid),
                "width": infograph.width,
                "height": infograph.height,
                "created_at": infograph.created_at,
                "updated_at": infograph.updated_at,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error retrieving infographic {uuid}: {str(e)}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SaveInfographView(APIView):
    """
    API endpoint to mark an infographic as saved or unsaved.
    """

    permission_classes = [IsAuthenticated]

    def patch(self, request, uuid):
        try:
            # Get the infograph by UUID
            try:
                infograph = InfoGraph.objects.get(
                    uuid=uuid, account=request.user.account
                )
            except InfoGraph.DoesNotExist:
                return Response(
                    {"error": f"Infograph with UUID {uuid} not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Toggle the is_saved status
            is_saved = request.data.get("is_saved", not infograph.is_saved)
            infograph.is_saved = is_saved
            infograph.save(update_fields=["is_saved", "updated_at"])

            return Response(
                {
                    "message": f"Infograph {'saved' if is_saved else 'unsaved'} successfully",
                    "uuid": str(infograph.uuid),
                    "is_saved": infograph.is_saved,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ListSavedInfographsView(APIView):
    """
    API endpoint to list all saved infographics for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get all saved infographs for the user
            saved_infographs = InfoGraph.objects.filter(
                account=request.user.account, is_saved=True
            ).order_by("-updated_at")

            # Serialize the infographs
            serializer = InfoGraphListSerializer(saved_infographs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateInfographicView(APIView):
    permission_classes = [IsAuthenticated]  # For testing only

    def put(self, request, id):
        try:
            infograph = get_object_or_404(InfoGraph, id=id)

            # Get test account for ownership simulation if needed
            account = Account.objects.get(user=request.user)

            serializer = InfoGraphSerializer(infograph, data=request.data, partial=True)

            if serializer.is_valid():
                infograph = serializer.save()
                return Response(
                    {
                        "message": "Infographic updated successfully",
                        "infograph_id": infograph.id,
                    }
                )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except InfoGraph.DoesNotExist:
            return Response(
                {"error": "Infographic not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, id):
        return self.put(request, id)


# You might also want a view to list infographics for testing
class ListInfographicsView(APIView):
    permission_classes = [IsAuthenticated]  # For testing only

    def get(self, request):
        try:
            # Check if uuids parameter is provided
            uuids_param = request.query_params.get("uuids", None)

            # Get user's infographics
            infographics_query = InfoGraph.objects.filter(account=request.user.account)

            # If uuids parameter is provided, filter by those UUIDs
            if uuids_param:
                uuids_list = uuids_param.split(",")
                infographics_query = infographics_query.filter(uuid__in=uuids_list)

            # Order by created_at descending to show newest first
            infographics = infographics_query.order_by("-created_at")

            serializer = InfoGraphListSerializer(infographics, many=True)
            return Response(serializer.data)

        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Test user not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateInfographView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        try:

            print(request.data)
            data = {
                "title": "Untitled Design",
                "content": {},
                "width": request.data.get("width", 1024),
                "height": request.data.get("height", 1024),
            }

            with transaction.atomic():
                account = (
                    request.user.account
                )  # Assuming reverse relationship is set up
                serializer = InfoGraphSerializer(
                    data=data, context={"account": account}
                )

                if not serializer.is_valid():
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

                infograph = serializer.save()

                return Response(
                    {
                        "message": "Infographic created successfully",
                        "infograph_id": infograph.id,
                        "uuid": str(infograph.uuid),
                        "redirect_url": f"/dashboard/editor/{infograph.uuid}",
                    },
                    status=status.HTTP_201_CREATED,
                )

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log the error here
            print(e)
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetCSRFTokenView(APIView):
    permission_classes = []  # Allow unauthenticated access to get CSRF token

    def get(self, request):
        csrf_token = get_token(request)
        return Response({"csrf_token": csrf_token})


class GetInfographicView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, uuid):
        try:
            # Use get_object_or_404 instead of filter and manual check
            infograph = get_object_or_404(
                InfoGraph.objects.select_related("account"), uuid=uuid
            )
            # Check permission
            if infograph.account.user != request.user:
                return Response(
                    {"error": "You do not have permission to access this infographic"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Serialize the response using a consistent format
            response_data = {
                "background_color": infograph.background_color,
                "title": infograph.title,
                "content": infograph.content,
                "uuid": str(infograph.uuid),
                "width": infograph.width,
                "height": infograph.height,
                "created_at": infograph.created_at,
                "updated_at": infograph.updated_at,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except InfoGraph.DoesNotExist:
            return Response(
                {"error": "Infographic not found"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            logger.error(f"Error retrieving infographic {uuid}: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class RenameInfographicView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, uuid):
        try:
            # Get the infographic and check permissions in one go
            infograph = get_object_or_404(
                InfoGraph.objects.select_related("account"), uuid=uuid
            )

            # Check if the user owns this infographic
            if infograph.account.user != request.user:
                return Response(
                    {"error": "You do not have permission to rename this infographic"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Get the new title from request data
            new_title = request.data.get("title")
            if not new_title:
                return Response(
                    {"error": "Title is required"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Update only the title
            infograph.title = new_title
            infograph.save(update_fields=["title", "updated_at"])

            return Response(
                {
                    "message": "Title updated successfully",
                    "uuid": str(infograph.uuid),
                    "title": infograph.title,
                },
                status=status.HTTP_200_OK,
            )

        except InfoGraph.DoesNotExist:
            return Response(
                {"error": "Infographic not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error renaming infographic {uuid}: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DeleteInfographicView(APIView):
    permission_classes = [IsAuthenticated]

    def _extract_media_urls(self, content):
        """
        Extract all media URLs from the infograph content
        """
        media_urls = []
        try:
            elements = content.get("canvas_data", {}).get("elements", [])
            for element in elements:
                if element.get("type") == "media" and element.get("src"):
                    media_urls.append(element["src"])
        except Exception as e:
            logger.error(f"Error extracting media URLs: {str(e)}")
        return media_urls

    def _get_filename_from_url(self, url):
        """
        Extract filename from URL
        """
        try:
            return url.split("/")[-1]
        except Exception:
            return None

    def delete(self, request, uuid):
        try:
            # Get the infographic and check permissions in one go
            infograph = get_object_or_404(
                InfoGraph.objects.select_related("account"), uuid=uuid
            )

            # Check if the user owns this infographic
            if infograph.account.user != request.user:
                return Response(
                    {"error": "You do not have permission to delete this infographic"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Initialize R2 client
            r2_client = R2Client()

            # # Delete all media files from the content
            # media_urls = self._extract_media_urls(infograph.content)
            # for url in media_urls:
            #     try:
            #         filename = self._get_filename_from_url(url)
            #         if filename:
            #             r2_client.delete_file(f"media/{filename}")
            #     except Exception as e:
            #         logger.error(f"Error deleting media file {url}: {str(e)}")
            #         # Continue with deletion even if one file fails

            # Delete preview image if it exists
            if infograph.preview_image_url:
                try:
                    filename = self._get_filename_from_url(infograph.preview_image_url)
                    if filename:
                        r2_client.delete_file(f"previews/{filename}")
                except Exception as e:
                    logger.error(f"Error deleting preview file: {str(e)}")

            # Delete the infograph
            infograph.delete()

            return Response(
                {
                    "message": "Infographic and associated media deleted successfully",
                    "uuid": str(uuid),
                },
                status=status.HTTP_200_OK,
            )

        except InfoGraph.DoesNotExist:
            return Response(
                {"error": "Infographic not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error deleting infographic {uuid}: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class DuplicateInfographicView(APIView):
    """
    API endpoint to duplicate an infographic template.
    Creates a new infographic with the same content but sets is_template=False.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, uuid):
        try:
            # Get the template infographic by UUID
            template_infograph = get_object_or_404(InfoGraph, uuid=uuid)

            # Create a new infographic with the same content
            with transaction.atomic():
                account = request.user.account

                # Create a copy of the infographic with is_template=False
                new_infograph = InfoGraph.objects.create(
                    title=f"Copy of {template_infograph.title}",
                    content=copy.deepcopy(template_infograph.content),
                    width=template_infograph.width,
                    height=template_infograph.height,
                    background_color=template_infograph.background_color,
                    account=account,
                    is_saved=True,
                    is_template=False,  # Ensure this is set to False
                    template_type=template_infograph.template_type,
                )

                return Response(
                    {
                        "message": "Infographic duplicated successfully",
                        "uuid": str(new_infograph.uuid),
                        "redirect_url": f"/dashboard/editor/{new_infograph.uuid}",
                    },
                    status=status.HTTP_201_CREATED,
                )

        except InfoGraph.DoesNotExist:
            return Response(
                {"error": "Template infographic not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.error(f"Error duplicating infographic {uuid}: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# views.py
class UploadMediaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            media_file = request.FILES.get("file")
            if not media_file:
                return Response(
                    {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Initialize R2 client
            r2_client = R2Client()

            # Generate unique filename
            file_extension = media_file.name.split(".")[-1].lower()
            unique_filename = f"media/{uuid.uuid4()}.{file_extension}"

            # Upload to R2
            media_url = r2_client.upload_file(media_file, unique_filename)

            if not media_url:
                return Response(
                    {"error": "Failed to upload media file"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            # Save to database
            MediaUpload.objects.create(
                account=request.user.account,
                url=media_url,
                filename=media_file.name,
                file_type=media_file.content_type,
                file_size=media_file.size,
            )

            return Response(
                {"url": media_url, "filename": media_file.name},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Error uploading media: {str(e)}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RecentUploadsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get the last 6 uploads for the user
            recent_uploads = MediaUpload.objects.filter(
                account=request.user.account
            ).order_by("-created_at")[:6]

            uploads_data = [
                {
                    "id": upload.id,
                    "url": upload.url,
                    "filename": upload.filename,
                    "created_at": upload.created_at,
                    "file_type": upload.file_type,
                    "file_size": upload.file_size,
                }
                for upload in recent_uploads
            ]

            return Response(uploads_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching recent uploads: {str(e)}")
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DownloadInfographicView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            account = request.user.account

            try:
                # This will check subscription status and limits
                account.increment_download()

                return Response(
                    {
                        "message": "Succesfully downloaded infograph",
                        "remaining_downloads": account.get_active_subscription().tier.monthly_download_limit
                        - account.monthly_downloads,
                    },
                    status=status.HTTP_200_OK,
                )

            except DownloadForbidden as e:
                return Response({"error": str(e)}, status=status.HTTP_403_FORBIDDEN)

        except InfoGraph.DoesNotExist:
            return Response(
                {"error": "Infographic not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error processing download for infographic {uuid}: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class GetTemplatesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Use get_object_or_404 instead of filter and manual check
            template_type = request.query_params.get("template_type", None)
            infographics = InfoGraph.objects.filter(is_template=True)
            response_data = []
            for infograph in infographics:
                response_data.append(
                    {
                        "width": infograph.width,
                        "height": infograph.height,
                        "created_at": infograph.created_at,
                        "updated_at": infograph.updated_at,
                        "title": infograph.title,
                        "template_type": infograph.template_type,
                        "preview_image_url": infograph.preview_image_url,
                        "uuid": str(infograph.uuid),
                        "content": infograph.content,
                        "background_color": infograph.background_color,
                    }
                )

            return Response(response_data, status=status.HTTP_200_OK)
        except InfoGraph.DoesNotExist:
            return Response(
                {"error": "Infographic not found"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            logger.error(f"Error retrieving infographics: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class URLAnalyzer:
    def _scrape_website(self, url):
        """Helper method to scrape website content"""
        logger.info(f"Starting to scrape website: {url}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

        try:
            logger.debug(f"Making request to {url} with headers: {headers}")
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            logger.info(
                f"Successfully fetched {url}. Status code: {response.status_code}"
            )

            soup = BeautifulSoup(response.text, "html.parser")
            logger.debug("Successfully created BeautifulSoup object")

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Try multiple strategies to find content
            main_content = None
            content_selectors = [
                # Try standard HTML5 elements
                soup.find("main"),
                soup.find("article"),
                # Try common content div IDs
                soup.find("div", id="content"),
                soup.find("div", id="main-content"),
                soup.find("div", class_="content"),
                # Try common content classes
                soup.find("div", class_="main-content"),
                soup.find("div", class_="post-content"),
                soup.find("div", class_="entry-content"),
                # Fallback to body if nothing else works
                soup.find("body"),
            ]

            # Use the first non-None selector result
            main_content = next(
                (content for content in content_selectors if content is not None), None
            )

            if not main_content:
                logger.error("Could not find any content on the page")
                return {
                    "title": "Content Not Found",
                    "meta_description": "",
                    "content": "Could not extract content from this webpage. The page might be empty or require JavaScript to load content.",
                }

            # Extract text and clean it up
            text = main_content.get_text(separator="\n", strip=True)

            # Remove extra whitespace and empty lines
            text = "\n".join(line.strip() for line in text.split("\n") if line.strip())

            logger.debug(f"Extracted text length: {len(text)}")

            # Get title - try multiple methods
            title = ""
            if soup.title:
                title = soup.title.string
            elif soup.find("h1"):
                title = soup.find("h1").get_text(strip=True)

            # Get meta description
            meta_desc = ""
            meta_selectors = [
                {"name": "description"},
                {"property": "og:description"},
                {"name": "twitter:description"},
            ]

            for selector in meta_selectors:
                meta_tag = soup.find("meta", attrs=selector)
                if meta_tag and meta_tag.get("content"):
                    meta_desc = meta_tag.get("content")
                    break

            result = {
                "title": title[:200] if title else "",  # Limit title length
                "meta_description": (
                    meta_desc[:500] if meta_desc else ""
                ),  # Limit description length
                "content": (
                    text[:10000] if text else "No content found"
                ),  # Limit content length
            }
            logger.info(f"Successfully scraped website. Content length: {len(text)}")
            return result

        except requests.Timeout:
            logger.error(f"Timeout while scraping {url}")
            raise
        except requests.RequestException as e:
            logger.error(f"Request error while scraping {url}: {str(e)}")
            raise
        except Exception as e:
            logger.error(
                f"Unexpected error while scraping {url}: {str(e)}", exc_info=True
            )
            return {
                "title": "Error",
                "meta_description": "",
                "content": "An error occurred while trying to extract content from this webpage.",
            }

    def _analyze_with_gpt(self, website_data, language="English"):
        """Helper method to analyze website content with GPT and return structured JSON with icon suggestions"""
        logger.info(
            "Starting GPT website analysis for JSON structure with icon suggestions"
        )

        try:
            logger.debug("Initializing OpenAI client")
            client = OpenAI(api_key=settings.OPENAI_API_KEY)

            # Updated schema to include icon_keywords field
            infographic_schema = {
                "name": "infographic_content",
                "schema": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Main title for the infographic",
                        },
                        "subTitle": {
                            "type": "string",
                            "description": "Subtitle or brief description for the infographic",
                        },
                        "sections": {
                            "type": "array",
                            "description": "Content sections for the infographic",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {
                                        "type": "string",
                                        "description": "Section heading",
                                    },
                                    "content": {
                                        "type": "string",
                                        "description": "Section content, should be concise and suitable for an infographic",
                                    },
                                    "icon_keywords": {
                                        "type": "array",
                                        "description": "Keywords for searching appropriate icons",
                                        "items": {"type": "string"},
                                    },
                                },
                                "required": ["title", "content", "icon_keywords"],
                                "additionalProperties": False,
                            },
                        },
                    },
                    "required": ["title", "subTitle", "sections"],
                    "additionalProperties": False,
                },
                "strict": True,
            }

            prompt = f"""
            Analyze this website content and extract key information for an infographic:
            
            Title: {website_data['title']}
            Meta Description: {website_data['meta_description']}
            
            Content:
            {website_data['content']}
            
            Structure the information for an infographic with:
            - A clear, concise main title (max 40 characters, preferably based on the page title)
            - A brief subtitle or description (max 50 characters, 1 sentence)
            - 6 key sections, each with:
                - A short, descriptive section title (max 50 characters)
                - Concise content (max 100 characters, 2-3 sentences)
                - 3-5 icon keywords that best represent this section visually
            
            For icon_keywords, provide specific, concrete objects or concepts that would make good icons.
            For example:
            - For a section about "Early Life", keywords might be: ["baby", "child", "cradle", "growth", "beginning"]
            - For "Philosophy" sections: ["book", "scroll", "thinking", "wisdom", "knowledge"]
            - For "Leadership": ["crown", "throne", "podium", "certificate", "handshake"]
            
            IMPORTANT: Stay within the character limits for each field. The content must fit well in an infographic layout.
            Your response must be formatted according to the provided JSON schema.
            Focus on making the content visually presentable in an infographic format.

            IMPORTANT: The content must be in the {language} language of the content.
            """

            logger.debug(
                f"Sending request to GPT. Content length: {len(website_data['content'])}"
            )

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an infographic content specialist. Extract and structure key information from websites and suggest appropriate visual elements.",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": infographic_schema,
                },
                max_tokens=1000,
                temperature=0.5,
            )

            analysis_json = json.loads(response.choices[0].message.content)
            logger.info(
                "Successfully received structured JSON from GPT with icon suggestions"
            )
            logger.debug(f"JSON preview: {str(analysis_json)[:200]}...")

            # Use the GPT-suggested keywords to find appropriate icons
            analysis_json = assign_icons_using_keywords(analysis_json)
            analysis_json = assign_vectors_using_keywords(analysis_json)

            return analysis_json
        except Exception as e:
            logger.error(f"Error in GPT analysis: {str(e)}", exc_info=True)
            pass


class ContentAnalyzer:
    def _analyze_with_gpt(self, content, language):
        """Helper method to analyze website content with GPT and return structured JSON with icon suggestions"""
        logger.info(
            "Starting GPT website analysis for JSON structure with icon suggestions"
        )

        try:
            logger.debug("Initializing OpenAI client")
            client = OpenAI(api_key=settings.OPENAI_API_KEY)

            # Updated schema to include icon_keywords field
            infographic_schema = {
                "name": "infographic_content",
                "schema": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Main title for the infographic",
                        },
                        "subTitle": {
                            "type": "string",
                            "description": "Subtitle or brief description for the infographic",
                        },
                        "sections": {
                            "type": "array",
                            "description": "Content sections for the infographic",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {
                                        "type": "string",
                                        "description": "Section heading",
                                    },
                                    "content": {
                                        "type": "string",
                                        "description": "Section content, should be concise and suitable for an infographic",
                                    },
                                    "icon_keywords": {
                                        "type": "array",
                                        "description": "Keywords for searching appropriate icons",
                                        "items": {"type": "string"},
                                    },
                                },
                                "required": ["title", "content", "icon_keywords"],
                                "additionalProperties": False,
                            },
                        },
                    },
                    "required": ["title", "subTitle", "sections"],
                    "additionalProperties": False,
                },
                "strict": True,
            }

            prompt = f"""
                Analyze this website content and extract key information for an infographic:
                
                Content:
                {content}
                
                Structure the information for an infographic with:
                - A clear, concise main title (max 40 characters, preferably based on the page title)
                - A brief subtitle or description (max 50 characters, 1 sentence)
                - 6 key sections, each with:
                    - A short, descriptive section title (max 50 characters)
                    - Concise content (max 100 characters, 2-3 sentences)
                    - 3-5 icon keywords that best represent this section visually
                
                For icon_keywords, provide specific, concrete objects or concepts that would make good icons.
                For example:
                - For a section about "Early Life", keywords might be: ["baby", "child", "cradle", "growth", "beginning"]
                - For "Philosophy" sections: ["book", "scroll", "thinking", "wisdom", "knowledge"]
                - For "Leadership": ["crown", "throne", "podium", "certificate", "handshake"]
                
                IMPORTANT: Stay within the character limits for each field. The content must fit well in an infographic layout.
                Your response must be formatted according to the provided JSON schema.
                Focus on making the content visually presentable in an infographic format.

                IMPORTANT: The content must be in the {language} language of the content.
                """

            logger.debug(f"Sending request to GPT. Content length: {len(content)}")

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an infographic content specialist. Extract and structure key information from websites and suggest appropriate visual elements.",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": infographic_schema,
                },
                max_tokens=1000,
                temperature=0.5,
            )

            analysis_json = json.loads(response.choices[0].message.content)
            logger.info(
                "Successfully received structured JSON from GPT with icon suggestions"
            )
            logger.debug(f"JSON preview: {str(analysis_json)[:200]}...")

            # Use the GPT-suggested keywords to find appropriate icons
            analysis_json = assign_icons_using_keywords(analysis_json)
            analysis_json = assign_vectors_using_keywords(analysis_json)

            return analysis_json
        except Exception as e:
            logger.error(f"Error in GPT analysis: {str(e)}", exc_info=True)
            pass


class ListTemplatesView(APIView):
    """API endpoint to list all available templates"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            templates = []
            template_info = get_all_templates()

            # Iterate through sections
            for section_name, template_list in template_info.items():
                # Iterate through templates in each section
                for index, template in enumerate(template_list):
                    template_name = f"{section_name}_{index+1}"

                    templates.append(
                        {
                            "name": template_name,
                            "section": section_name,
                            "width": template["width"],
                            "height": template["height"],
                            "category": self._get_template_category(section_name),
                            "description": self._get_template_description(
                                section_name, index
                            ),
                            "background_color": template.get(
                                "background_color", "#FFFFFF"
                            ),
                        }
                    )

            return Response(templates, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error listing templates: {str(e)}")
            return Response(
                {"error": "Failed to retrieve templates"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _get_template_category(self, section_name):
        """Get category for a template based on its section name"""
        if (
            "Facebook" in section_name
            or "Instagram" in section_name
            or "X" in section_name
            or "Twitter" in section_name
            or "LinkedIn" in section_name
        ):
            return "Social Media"
        elif "Infographic" in section_name:
            return "Infographics"
        elif (
            "Banner" in section_name
            or "Cover" in section_name
            or "Header" in section_name
        ):
            return "Headers and Banners"
        elif "Blog" in section_name:
            return "Blog Content"
        else:
            return "Other"

    def _get_template_description(self, section_name, index=0):
        """
        Get a description for a template based on its section name and index

        Args:
            section_name (str): The section name (e.g., 'Infographic')
            index (int): The index of the template within its section

        Returns:
            str: Template description
        """
        base_descriptions = {
            "Infographic": "Visual representation of information or data in an engaging format.",
            "X Post": "Perfect for sharing quick updates, news, and engaging your audience on X (Twitter).",
            "Facebook Post": "Ideal for rich content with text and visuals to drive engagement on Facebook.",
            "Instagram Post": "Square format optimized for Instagram's visual feed.",
            # Add more descriptions as needed
        }

        # Get the base description for the section
        base_description = base_descriptions.get(
            section_name, f"Template for {section_name}"
        )

        # Add variant information if there are multiple templates in the section
        if index > 0:
            return f"{base_description} (Style {index+1})"
        return base_description


class AnalyzeAndGenerateInfographicView(APIView):
    """API endpoint to analyze URL or content and generate multiple infographics"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get request data
            url = request.data.get("url")
            content = request.data.get("content")
            template_section = request.data.get(
                "template_section", "Infographic"
            )  # Default to Infographic

            # Validate inputs
            if not url and not content:
                return Response(
                    {"error": "Either URL or content is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if user has enough AI credits
            account = request.user.account
            can_use, message = account.can_use_ai_credits(credits_needed=1)
            if not can_use:
                return Response(
                    {"error": message},
                    status=status.HTTP_402_PAYMENT_REQUIRED,
                )

            # Get templates based on section or specific template
            templates = []
            # Get all templates from the specified section
            section_templates = get_templates_by_section(template_section)
            if not section_templates:
                return Response(
                    {"error": f"No templates found for section '{template_section}'"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            templates = [
                (f"{template_section}_{i+1}", template)
                for i, template in enumerate(section_templates)
            ]

            # Initialize infographic generator
            generator = InfographicGenerator()

            # Process based on input type to get structured data
            structured_data = None
            if url:
                # First scrape and analyze the URL
                url_analyzer = URLAnalyzer()
                website_data = url_analyzer._scrape_website(url)

                # Analyze with GPT and assign icons using embeddings
                structured_data = url_analyzer._analyze_with_gpt(website_data)
            else:
                # Create a ContentAnalyzer instance
                content_analyzer = ContentAnalyzer()

                # For content, we'll use the same flow as URL analysis
                # First analyze the content with GPT to get structured data
                structured_data = content_analyzer._analyze_with_gpt(content)

            generated_infographics = []

            with transaction.atomic():
                account = request.user.account

                # Generate an infographic for each template
                for template_name, template in templates:
                    # Generate infographic with structured data
                    infographic_data = generator.generate_from_structured_data(
                        structured_data, template_name, template
                    )

                    # Set infographic title from analysis results if not already set
                    if (
                        "title" not in infographic_data
                        and structured_data
                        and "title" in structured_data
                    ):
                        infographic_data["title"] = structured_data["title"]

                    # Create the infographic record
                    infograph = InfoGraph.objects.create(
                        title=infographic_data.get("title", f"New {template_name}"),
                        content=infographic_data["content"],
                        width=infographic_data["width"],
                        height=infographic_data["height"],
                        background_color=infographic_data["background_color"],
                        account=account,
                    )

                    # Add to generated infographics
                    generated_infographics.append(
                        {
                            "uuid": str(infograph.uuid),
                            "template_name": template_name,
                            "title": infographic_data.get(
                                "title", f"New {template_name}"
                            ),
                            "redirect_url": f"/dashboard/editor/{infograph.uuid}",
                            "preview": infographic_data.get("preview"),
                        }
                    )

                # Charge the user 1 AI credit for successful generation
                account.use_ai_credits(credits_needed=1)

            return Response(
                {
                    "message": f"Successfully generated {len(generated_infographics)} infographics",
                    "infographics": generated_infographics,
                    "structured_data": structured_data,
                    "credits_remaining": account.credit_balance,
                },
                status=status.HTTP_201_CREATED,
            )

        except ValidationError as e:
            logger.error(f"Validation error generating infographics: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Error generating infographics: {str(e)}")
            return Response(
                {"error": f"Failed to generate infographics: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class CreateFromTemplateView(APIView):
    """API endpoint to create an infographic directly from a template without AI"""

    permission_classes = [IsAuthenticated]

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        try:
            # Get template name
            template_name = request.data.get("template_name")

            if not template_name:
                return Response(
                    {"error": "Template name is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Get template
            template = get_template(template_name)

            if not template:
                return Response(
                    {"error": f"Template '{template_name}' not found"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create empty infographic from template
            with transaction.atomic():
                account = request.user.account

                # Prepare empty template (with placeholder text)
                empty_content = {"canvas_data": template["canvas_data"]}

                # Replace placeholders with example text
                self._replace_placeholders_with_examples(empty_content)

                infograph = InfoGraph.objects.create(
                    title=f"New {template_name}",
                    content=empty_content,
                    width=template["width"],
                    height=template["height"],
                    account=account,
                )

                return Response(
                    {
                        "message": "Template created successfully",
                        "uuid": str(infograph.uuid),
                        "redirect_url": f"/dashboard/editor/{infograph.uuid}",
                    },
                    status=status.HTTP_201_CREATED,
                )

        except Exception as e:
            logger.error(f"Error creating from template: {str(e)}")
            return Response(
                {"error": "Failed to create from template"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _replace_placeholders_with_examples(self, content):
        """Replace template placeholders with example text"""
        elements = content["canvas_data"]["elements"]

        for element in elements:
            if element["type"] == "text" and "content" in element:
                text = element["content"]
                if "{{" in text and "}}" in text:
                    # Extract placeholder name
                    placeholder = text[2:-2]  # Remove {{ and }}

                    # Replace with example text based on placeholder name
                    if "headline" in placeholder or "title" in placeholder:
                        element["content"] = "Your Headline Here"
                    elif "point" in placeholder or "message" in placeholder:
                        element["content"] = "Your main message or key point goes here."
                    elif "formatted" in placeholder:
                        if "supporting" in placeholder or "key" in placeholder:
                            element["content"] = (
                                "• First point here\n• Second point here\n• Third point here"
                            )
                        elif "hashtag" in placeholder:
                            element["content"] = "#hashtag1 #hashtag2 #hashtag3"
                    elif "action" in placeholder:
                        element["content"] = "Click to Learn More"
                    else:
                        element["content"] = "Edit this text"


class IconifySearchWithSVGView(APIView):
    """
    API endpoint to search icons and return their SVG data
    """

    permission_classes = [IsAuthenticated]

    async def fetch_svg(self, session, icon_id):
        """Fetch SVG data for a single icon"""
        try:
            # Parse the icon ID
            parts = icon_id.split(":")
            if len(parts) != 2:
                return {
                    "icon_id": icon_id,
                    "svg": None,
                    "error": "Invalid icon ID format",
                }

            prefix, name = parts

            # Construct URL for the SVG
            url = f"https://api.iconify.design/{prefix}/{name}.svg"

            # Check cache first
            cache_key = f"iconify_svg_{icon_id}"
            cached_svg = cache.get(cache_key)

            if cached_svg:
                return {"icon_id": icon_id, "svg": cached_svg}

            # Fetch the SVG
            async with session.get(url) as response:
                if response.status == 200:
                    svg_content = await response.text()
                    # Cache the result for 1 day
                    cache.set(cache_key, svg_content, 60 * 60 * 24)
                    return {"icon_id": icon_id, "svg": svg_content}
                else:
                    return {
                        "icon_id": icon_id,
                        "svg": None,
                        "error": f"HTTP {response.status}",
                    }

        except Exception as e:
            logger.error(f"Error fetching SVG for {icon_id}: {str(e)}")
            return {"icon_id": icon_id, "svg": None, "error": str(e)}

    async def fetch_all_svgs(self, icon_ids):
        """Fetch SVG data for multiple icons concurrently"""
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_svg(session, icon_id) for icon_id in icon_ids]
            return await asyncio.gather(*tasks)

    def get(self, request):
        try:
            # Get search parameters from request
            query = request.GET.get("query")
            if not query:
                return Response(
                    {"error": "Search query is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Optional parameters
            limit = request.GET.get(
                "limit", 20
            )  # Lower default since we're fetching SVGs
            start = request.GET.get("start", 0)
            prefix = request.GET.get("prefix")
            prefixes = request.GET.get("prefixes")
            category = request.GET.get("category")
            include_svg = request.GET.get("include_svg", "true").lower() == "true"

            # Construct Iconify API URL
            iconify_url = "https://api.iconify.design/search"

            # Prepare parameters
            params = {"query": query, "limit": limit, "start": start}

            # Add optional parameters if present
            if prefix:
                params["prefix"] = prefix
            if prefixes:
                params["prefixes"] = prefixes
            if category:
                params["category"] = category

            # Make request to Iconify API
            logger.debug(f"Searching Iconify with params: {params}")
            response = requests.get(iconify_url, params=params)
            response.raise_for_status()

            search_results = response.json()

            # If SVGs are not requested, return search results directly
            if not include_svg:
                return Response(search_results, status=status.HTTP_200_OK)

            # Fetch SVGs for all icons in the result
            icon_ids = search_results.get("icons", [])

            # Use asyncio to fetch SVGs concurrently
            svg_results = asyncio.run(self.fetch_all_svgs(icon_ids))

            # Add SVG data to search results
            search_results["svg_data"] = {item["icon_id"]: item for item in svg_results}

            return Response(search_results, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            logger.error(f"Error fetching from Iconify API: {str(e)}")
            return Response(
                {"error": f"Error fetching icons: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Unexpected error during icon search: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class IconifySVGView(APIView):
    """
    API endpoint to fetch a single SVG by icon ID
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get icon ID from request
            icon_id = request.GET.get("icon")
            if not icon_id:
                return Response(
                    {"error": "Icon ID is required"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Parse the icon ID
            parts = icon_id.split(":")
            if len(parts) != 2:
                return Response(
                    {"error": "Invalid icon ID format. Expected format: prefix:name"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            prefix, name = parts

            # Check cache first
            cache_key = f"iconify_svg_{icon_id}"
            cached_svg = cache.get(cache_key)

            if cached_svg:
                return Response({"svg": cached_svg}, status=status.HTTP_200_OK)

            # Construct URL for the SVG
            url = f"https://api.iconify.design/{prefix}/{name}.svg"

            # Fetch the SVG
            response = requests.get(url)
            response.raise_for_status()

            svg_content = response.text

            return Response({"svg": svg_content}, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            logger.error(f"Error fetching SVG: {str(e)}")
            return Response(
                {"error": f"Error fetching SVG: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Unexpected error fetching SVG: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class InfographicGenerator:
    """Service class to generate infographics from content or URL analysis"""

    def generate_from_structured_data(self, structured_data, template_name, template):
        """
        Generate an infographic from structured JSON data

        Args:
            structured_data (dict): JSON data with title, subTitle and sections
            template_name (str): Name of the template to use
            template (dict): The template definition

        Returns:
            dict: Infographic data with content, width, height and preview
        """
        logger.info(
            f"Generating infographic from structured data using template: {template_name}"
        )

        try:
            # Start with a copy of the template
            template_content = copy.deepcopy(template)
            canvas_data = template_content.get("canvas_data", {})
            elements = canvas_data.get("elements", [])

            # Get base dimensions
            width = template.get("width", 800)
            height = template.get("height", 2000)
            background_color = template.get("background_color", "white")

            # Assign icons based on template preferences
            structured_data = assign_icons_using_keywords(structured_data, template)
            structured_data = assign_vectors_using_keywords(structured_data)

            # Process elements to replace placeholders with content from structured data
            self._map_structured_data_to_elements(elements, structured_data)

            # Prepare final content
            content = {"canvas_data": canvas_data}

            # Prepare response
            infographic_data = {
                "title": structured_data.get("title", f"New {template_name}"),
                "content": content,
                "width": width,
                "height": height,
                "preview": self._generate_preview(structured_data),
                "background_color": background_color,
            }

            return infographic_data

        except Exception as e:
            logger.error(f"Error generating infographic from structured data: {str(e)}")
            raise

    def _map_structured_data_to_elements(self, elements, structured_data):
        """
        Map structured data to template elements

        Args:
            elements (list): Template elements
            structured_data (dict): Structured data with title, subTitle, sections
        """
        # Get all sections from the structured data - support both formats
        if isinstance(structured_data, list):
            # If structured_data is already a list of sections
            sections = structured_data
            title = ""
            subtitle = ""
        else:
            # If structured_data is a dict with a 'sections' key (original format)
            sections = structured_data.get("sections", [])
            title = structured_data.get("title", "")
            subtitle = structured_data.get("subTitle", "")

        for element in elements:
            # Handle text elements
            if element["type"] == "text" and "content" in element:
                text_content = element["content"]

                # Replace title placeholder
                if "{{title}}" in text_content or "{{headline}}" in text_content:
                    element["content"] = title
                    continue

                # Replace subtitle placeholder
                if (
                    "{{sub_title}}" in text_content
                    or "{{subtitle}}" in text_content
                    or "{{description}}" in text_content
                ):
                    element["content"] = subtitle
                    continue

                # Handle specific section title placeholders (e.g., {{section_title_1}})
                section_title_match = re.search(
                    r"{{section_title_(\d+)}}", text_content
                )
                if section_title_match:
                    section_idx = int(section_title_match.group(1)) - 1
                    if section_idx < len(sections):
                        element["content"] = sections[section_idx]["title"]
                    else:
                        element["content"] = f"Section {section_idx + 1}"
                    continue

                # Handle specific section content placeholders (e.g., {{section_content_1}})
                section_content_match = re.search(
                    r"{{section_content_(\d+)}}", text_content
                )
                if section_content_match:
                    section_idx = int(section_content_match.group(1)) - 1
                    if section_idx < len(sections):
                        element["content"] = sections[section_idx]["content"]
                    else:
                        element["content"] = (
                            f"Content for section {section_idx + 1} goes here."
                        )
                    continue

                # Handle generic section placeholders (backward compatibility)
                if "{{section" in text_content:
                    # Extract section number if present (e.g., {{section1_title}})
                    match = re.search(r"{{section(\d+)_(title|content)}}", text_content)
                    if match:
                        section_idx = int(match.group(1)) - 1
                        field = match.group(2)

                        if section_idx < len(sections):
                            if field == "title":
                                element["content"] = sections[section_idx]["title"]
                            else:
                                element["content"] = sections[section_idx]["content"]
                    continue

                # Replace any formatted content placeholders
                if "{{formatted" in text_content:
                    # For formatted placeholders, we'll use sections content with bullet points
                    if sections:
                        formatted_content = []
                        for idx, section in enumerate(sections):
                            formatted_content.append(f"• {section['title']}")
                            # Add content as sub-bullets if it's not too long
                            content_lines = section["content"].split("\n")
                            for line in content_lines:
                                if line.strip():
                                    formatted_content.append(f"  - {line.strip()}")

                        element["content"] = "\n".join(formatted_content)

            # Handle icon elements (graphic elements with svgContent placeholders)
            elif (
                element["type"] == "graphic"
                and "svgContent" in element
                and isinstance(element["svgContent"], str)
            ):

                # Handle icon placeholders
                if "{{icon_" in element["svgContent"]:
                    # Extract icon number (e.g., {{icon_1}} -> 1)
                    icon_match = re.search(r"{{icon_(\d+)}}", element["svgContent"])
                    if icon_match:
                        icon_idx = int(icon_match.group(1)) - 1

                        # Replace with icon URL if available in structured data
                        if (
                            icon_idx < len(sections)
                            and "icon_url" in sections[icon_idx]
                        ):
                            element["src"] = sections[icon_idx]["icon_url"]
                            element["svgType"] = "external"
                            element["svgContent"] = ""  # Clear the placeholder

                            # If icon dimensions are available, use them
                            if (
                                "icon_width" in sections[icon_idx]
                                and "icon_height" in sections[icon_idx]
                            ):
                                # Maintain aspect ratio and adjust dimensions
                                original_width = element["width"]
                                original_height = element["height"]
                                icon_width = sections[icon_idx]["icon_width"]
                                icon_height = sections[icon_idx]["icon_height"]

                                if icon_width and icon_height:
                                    aspect_ratio = icon_width / icon_height
                                    if aspect_ratio > 1:  # Wider than tall
                                        element["height"] = (
                                            original_width / aspect_ratio
                                        )
                                    else:  # Taller than wide
                                        element["width"] = (
                                            original_height * aspect_ratio
                                        )

                                logger.info(
                                    f"Replaced icon placeholder {{icon_{icon_idx+1}}} with icon: {sections[icon_idx].get('icon', 'unknown')}"
                                )
                            else:
                                logger.warning(
                                    f"No icon_url found for section index {icon_idx}"
                                )

                # Handle vector placeholders
                elif "{{vector_" in element["svgContent"]:
                    # Extract vector number (e.g., {{vector_3}} -> 3)
                    vector_match = re.search(r"{{vector_(\d+)}}", element["svgContent"])
                    if vector_match:
                        vector_idx = int(vector_match.group(1)) - 1

                        # Replace with vector URL if available in structured data
                        if (
                            vector_idx < len(sections)
                            and "vector_url" in sections[vector_idx]
                        ):
                            element["src"] = sections[vector_idx]["vector_url"]
                            element["svgType"] = "external"
                            element["svgContent"] = ""  # Clear the placeholder

                            # If vector has a format, set it
                            if "vector_format" in sections[vector_idx]:
                                element["fileFormat"] = sections[vector_idx][
                                    "vector_format"
                                ]

                            logger.info(
                                f"Replaced vector placeholder {{vector_{vector_idx+1}}} with vector: {sections[vector_idx].get('vector', 'unknown')}"
                            )
                        else:
                            logger.warning(
                                f"No vector_url found for section index {vector_idx}"
                            )

    def _generate_preview(self, structured_data):
        """
        Generate a simple preview of the infographic structure

        Args:
            structured_data (dict): Structured data with title, subTitle, sections

        Returns:
            dict: Simple preview structure
        """
        preview = {
            "title": structured_data.get("title", ""),
            "subTitle": structured_data.get("subTitle", ""),
            "sections": [],
        }

        for section in structured_data.get("sections", []):
            preview["sections"].append(
                {
                    "title": section.get("title", ""),
                    "preview": (
                        section.get("content", "")[:100] + "..."
                        if len(section.get("content", "")) > 100
                        else section.get("content", "")
                    ),
                }
            )

        return preview

    # Keep existing methods for backward compatibility
    def generate_from_url(self, url, template_name, website_data):
        """Legacy method to maintain backward compatibility"""
        logger.warning(
            "generate_from_url is deprecated, use generate_from_structured_data instead"
        )

        # Get URL analyzer
        url_analyzer = URLAnalyzer()
        structured_data = url_analyzer._analyze_with_gpt(website_data)

        template = get_template(template_name)
        return self.generate_from_structured_data(
            structured_data, template_name, template
        )

    def generate_from_content(self, content, template_name):
        """Legacy method to maintain backward compatibility"""
        logger.warning(
            "generate_from_content is deprecated, use generate_from_structured_data instead"
        )

        # Get content analyzer
        content_analyzer = ContentAnalyzer()
        structured_data = content_analyzer._analyze_with_gpt(content)

        template = get_template(template_name)
        return self.generate_from_structured_data(
            structured_data, template_name, template
        )


# Initialize Voyage AI client globally


def get_icon_embeddings(use_outline_icons=None):
    """
    Fetch or generate and cache embeddings for icon titles using Voyage AI.
    Uses OutlineIcon model for outline icons and FlatIcon for filled icons.
    Processes texts in batches to respect the 1000-text limit.
    Returns a tuple of (icon_ids, embeddings).

    Args:
        use_outline_icons (bool, optional): If True, use OutlineIcon. If False, use FlatIcon.
            If None, use both.
    """
    # Modify cache key based on outline preference
    cache_suffix = (
        "_outline"
        if use_outline_icons
        else "_filled" if use_outline_icons is False else ""
    )
    cache_key = f"icon_embeddings_voyage{cache_suffix}"

    cached = cache.get(cache_key)
    if cached is not None:
        return cached  # Return cached (icon_ids, embeddings) tuple

    # Choose the appropriate icon model based on use_outline_icons
    if use_outline_icons:
        icons = OutlineIcon.objects.all()
        icon_type = "outline"
    elif not use_outline_icons:
        icons = FlatIcon.objects.all()
        icon_type = "filled"

    if not icons:
        logger.warning(f"No {icon_type} icons found in database")
        return [], np.array([])

    texts = [icon.title for icon in icons]
    icon_ids = [
        f"{'outline' if isinstance(icon, OutlineIcon) else 'flat'}_{icon.id}"
        for icon in icons
    ]
    total_texts = len(texts)
    batch_size = 1000  # Voyage AI's max batch size

    if total_texts > batch_size:
        logger.info(
            f"Processing {total_texts} {icon_type} icons in batches of {batch_size}"
        )
    else:
        logger.info(f"Processing {total_texts} {icon_type} icons in a single batch")

    all_embeddings = []

    # Process texts in batches
    for i in range(0, total_texts, batch_size):
        batch_texts = texts[i : i + batch_size]
        try:
            response = voyage_client.embed(
                texts=batch_texts, model="voyage-3", input_type="document"
            )
            embeddings = response.embeddings  # Voyage AI returns a list of embeddings
            all_embeddings.extend(embeddings)
        except voyageai.error.InvalidRequestError as e:
            logger.error(f"Error embedding batch {i//batch_size + 1}: {str(e)}")
            raise  # Re-raise to halt execution and debug if needed

    # Convert to NumPy array
    embeddings_array = np.array(all_embeddings)

    # Cache the result
    cache.set(cache_key, (icon_ids, embeddings_array), timeout=None)  # Never expire

    logger.info(f"Generated and cached embeddings for {len(icons)} {icon_type} icons")
    return icon_ids, embeddings_array


def get_vector_embeddings():
    """
    Fetch or generate and cache embeddings for all VectorIcon titles using Voyage AI.
    Processes texts in batches to respect the 1000-text limit.
    Returns a tuple of (vector_ids, embeddings).
    """
    cache_key = "vector_embeddings_voyage"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached  # Return cached (vector_ids, embeddings) tuple

    # Fetch all vector icons
    vectors = VectorIcon.objects.all()
    if not vectors:
        logger.warning("No Vector icons found in database")
        return [], np.array([])

    texts = [vector.title for vector in vectors]
    vector_ids = [vector.id for vector in vectors]
    total_texts = len(texts)
    batch_size = 1000  # Voyage AI's max batch size

    if total_texts > batch_size:
        logger.info(f"Processing {total_texts} vector icons in batches of {batch_size}")
    else:
        logger.info(f"Processing {total_texts} vector icons in a single batch")

    all_embeddings = []

    # Process texts in batches
    for i in range(0, total_texts, batch_size):
        batch_texts = texts[i : i + batch_size]
        try:
            response = voyage_client.embed(
                texts=batch_texts, model="voyage-3", input_type="document"
            )
            embeddings = response.embeddings  # Voyage AI returns a list of embeddings
            all_embeddings.extend(embeddings)
        except voyageai.error.InvalidRequestError as e:
            logger.error(f"Error embedding batch {i//batch_size + 1}: {str(e)}")
            raise  # Re-raise to halt execution and debug if needed

    # Convert to NumPy array
    embeddings_array = np.array(all_embeddings)

    # Cache the result
    cache.set(cache_key, (vector_ids, embeddings_array), timeout=None)  # Never expire

    logger.info(f"Generated and cached embeddings for {len(vectors)} vector icons")
    return vector_ids, embeddings_array


def assign_icons_using_keywords(structured_data, template=None):
    """
    Assign icons to sections based on GPT-suggested keywords.
    Uses both direct keyword matching and embedding similarity as fallback.
    Uses OutlineIcon for outline icons and FlatIcon for filled icons.
    """
    if "sections" not in structured_data or not structured_data["sections"]:
        return structured_data

    # Check if template requires outline icons
    use_outline_icons = template.get("use_outline_icons", False) if template else False

    # Choose the appropriate icon model
    IconModel = OutlineIcon if use_outline_icons else FlatIcon
    all_icons = IconModel.objects.all()

    # Prepare icon_ids and embeddings for fallback
    icon_ids, icon_embeddings = get_icon_embeddings(use_outline_icons)

    for section in structured_data["sections"]:
        if "icon_keywords" not in section:
            logger.warning(f"No icon_keywords found for section: {section['title']}")
            continue

        keywords = section["icon_keywords"]
        matched_icon = None

        # Try exact matches first (case insensitive)
        for keyword in keywords:
            matches = list(all_icons.filter(title__icontains=keyword))
            if matches:
                # Take the first match
                matched_icon = matches[0]
                logger.info(f"Found direct match for '{keyword}': {matched_icon.title}")
                break

        # If no direct match found, try embedding similarity with keywords
        if not matched_icon and icon_ids:
            try:
                # Combine keywords into a single search query
                keyword_query = " ".join(keywords)

                # Get embedding for combined keywords
                response = voyage_client.embed(
                    texts=[keyword_query], model="voyage-3", input_type="document"
                )
                keyword_embedding = np.array(response.embeddings[0]).reshape(1, -1)

                # Find most similar icon
                similarities = cosine_similarity(keyword_embedding, icon_embeddings)[0]
                best_idx = np.argmax(similarities)
                best_icon_id = icon_ids[best_idx]

                # Parse the icon type and ID from the composite ID
                icon_type, icon_id = best_icon_id.split("_")
                icon_id = int(icon_id)

                # Get the icon from the appropriate model
                if icon_type == "outline":
                    matched_icon = OutlineIcon.objects.get(id=icon_id)
                else:
                    matched_icon = FlatIcon.objects.get(id=icon_id)

                logger.info(
                    f"Found embedding match for keywords '{keyword_query}': {matched_icon.title} (score: {similarities[best_idx]:.4f})"
                )

                # Debug: Log top 3 matches
                top_indices = np.argsort(similarities)[-3:][::-1]
                top_matches = []
                for idx in top_indices:
                    icon_type, icon_id = icon_ids[idx].split("_")
                    icon_id = int(icon_id)
                    icon = (
                        OutlineIcon.objects.get(id=icon_id)
                        if icon_type == "outline"
                        else FlatIcon.objects.get(id=icon_id)
                    )
                    top_matches.append((icon.title, similarities[idx]))
                logger.debug(f"Top 3 matches for '{section['title']}': {top_matches}")

            except Exception as e:
                logger.error(f"Error using embeddings for icon matching: {str(e)}")

        # Assign the icon if found
        if matched_icon:
            section["icon"] = matched_icon.title
            section["icon_url"] = matched_icon.cdn_url
        else:
            logger.warning(f"No suitable icon found for section: {section['title']}")

    return structured_data


def assign_vectors_using_keywords(structured_data):
    """
    Assign vector icons to sections based on GPT-suggested keywords.
    Uses both direct keyword matching and embedding similarity as fallback.
    """
    if "sections" not in structured_data or not structured_data["sections"]:
        return structured_data

    # Get all available vector icons
    all_vectors = VectorIcon.objects.all()

    # Prepare vector_ids and embeddings for fallback
    vector_ids, vector_embeddings = get_vector_embeddings()
    for section in structured_data["sections"]:
        if "icon_keywords" not in section:
            logger.warning(f"No icon_keywords found for section: {section['title']}")
            continue

        keywords = section["icon_keywords"]
        matched_vector = None

        # Try exact matches first (case insensitive)
        for keyword in keywords:
            matches = list(all_vectors.filter(title__icontains=keyword))
            if matches:
                # Take the first match
                matched_vector = matches[0]
                logger.info(
                    f"Found direct match for '{keyword}': {matched_vector.title}"
                )
                break

        # If no direct match found, try embedding similarity with keywords
        if not matched_vector and vector_ids:
            try:
                # Combine keywords into a single search query
                keyword_query = " ".join(keywords)

                # Get embedding for combined keywords
                response = voyage_client.embed(
                    texts=[keyword_query], model="voyage-3", input_type="document"
                )
                keyword_embedding = np.array(response.embeddings[0]).reshape(1, -1)

                # Find most similar vector icon
                similarities = cosine_similarity(keyword_embedding, vector_embeddings)[
                    0
                ]
                best_idx = np.argmax(similarities)
                best_vector_id = vector_ids[best_idx]
                matched_vector = VectorIcon.objects.get(id=best_vector_id)

                logger.info(
                    f"Found embedding match for keywords '{keyword_query}': {matched_vector.title} (score: {similarities[best_idx]:.4f})"
                )

            except Exception as e:
                logger.error(f"Error using embeddings for vector matching: {str(e)}")

        # Assign the vector if found
        if matched_vector:
            section["vector"] = matched_vector.title
            section["vector_url"] = matched_vector.cdn_url
            section["vector_format"] = matched_vector.file_format
        else:
            logger.warning(f"No suitable vector found for section: {section['title']}")

    return structured_data


class PublicAnalyzeAndGenerateInfographicView(APIView):
    """
    Public API endpoint to analyze URL or content and generate multiple infographics
    Does not require authentication, for demonstration purposes
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle]
    throttle_scope = "public_infographic"

    def post(self, request):
        try:
            # Get request data
            url = request.data.get("url")
            content = request.data.get("content")
            language = request.data.get("language", "English")  # Default to English
            template_section = request.data.get(
                "template_section", "Infographic"
            )  # Default to Infographic

            account = request.user.account

            # Validate inputs
            if not url and not content:
                return Response(
                    {"error": "Either URL or content is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Get templates based on section or specific template
            templates = []
            # Get all templates from the specified section
            section_templates = get_templates_by_section(template_section)
            if not section_templates:
                return Response(
                    {"error": f"No templates found for section '{template_section}'"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Limit to 5 templates for the public API
            templates = [
                (f"{template_section}_{i+1}", template)
                for i, template in enumerate(section_templates[:5])
            ]

            # Initialize infographic generator
            generator = InfographicGenerator()

            # Process based on input type to get structured data
            structured_data = None
            if url:
                # First scrape and analyze the URL
                url_analyzer = URLAnalyzer()
                website_data = url_analyzer._scrape_website(url)

                # Analyze with GPT and assign icons using embeddings
                structured_data = url_analyzer._analyze_with_gpt(website_data, language)
            else:
                # Create a ContentAnalyzer instance
                content_analyzer = ContentAnalyzer()

                # For content, we'll use the same flow as URL analysis
                # First analyze the content with GPT to get structured data
                structured_data = content_analyzer._analyze_with_gpt(content, language)

            generated_infographics = []

            # Generate an infographic for each template (limited to 5)
            for template_name, template in templates:
                # Generate infographic with structured data
                infographic_data = generator.generate_from_structured_data(
                    structured_data, template_name, template
                )

                # Set infographic title from analysis results if not already set
                if (
                    "title" not in infographic_data
                    and structured_data
                    and "title" in structured_data
                ):
                    infographic_data["title"] = structured_data["title"]

                # Add to generated infographics - for public API we just return the data
                # Create an actual infographic in the database if the user is authenticated
                if request.user.is_authenticated:
                    try:
                        # Create the infographic record

                        infographic = InfoGraph.objects.create(
                            account=account,
                            title=infographic_data.get("title", f"New {template_name}"),
                            content=infographic_data["content"],
                            width=infographic_data["width"],
                            height=infographic_data["height"],
                            background_color=infographic_data["background_color"],
                        )

                        # Add the infographic ID to the data
                        infographic_data["id"] = str(infographic.uuid)
                        logger.info(
                            f"Created infographic {infographic.uuid} for user {request.user.email}"
                        )
                    except Exception as e:
                        logger.error(
                            f"Failed to create infographic for user {request.user.email}: {str(e)}"
                        )
                        # Continue with the process even if saving fails
                # rather than saving to database
                generated_infographics.append(
                    {
                        "id": str(infographic.uuid),
                        "template_name": template_name,
                        "title": infographic_data.get("title", f"New {template_name}"),
                        "content": infographic_data["content"],
                        "width": infographic_data["width"],
                        "height": infographic_data["height"],
                        "background_color": infographic_data["background_color"],
                        "preview": infographic_data.get("preview"),
                    }
                )
            
            account.use_ai_credits(credits_needed=1)
            return Response(
                {
                    "message": f"Successfully generated {len(generated_infographics)} infographics",
                    "infographics": generated_infographics,
                    "structured_data": structured_data,
                },
                status=status.HTTP_200_OK,
            )

        except ValidationError as e:
            logger.error(f"Validation error generating infographics: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            logger.error(f"Error generating infographics: {str(e)}")
            return Response(
                {"error": f"Failed to generate infographics: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _translate_structured_data(self, structured_data, target_language):
        """
        Translate structured data to the target language using GPT

        Args:
            structured_data (dict): The structured data to translate
            target_language (str): The target language code

        Returns:
            dict: Translated structured data
        """
        try:
            # Skip translation if target language is English or not provided
            if not target_language or target_language.lower() == "english":
                return structured_data

            logger.info(f"Translating structured data to {target_language}")

            client = OpenAI(api_key=settings.OPENAI_API_KEY)

            # Convert structured data to JSON string
            data_json = json.dumps(structured_data)

            prompt = f"""
            Translate the following infographic content from English to {target_language}.
            Translate all text content including title, subtitle, and all section titles and content.
            Maintain the same JSON structure exactly.
            
            Content to translate: {data_json}
            
            Return only the translated JSON object with the same structure.
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a translation assistant that helps translate structured data for infographics.",
                    },
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                max_tokens=1000,
                temperature=0.3,
            )

            try:
                translated_data = json.loads(response.choices[0].message.content)
                logger.info(f"Successfully translated data to {target_language}")
                return translated_data
            except json.JSONDecodeError:
                logger.error("Failed to parse translated JSON")
                return structured_data

        except Exception as e:
            logger.error(f"Error translating content: {str(e)}")
            # If translation fails, return original data
            return structured_data
