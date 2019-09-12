from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import register

app_name = 'user'

urlpatterns = [
    path('register', register, name='register'),
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(template_name='index.html'), name='logout'),
]