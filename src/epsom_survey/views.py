from django.shortcuts import render
from django.views.generic import CreateView

from epsom_survey.models import EpsomSurvey, EPSOM


class AssessmentAddView(CreateView):
    model = EPSOM
    template_name = 'epsom_survey/epsom_survey.html'
    form_class = EpsomSurvey

    def get_form_kwargs(self):
        kwargs = super(AssessmentAddView, self).get_form_kwargs()
        kwargs['pk'] = self.kwargs.get('pk')
        return kwargs


def epsom_run(request, pk):
    form = EpsomSurvey()
    context = {'form': form}
    return render(request, 'epsom_survey/epsom_survey.html', context=context)
