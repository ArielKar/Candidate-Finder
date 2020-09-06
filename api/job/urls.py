from django.urls import path

from .views import get_stats, update_status

urlpatterns = [
    path('<str:job_id>/stats', get_stats),
    path('<str:job_id>/status', update_status)
]
