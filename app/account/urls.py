from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.AccountListView.as_view(), name="account.list"),
    path("create/", views.AccountCreateView.as_view(), name="account.create"),
    path("me/", views.AccountGetView.as_view(), name="account.me"),
    path("user/", views.CustomUserView.as_view(), name="custom_user"),
    path(
        "api-token-auth/", views.CustomObtainAuthToken.as_view(), name="api_token_auth"
    ),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "signup/", views.UserSignupView.as_view(), name="signup"
    ),  # Added user sign-up URL
    path(
        "verify/<uidb64>/<token>/", views.VerifyEmailView.as_view(), name="verify"
    ),  # Verification URL
    path(
        "upload-profile-picture/",
        views.ProfilePictureUploadView.as_view(),
        name="upload-profile-picture",
    ),
    path("google/login/", views.google_login, name="google_login"),
    path("google/callback/", views.google_callback, name="google_callback"),
    path("google/callback/public/", views.google_callback_public, name="google_callback_public"),
    path("credit-packs/", views.CreditPackListAPIView.as_view(), name="credit_packs"),
    path("purchase-credits/", views.PurchaseCreditsView.as_view(), name="purchase_credits"),
    path("stripe-webhook/", views.StripeWebhookView.as_view(), name="stripe_webhook"),
    path("credits-user/", views.CreditsUserView.as_view(), name="credits_user")
]
