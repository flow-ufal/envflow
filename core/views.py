from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from odm2admin.models import Samplingfeatures


# Create your views here.
class IndexView(CreateView):

    model = Samplingfeatures
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):

        stations = Samplingfeatures.objects.all()

        context = {'stations': stations}

        return render(request, self.template_name, context)


class ResultsView(TemplateView):

    template_name = 'results.html'


index = IndexView.as_view()
results = ResultsView.as_view()
