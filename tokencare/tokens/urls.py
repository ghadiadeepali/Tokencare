from django.urls import path
from . import views  # or your specific view file

urlpatterns = [
    path("", views.list_tokens),
    path("update/<int:token_number>/", views.update_token_status),
    path("pending/", views.list_pending_tokens)]