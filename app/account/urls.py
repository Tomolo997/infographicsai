from django.urls import path
from . import views
from account.stripe_app.views import (
    stripe_webhook,
    CreateCheckoutSessionView,
    UpgradeSubscriptionView,
    CancelSubscriptionView,
    ReactivateSubscriptionView,
    GetSubscriptionStatusView,
    AvailableUpgradesView,
    AllSubscriptionTiersView,
    PublicCheckoutSessionView,
)

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
    path("stripe-webhook/", stripe_webhook, name="stripe_webhook"),
    path(
        "request-magic-link/",
        views.RequestMagicLinkView.as_view(),
        name="request_magic_link",
    ),
    path(
        "login-magic-link/",
        views.LoginMagicLinkView.as_view(),
        name="login_magic_link",
    ),
    path(
        "verify-magic-link/",
        views.VerifyMagicLinkView.as_view(),
        name="verify_magic_link",
    ),
    path("suggest/", views.SuggestionView.as_view(), name="suggestion"),
    path(
        "create-checkout-session/",
        CreateCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path(
        "public-checkout-session/",
        PublicCheckoutSessionView.as_view(),
        name="public-checkout-session",
    ),
    path(
        "upgrade-subscription/",
        UpgradeSubscriptionView.as_view(),
        name="upgrade-subscription",
    ),
    path(
        "cancel-subscription/",
        CancelSubscriptionView.as_view(),
        name="cancel-subscription",
    ),
    path(
        "reactivate-subscription/",
        ReactivateSubscriptionView.as_view(),
        name="reactivate-subscription",
    ),
    path(
        "subscription-status/",
        GetSubscriptionStatusView.as_view(),
        name="subscription-status",
    ),
    path(
        "available-upgrades/",
        AvailableUpgradesView.as_view(),
        name="available-upgrades",
    ),
    path(
        "subscription-tiers/",
        AllSubscriptionTiersView.as_view(),
        name="subscription-tiers",
    ),
]
