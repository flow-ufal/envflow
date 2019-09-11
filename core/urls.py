from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import (index, result_station, samplingfeatures, time_serie_values, units, time_serie_result, data_results,
                    processing_level, feature_action, action, method, organization)

name_app = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('result_station/<code>', result_station, name='result_station'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='index.html'), name='logout'),
    path('station/add', samplingfeatures, name='station'),
    path('station/<code>/add_data', time_serie_values, name='add_values'),
    path('add_data', time_serie_values, name='add'),
    path('units/add', units, name='units'),
    path('result_series/add', time_serie_result, name='results_serie_results'),
    path('data_results/add', data_results, name='data_results'),
    path('processing/add', processing_level, name='processing_level'),
    path('feature_action/add', feature_action, name='feature_action'),
    path('action/add', action, name='action'),
    path('method/add', method, name='method'),
    path('organization/add', organization, name='org')
]