from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
# Create your views here.
from odm2admin.models import Featureactions, Samplingfeatures


class IndexView(CreateView):

    template_name = 'iha/index.html'

    def get(self, request, *args, **kwargs):

        sampling = Samplingfeatures.objects.get(samplingfeaturecode=kwargs['code'])
        context = {"sampling": sampling}

        return render(request, self.template_name, context=context)

class ResultsView(TemplateView):

    template_name = 'iha/results.html'


index = IndexView.as_view()
results = ResultsView.as_view()
