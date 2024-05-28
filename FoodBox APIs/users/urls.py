from django.urls import path, include
from users.views import Register, LoginView, TokenAuthenticationView, ChangePassword, ForgotPasswordView, FOBListView
from rest_framework.routers import DefaultRouter
from django.urls import re_path
# router = DefaultRouter()
# router.register(r'feedback', FeedbackViewSet)

urlpatterns = [
    re_path(r'^register/?$', Register.as_view(), name='register'),
    re_path(r'^login/?$', LoginView.as_view(), name='login'),
    re_path(r'^authenticate/?$', TokenAuthenticationView.as_view(),
            name='authenticate'),
    re_path(r'^change_password/?$', ChangePassword.as_view(),
            name='change_password'),
    re_path(r'^forgot/?$', ForgotPasswordView.as_view(),
            name='forgot'),
    path('users/<str:fieldName>/<str:username>/',
         FOBListView.as_view(), name='billing_address'),
]
