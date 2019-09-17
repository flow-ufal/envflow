from django.urls import path

from core.views import add_variable
from .views import (index, result_station, add_samplingfeatures, add_time_serie_values, add_units, add_time_serie_result, add_data_results,
                    add_processing_level, add_action, add_method, add_organization)

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('result_station/<code>', result_station, name='result_station'),
    path('station/add', add_samplingfeatures, name='station'),
    path('station/<code>/add_data', add_time_serie_values, name='add_values'),
    path('add_data', add_time_serie_values, name='add'),
    path('units/add', add_units, name='units'),
    path('result_series/add', add_time_serie_result, name='results_serie_results'),
    path('data_results/add', add_data_results, name='data_results'),
    path('processing/add', add_processing_level, name='processing_level'),
    path('action/add', add_action, name='action'),
    path('variable/add', add_variable, name='variable'),
    path('method/add', add_method, name='method'),
    path('organization/add', add_organization, name='org')
]