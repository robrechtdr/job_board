from django.urls import path, include
from rest_framework import routers
from .views import (
    JobSearchView,
    JobApplicantsView,
    JobDetailView,
    JobApplyView,
    ProfessionalSearchView,
)


urlpatterns = [
    path('v1/job', JobSearchView.as_view()),
    path('v1/job/<int:pk>', JobDetailView.as_view()),
    path('v1/job/<int:pk>/applicants', JobApplicantsView.as_view()),
    path('v1/job/apply', JobApplyView.as_view()),
    path('v1/professional', ProfessionalSearchView.as_view()),
    path('v1/auth', include('rest_framework.urls', namespace='rest_framework')),
]
