from django.urls import path, include
from rest_framework import routers
from .views import JobListView, ProfessionalViewSet


router = routers.DefaultRouter()
router.register(r'professionals', ProfessionalViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('jobs/', JobListView.as_view()),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
]
