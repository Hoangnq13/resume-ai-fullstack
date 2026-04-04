from django.urls import path
from . import views

urlpatterns = [
    path('parse-resume/', views.parse_resume_api, name='parse_resume_api'),
    path('candidates/', views.get_candidates_api, name='get_candidates_api'),
]