from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from healthcare_ms.users.jwt import CustomTokenObtainPairView
from healthcare_ms.users.views import UserRegistrationView

app_name = "auth"

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
