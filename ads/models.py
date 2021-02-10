from django.db import models

# Create your models here.


class Ad(models.Model):
    title = models.CharField(max_length=64)
    company_name = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    work_experience = models.CharField(max_length=20)
    employment_type = models.CharField(max_length=32)
    schedule = models.CharField(max_length=16)
    description = models.TextField()
    salary = models.IntegerField(null=True, blank=True)
    phone = models.CharField(null=True, blank=True)
