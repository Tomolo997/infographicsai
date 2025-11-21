from rest_framework import generics
from rest_framework import permissions
from account.models import Account, Suggestion

from account.serializers import AccountSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CustomUserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
import logging
import requests
from django.conf import settings
from .models import CustomUser, MagicLink
from django.shortcuts import redirect
from urllib.parse import urlencode
from file_upload.client import R2Client
from email_client import services as email_services
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils import timezone
from rest_framework.permissions import AllowAny
from account.models import UserSubscription
import os
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from rest_framework import generics
from .serializers import UserSignupSerializer

logger = logging.getLogger(__name__)


class AccountListView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountCreateView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountGetView(generics.RetrieveAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        
        try:
            account = Account.objects.get(user=user)
            subscription = UserSubscription.objects.filter(
                user=user,
            ).select_related('tier').last()

            if not user.is_active:
                return Response(
                    {"error": "User account is not active"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            account.reset_monthly_downloads_if_needed()
            response_data = {
                "email": user.email,
                "profile_picture_url": account.profile_picture_url,
                "credits": {
                    "current": account.credit_balance,
                    "total": subscription.tier.ai_credits
                },
                "downloads": {
                    "used": account.monthly_downloads,
                    "limit": subscription.tier.monthly_download_limit,
                    "remaining": subscription.tier.monthly_download_limit - account.monthly_downloads
                },
                "subscription": {
                    "status": subscription.status,
                    "tier": subscription.tier.name,
                    "is_lifetime": subscription.is_lifetime,
                    "is_free": subscription.tier.is_free,
                    "end_date": subscription.end_date
                }
            }

            return Response(response_data)

        except Account.DoesNotExist:
            return Response(
                {"error": "Account not found"},
                status=status.HTTP_404_NOT_FOUND
            )

class CustomUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        logger.info(f"Authenticated user: {user}")
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user_id": token.user_id, "email": token.user.email}
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]


# views.py
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import CustomUser


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(CustomUser, pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"status": "Account verified"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"status": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


def google_login(request):
    google_auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent",
    }
    url = f"{google_auth_url}?{urlencode(params)}"
    return redirect(url)


def google_callback(request):
    code = request.GET.get("code")

    frontend_url = settings.FRONTEND_URL
    if not code:
        return redirect(frontend_url)  # Handle the error appropriately
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    logger.info(f"Using redirect URI: {settings.GOOGLE_REDIRECT_URI}")
    token_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    token_response = requests.post(token_url, data=token_data, headers=token_headers)

    token_response_data = token_response.json()

    if "error" in token_response_data:
        # Handle the error appropriately
        return redirect(frontend_url)

    access_token = token_response_data.get("access_token")
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    user_info_params = {"access_token": access_token}
    user_info_response = requests.get(user_info_url, params=user_info_params)
    user_info_data = user_info_response.json()
    logger.info(f"token response use_info_data", user_info_data)

    if "error" in user_info_data:
        logger.info("User info data retrieved successfully: %s", user_info_data)
        # Handle the error appropriately
        return redirect(frontend_url)

    email = user_info_data.get("email")
    if not email:
        raise ValueError("Email is required.")

    try:
        user = CustomUser.objects.get(email=email)
        user.is_active = True
        user.save()
    except CustomUser.DoesNotExist:
        user = CustomUser.objects.create_user(email=email)
        user.is_active = True
        user.save()

    print(user, "USER, CREATED")

    token, created = Token.objects.get_or_create(user=user)
    response_data = {
        "token": token.key,
        "user_id": user.id,
        "email": user.email,
    }
    print(response_data, "RESPONSE DATA")
    return redirect(f"{frontend_url}/dashboard/?token={token.key}")


def google_callback_public(request):
    code = request.GET.get("code")

    frontend_url = settings.FRONTEND_URL
    print(code, "CODE")
    if not code:
        return redirect(frontend_url)  # Handle the error appropriately
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI_PUBLIC,
        "grant_type": "authorization_code",
    }
    logger.info(f"Using redirect URI: {settings.GOOGLE_REDIRECT_URI_PUBLIC}")
    print(token_data, "TOKEN DATA")
    token_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    token_response = requests.post(token_url, data=token_data, headers=token_headers)

    token_response_data = token_response.json()
    print(token_response_data, "TOKEN RESPONSE DATA")
    if "error" in token_response_data:
        # Handle the error appropriately
        return redirect(frontend_url)

    access_token = token_response_data.get("access_token")
    user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    user_info_params = {"access_token": access_token}
    user_info_response = requests.get(user_info_url, params=user_info_params)
    user_info_data = user_info_response.json()

    if "error" in user_info_data:
        logger.info("User info data retrieved successfully: %s", user_info_data)
        # Handle the error appropriately
        return redirect(frontend_url)

    email = user_info_data.get("email")
    if not email:
        raise ValueError("Email is required.")

    try:
        user = CustomUser.objects.get(email=email)
        user.is_active = True
        user.save()
    except CustomUser.DoesNotExist:
        user = CustomUser.objects.create_user(email=email)
        user.is_active = True
        user.save()

    token, created = Token.objects.get_or_create(user=user)
    response_data = {
        "token": token.key,
        "user_id": user.id,
        "email": user.email,
    }
    return redirect(f"{frontend_url}/?token={token.key}")


logger = logging.getLogger(__name__)

class ProfilePictureUploadView(APIView):
    permission_classes = [IsAuthenticated]
    
    # Maximum file size (5MB)
    MAX_FILE_SIZE = 5 * 1024 * 1024
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}
    
    # Allowed MIME types
    ALLOWED_MIME_TYPES = {'image/jpeg', 'image/png', 'image/gif'}

    def validate_file(self, file):
        """Validate the uploaded file."""
        # Check file size
        if file.size > self.MAX_FILE_SIZE:
            return False, "File size exceeds 5MB limit"

        # Get file extension and check if it's allowed
        _, extension = os.path.splitext(file.name.lower())
        if extension not in self.ALLOWED_EXTENSIONS:
            return False, "Invalid file extension. Only .jpg, .jpeg, .png, and .gif are allowed"

        # Check content type
        content_type = file.content_type
        if content_type not in self.ALLOWED_MIME_TYPES:
            return False, "Invalid file type. Only JPEG, PNG, and GIF are allowed"

        return True, None

    def get(self, request):
        """Get current profile picture information."""
        try:
            account = Account.objects.get(user=request.user)
            serializer = AccountSerializer(account)
            return Response({
                'profile_picture_url': account.profile_picture_url,
                'last_updated': account.updated_at
            }, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response(
                {"error": "Account not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):
        """Upload a new profile picture."""
        # Check if file was provided
        if 'file' not in request.FILES:
            return Response(
                {"error": "No file provided"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        file_obj = request.FILES['file']
        
        # Validate file
        is_valid, error_message = self.validate_file(file_obj)
        if not is_valid:
            return Response(
                {"error": error_message}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Generate a unique filename using user ID and original extension
            _, extension = os.path.splitext(file_obj.name.lower())
            file_name = f"profile_pictures/{request.user.id}_profile{extension}"

            # Upload file using R2Client
            r2_client = R2Client()
            file_url = r2_client.upload_file(file_obj, file_name)

            if not file_url:
                return Response(
                    {"error": "File upload failed"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Update user's account with new profile picture URL
            account = Account.objects.get(user=request.user)
            
            # Store the old URL for potential cleanup
            old_url = account.profile_picture_url
            
            # Update with new URL
            account.profile_picture_url = file_url
            account.save()

            # If there was an old profile picture, we could delete it here
            if old_url and old_url != file_url:
                try:
                    r2_client.delete_file(old_url)
                except Exception as e:
                    # Log the error but don't fail the request
                    logger.error(f"Failed to delete old profile picture: {str(e)}")

            return Response({
                "message": "Profile picture updated successfully",
                "profile_picture_url": file_url
            }, status=status.HTTP_200_OK)

        except Account.DoesNotExist:
            return Response(
                {"error": "Account not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        """Remove current profile picture."""
        try:
            account = Account.objects.get(user=request.user)
            
            if not account.profile_picture_url:
                return Response(
                    {"error": "No profile picture to delete"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Store the URL for deletion
            old_url = account.profile_picture_url
            
            # Remove the profile picture URL from the account
            account.profile_picture_url = None
            account.save()

            # Delete the file from storage
            try:
                r2_client = R2Client()
                r2_client.delete_file(old_url)
            except Exception as e:
                # Log the error but don't fail the request
                logger.error(f"Failed to delete profile picture file: {str(e)}")

            return Response(
                {"message": "Profile picture removed successfully"}, 
                status=status.HTTP_200_OK
            )

        except Account.DoesNotExist:
            return Response(
                {"error": "Account not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Create a custom throttle class for magic link requests
class MagicLinkRateThrottle(AnonRateThrottle):
    rate = '3/hour'  # Limit to 3 requests per hour per IP
    scope = 'magic_link'

class RequestMagicLinkView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view
    throttle_classes = [MagicLinkRateThrottle]  # Apply throttling
    
    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        """
        Request a magic link for passwordless login.
        
        Expects an email in the request data.
        """
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {"error": "Invalid email format"}, status=status.HTTP_400_BAD_REQUEST
            )

        user, created = CustomUser.objects.get_or_create(email=email)

        # If the user was just created, we might want to set some default values
        if created:
            user.username = email.split("@")[0]  # Set a default username
            user.save()

        # Delete any existing unused magic links for this user
        MagicLink.objects.filter(user=user, is_used=False).delete()

        # Create and send new magic link
        email_services.send_magic_link_email(user)

        # In a production environment, you might want to use a task queue (like Celery)
        # to send emails asynchronously

        return Response(
            {"message": "Magic link sent", "user_id": user.id, "email": user.email},
            status=status.HTTP_200_OK,
        )


class LoginMagicLinkView(APIView):
    permission_classes = [AllowAny]  # Allow any user to access this view
    throttle_classes = [MagicLinkRateThrottle]  # Apply throttling

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        """
        Request a magic link for passwordless login.
        
        Expects an email in the request data.
        Checks if the user exists before sending a magic link.
        """
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_email(email)
        except ValidationError:
            return Response(
                {"error": "Invalid email format"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user exists
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "No account found with this email. Please sign up first."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Delete any existing unused magic links for this user
        MagicLink.objects.filter(user=user, is_used=False).delete()

        # Create and send new magic link
        email_services.send_magic_link_email(user)

        return Response(
            {"message": "Magic link sent", "user_id": user.id, "email": user.email},
            status=status.HTTP_200_OK,
        )


class VerifyMagicLinkView(APIView):
    permission_classes = [AllowAny]  #

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        token = request.data.get("token")

        if not token:
            return Response(
                {"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            magic_link = MagicLink.objects.get(token=token, is_used=False)

            # Check if the magic link has expired
            expiry_time = magic_link.created_at + timezone.timedelta(
                minutes=settings.MAGIC_LINK_EXPIRY_MINUTES
            )
            if timezone.now() > expiry_time:
                magic_link.is_used = True
                magic_link.save()
                return Response(
                    {"error": "Magic link has expired"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Mark the magic link as used
            magic_link.is_used = True
            magic_link.save()

            user = magic_link.user

            # Generate or get the token for the user
            auth_token, created = Token.objects.get_or_create(user=user)

            # Activate the user if not already active
            if not user.is_active:
                user.is_active = True
                user.save()

            return Response(
                {
                    "message": "Authenticated successfully",
                    "token": auth_token.key,
                    "user_id": user.id,
                    "email": user.email,
                },
                status=status.HTTP_200_OK,
            )

        except MagicLink.DoesNotExist:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SuggestionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        suggestion_title = request.data.get("title")
        suggestion_text = request.data.get("suggestion")
        category = request.data.get("category", "general")
        rating = request.data.get("rating")

        if not suggestion_title or not suggestion_text:
            return Response(
                {"error": "Title and suggestion text are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        # Validate category
        valid_categories = [choice[0] for choice in Suggestion.CATEGORY_CHOICES]
        if category not in valid_categories:
            return Response(
                {"error": f"Invalid category. Choose from: {', '.join(valid_categories)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        # Validate rating if provided
        if rating is not None:
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    return Response(
                        {"error": "Rating must be between 1 and 5"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            except (ValueError, TypeError):
                return Response(
                    {"error": "Rating must be a number between 1 and 5"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        suggestion = Suggestion.objects.create(
            user=user,
            suggestion_title=suggestion_title,
            suggestion_text=suggestion_text,
            category=category,
            rating=rating,
        )

        return Response(
            {
                "message": "Feedback submitted successfully",
                "suggestion_id": suggestion.id,
            },
            status=status.HTTP_201_CREATED,
        )
        
    def get(self, request):
        """Return the user's feedback history"""
        if not request.user.is_staff:
            # Regular users can only see their own feedback
            suggestions = Suggestion.objects.filter(user=request.user).order_by('-created_at')
        else:
            # Staff users can see all feedback
            suggestions = Suggestion.objects.all().order_by('-created_at')
            
        data = [{
            'id': suggestion.id,
            'title': suggestion.suggestion_title,
            'text': suggestion.suggestion_text,
            'category': suggestion.category,
            'rating': suggestion.rating,
            'created_at': suggestion.created_at,
            'user_email': suggestion.user.email
        } for suggestion in suggestions]
        
        return Response(data, status=status.HTTP_200_OK)


import json
import logging
import subprocess
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def github_webhook(request):
    try:
        # Parse the JSON payload
        payload = json.loads(request.body)

        if payload["ref"] == "refs/heads/main":
            # Trigger your deployment script here
            try:
                print("pushed")
                return HttpResponse(
                    "Webhook received and deployment triggered", status=200
                )
            except subprocess.CalledProcessError as e:
                logger.error(f"Deployment script error: {e.stderr}")
                return HttpResponse("Error during deployment", status=500)
        else:
            logger.info("Push to non-main branch, no deployment triggered")
            return HttpResponse("Webhook received, no deployment needed", status=200)

    except json.JSONDecodeError:
        logger.error("Invalid JSON payload received")
        return HttpResponse("Invalid payload", status=400)
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return HttpResponse("Error processing webhook", status=500)
