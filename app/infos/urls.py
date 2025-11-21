from django.urls import path
from . import views


# urls.py
urlpatterns = [
    path(
        "save-infographic/",
        views.SaveInfographicView.as_view(),
        name="infos.save_infographic"
    ),
#     path(
#         "save-infographic-admin/",
#         views.AdminSaveInfographicView.as_view(),
#         name="infos.save_infographic_admin"
#     ),
#     path(
#     "admin-infographic/<uuid:uuid>/",
#     views.AdminGetInfographicView.as_view(),
#     name="infos.admin_get_infographic",
# ),
    path(
        "create-infographic/",
        views.CreateInfographView.as_view(),
        name="infos.save_infographic"
    ),
    path(
        "update-infographic/<int:id>/",
        views.UpdateInfographicView.as_view(),
        name="infos.update_infographic",
    ),
    path(
        "list-infographics/",
        views.ListInfographicsView.as_view(),
        name="infos.list_infographics",
    ),  # New
    path("get-csrf/", views.GetCSRFTokenView.as_view(), name="get_csrf"),
    path(
        "infographic/<uuid:uuid>/",
        views.GetInfographicView.as_view(),
        name="infos.get_infographic",
    ),
    path(
        "infographic/<uuid:uuid>/rename/",
        views.RenameInfographicView.as_view(),
        name="infos.rename_infographic",
    ),
    path(
        "infographic/<uuid:uuid>/delete/",
        views.DeleteInfographicView.as_view(),
        name="infos.delete_infographic",
    ),
    path(
        "infographic/<uuid:uuid>/duplicate/",
        views.DuplicateInfographicView.as_view(),
        name="infos.duplicate_infographic",
    ),
    path(
        "infographic/<uuid:uuid>/save/",
        views.SaveInfographView.as_view(),
        name="infos.save_infograph",
    ),
    path(
        "saved-infographics/",
        views.ListSavedInfographsView.as_view(),
        name="infos.list_saved_infographics",
    ),
    path("upload-media/", views.UploadMediaView.as_view(), name="infos.upload_media"),
    path(
        "download/",
        views.DownloadInfographicView.as_view(),
        name="infos.download_infographic",
    ),
    path(
        "templates/",
        views.GetTemplatesView.as_view(),
        name="infos.templates_infographic",
    ),
    path("recent-uploads/", views.RecentUploadsView.as_view(), name="recent-uploads"),
    path("template-list/", views.ListTemplatesView.as_view(), name="list-templates"),
    path(
        "analyze-and-generate/",
        views.AnalyzeAndGenerateInfographicView.as_view(),
        name="analyze-and-generate",
    ),
    path(
        "create-from-template/",
        views.CreateFromTemplateView.as_view(),
        name="create-from-template",
    ),
    path(
        "iconify/search/",
        views.IconifySearchWithSVGView.as_view(),
        name="iconify-search",
    ),
    # Public API for generating infographics
    path('generate-infographics/', views.PublicAnalyzeAndGenerateInfographicView.as_view(), name='public-generate-infographics'),
]
