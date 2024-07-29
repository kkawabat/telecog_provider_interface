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

from provider_portal.views import PatientList, PatientDetailView, patient_add, patient_delete, PatientAddView, AssessmentAddView, assessment_add, assessment_detail, assessment_run, assessment_edit, assessment_delete

urlpatterns = [
    path('patients/', PatientList.as_view(), name='patient-list'),
    path('patients/add_form', PatientAddView.as_view(), name='patient-add-form'),
    path('patients/add', patient_add, name='patient-add'),
    path('patients/<slug:pid>', PatientDetailView.as_view(), name='patient-detail'),
    path('patients/<slug:pid>/delete', patient_delete, name='patient-delete'),
    path('patients/<slug:pid>/assessment/add_form', AssessmentAddView.as_view(), name='assessment-add-form'),
    path('patients/<slug:pid>/assessment/add', assessment_add, name='assessment-add'),
    path('patients/<slug:pid>/assessment/<slug:pk>', assessment_detail, name='assessment-detail'),
    path('patients/<slug:pid>/assessment/<slug:pk>/run', assessment_run, name='assessment-run'),
    path('patients/<slug:pid>/assessment/<slug:pk>/edit', assessment_edit, name='assessment-edit'),
    path('patients/<slug:pid>/assessment/<slug:pk>/edit', assessment_delete, name='assessment-delete'),
]
