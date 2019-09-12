from django.urls import path
from .views import index, results


app_name = 'iha'

urlpatterns = [
    path('', index, name='index'),
    path('results/', results, name='results'),
]