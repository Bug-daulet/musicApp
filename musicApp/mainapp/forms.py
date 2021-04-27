from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *


class SimpleUserForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = UserManage
        fields = ('email', 'username', 'user_img')


class SimpleUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = UserManage
        fields = ('email', 'username', 'user_img')
