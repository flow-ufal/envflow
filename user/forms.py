from django.contrib.auth.forms import UserCreationForm
from django import forms

from betterforms.multiform import MultiModelForm
from odm2admin.forms import PeopleAdminForm
from odm2admin.models import People

from .models import User


class UserAdminCreationForm(UserCreationForm):

    fields = ['username', 'email']

    class Meta:
        model = User
        fields = ['username', 'email']


class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'people', 'email']


class PeopleFrom(PeopleAdminForm):

    def __init__(self, *args, **kwargs):
        super(PeopleFrom, self).__init__(*args, **kwargs)
        self.fields['personfirstname'].label = 'Nome'
        self.fields['personlastname'].label = 'Sobrenome'

    class Meta:
        model = People
        fields = ['personfirstname', 'personlastname']


class UserMultiForm(MultiModelForm):

    form_classes = {
        'people': PeopleFrom,
        'username': UserAdminCreationForm,
    }

    def save(self, commit=True):
        objects = super(UserMultiForm, self).save(commit=False)

        if commit:
            people = objects['people']
            people.save()
            username = objects['username']
            username.people = people
            username.save()
        return objects
