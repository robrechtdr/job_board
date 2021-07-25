from django.shortcuts import render
from rest_framework import generics, permissions, filters, viewsets
from .models import Job, Professional
from .serializers import JobSerializer, ProfessionalSerializer

class JobListView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']


class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer
    permission_classes = [permissions.IsAuthenticated]
