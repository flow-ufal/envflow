import pandas as pd

from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from hydrocomp.series.flow import Flow
from odm2admin.models import Featureactions, Samplingfeatures, Timeseriesresultvalues

from iha.forms import ParcialForm


def choice(type_threshold, type_criterion, type_event):

    type_threshold_choice = {'1': 'stationary', '2': 'events_by_year'}

    type_criterion_choice = {'1': 'median', '2': 'autocorrelation'}

    type_event_choice = {'1': 'flood', '2': 'drought'}
    return type_threshold_choice[type_threshold], type_criterion_choice[type_criterion], type_event_choice[type_event]


class IndexView(CreateView):

    template_name = 'iha/index.html'
    form_class = ParcialForm

    def get(self, request, *args, **kwargs):
        month_name = {1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril', 5: 'maio', 6: 'junho', 7: 'julho',
                      8: 'agosto', 9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'}

        sampling = Samplingfeatures.objects.get(samplingfeaturecode=kwargs['code'])
        featureaction = Featureactions.objects.filter(samplingfeatureid=sampling.samplingfeatureid,
                                                      action__method__methodcode=123)[0]

        data = Timeseriesresultvalues.objects.filter(
            resultid__resultid__featureactionid_id=featureaction.featureactionid).values_list('datavalue',
                                                                                              'valuedatetime')
        try:
            data = pd.DataFrame(list(data))
            data_df = pd.DataFrame(data[0].values, index=data[1].values, columns=[sampling.samplingfeaturename])
            flow = Flow(data_df, station=sampling.samplingfeaturename)
            year_water = 'Mês de ínicio do ano hidrológico: '+month_name[flow.month_start_year_hydrologic()[0]].title()
        except KeyError:
            year_water = None

        self.form_class.code = sampling.samplingfeatureid

        form = self.form_class()

        context = {"sampling": sampling,
                   "year_water": year_water,
                   "form": form}

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        self.template_name = 'iha/results.html'

        return render(request, self.template_name)


class ResultsView(TemplateView):

    template_name = 'iha/results.html'


index = IndexView.as_view()
results = ResultsView.as_view()
