from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from rest_framework.authtoken.models import Token

from core.models import (Professional, Business, Job, Application,
    AVAILABILITY_CHOICES, LOCATION_CHOICES)


User = get_user_model()


class Command(BaseCommand):
    def handle(self, **options):
        """
        Populate dummy db entries for convenience.
        """
        try:
            # Admin
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@gmail.com',
                password='admin',
            )
            print(f'Created {admin}')

            admin_token = Token.objects.create(user=admin)
            print(f'Created token {admin_token} for admin')
            print()


            # Professional 1
            professional_user1 = User.objects.create_user(
                username='fionasmith',
                email='fiona.smith@gmail.com',
                password='fionasmith',
                first_name='Fiona',
                last_name='Smith'
            )
            professional_user1_token = Token.objects.create(user=professional_user1)

            professional1, _ = Professional.objects.get_or_create(
                user=professional_user1,
                title='Recruiter',
                daily_rate=350,
                daily_rate_flexibility=0.3,
                availability=f'{AVAILABILITY_CHOICES[0][0]}, {AVAILABILITY_CHOICES[1][0]}',
                location=f'{LOCATION_CHOICES[0][0]}'
            )
            print(f'Created professional user: {professional_user1}')
            print(f'Created professional profile: {professional1}')
            print(f'Created token {professional_user1_token} for {professional_user1}')
            print()


            # Professional 2
            professional_user2 = User.objects.create_user(
                username='kimjohnson',
                email='kim.johnson@gmail.com',
                password='kimjohnson',
                first_name='Kim',
                last_name='Johnson'
            )
            professional_user2_token = Token.objects.create(user=professional_user2)

            professional2, _ = Professional.objects.get_or_create(
                user=professional_user2,
                title='Talent Consultant',
                daily_rate=450,
                daily_rate_flexibility=0.2,
                availability=f'{AVAILABILITY_CHOICES[0][0]}',
                location=f'{LOCATION_CHOICES[1][0]}, {LOCATION_CHOICES[2][0]}'
            )
            print(f'Created professional user: {professional_user2}')
            print(f'Created professional profile: {professional2}')
            print(f'Created token {professional_user2_token} for {professional_user2}')
            print()


            # Business 1
            business_user1 = User.objects.create_user(
                username='danaearl',
                email='dana.earl@gmail.com',
                password='danaearl',
                first_name='Dana',
                last_name='Earl'
            )
            business_user1_token = Token.objects.create(user=business_user1)

            business1, _ = Business.objects.get_or_create(
                user=business_user1,
                company_name='ExecHire',
                website='www.exechire.com'
            )
            print(f'Created business user: {business_user1}')
            print(f'Created business profile: {business1}')
            print(f'Created token {business_user1_token} for {business_user1}')
            print()

            # Job 1
            job1, _ = Job.objects.get_or_create(
                title='Senior HR Manager',
                daily_rate=325,
                daily_rate_flexibility=0.1,
                availability=f'{AVAILABILITY_CHOICES[0][0]}',
                location=f'{LOCATION_CHOICES[1][0]}',
                skills='Employee engagement, Employee onboarding, Employee contracts',
                posted_by=business1
            )
            print(f'Created job: {job1}')
            print()

            job2, _ = Job.objects.get_or_create(
                title='Head of Talent',
                daily_rate=600,
                daily_rate_flexibility=0.2,
                availability=f'{AVAILABILITY_CHOICES[1][0]}',
                location=f'{LOCATION_CHOICES[1][0]}',
                skills='Technical recruitment, Managing talent, Managing agencies',
                posted_by=business1
            )
            print(f'Created job: {job2}')
            print('\n')

            print("Dummy population finished!")
        except IntegrityError:
            print("Skipping dummy population as already populated.")
