from django.urls import path

from . import views

urlpatterns = [
    path("callback/", views.GoogleLoginApi.as_view()),
    path("redirect/", views.GoogleLoginRedirectApi.as_view(), name="google-login-redirect")
]