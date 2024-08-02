import os
from os.path import join, abspath, dirname

import pdfkit
from django import forms
from django.db import models, transaction
from django.shortcuts import render
from django.template.loader import render_to_string
from django.templatetags.static import static

import epsom_survey
from provider_portal.models import AssessmentData
from telecog_provider_interface.settings import BASE_DIR

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

    def generate_result_html(self, request=None):
        context = {'wkhtmltopdf': False,
                   'first_name': self.assessment.patient.full_name.split()[0],
                   'important_areas': list(zip(list(self.epsom_q7), [self.epsom_q8, self.epsom_q9, self.epsom_q10, self.epsom_q11, self.epsom_q12, self.epsom_q13]))}

        if request is None:
            return render_to_string('epsom_survey/epsom_result.html', context=context)

        return render(request, 'epsom_survey/epsom_result.html', context=context)

    def generate_result_pdf(self):
        config = pdfkit.configuration(wkhtmltopdf=os.environ['WKHTMLTOPDF_PATH'])
        html_str = self.generate_result_html()
        css_path = 'file:///' + join(dirname(abspath(epsom_survey.__file__)), 'static', 'epsom_survey', 'epsom_result.css')
        html_str = html_str.replace('/static/epsom_survey/epsom_result.css', css_path)
        css_path = 'file:///' + join(dirname(abspath(epsom_survey.__file__)), 'static', 'epsom_report')
        html_str = html_str.replace('/static/epsom_report/', css_path + '\\')
        css_path = 'file:///' + join(dirname(dirname(abspath(epsom_survey.__file__))), 'static', 'main.css')
        html_str = html_str.replace('/static/main.css', css_path)
        css_path = 'file:///' + join(dirname(dirname(abspath(epsom_survey.__file__))), 'static', 'logo2.png')
        html_str = html_str.replace('/static/logo2.png', css_path)
        css_path = 'file:///' + join(dirname(dirname(abspath(epsom_survey.__file__))), 'static', 'icon.svg')
        html_str = html_str.replace('/static/icon.svg', css_path)
        print(html_str)
        pdf_file = pdfkit.from_string(html_str, False, configuration=config, options={"enable-local-file-access": ""})
        return pdf_file


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
