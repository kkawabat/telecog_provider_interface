import uuid
from datetime import datetime

from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class Patient(models.Model):
    pid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=30)
    phone_number = PhoneNumberField(region='US')
    email = models.EmailField(max_length=254, blank=True)
    age = models.IntegerField()

    class Gender(models.TextChoices):
        MALE = 'm', 'Male'
        FEMALE = 'f', 'Female'
        OMIT = 'o', 'Prefer not to answer'

    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        default=Gender.OMIT
    )


class Assessment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField('scheduled date')

    survey_url = models.URLField()

    class Status(models.TextChoices):
        COMPLETED = 'Completed'
        INCOMPLETE = 'Incomplete'
        SCHEDULED = 'Scheduled'

    status = models.CharField(max_length=30, choices=Status.choices, default=Status.SCHEDULED)

    class AssessmentTypes(models.TextChoices):
        RDAC = 'rDAC'
        KINESIS = 'Kinesis Mobility Assessment'
        EPSOM = 'ePSOM'
        SPEECHVITALS = 'A2 Speech Vitals'
        QNRS = 'QNRs'

    type = models.CharField(max_length=30, choices=AssessmentTypes.choices)

    def save(self, *args, **kwargs):
        self.survey_url = reverse('epsom-survey', kwargs={'pk': self.pk})
        return super().save(*args, **kwargs)


class AssessmentData(models.Model):
    assessment = models.OneToOneField(Assessment, on_delete=models.CASCADE, primary_key=True)
    completion_date = models.DateTimeField(default=datetime.now())


class AssessmentReport(models.Model):
    assessment = models.OneToOneField(Assessment, on_delete=models.CASCADE, primary_key=True)
    name = models.TextField()
    url = models.URLField()
