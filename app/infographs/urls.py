from django.urls import path

from . import views

urlpatterns = [
    # Infograph CRUD
    path("list/", views.InfographListAPIView.as_view(), name="infograph.list"),
    path("create/", views.InfographCreateAPIView.as_view(), name="infograph.create"),
    path("create/pdf/", views.InfographCreateFromPDFAPIView.as_view(), name="infograph.create.pdf"),
    path("delete/<int:pk>/", views.InfographDeleteAPIView.as_view(), name="infograph.delete"),
    
    # Status and webhook endpoints
    path("status/<int:infograph_id>/", views.InfographStatusAPIView.as_view(), name="infograph.status"),
    path("webhook/<int:infograph_id>/", views.InfographWebhookAPIView.as_view(), name="infograph.webhook"),
    
    # Future endpoints
    # path("create/template/", views.InfographCreateTemplateAPIView.as_view(), name="infograph.create.template"),
    # path("create/own-template/", views.InfographCreateOwnTemplateAPIView.as_view(), name="infograph.create.own.template"),
    # path("get/<int:pk>/", views.InfographRetrieveAPIView.as_view(), name="infograph.get"),
    # path("update/<int:pk>/", views.InfographUpdateAPIView.as_view(), name="infograph.update"),
    # path("list/templates/", views.TemplateListAPIView.as_view(), name="template.list"),
]
