from django.contrib.auth.forms import UserCreationForm
from django import forms

from betterforms.multiform import MultiModelForm
from odm2admin.forms import PeopleAdminForm

from .models import User


class UserAdminCreationForm(UserCreationForm):

    fields = ['username', 'email', 'people']

    class Meta:
        model = User
        fields = ['username', 'email', 'people']


class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'people']


class UserMultiForm(MultiModelForm):

    form_classes = {
        'username': UserAdminCreationForm,
        'people': PeopleAdminForm
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
