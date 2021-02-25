import uuid

from django.db import models


related = '%(app_label)s_%(class)s_related'


class BaseInfo(models.Model):
    """An abstract base class model that provides common fields."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    created_date = models.DateTimeField(auto_now_add=True, editable=False, blank=True)
    modified_date = models.DateTimeField(auto_now_add=True, editable=False, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True


class Ad(BaseInfo):
    title = models.CharField(max_length=128)
    company_name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    salary = models.IntegerField(null=True, blank=True)
    work_experience = models.CharField(max_length=64, null=True, blank=True)
    employment_type = models.CharField(max_length=48, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    vacancy_url = models.CharField(max_length=254, null=True, blank=True, unique=True)
    phone = models.CharField(max_length=64, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    parsed = models.BooleanField(default=False)
    state = models.CharField(max_length=64, default='normal')
