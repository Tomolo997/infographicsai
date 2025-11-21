# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.conf import settings
from .models import SVGIcon, VectorIcon, Pattern, FlatIcon, OutlineIcon
from .serializers import SVGIconSerializer, VectorIconSerializer
import logging
from rest_framework.decorators import api_view, permission_classes
from .service import PexelsService

logger = logging.getLogger(__name__)

class ListSVGIconsView(APIView):
    permission_classes = [IsAuthenticated]
    page_size = 20  # Number of items per page
    cache_timeout = 300  # 5 minutes cache timeout

    def get_cache_key(self, search_query, icon_type, page, items_per_page):
        return f"svg_icons_list_{search_query}_{icon_type}_{page}_{items_per_page}"

    def get(self, request):
        try:
            # Get search parameters
            search_query = request.query_params.get('search', '')
            icon_type = request.query_params.get('type', '')
            page = request.query_params.get('page', 1)
            items_per_page = int(request.query_params.get('per_page', self.page_size))
            
            # Try to get cached response
            cache_key = self.get_cache_key(search_query, icon_type, page, items_per_page)
            cached_response = cache.get(cache_key)
            
            if cached_response:
                return Response(cached_response, status=status.HTTP_200_OK)
            
            # Start with user's icons and flat icons
            svg_icons = SVGIcon.objects.none()
            flat_icons = FlatIcon.objects.none()
            outline_icons = OutlineIcon.objects.none()

            if icon_type == 'outline':
                outline_icons = OutlineIcon.objects.all()
            elif icon_type == 'flat':
                flat_icons = FlatIcon.objects.all()
            else:
                svg_icons = SVGIcon.objects.all()
                flat_icons = FlatIcon.objects.all()
                outline_icons = OutlineIcon.objects.all()
            
            # Apply search filter to each queryset if provided
            if search_query:
                if icon_type == 'outline':
                    outline_icons = outline_icons.filter(Q(title__icontains=search_query))
                elif icon_type == 'flat':
                    flat_icons = flat_icons.filter(Q(title__icontains=search_query))
                else:
                    svg_icons = svg_icons.filter(Q(title__icontains=search_query))
                    flat_icons = flat_icons.filter(Q(title__icontains=search_query))
                    outline_icons = outline_icons.filter(Q(title__icontains=search_query))

            # Combine querysets after filtering
            queryset = svg_icons.union(flat_icons).union(outline_icons)
            
            # Order by most recent first
            queryset = queryset.order_by('created_at')
            
            # Apply pagination
            paginator = Paginator(queryset, items_per_page)
            
            try:
                paginated_icons = paginator.page(page)
            except PageNotAnInteger:
                paginated_icons = paginator.page(1)
            except EmptyPage:
                paginated_icons = paginator.page(paginator.num_pages)
            
            serializer = SVGIconSerializer(paginated_icons, many=True)
            
            response_data = {
                'icons': serializer.data,
                'total': queryset.count(),
                'page': int(page),
                'total_pages': paginator.num_pages,
                'per_page': items_per_page,
                'has_next': paginated_icons.has_next(),
                'has_previous': paginated_icons.has_previous(),
            }

            # Cache the response
            cache.set(cache_key, response_data, self.cache_timeout)
            
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error listing SVG icons: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ListVectorIconsView(APIView):
    permission_classes = [IsAuthenticated]
    page_size = 20  # Number of items per page

    def get(self, request):
        try:
            # Get search parameters
            search_query = request.query_params.get('search', '')
            file_format = request.query_params.get('format', '')
            page = request.query_params.get('page', 1)
            items_per_page = int(request.query_params.get('per_page', self.page_size))
            
            # Start with user's icons
            queryset = VectorIcon.objects.all()
            
            # Apply search if provided
            if search_query:
                queryset = queryset.filter(
                    Q(title__icontains=search_query)
                )
            
            # Filter by format if provided
            if file_format:
                queryset = queryset.filter(file_format=file_format)
            
            # Order by most recent first
            queryset = queryset.order_by('-created_at')
            
            # Apply pagination
            paginator = Paginator(queryset, items_per_page)
            
            try:
                paginated_icons = paginator.page(page)
            except PageNotAnInteger:
                paginated_icons = paginator.page(1)
            except EmptyPage:
                paginated_icons = paginator.page(paginator.num_pages)
            
            serializer = VectorIconSerializer(paginated_icons, many=True)
            
            return Response({
                'icons': serializer.data,
                'total': queryset.count(),
                'page': int(page),
                'total_pages': paginator.num_pages,
                'per_page': items_per_page,
                'has_next': paginated_icons.has_next(),
                'has_previous': paginated_icons.has_previous(),
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error listing vector icons: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class ListPatternsView(APIView):
    permission_classes = [IsAuthenticated]
    page_size = 20  # Number of items per page

    def get(self, request):
        try:
            # Get search parameters
            search_query = request.query_params.get('search', '')
            file_format = request.query_params.get('format', '')
            page = request.query_params.get('page', 1)
            items_per_page = int(request.query_params.get('per_page', self.page_size))
            
            # Start with user's icons
            queryset = Pattern.objects.all()
            
            # Apply search if provided
            if search_query:
                queryset = queryset.filter(
                    Q(title__icontains=search_query)
                )
            
            # Filter by format if provided
            if file_format:
                queryset = queryset.filter(file_format=file_format)
            
            # Order by most recent first
            queryset = queryset.order_by('-created_at')
            
            # Apply pagination
            paginator = Paginator(queryset, items_per_page)
            
            try:
                paginated_icons = paginator.page(page)
            except PageNotAnInteger:
                paginated_icons = paginator.page(1)
            except EmptyPage:
                paginated_icons = paginator.page(paginator.num_pages)
            
            serializer = VectorIconSerializer(paginated_icons, many=True)
            
            return Response({
                'patterns': serializer.data,
                'total': queryset.count(),
                'page': int(page),
                'total_pages': paginator.num_pages,
                'per_page': items_per_page,
                'has_next': paginated_icons.has_next(),
                'has_previous': paginated_icons.has_previous(),
            }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error listing vector icons: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# views.py
import requests
from django.http import HttpResponse

class MediaProxyView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, path):
        try:
            r2_url = f"{path}"
            response = requests.get(r2_url)
            
            return HttpResponse(
                response.content,
                content_type=response.headers['Content-Type']
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PexelsPhotosView(APIView):
    permission_classes = [IsAuthenticated]
    pexels_service = PexelsService()

    def get(self, request):
        try:
            # Get search parameters
            search_query = request.query_params.get('query', '')
            page = int(request.query_params.get('page', 1))
            per_page = int(request.query_params.get('per_page', 15))
            orientation = request.query_params.get('orientation')
            size = request.query_params.get('size')
            color = request.query_params.get('color')

            if search_query:
                data = self.pexels_service.search_photos(
                    search_query,
                    page=page,
                    per_page=per_page,
                    orientation=orientation,
                    size=size,
                    color=color
                )
            else:
                data = self.pexels_service.get_curated_photos(
                    page=page,
                    per_page=per_page
                )

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error fetching Pexels photos: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PexelsPhotoDetailView(APIView):
    permission_classes = [IsAuthenticated]
    pexels_service = PexelsService()

    def get(self, request, photo_id):
        try:
            data = self.pexels_service.get_photo(photo_id)
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching Pexels photo detail: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

