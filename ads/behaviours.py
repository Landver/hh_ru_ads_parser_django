import uuid
from datetime import datetime

from django.db import models

from django.contrib.auth import get_user_model


related = '%(app_label)s_%(class)s_related'


class BaseInfo(models.Model):
    """An abstract base class model that provides common fields."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    created_date = models.DateTimeField(editable=False, blank=True, default=datetime.now)
    modified_date = models.DateTimeField(editable=False, blank=True, default=datetime.now)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                   null=True, blank=True, related_name=related + '_created_by')
    modified_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, 
                                    null=True, blank=True, default=None, related_name=related + '_modified_by')

    def __str__(self):
        return str(self.id)

    class Meta:
        abstract = True