from django.urls import path
from .controllers.create import UserSettingsToggleAPI, Enable2FAAPIView
from .controllers.details import UserSettingsListAPIView

from django.urls import path
from helpers import fields as input_fields
from .controllers.avatar import UserAvatarAPI
from .controllers.create import UserRegistrationAPI
from .controllers.names_update import UserNamesUpdateAPI
from .controllers.password_update import UserPasswordUpdateAPI
from .controllers.user_account import UserAccountAPI
from .controllers.login import UserLoginAPIView
from .controllers.login_2fa import TwoFactorVerificationAPIView
from .controllers.resend_2fa import ResendTwoFactorTokenAPIView
from .controllers.forgot_password import (
    SendForgotPasswordOTPAPIView,
    PasswordResetOTPVerificationAPIView,
    CreateNewPasswordTokenAPIView
)

from .controllers.logout import (
    LogoutViewAPI,
    LogoutAllViewAPI
)
from .controllers.user_status import UserStatusAPI

app_name = "user"

urlpatterns = [
    path("register/", UserRegistrationAPI.as_view(), name=input_fields.REGISTER),
    path("login/", UserLoginAPIView.as_view(), name=input_fields.LOGIN),
    path("login/verify/<str:endpoint_token>/", TwoFactorVerificationAPIView.as_view(), name='two-factor-verify'),
    path("resend-token/<str:endpoint_token>/", ResendTwoFactorTokenAPIView.as_view(), name='resent-two-factor-token'),
    path("logout/", LogoutViewAPI.as_view(), name=input_fields.LOGOUT),
    path("logoutall/", LogoutAllViewAPI.as_view(), name=input_fields.LOGOUTALL),
    path("change-avatar/", UserAvatarAPI.as_view(), name=input_fields.CHANGE_AVATAR),
    path("change-names/", UserNamesUpdateAPI.as_view(), name=input_fields.CHANGE_NAME),
    path("change-password/", UserPasswordUpdateAPI.as_view(), name=input_fields.CHANGE_PASSWORD),
    path("user-account/", UserAccountAPI.as_view(), name="user-account"),
    path("forgot-password/", SendForgotPasswordOTPAPIView.as_view(), name="forgot-password"),
    path("forgot-password/verify/<str:endpoint_token>/", PasswordResetOTPVerificationAPIView.as_view(), name="forgot-password-verify"),
    path("create-new-password/<str:endpoint_token>/", CreateNewPasswordTokenAPIView.as_view(), name="create-new-password"),
    path("whoami/", UserStatusAPI.as_view(), name="user-status"),


    path('<str:setting_name>/create/', UserSettingsToggleAPI.as_view(), name='user_settings_toggle'),
    path('lists/config/', UserSettingsListAPIView.as_view(), name='config-lists'),
    path('enable-2fa/', Enable2FAAPIView.as_view(), name='enable-2fa'),
]