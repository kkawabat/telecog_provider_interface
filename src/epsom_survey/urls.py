"""
URL configuration for telecog_provider_interface project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from epsom_survey.views import epsom_run
from provider_portal.views import PatientList, PatientDetailView, patient_add, patient_delete, PatientAddView, AssessmentAddView, assessment_add, assessment_detail, assessment_run, assessment_edit

urlpatterns = [
    path('<slug:pk>', epsom_run, name='epsom-survey'),
]
