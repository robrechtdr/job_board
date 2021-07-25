from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from multiselectfield import MultiSelectField


AVAILABILITY_CHOICES = [
    ('PW 1-2d', '1-2 days pw'),
    ('PW 3-4d', '3-4 days pw'),
    ('PW 5d', 'Full time')
]

LOCATION_CHOICES = [
    ('ONSITE', 'on-site'),
    ('REMOTE', 'remote'),
    ('ONSITE AND REMOTE', 'on-site & remote')
]


# Recommended to create custom user even if no immediate need to
# define additional fields as huge pain later otherwise:
# https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
class User(AbstractUser):
    pass

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Professional(models.Model):
    # https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#extending-the-existing-user-model
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=254)
    daily_rate = models.IntegerField(null=True)
    daily_rate_flexibility = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    # https://stackoverflow.com/questions/27440861/django-model-multiplechoice
    availability = MultiSelectField(choices=AVAILABILITY_CHOICES)
    location = MultiSelectField(choices=LOCATION_CHOICES)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.full_name


class Business(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=254)
    website = models.URLField(max_length=254)
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.company_name


class Job(models.Model):
    title = models.CharField(max_length=254)
    daily_rate = models.IntegerField(null=True)
    daily_rate_flexibility = models.DecimalField(max_digits=3, decimal_places=2, null=True)
    availability = MultiSelectField(choices=AVAILABILITY_CHOICES)
    location = MultiSelectField(choices=LOCATION_CHOICES)
    skills = models.CharField(max_length=500) # Assuming comma separated for now
    posted_by = models.ForeignKey(
            'Business',
            on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


class Application(models.Model):
    job = models.ForeignKey(
        'Job',
        on_delete=models.CASCADE,
    )
    applicant = models.ForeignKey(
        'Professional',
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Application from {self.applicant.user.full_name} as {job.title}"
