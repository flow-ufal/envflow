import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, resolve
from django.views.generic import CreateView
from django.contrib.gis.geos import Point

from core.forms import UnitsForm, ResultsForm, ProcessingLevelsForm, FeatureAcrionForm, ActionsForm, MethodsForm, \
    ActionMultiForm, VariablesForm
from envflow.settings import MEDIA_ROOT
from .forms import SamplingFeaturesForm, TimeResultsSeriesValuesForm, OrganizationsForm, TimeSeriesResultsForm
from odm2admin.models import Samplingfeatures, Timeseriesresultvalues, Featureactions, CvSamplingfeaturetype, \
    Organizations, Units, Timeseriesresults, Results, Processinglevels, Actions, Methods, CvCensorcode, CvQualitycode, \
    Variables
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
        flow = Flow(data=data_flow, station=station)
        fig_hydro, data_hydro = flow.hydrogram()
        hydrogram = opy.plot(fig_hydro,  include_plotlyjs=True, output_type='div', auto_open=False)

        fig_hydro_by_year, data_hydro_by_year = flow.hydrogram_year()
        hydro_by_year = opy.plot(fig_hydro_by_year, include_plotlyjs=True, output_type='div', auto_open=False)

        month = flow.get_month_name()
        q710 = flow.flow_min('q710')

        context = {"featureaction": featureaction,
                   'hydrogram': hydrogram,
                   'hydro_by_year': hydro_by_year,
                   'month': month,
                   'mean': '{:.3f}'.format(flow.mean()[0]),
                   'q95': '{:.3f}'.format(flow.quantile(0.05)[0]),
                   'min': '{:.3f}'.format(flow.data.min().values[0]),
                   'max': '{:.3f}'.format(flow.data.max().values[0]),
                   'q710': '{:.3f}'.format(q710)
                   }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        stations = Samplingfeatures.objects.all()

        context = {'stations': stations}

        return render(request, self.template_name, context)


class AddSamplingFeaturesView(LoginRequiredMixin, CreateView):

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


class AddOrganizationsView(LoginRequiredMixin, CreateView):

    model = Organizations
    form_class = OrganizationsForm
    template_name = 'organizations.html'
    success_url = reverse_lazy('core:index')


class AddTimeResultsSeriesValuesView(LoginRequiredMixin, CreateView):

    model = Timeseriesresultvalues
    form_class = TimeResultsSeriesValuesForm
    template_name = 'time_serie_values.html'
    success_url = reverse_lazy('core:index')

    def get(self, request, *args, **kwargs):

        context = {}
        if 'code' in kwargs.keys():
            sampling = Samplingfeatures.objects.get(samplingfeaturecode=kwargs['code'])
            context["sampling"] = sampling

        context["form"] = self.form_class

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        post = request.POST
        file = request.FILES['File']

        sampling = Samplingfeatures.objects.get(samplingfeaturecode=kwargs['code'])

        path = default_storage.save('data_file/%s' % file.name, file)
        file = os.path.abspath(os.path.join(MEDIA_ROOT, path))

        result = Timeseriesresults.objects.get(pk=post['resultid'])
        censor = CvCensorcode.objects.get(pk=post['censorcodecv'])
        quality = CvQualitycode.objects.get(pk=post['qualitycodecv'])
        units_time = Units.objects.get(pk=post['timeaggregationintervalunitsid'])
        time_inter = post['timeaggregationinterval']
        value_utc = post['valuedatetimeutcoffset']

        source = 'ANA'

        station = sampling.samplingfeaturename
        print(station.upper())

        dados = Flow(path=file, source=source.upper(), station=station.upper(), consistence=2)
        default_storage.delete(path)
        dados.data = dados.data.dropna()
        time_serie_result_list = []
        print(dados.data)

        for i in dados.data.index:
            obj_ts = Timeseriesresultvalues(resultid=result, censorcodecv=censor,
                                            qualitycodecv=quality, valuedatetimeutcoffset=value_utc,
                                            timeaggregationinterval=time_inter,
                                            timeaggregationintervalunitsid=units_time,
                                            valuedatetime=i.to_datetime(),
                                            datavalue=float(dados.data[dados.data.columns.values[0]][i]))

            time_serie_result_list.append(obj_ts)
        Timeseriesresultvalues.objects.bulk_create(time_serie_result_list)
        return redirect(self.success_url)


class AddUnitsView(LoginRequiredMixin, CreateView):

    model = Units
    form_class = UnitsForm
    template_name = 'units.html'
    success_url = reverse_lazy('core:index')

    def get(self, request, *args, **kwargs):
        url = resolve('/'+'/'.join(request.META.get("HTTP_REFERER").split('/')[3:]))
        self.success_url = reverse_lazy('{}:{}'.format(url.app_name, url.url_name))
        context = {'form': self.form_class}
        return render(request, self.template_name, context=context)


class AddTimeSeriesResultView(LoginRequiredMixin, CreateView):

    model = Timeseriesresults
    form_class = TimeSeriesResultsForm
    template_name = 'time_serie_result.html'
    success_url = reverse_lazy('core:index')


class AddDataResultsView(LoginRequiredMixin, CreateView):

    model = Results
    template_name = 'data_results.html'
    form_class = ResultsForm
    success_url = reverse_lazy('core:index')


class AddProcessingLevelsView(LoginRequiredMixin, CreateView):

    model = Processinglevels
    template_name = 'processing_level.html'
    form_class = ProcessingLevelsForm
    success_url = reverse_lazy('core:index')


class AddActionView(LoginRequiredMixin, CreateView):

    model = Actions
    form_class = ActionMultiForm
    template_name = 'action.html'
    success_url = reverse_lazy('core:index')


class AddMethodsView(LoginRequiredMixin, CreateView):

    model = Methods
    form_class = MethodsForm
    template_name = 'method.html'
    success_url = reverse_lazy('core:index')


class AddVariablesView(LoginRequiredMixin, CreateView):
    model = Variables
    form_class = VariablesForm
    template_name = 'variable.html'
    success_url = reverse_lazy('core:variable')


class StationInfoView(CreateView):

    template_name = 'station_info.html'

    def get(self, request, *args, **kwargs):

        station = Samplingfeatures.objects.get(samplingfeaturecode=kwargs['code'])
        features = Featureactions.objects.filter(samplingfeatureid=station.samplingfeatureid)

        context = {
            'station': station,
            'features': features,
        }

        return render(request, self.template_name, context=context)


index = IndexView.as_view()
result_station = ResultStationView.as_view()
add_samplingfeatures = AddSamplingFeaturesView.as_view()
add_time_serie_values = AddTimeResultsSeriesValuesView.as_view()
add_units = AddUnitsView.as_view()
add_time_serie_result = AddTimeSeriesResultView.as_view()
add_data_results = AddDataResultsView.as_view()
add_processing_level = AddProcessingLevelsView.as_view()
add_variable = AddVariablesView.as_view()
add_action = AddActionView.as_view()
add_method = AddMethodsView.as_view()
add_organization = AddOrganizationsView.as_view()
station_info = StationInfoView.as_view()
