import uuid

from django import forms
from django.db import models
from django.db.models import Model
from django.forms import DateTimeInput
from django.shortcuts import get_object_or_404
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class Patient(Model):
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


class PatientAddForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'


class Assessment(Model):
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


class AssessmentAddForm(forms.ModelForm):
    scheduled_date = forms.DateTimeField(widget=DateTimeInput(attrs={'class': "datetime-input"}),
                                         input_formats=['%Y/%m/%d %H:%M'])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patient_pid = None

    class Meta:
        model = Assessment
        fields = ['type', 'scheduled_date']

    def save(self, commit=True):
        assessment = super(AssessmentAddForm, self).save(commit=False)
        assessment.Status = 'Scheduled'
        assessment.patient = get_object_or_404(Patient, pk=self.patient_pid)
        if commit:
            assessment.save()
        return assessment


class AssessmentReport(Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.TextField()
    url = models.URLField()
