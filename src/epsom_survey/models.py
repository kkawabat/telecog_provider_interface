from django import forms
from django.db import models, transaction
from django.shortcuts import get_object_or_404

from provider_portal.models import AssessmentData, Assessment

SPECTRUM_CHOICES = {
    "NOTATALL": "Not at all",
    "SLIGHT": "Slightly",
    "SOMEWHAT": "Somewhat",
    "FAIRLY": "Fairly",
    "COMPLETELY": "Completely",
}

YN_CHOICES = {
    "YES": "Yes",
    "NO": "No",
}


class EpsomSurvey(AssessmentData):
    epsom_q1 = models.JSONField(default=list)
    epsom_q2 = models.JSONField(default=list)
    epsom_q3 = models.JSONField(default=list)
    epsom_q4 = models.JSONField(default=list)
    epsom_q5 = models.JSONField(default=list)
    epsom_q6 = models.JSONField(default=list, blank=True, null=True)
    epsom_q7 = models.JSONField(default=list)
    epsom_q8 = models.TextField()
    epsom_q9 = models.TextField()
    epsom_q10 = models.TextField()
    epsom_q11 = models.TextField()
    epsom_q12 = models.TextField()
    epsom_q13 = models.TextField()


class EpsomSurveyForm(forms.ModelForm):
    epsom_q8 = forms.Select(choices=SPECTRUM_CHOICES)
    epsom_q9 = forms.Select(choices=SPECTRUM_CHOICES)
    epsom_q10 = forms.Select(choices=SPECTRUM_CHOICES)
    epsom_q11 = forms.Select(choices=SPECTRUM_CHOICES)
    epsom_q12 = forms.Select(choices=SPECTRUM_CHOICES)
    epsom_q13 = forms.Select(choices=YN_CHOICES)

    class Meta:
        model = EpsomSurvey
        fields = '__all__'
        widgets = {
            'epsom_q1': forms.TextInput(),
            'epsom_q2': forms.TextInput(),
            'epsom_q3': forms.TextInput(),
            'epsom_q4': forms.TextInput(),
            'epsom_q5': forms.TextInput(),
            'epsom_q6': forms.TextInput(attrs={'required': False}),
            'epsom_q7': forms.TextInput(),
            'epsom_q8': forms.TextInput(),
            'epsom_q9': forms.TextInput(),
            'epsom_q10': forms.TextInput(),
            'epsom_q11': forms.TextInput(),
            'epsom_q12': forms.TextInput(),
            'epsom_q13': forms.TextInput(),
        }

    def save(self, commit=True):
        epsom_model = super(EpsomSurveyForm, self).save(commit=False)
        if commit:
            with transaction.atomic():
                epsom_model.assessment.status = 'Completed'
                epsom_model.assessment.save()
                epsom_model.save()
        return epsom_model
