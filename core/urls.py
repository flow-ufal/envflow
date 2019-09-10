from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import index, results, samplingfeatures, time_serie_values

name_app = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('results/<code>', results, name='results'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='index.html'), name='logout'),
    path('station', samplingfeatures, name='station'),
    path('station/<code>/add_data', time_serie_values, name='add_values'),
    path('add_data', time_serie_values, name='add')
]