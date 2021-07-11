import itertools

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView, View
from django.contrib.auth.models import User, Group

from itertools import *
from operator import *

from .models import EngRec, DirRec
from .forms import LoginForm, RegistrationForm


def rec_list(request):

    if request.user.is_authenticated:
        roles = []
        role = ''
        records_list = None

        for g in request.user.groups.all():
            roles.append(g.name)

        if not roles:
            records_list = None
            return render(request, 'not_in_group.html')

        else:

            role = roles[0]

            if role == 'Техдирекция':
                records_list = EngRec.objects.order_by('-created_date')

            elif role == 'Режиссеры':
                records_list = DirRec.objects.order_by('-created_date')

            elif role == 'Все отчеты':
                records_list = list(chain(EngRec.objects.all(), DirRec.objects.all()))
                records_list.sort(key=attrgetter('created_date'), reverse=True)

        context = {'records_list': records_list, 'role': role}
        return render(request, 'rec_list.html', context)

    else:
        return HttpResponseRedirect('login/')


def record_full_text(request, rec_id, role):

    record_text = None

    if role == 'Техдирекция':
        record_text = EngRec.objects.filter(id=rec_id)
    if role == 'Режиссеры':
        record_text = DirRec.objects.filter(id=rec_id)
    if role == 'Все отчеты':
        record_text = chain(DirRec.objects.filter(id=rec_id), EngRec.objects.filter(id=rec_id))

    return render(request, 'record.html', {'record_text': record_text})


class LoginView(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {'form': form}
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


class RegistrationView(View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {'form': form}

        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)

            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.phone = form.cleaned_data['phone']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {'form': form}
        return render(request, 'registration.html', context)


