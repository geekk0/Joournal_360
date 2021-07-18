import itertools

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView, View
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User


from itertools import *
from operator import *

from .models import EngRec, DirRec, EngNotes, DirNotes, Notes
from .forms import LoginForm, RegistrationForm, SendEngReport, SendDirReport, AddEngNote, AddDirNote


def get_role(request):

    if request.user.is_authenticated:
        roles = []
        role = ''
        records_list = None
        notes = None

        for g in request.user.groups.all():
            roles.append(g.name)

        if not roles:
            records_list = None
            return render(request, 'not_in_group.html')

        else:

            role = roles[0]

            if role == 'Техдирекция':
                records_list = EngRec.objects.order_by('-report_date')
                notes = EngNotes.objects.order_by('-created_date')

            elif role == 'Режиссеры':
                records_list = DirRec.objects.order_by('-report_date')
                notes = DirNotes.objects.order_by('-created_date')

            elif role == 'Все отчеты':
                records_list = list(chain(EngRec.objects.all(), DirRec.objects.all()))
                records_list.sort(key=attrgetter('report_date'), reverse=True)
                notes = list(chain(EngNotes.objects.all(), DirNotes.objects.all()))
                notes.sort(key=attrgetter('created_date'), reverse=True)

        context = {'records_list': records_list, 'notes': notes, 'role': role}
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




class SendEngReportView(View):

    def get(self, request, *args, **kwargs):
        form = SendEngReport(request.POST or None)
        context = {'form': form}

        return render(request, 'add_rec.html', context)

    def post(self, request, *args, **kwargs):

        form = SendEngReport(request.POST or None)

        if form.is_valid():
            report = form.save(commit=False)

            report.author = request.user
            report.created_date = timezone.now()
            report.tags = form.cleaned_data['tags']
            report.save()

            return HttpResponseRedirect('/')


class SendDirReportView(SendEngReportView):

    def get(self, request, *args, **kwargs):
        form = SendDirReport(request.POST or None)
        context = {'form': form}

        return render(request, 'add_rec.html', context)

    def post(self, request, *args, **kwargs):

        form = SendDirReport(request.POST or None)

        if form.is_valid():
            report = form.save(commit=False)

            report.author = request.user
            report.created_date = timezone.now()
            report.tags = form.cleaned_data['tags']
            report.save()

            return HttpResponseRedirect('/')


def delete_note(request, note_id):

    Notes.objects.filter(id=note_id).delete()
    return HttpResponseRedirect('/')


class AddEngNoteView(View):

    def get(self, request, *args, **kwargs):
        form = AddEngNote(request.POST or None)
        context = {'form': form}

        return render(request, 'add_note.html', context)

    def post(self, request, *args, **kwargs):

        form = AddEngNote(request.POST or None)

        if form.is_valid():
            report = form.save(commit=False)

            report.author = request.user
            report.created_date = timezone.now()
            report.save()

            return HttpResponseRedirect('/')


class AddDirNoteView(View):

    def get(self, request, *args, **kwargs):
        form = AddDirNote(request.POST or None)
        context = {'form': form}

        return render(request, 'add_note.html', context)

    def post(self, request, *args, **kwargs):

        form = AddDirNote(request.POST or None)

        if form.is_valid():
            report = form.save(commit=False)

            report.author = request.user
            report.created_date = timezone.now()
            report.save()

            return HttpResponseRedirect('/')


def search_eng_recs(request):

    input_text = request.GET.get('q')

    #search_query = EngRec.objects.filter(text__icontains=input_text)

    roles = []
    role = ''
    records_list = None
    notes = None

    for g in request.user.groups.all():
        roles.append(g.name)

    if not roles:
        records_list = None
        return render(request, 'not_in_group.html')

    else:

        role = roles[0]

        if role == 'Техдирекция':
            search_query = EngRec.objects.filter(text__icontains=input_text)
            notes = EngNotes.objects.order_by('-created_date')

        elif role == 'Режиссеры':
            search_query = DirRec.objects.filter(text__icontains=input_text)
            notes = DirNotes.objects.order_by('-created_date')

        elif role == 'Все отчеты':
            search_query = list(chain(EngRec.objects.filter(text__icontains=input_text),
                                      DirRec.objects.filter(text__icontains=input_text)))
            notes = list(chain(EngNotes.objects.all(), DirNotes.objects.all()))
            notes.sort(key=attrgetter('created_date'), reverse=True)

        context = {'search_query': search_query, "notes": notes, "input_text": input_text, 'role': role}

    return render(request, 'search_result.html', context)
