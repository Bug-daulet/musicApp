from django.urls import path
from .views import (
    LoginView,
    index,
    logout,
    registration,
)

urlpatterns = [
    path('', index, name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path('registration/', registration, name='registration'),
]
