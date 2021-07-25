from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Professional, Business, Job, Application


class ProfessionalSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professional
        fields = '__all__'


class BusinessSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
