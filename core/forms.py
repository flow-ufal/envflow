from betterforms.multiform import MultiModelForm
from django import forms
from ajax_select import make_ajax_field
from django.urls import reverse
from django.utils.html import format_html
from odm2admin.forms import OrganizationsAdminForm, TimeseriesresultvaluesAdminForm, UnitsAdminForm, \
    TimeseriesresultsAdminForm, ResultsAdminForm, ProcessingLevelsAdminForm, FeatureactionsAdminForm, ActionsAdminForm, \
    MethodsAdminForm, ActionByAdminForm, VariablesAdminForm
from odm2admin.models import (Results, Samplingfeatures, Featureactions,
                              Timeseriesresults, Timeseriesresultvalues, Organizations, Units, Processinglevels,
                              Actions, Methods, Actionby, Variables)


def link_add(label, url):
    return format_html('{} <a href="{}"><img src="/static/admin/img/icon-addlink.svg" alt="Add"></a>'.format(
        label, reverse('{}'.format(url)))
    )


class SamplingFeaturesForm(forms.ModelForm):

    sampling_feature_type = make_ajax_field(Samplingfeatures, 'sampling_feature_type',
                                            'cv_sampling_feature_type')

    lat = forms.CharField(max_length=10, label='Latitude')
    lon = forms.CharField(max_length=10, label='Longitude')

    def __init__(self, *args, **kwargs):
        super(SamplingFeaturesForm, self).__init__(*args, **kwargs)
        self.fields['samplingfeaturecode'].label = 'Código da Estação'
        self.fields['sampling_feature_type'].label = 'Tipo de característica de amostragem'

    class Meta:
        model = Samplingfeatures
        fields = ['samplingfeaturecode', 'sampling_feature_type', 'samplingfeaturename', 'lat', 'lon']
        labels = {'samplingfeaturename': 'Nome da Estação'}


class ResultsForm(ResultsAdminForm):

    def __init__(self, *args, **kwargs):
        super(ResultsForm, self).__init__(*args, **kwargs)
        self.fields['featureactionid'].label = link_add('Ação', url='core:action')
        self.fields['valuecount'].label = 'Quantidade de valores registrado'
        self.fields['processing_level'].label = link_add('Nível de processamento', 'core:processing_level')
        self.fields['unitsid'].label = link_add('Unidade', 'core:units')
        self.fields['result_type'].label = 'Tipo'
        self.fields['variableid'].label = link_add('Variável', url='core:variable')
        self.fields['sampledmediumcv'].label = 'Meio Amostral'

    class Meta:
        model = Results
        fields = ['featureactionid', 'valuecount', 'processing_level', 'result_type', 'unitsid', 'variableid',
                  'sampledmediumcv']


class FeatureAcrionForm(FeatureactionsAdminForm):

    def __init__(self, *args, **kwargs):
        super(FeatureAcrionForm, self).__init__(*args, **kwargs)
        self.fields['samplingfeatureid'].label = 'Estação'

    class Meta:
        model = Featureactions
        fields = ['samplingfeatureid']


class TimeSeriesResultsForm(TimeseriesresultsAdminForm):

    def __init__(self, *args, **kwargs):
        super(TimeSeriesResultsForm, self).__init__(*args, **kwargs)
        self.fields['aggregationstatisticcv'].label = 'Agregação Estatística'
        self.fields['resultid'].label = link_add('Resultado dos dados', 'core:data_results')

    class Meta:
        model = Timeseriesresults
        fields = ['aggregationstatisticcv', 'resultid']


class TimeResultsSeriesValuesForm(TimeseriesresultvaluesAdminForm):

    def __init__(self, *args, **kwargs):
        super(TimeResultsSeriesValuesForm, self).__init__(*args, **kwargs)
        self.fields['resultid'].label = link_add('Time série', 'core:results_serie_results')
        self.fields['valuedatetimeutcoffset'].label = 'Value UTC'
        self.fields['censorcodecv'].label = 'Sensor'
        self.fields['qualitycodecv'].label = 'Qualidade'
        self.fields['timeaggregationinterval'].label = 'Intervalo de Tempo'
        self.fields['timeaggregationintervalunitsid'].label = link_add('Unidade de Tempo', 'core:units')
        self.fields['File'] = forms.FileField()

    class Meta:
        model = Timeseriesresultvalues
        exclude = ['datavalue', 'valuedatetime']
        ordering = ['resultid', 'valuedatetimeutcoffset', 'censorcodecv', 'qualitycodecv', 'File']


