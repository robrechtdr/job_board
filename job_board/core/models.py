from django.db import models


class Professional(models.Model):
    full_name = models.CharField(max_length=254)
    email = models.EmailField(max_length=254)
    title = models.CharField(max_length=254)
    #daily_rate_range
    #availability
    #location

    def __str__(self):
        return self.full_name


class Business(models.Model):
    company_name = models.CharField(max_length=254)
    website = models.URLField(max_length=254)

    def __str__(self):
        return self.company_name


class Job(models.Model):
    title = models.CharField(max_length=254)
    #daily_rate_range
    #availability
    #location
    #skills

    def __str__(self):
        return self.title
