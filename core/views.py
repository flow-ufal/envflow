from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, resolve
from django.views.generic import CreateView
from django.contrib.gis.geos import Point

from core.forms import UnitsForm, ResultsForm, ProcessingLevelsForm, FeatureAcrionForm, ActionsForm, MethodsForm
from .forms import SamplingFeaturesForm, TimeResultsSeriesValuesForm, OrganizationsForm, TimeSeriesResultsForm
from odm2admin.models import Samplingfeatures, Timeseriesresultvalues, Featureactions, CvSamplingfeaturetype, \
    Organizations, Units, Timeseriesresults, Results, Processinglevels, Actions, Methods
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


class ResultStationView(CreateView):

    template_name = 'result_station.html'

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


class SamplingFeaturesView(LoginRequiredMixin, CreateView):

    model = Samplingfeatures
    form_class = SamplingFeaturesForm
    template_name = 'sampling.html'
    success_url = reverse_lazy('core:index')

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


class OrganizationsView(LoginRequiredMixin, CreateView):

    model = Organizations
    form_class = OrganizationsForm
    template_name = 'organizations.html'
    success_url = reverse_lazy('index')


class TimeResultsSeriesValuesView(LoginRequiredMixin, CreateView):

    model = Timeseriesresultvalues
    form_class = TimeResultsSeriesValuesForm
    template_name = 'time_serie_values.html'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):

        context = {}
        if 'code' in kwargs.keys():
            sampling = Samplingfeatures.objects.get(samplingfeaturecode=kwargs['code'])
            context["sampling"] = sampling

        context["form"] = self.form_class

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        post = request.POST

        sampling = Samplingfeatures.objects.get(samplingfeaturecode=kwargs['code'])

        context = {"sampling": sampling}

        return render(request, self.template_name, context=context)


class UnitsView(LoginRequiredMixin, CreateView):

    model = Units
    form_class = UnitsForm
    template_name = 'units.html'
    success_url = reverse_lazy('core:index')

    def get(self, request, *args, **kwargs):
        url = resolve('/'+'/'.join(request.META.get("HTTP_REFERER").split('/')[3:]))
        self.success_url = reverse_lazy('{}:{}'.format(url.app_name, url.url_name))
        context = {'form': self.form_class}
        return render(request, self.template_name, context=context)


class TimeSeriesResultView(LoginRequiredMixin, CreateView):

    model = Timeseriesresults
    form_class = TimeSeriesResultsForm
    template_name = 'time_serie_result.html'
    success_url = reverse_lazy('core:index')


class DataResultsView(LoginRequiredMixin, CreateView):

    model = Results
    template_name = 'data_results.html'
    form_class = ResultsForm
    success_url = reverse_lazy('core:index')


class ProcessingLevelsView(LoginRequiredMixin, CreateView):

    model = Processinglevels
    template_name = 'processing_level.html'
    form_class = ProcessingLevelsForm
    success_url = reverse_lazy('core:index')


class FeatureActionView(LoginRequiredMixin, CreateView):

    model = Featureactions
    form_class = FeatureAcrionForm
    template_name = 'feature_action.html'
    success_url = reverse_lazy('core:index')


class ActionView(LoginRequiredMixin, CreateView):

    model = Actions
    form_class = ActionsForm
    template_name = 'action.html'
    success_url = reverse_lazy('core:index')


class MethodsView(LoginRequiredMixin, CreateView):

    model = Methods
    form_class = MethodsForm
    template_name = 'method.html'
    success_url = reverse_lazy('core:index')


index = IndexView.as_view()
result_station = ResultStationView.as_view()
samplingfeatures = SamplingFeaturesView.as_view()
time_serie_values = TimeResultsSeriesValuesView.as_view()
units = UnitsView.as_view()
time_serie_result = TimeSeriesResultView.as_view()
data_results = DataResultsView.as_view()
processing_level = ProcessingLevelsView.as_view()
feature_action = FeatureActionView.as_view()
action = ActionView.as_view()
method = MethodsView.as_view()
organization = OrganizationsView.as_view()
