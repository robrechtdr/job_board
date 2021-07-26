import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from multiselectfield import MultiSelectField
from .errors import ImproperCallConditionError


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

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def is_professional(self):
        if hasattr(self, 'professional'):
            return True
        else:
            return False

    def is_business(self):
        if hasattr(self, 'business'):
            return True
        else:
            return False


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

    def apply(self, job):
        if Application.objects.filter(applicant=self).exists():
            # I don't really like this error here; but we need to mark it
            # somehow to be able to raise a client error instead of a 500.
            # when used from a view.
            raise ImproperCallConditionError(f'{self} already applied for {job} job')

        today = datetime.date.today()
        applications = Application.objects.filter(job=job, created__date=today)
        if applications.count() >= 5:
            raise ImproperCallConditionError(f'Maximum applications reached for today on {job} job')

        application = Application(job=job, applicant=self)
        application.save()
        return application


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

    def get_applicants(self, as_queryset=False):
        job_apps = Application.objects.filter(job=self)
        applicant_ids = [job_app.applicant.id for job_app in job_apps]
        applicants = Professional.objects.filter(pk__in=applicant_ids)
        if as_queryset:
            return applicants
        else:
            return list(applicants)


class Application(models.Model):
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    applicant = models.ForeignKey('Professional', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"by {self.applicant.user.full_name} for {self.job.title} job"
