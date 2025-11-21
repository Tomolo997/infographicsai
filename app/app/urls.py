from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



from account.views import github_webhook
# Routers provide an easy way of automatically determining the URL conf.

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('account.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/infos/', include(('infos.urls', 'infos'), namespace='infos_api')),
    path('api/icons/', include(('icons.urls', 'infos'), namespace='icons_api')),
    path('webhook', github_webhook, name="github_webhook"),
] 

if settings.DEBUG:
    # Serve static files in development
    urlpatterns += staticfiles_urlpatterns()
    # Add explicit static serving
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])