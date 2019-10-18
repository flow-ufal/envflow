import re

from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from odm2admin.models import People


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        last_name = input('Last Name: ')
        first_name = input('First Name: ')
        people = People(personlastname=last_name, personfirstname=first_name)
        people.save()
        user = self.model(
            username=username,
            people=people,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


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
    profile_picture = models.ImageField(upload_to='profile_picture', null=True,
                                        blank=True, default='profile_picture/avatar.png')
    people = models.OneToOneField(People, null=True, blank=True, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField('E-mail', unique=True)
    is_staff = models.BooleanField('Equipe', default=False)
    is_active = models.BooleanField('Ativo', default=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.username

    def get_full_name(self):
        return str(self)

    def get_short_name(self):
        return str(self).split(" ")[0]
