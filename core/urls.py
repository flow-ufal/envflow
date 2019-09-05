from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import index, results

name_app = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('results/<code>', results, name='results'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='index.html'), name='logout'),
]