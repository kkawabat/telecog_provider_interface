from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView

from epsom_survey.models import EpsomSurvey, EpsomSurveyForm
from provider_portal.models import Assessment


class EpsomSurveyView(CreateView):
    model = EpsomSurvey
    template_name = 'epsom_survey/epsom_survey.html'
    form_class = EpsomSurveyForm

    def get_context_data(self, **kwargs):
        context = super(EpsomSurveyView, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


def epsom_submit(request, pk):
    if request.method == 'POST':
        a = request.POST.copy()
        a['assessment'] = get_object_or_404(Assessment, pk=pk)
        form = EpsomSurveyForm(a)
        if form.is_valid():
            form.save()
            messages.success(request, "Epsom submitted successfully")
        else:
            messages.error(request, str(form.errors))
    return render(request, 'epsom_survey/epsom_completion_screen.html')
