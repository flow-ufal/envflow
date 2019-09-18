from django.urls import path
from .views import index, results


app_name = 'iha'

urlpatterns = [
    path('<code>', index, name='index'),
    path('#', results, name='results'),
]