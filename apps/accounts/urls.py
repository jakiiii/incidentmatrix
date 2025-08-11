from django.urls import path
from apps.accounts.views import (
    LoginView, LogoutView, CustomPasswordChangeView, ProfileView, PermissionDeniedView
)

app_name = "accounts"


urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('password-changed/', CustomPasswordChangeView.as_view(), name='password_changed'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('permission-denied/', PermissionDeniedView.as_view(), name='permission_denied'),
]
