from django.contrib import admin
from django.urls import path, re_path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/login/", views.login),
    path("api/signup/", views.signup),
    path("api/test_token/", views.test_token),
]
