from django.urls import path

from . import views

urlpatterns = [
    # Infograph CRUD
    path("list/", views.InfographListAPIView.as_view(), name="infograph.list"),
    path("create/", views.InfographCreateAPIView.as_view(), name="infograph.create"),
    path("create/pdf/", views.InfographCreateFromPDFAPIView.as_view(), name="infograph.create.pdf"),
    path("create/own-template/", views.InfographCreateFromOwnTemplateAPIView.as_view(), name="infograph.create.own.template"),
    path("create/template/", views.InfographCreateFromTemplateAPIView.as_view(), name="infograph.create.template"),
    path("delete/<int:pk>/", views.InfographDeleteAPIView.as_view(), name="infograph.delete"),
    
    # Status and webhook endpoints
    path("status/<int:infograph_id>/", views.InfographStatusAPIView.as_view(), name="infograph.status"),
    path("webhook/<int:infograph_id>/", views.InfographWebhookAPIView.as_view(), name="infograph.webhook"),
    
    # Download endpoint (proxy with CORS)
    path("download/<int:infograph_id>/", views.InfographDownloadAPIView.as_view(), name="infograph.download"),
    
    # Template endpoints
    path("templates/list/", views.TemplateListAPIView.as_view(), name="template.list"),
    path("templates/create/", views.TemplateCreateAPIView.as_view(), name="template.create"),
]
