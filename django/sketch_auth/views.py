from django.shortcuts import render
from django.contrib.auth.views import LoginView  

# Create your views here.

class SketchLogin(LoginView):
    template_name="sketch_auth/login.html"

def logoutnlogin(request):
    return logout_then_login(request,login_url='login/')
