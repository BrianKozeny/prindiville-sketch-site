from django.shortcuts import render
from django.contrib.auth.views import LoginView  
from login_required import LoginNotRequiredMixin
from django.views.generic import RedirectView


# Create your views here.


class SketchLoginView(LoginView, LoginNotRequiredMixin):
    next_page = None
    template_name = 'sketch_auth/login.html'

