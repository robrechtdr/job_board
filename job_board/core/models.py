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


class Professional(models.Model):
    full_name = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    title = models.CharField(max_length=254)
    daily_rate = models.IntegerField(null=True)
    daily_rate_flexibility = models.IntegerField(null=True)
    # https://stackoverflow.com/questions/27440861/django-model-multiplechoice
    availability = MultiSelectField(choices=AVAILABILITY_CHOICES)
    location = MultiSelectField(choices=LOCATION_CHOICES)

    def __str__(self):
        return self.full_name


class Business(models.Model):
    company_name = models.CharField(max_length=254)
    website = models.URLField(max_length=254)

    def __str__(self):
        return self.company_name


class Job(models.Model):
    title = models.CharField(max_length=254)
    daily_rate = models.IntegerField(null=True)
    daily_rate_flexibility = models.IntegerField(null=True)
    availability = MultiSelectField(choices=AVAILABILITY_CHOICES)
    location = MultiSelectField(choices=LOCATION_CHOICES)
    #skills
    posted_by = models.ForeignKey(
            'Business',
            on_delete=models.CASCADE,
    )

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

    def __str__(self):
        return f"Application from {self.applicant.full_name} as {job.title}"
