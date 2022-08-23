from django.urls import path
from .views import (
    RegistrationView,
    CustomAuthToken,
    CustomDiscardAuthToken,
    ChangePasswordView,
    ProfileApiView,
    EmailSendView,
    ActivationApiView,
    ActivationResendView,
)
from rest_framework_simplejwt.views import TokenVerifyView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "api-v1"

urlpatterns = [
    path(
        "change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
    path(
        "activation/confirm/<str:token>",
        ActivationApiView.as_view(),
        name="activation",
    ),
    path(
        "activation/resend/",
        ActivationResendView.as_view(),
        name="resend_token",
    ),
    path("jwt/create/", TokenObtainPairView.as_view(), name="token-create"),
    path("jwt/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("token/login", CustomAuthToken.as_view(), name="login-token"),
    path("token/logout", CustomDiscardAuthToken.as_view(), name="logout-token"),
    path("profile/", ProfileApiView.as_view(), name="user-profile"),
    path("test-email", EmailSendView.as_view(), name="email-test"),
]
