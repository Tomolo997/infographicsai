from django.urls import path
from . import views


# urls.py
urlpatterns = [
    path('svg/', views.ListSVGIconsView.as_view(), name='icons.svg_views'),
    path('vectors/', views.ListVectorIconsView.as_view(), name='icons.vector_views'),
    path('patterns/', views.ListPatternsView.as_view(), name='icons.pattern_views'),
    path('media-proxy/<path:path>', views.MediaProxyView.as_view(), name='media_proxy'),
    path('pexels/photos/', views.PexelsPhotosView.as_view(), name='pexels.photos'),
    path('pexels/photos/<int:photo_id>/', views.PexelsPhotoDetailView.as_view(), name='pexels.photo_detail'),
]

# TODO add these urls 
    # Update infograph / Save infograph ✅re 