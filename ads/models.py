from django.db import models
from .behaviours import BaseInfo


class Ad(BaseInfo):
    title = models.CharField(max_length=128)
    company_name = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    salary = models.IntegerField(null=True, blank=True)
    work_experience = models.CharField(max_length=32)
    employment_type = models.CharField(max_length=48)
    description = models.TextField()
    vacancy_url = models.CharField(max_length=128, null=True, blank=True)
    phone = models.CharField(max_length=32, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)