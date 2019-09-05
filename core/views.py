from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from odm2admin.models import Samplingfeatures, Timeseriesresultvalues, Featureactions
import pandas as pd
from hydrocomp.series.flow import Flow
import plotly.offline as opy


# Create your views here.
class IndexView(CreateView):

    model = Samplingfeatures
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):

        featureaction = Featureactions.objects.all()
        context = {'feactureaction': featureaction}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print('aqui')


class ResultsView(CreateView):

    template_name = 'results.html'

    def get(self, request, *args, **kwargs):

        featureaction = Featureactions.objects.get(pk=kwargs['code'])
        data = Timeseriesresultvalues.objects.filter(
            resultid__resultid__featureactionid_id=featureaction.featureactionid).values_list('datavalue',
                                                                                              'valuedatetime')
        station = featureaction.samplingfeatureid.samplingfeaturename

        dic = {'Data': [], station: []}
        for i in data:
            dic['Data'].append(i[1])
            dic[station].append(i[0])
        data_flow = pd.DataFrame(dic, index=dic['Data'], columns=[station])
        flow = Flow(data=data_flow, source=station)
        print(flow)
        data, fig = flow.plot_hydrogram()
        hydrogram = opy.plot(data, auto_open=False, output_type='div')

        context = {"featureaction": featureaction,
                   'hydrogram': hydrogram}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        stations = Samplingfeatures.objects.all()

        context = {'stations': stations}

        return render(request, self.template_name, context)


index = IndexView.as_view()
results = ResultsView.as_view()
