from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import User
from .forms import UserMultiForm


# Create your views here.
class RegisterView(CreateView):

    model = User
    template_name = 'register.html'
    form_class = UserMultiForm
    success_url = reverse_lazy('core:index')


register = RegisterView.as_view()
