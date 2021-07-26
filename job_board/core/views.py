from django.shortcuts import render
from django.http import HttpResponse, Http404

from rest_framework import generics, permissions, filters, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response

from .errors import ImproperCallConditionError
from .models import Job, Professional, Application
from .permissions import IsProfessional, IsBusiness
from .serializers import JobSerializer, ProfessionalSerializer, ApplicationSerializer


class JobSearchView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering = ['created']


class ProfessionalSearchView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering = ['created']


class JobApplyView(APIView):
    """
    As a professional, apply for a given job.
    """
    permission_classes = [IsProfessional]

    def post(self, request, format=None):
        if not request.data.get('job'):
            return Response("Supply a 'job' (id) payload", status=status.HTTP_400_BAD_REQUEST)

        job = Job.objects.get(id=request.data['job'])
        user = request.user
        try:
            application = user.professional.apply(job)
        except ImproperCallConditionError as error:
            return Response(error, status=status.HTTP_403_FORBIDDEN)

        serializer = ApplicationSerializer(application)
        # https://www.django-rest-framework.org/api-guide/serializers/#saving-instances
        # We don't call serlializer.save() here as creation already happened.
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Ideally we do AllowAll but with custom serializer only exposing certain fields
# Keeping it simple for now.
class JobDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Job.objects.all()
    serializer_class = JobSerializer


class JobApplicantsView(APIView):
    """
    As a business user, list all applicants who applied for a given job.
    """
    permission_classes = [IsBusiness]

    # https://www.django-rest-framework.org/tutorial/3-class-based-views/#rewriting-our-api-using-class-based-views
    def get_object(self, pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        job = self.get_object(pk)
        professionals = job.get_applicants()
        serializer = ProfessionalSerializer(professionals, many=True)
        return Response(serializer.data)
