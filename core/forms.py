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

    class Meta:
        model = Samplingfeatures
        fields = ['samplingfeaturecode', 'sampling_feature_type', 'samplingfeaturename', 'lat', 'lon', ]
