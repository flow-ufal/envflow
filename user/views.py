from django.views.generic import CreateView
from .models import User


# Create your views here.
class RegisterView(CreateView):

    model = User
    template_name = 'user/register.html'
    form_class = UserAdminCreationForm
    success_url = reverse_lazy('index')