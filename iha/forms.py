from django import forms
from odm2admin.models import Methods, Featureactions


class SeriesForm(forms.Form):

    code = None

    preimpacto = forms.ModelChoiceField(label='Pré-Impacto',
                                        queryset=Featureactions.objects.filter(samplingfeatureid=code))
    posimpacto = forms.ModelChoiceField(label='Pós-Impacto',
                                        queryset=Featureactions.objects.filter(samplingfeatureid=code))
    date_start = forms.DateField(label='Data de Ínicio', required=False)
    date_end = forms.DateField(label='Data de Fim', required=False)

    def __init__(self, *args, **kwargs):
        super(SeriesForm, self).__init__(*args, **kwargs)
        self.fields['preimpacto'].queryset = Featureactions.objects.filter(samplingfeatureid=self.code)
        self.fields['posimpacto'].queryset = Featureactions.objects.filter(samplingfeatureid=self.code)


class ParcialForm(SeriesForm):
    type_threshold_choices = (
        ('1', 'Fixo'),
        ('2', 'Eventos por ano'))

    type_criterion_choices = (
        ('1', 'Mediana'),
        ('2', 'autocorrelation'))

    type_event_choices = (
        ('1', 'Cheia'),
        ('2', 'Estiagem'),)

    type_threshold = forms.ChoiceField(label='Tipo de Limiar', choices=type_threshold_choices)
    value_threshold = forms.FloatField(label='Valor do Limiar')
    type_criterion = forms.ChoiceField(label='Critério de Independência', choices=type_criterion_choices)
    type_event = forms.ChoiceField(label='Tipo de Eventos', choices=type_event_choices)
    duration = forms.IntegerField(label='Duração entre eventos', required=False)

    def __init__(self, *args, **kwargs):
        super(ParcialForm, self).__init__(*args, **kwargs)
