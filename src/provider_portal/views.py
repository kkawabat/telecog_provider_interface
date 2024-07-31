from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from provider_portal.models import Patient, Assessment, AssessmentReport
from provider_portal.forms import AssessmentAddForm, PatientAddForm
from utils.twilio import send_sms


class PatientAddView(CreateView):
    model = Patient
    form_class = PatientAddForm


def patient_add(request):
    if request.method == 'POST':
        form = PatientAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient added successfully")
    return redirect('patient-list')


def patient_delete(request):
    if request.method == 'POST':
        form = PatientAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient added successfully")
    return redirect('patient-list')


class PatientDetailView(DetailView):
    model = Patient
    template_name = "provider_portal/patient_detail.html"
    slug_field = 'pid'
    slug_url_kwarg = 'pid'

    def get_context_data(self, **kwargs):
        patient = kwargs['object']
        context = super(PatientDetailView, self).get_context_data(**kwargs)
        context['scheduled_assessment_list'] = Assessment.objects.filter(patient__pid=patient.pid).exclude(status='Completed')
        context['assessment_history_list'] = Assessment.objects.filter(patient__pid=patient.pid).filter(status='Completed')
        context['report_list'] = []
        return context


class PatientList(ListView):
    model = Patient
    template_name = "provider_portal/patient_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AssessmentAddView(CreateView):
    model = Assessment
    form_class = AssessmentAddForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pid'] = context['view'].kwargs['pid']
        return context


def assessment_add(request, pid):
    if request.method == 'POST':
        form = AssessmentAddForm(request.POST)
        form.patient_pid = pid
        if form.is_valid():
            form.save()
            messages.success(request, "Assessment added successfully")
        else:
            messages.error(request, form.errors)
    return redirect('patient-detail', pid=pid)


def assessment_detail(request, pid, pk):

    pass


def assessment_run(request, pid, pk):
    assessment = get_object_or_404(Assessment, pk=pk)
    patient = get_object_or_404(Patient, pid=pid)

    if assessment.type == 'ePSOM':
        send_epsom_invite(request, patient, assessment)
        messages.success(request, f"epsom invite sent to {patient.full_name}")
    else:
        messages.error(request, "only epsom assessment is supported atm.")
    return redirect('patient-detail', pid=pid)


def send_epsom_invite(request, patient, assessment):
    epsom_survey_url = request.build_absolute_uri(reverse('epsom-survey', kwargs={'pk': assessment.pk}))
    text_message = f"Hello {patient.full_name} please click the link below to run the ePSOM survey {epsom_survey_url}"
    print(text_message)
    send_sms(str(patient.phone_number), text_message)


def assessment_edit(request, pid, pk):
    return redirect('patient-detail', pid=pid)


def assessment_delete(request, pid, pk):
    return redirect('patient-detail', pid=pid)
