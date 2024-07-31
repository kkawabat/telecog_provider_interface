from django import forms
from django.forms import DateTimeInput
from django.shortcuts import get_object_or_404

from provider_portal.models import Assessment, Patient


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


class PatientAddForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
