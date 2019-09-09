from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.contrib.gis.geos import Point
from .forms import SamplingFeaturesForm
from odm2admin.models import Samplingfeatures, Timeseriesresultvalues, Featureactions, CvSamplingfeaturetype
import pandas as pd
from hydrocomp.series.flow import Flow
import plotly.offline as opy


# Create your views here.
class IndexView(CreateView):

    model = Samplingfeatures
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):

        samplingfeatures = Samplingfeatures.objects.all()
        features = Featureactions.objects.all()

        context = {'samplingfeatures': samplingfeatures,
                   'features': features}

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

        data, fig = flow.hydrogram()

        hydrogram = opy.plot(data,  include_plotlyjs=True, output_type='div', auto_open=False)

        context = {"featureaction": featureaction,
                   'hydrogram': hydrogram}

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        stations = Samplingfeatures.objects.all()

        context = {'stations': stations}

        return render(request, self.template_name, context)


class FeatureActionsView(FormView):

    model = Samplingfeatures
    form_class = SamplingFeaturesForm
    template_name = 'feature.html'
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        post = request.POST
        name = post['samplingfeaturename']
        code = post['samplingfeaturecode']
        feature_type = CvSamplingfeaturetype.objects.get(pk=post['sampling_feature_type'])
        lat = post['lat']
        lon = post['lon']
        point = Point(float(lat), float(lon))

        sampling = Samplingfeatures(samplingfeaturecode=code, samplingfeaturename=name, featuregeometry=point,
                                    sampling_feature_type=feature_type)

        sampling.save()
        return redirect(self.success_url)


index = IndexView.as_view()
results = ResultsView.as_view()
featureaction = FeatureActionsView.as_view()
