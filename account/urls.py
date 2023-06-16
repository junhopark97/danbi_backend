from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegisterView, UserLoginView

router = DefaultRouter()
# router.register()

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    # path('verify/', UserVerifyView.as_view(), name='verify'),
]
