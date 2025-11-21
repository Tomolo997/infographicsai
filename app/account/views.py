
import logging
import os
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt

import requests
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import Account
from account.serializers import AccountSerializer
from file_upload.client import R2Client

from .models import CustomUser
from .serializers import CustomUserSerializer, UserSignupSerializer

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

            if not user.is_active:
                return Response(
                    {"error": "User account is not active"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            response_data = {
                "email": user.email,
                "profile_picture_url": account.profile_picture_url,
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
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class CustomObtainAuthToken(ObtainAuthToken):
    authentication_classes = []  # Disable authentication for this view

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

@method_decorator(csrf_exempt, name='dispatch')
class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # Disable authentication for this view




class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(CustomUser, pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
        
        if user is not None and default_token_generator.check_token(user, token):
            # Activate the user
            user.is_active = True
            user.save()
            
            # Generate authentication token for auto-login
            auth_token, created = Token.objects.get_or_create(user=user)
            
            # Redirect to frontend with token
            return redirect(f"{frontend_url}/verify-success?token={auth_token.key}")
        else:
            # Invalid token - redirect to error page
            return redirect(f"{frontend_url}/verify-error")


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
        # Existing user - just activate them
        user = CustomUser.objects.get(email=email)
        if not user.is_active:
            user.is_active = True
            user.save()
    except CustomUser.DoesNotExist:
        # New user from Google - no password needed
        user = CustomUser.objects.create_user(email=email)
        user.is_active = True
        user.save()


    token, created = Token.objects.get_or_create(user=user)
    # Redirect to dashboard with token - frontend will handle auth automatically
    return redirect(f"{frontend_url}/dashboard?token={token.key}")


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
    # Redirect to dashboard with token - frontend will handle auth automatically
    return redirect(f"{frontend_url}/dashboard?token={token.key}")


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
