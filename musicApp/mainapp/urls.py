from django.urls import path
from django.contrib.auth.views import auth_login
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('', auth_login, name="login"),
    path("register/", registerView.as_view(), name="registration"),
]
