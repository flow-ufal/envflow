from django.views.generic import CreateView, TemplateView
# Create your views here.


class IndexView(TemplateView):

    template_name = 'iha/index.html'

class ResultsView(TemplateView):

    template_name = 'iha/results.html'


index = IndexView.as_view()
results = ResultsView.as_view()
