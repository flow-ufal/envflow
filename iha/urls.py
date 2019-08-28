from django.urls import path
from .views import index, results


name_app = 'iha'

urlpatterns = [
    path('', index, name='index'),
    path('results/', results, name='results'),
]