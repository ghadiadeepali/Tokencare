from django.urls import path
from . import views  # or your specific view file

urlpatterns = [
    path("", views.list_tokens)]