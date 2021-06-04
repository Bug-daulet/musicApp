from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class UpdateForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.CharField(label='Email', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    first_name = forms.CharField(label='First name', widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(label='Last name', widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    password2 = forms.CharField(
        label='Password confirmation',
        help_text='Enter the same password as before, for verification.',
        widget=forms.PasswordInput(attrs={'placeholder': 'Re Enter Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', ]

    def save(self, commit=True):
        user = super(UpdateForm, self).save(commit=False)
        if commit:
            user.save()
        return user