class OrganizationsForm(OrganizationsAdminForm):

    def __init__(self, *args, **kwargs):
        super(OrganizationsForm, self).__init__(*args, **kwargs)
        self.fields['organizationcode'].label = 'Código da Organização'
        self.fields['organizationname'].label = 'Nome da Organização'
        self.fields['organizationtypecv'].label = 'Tipo de Organização'
        self.fields['parentorganizationid'].label = 'Parentesco'

    class Meta:
        model = Organizations
        fields = ['organizationcode', 'organizationname', 'organizationtypecv', 'parentorganizationid']


class UnitsForm(UnitsAdminForm):

    def __init__(self, *args, **kwargs):
        super(UnitsForm, self).__init__(*args, **kwargs)
        self.fields['unit_type'].label = 'Tipo'

    class Meta:
        model = Units
        exclude = ['unitslink']
        labels = {
            'unitsabbreviation': 'Abreviatura',
            'unitsname': 'Nome'
        }


class ProcessingLevelsForm(ProcessingLevelsAdminForm):

    def __init__(self, *args, **kwargs):
        super(ProcessingLevelsForm, self).__init__(*args, **kwargs)
        self.fields['processinglevelcode'].label = 'Código'
        self.fields['definition'].label = 'Definição'
        self.fields['explanation'].label = 'Explicação'

    class Meta:
        model = Processinglevels
        fields = '__all__'


class ActionsForm(ActionsAdminForm):

    def __init__(self, *args, **kwargs):
        super(ActionsForm, self).__init__(*args, **kwargs)
        self.fields['actiondescription'].label = 'Descrição'
        self.fields['method'].label = link_add('Método', url='core:method')

    class Meta:
        model = Actions
        fields = ['action_type', 'method', 'begindatetime', 'begindatetimeutcoffset', 'actiondescription']
        labels = {
            'action_type': 'Tipo',
            'begindatetime': 'Hora e data de início',
            'begindatetimeutcoffset': 'Tempo Médio de Greenwich',
            'actiondescription': 'Descrição'
        }


class MethodsForm(MethodsAdminForm):

    def __init__(self, *args, **kwargs):
        super(MethodsForm, self).__init__(*args, **kwargs)
        self.fields['methodtypecv'].label = 'Tipo'
        self.fields['organizationid'].label = link_add('Organização', 'core:org')

    class Meta:
        model = Methods
        fields = ['methodtypecv', 'methodcode', 'methodname', 'methoddescription', 'organizationid']
        labels = {
            'methodcode': 'Código',
            'methodname': 'Nome',
            'methoddescription': 'Descrição',
        }


class ActionMultiForm(MultiModelForm):

    form_classes = {
        'action': ActionsForm,
        'feature_action': FeatureAcrionForm,
    }

    def save(self, commit=True):
        objects = super(ActionMultiForm, self).save(commit=False)

        if commit:
            action = objects['action']
            action.save()
            feature_action = objects['feature_action']
            feature_action.action = action
            feature_action.save()
        return objects


class VariablesForm(VariablesAdminForm):

    def __init__(self, *args, **kwargs):
        super(VariablesForm, self).__init__(*args, **kwargs)
        self.fields['variable_name'].label = 'Nome'
        self.fields['variable_type'].label = 'Tipo'
        self.fields['variablecode'].label = 'Código'
        self.fields['variabledefinition'].label = 'Definição'
        self.fields['nodatavalue'].label = 'Não tem dado?'
        self.fields['speciation'].label = 'Especiação'

    class Meta:
        model = Variables
        fields = '__all__'
