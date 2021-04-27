from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import *
from django.urls import reverse_lazy

from .forms import *
from .models import *


def index(request):
    return render(request, 'mainapp/layout.html')


class registerView(CreateView):
    form_class = SimpleUserForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration.html'
