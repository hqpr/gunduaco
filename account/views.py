from django.shortcuts import render
import json
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.views import password_reset
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
# from .models import Profile
from datetime import date
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext


def login_view(request):
    logout(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
    return render_to_response('registration/login.html', context_instance=RequestContext(request))


def logout_view(request):
    logout(request)
    return redirect('index')


def register(request):
    errors = []
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect('success')
        else:
            errors.append('Something not right. Try again')
    else:
        form = UserCreationForm()
    return render(request, "account/register.html", {
        'form': form, 'errors': errors
    })

def success(request):
    return render(request, 'account/ok.html')