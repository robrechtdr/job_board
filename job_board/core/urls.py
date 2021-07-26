from django.urls import path, include
from rest_framework import routers
from .views import (
    JobSearchView,
    JobApplicantsView,
    JobDetailView,
    JobApplyView,
    ProfessionalSearchView,
    api_root
)


urlpatterns = [
    path('v1', api_root),
    path('v1/job', JobSearchView.as_view(), name='job_search'),
    path('v1/job/<int:pk>', JobDetailView.as_view(), name='job_detail'),
    path('v1/job/<int:pk>/applicants', JobApplicantsView.as_view(), name='job_applicants'),
    path('v1/job/apply', JobApplyView.as_view(), name='job_apply'),
    path('v1/professional', ProfessionalSearchView.as_view(), name='professional_search'),
    path('v1/auth/', include('rest_framework.urls', namespace='rest_framework')),
]
