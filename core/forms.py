from django import forms
from ajax_select import make_ajax_field
from odm2admin.models import (Results, Samplingfeatures, Featureactions,
                              Timeseriesresults, Timeseriesresultvalues, Organizations)
from odm2admin.forms import (ResultsAdminForm, TimeseriesresultvaluesAdminForm,
                             TimeseriesresultsAdminForm, OrganizationsAdminForm)


class SamplingFeaturesForm(forms.ModelForm):

    sampling_feature_type = make_ajax_field(Samplingfeatures, 'sampling_feature_type',
                                            'cv_sampling_feature_type')

    lat = forms.CharField(max_length=10, label='Latitude')
    lon = forms.CharField(max_length=10, label='Longitude')

    def __init__(self, *args, **kwargs):
        super(SamplingFeaturesForm, self).__init__(*args, **kwargs)
        self.fields['samplingfeaturecode'].label = 'Código da Estação'
        self.fields['sampling_feature_type'].label = 'Tipo de característica de amostragem'
        self.fields['samplingfeaturename'].label = 'Nome da Estação'

    class Meta:
        model = Samplingfeatures
        fields = ['samplingfeaturecode', 'sampling_feature_type', 'samplingfeaturename', 'lat', 'lon', ]


class ResultsForm(ResultsAdminForm):

    def __int__(self, *args, **kwargs):
        super(ResultsForm, self).__init__(*args, **kwargs)
        self.fields['taxonomicclassifierid'].label = 'Classificador taxonómico'
        self.fields['featureactionid'].label = 'Ação'
        self.fields['valuecount'].label = 'Quantidade de valores registrado'
        self.fields['processing_level'].label = 'Processing level'

    class Meta:
        model = Results
        exclude = ['taxonomicclassifierid', 'featureactionid', 'valuecount', 'processing_level']


class FeatureForm(forms.ModelForm):

    def __int__(self, *args, **kwargs):
        super(FeatureForm, self).__init__(*args, **kwargs)
        self.fields['samplingfeatureid'].label = 'Estação'
        self.fields['action'].label = 'Ação'

    class Meta:
        model = Featureactions
        fields = '__all__'


class TimeSeriesResultsForm(TimeseriesresultsAdminForm):

    def __init__(self, *args, **kwargs):
        super(TimeSeriesResultsForm, self).__init__(*args, **kwargs)
        self.fields['aggregationstatisticcv'].label = 'Agregação Estatística'

    class Meta:
        model = Timeseriesresults
        fields = ['aggregationstatisticcv', 'resultid']


class TimeResultsSeriesValuesForm(TimeseriesresultvaluesAdminForm, forms.Form):

    def __init__(self, *args, **kwargs):
        super(TimeResultsSeriesValuesForm, self).__init__(*args, **kwargs)
        self.fields['resultid'] = 'Time série'
        self.fields['valuedatetimeutcoffset'].label = 'Value UTC'
        self.fields['censorcodecv'].label = 'Censor Code'
        self.fields['qualitycodecv'].label = 'Quality Code'
        self.fields['File'] = forms.FileField()

    class Meta:
        model = Timeseriesresultvalues
        exclude = ['datavalue', 'valuedatetime']
        ordering = ['resultid', 'valuedatetimeutcoffset', 'censorcodecv', 'qualitycodecv', 'File']


class OrganizationsForm(OrganizationsAdminForm):

    def __init__(self, *args, **kwargs):
        super(OrganizationsForm, self).__init__(*args, **kwargs)
        self.fields['organizationcode'] = 'Código da Organização'
        self.fields['organizationname'] = 'Nome da Organização'
        self.fields['organizationtypecv'] = 'Tipo de Organização'
        self.fields['parentorganizationid'] = 'Parentesco'

    class Meta:
        model = Organizations
        fields = ['organizationcode', 'organizationname', 'organizationtypecv', 'parentorganizationid']
