import re
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from odm2admin.models import People


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        "Apelido/Usuário", max_length=30, unique=True,
            validators=[validators.RegexValidator(
                re.compile('^[\w.@+=]+$'),
                'Informe um nome de usuário válido. '
                'Este valor deve conter apenas letras, números '
                'e os caracteres: @/./+/-/_ .',
                'invalid'
            )
        ], help_text='Um nome curto que será usado para identificá-lo de forma'
                'única na plataforma'
    )
    people = models.ForeignKey(People, null=False, on_delete=models.CASCADE)
    email = models.EmailField('E-mail', unique=True)
    is_staff = models.BooleanField('Equipe', default=False)
    is_active = models.BooleanField('Ativo', default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.people or self.username

    def get_full_name(self):
        return str(self)

    def get_short_name(self):
        return str(self).split(" ")[0]