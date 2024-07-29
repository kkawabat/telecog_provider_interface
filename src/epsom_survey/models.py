import uuid

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.forms import ModelForm

from provider_portal.models import Patient


class EPSOM(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    daily_tasks_1 = models.JSONField(default=list)
    daily_tasks_2 = models.JSONField(default=list)
    daily_tasks_3 = models.JSONField(default=list)
    daily_tasks_4 = models.JSONField(default=list)
    daily_tasks_5 = models.JSONField(default=list)
    daily_tasks_6 = models.JSONField(default=list)
    daily_tasks_7 = models.JSONField(default=list)
    daily_tasks_8 = models.TextField()
    daily_tasks_9 = models.TextField()
    daily_tasks_10 = models.TextField()
    daily_tasks_11 = models.TextField()
    daily_tasks_12 = models.TextField()
    daily_tasks_13 = models.TextField()


class EpsomSurvey(ModelForm):
    class Meta:
        model = EPSOM
        fields = '__all__'
