from django.urls import path
from .views import LoginView, Verify2FAView, RegisterView, UserUpdateView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('verify-2fa/', Verify2FAView.as_view(), name='verify-2fa'),
    path('register/', RegisterView.as_view(), name='register'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='update'),
]
