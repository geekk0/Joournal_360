import itertools

from django.contrib.auth import authenticate, login, logout
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView, View
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User, Group


from itertools import *
from operator import *

from .models import EngRec, DirRec, EngNotes, DirNotes, Notes, Record, Images
from .forms import LoginForm, RegistrationForm, SendEngReport, SendDirReport, AddEngNote, AddDirNote, ImageForm


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
        return role


def send_report(request):           # Склеивает заметки, запихивает их в запись и удаляет заметки

    role = get_role(request)

    if role == "Техдирекция":

        full_text = ''
        author = request.user
        created_date = timezone.now()

        for note in EngNotes.objects.all():

            full_text = note.message

        EngRec.objects.create(author=author, created_date=created_date, text=full_text)

        EngNotes.objects.all().delete()

    return HttpResponseRedirect('/')


def edit_note(request, note_id):
    note = EngNotes.objects.get(id=note_id)

    if request.method != 'POST':
        form = AddEngNote(instance=note, initial={'message': note.message})
        context = {'form': form}

        return render(request, 'add_note.html', context)

    else:
        form = AddEngNote(instance=note, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

    context = {'note': note, 'index': index, 'form': form}
    return render(request, 'record.html', context)


def rec_list(request):

    role = get_role(request)
    author_list = User.objects.filter(groups__name=role)

    group_list = Group.objects.all()

    if role == 'Техдирекция':
        records_list = EngRec.objects.order_by('-created_date')
        notes = EngNotes.objects.order_by('-created_date')
        taglist = EngRec.tag_list

    elif role == 'Режиссеры':
        records_list = DirRec.objects.order_by('-created_date')
        notes = DirNotes.objects.order_by('-created_date')
        taglist = DirRec.tag_list

    elif role == 'Все отчеты':
        records_list = list(chain(EngRec.objects.all(), DirRec.objects.all()))
        records_list.sort(key=attrgetter('created_date'), reverse=True)
        notes = None
        """list(chain(EngNotes.objects.all(), DirNotes.objects.all()))
        notes.sort(key=attrgetter('created_date'), reverse=True)"""
        taglist = chain(EngRec.tag_list, DirRec.tag_list)
        author_list = User.objects.all()

    else:
        return HttpResponseRedirect('login/')

    context = {'records_list': records_list, 'notes': notes, 'role': role,
           'author_list': author_list, "taglist": taglist, 'group_list': group_list}
    return render(request, 'rec_list.html', context)


def record_full_text(request, rec_id, role):

    record_text = None
    images = None

    if role == 'Техдирекция':
        record_text = EngRec.objects.filter(id=rec_id)
        images = Images.objects.filter(record=rec_id)
    if role == 'Режиссеры':
        record_text = DirRec.objects.filter(id=rec_id)
        images = Images.objects.filter(record_id=rec_id)
    if role == 'Все отчеты':
        record_text = chain(DirRec.objects.filter(id=rec_id), EngRec.objects.filter(id=rec_id))
        images = Images.objects.filter(record_id=rec_id)

    return render(request, 'record.html', {'record_text': record_text, 'images': images})


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

        ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3)

        formset = ImageFormSet(queryset=Images.objects.none())
        context = {'form': form, "formset": formset}

        return render(request, 'add_rec.html', context)

    def post(self, request, *args, **kwargs):

        form = SendEngReport(request.POST or None)

        ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3)

        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())

        if form.is_valid() and formset.is_valid():
            report = form.save(commit=False)

            report.author = request.user
            report.created_date = timezone.now()
            report.tags = form.cleaned_data['tags']
            report.save()

            for form in formset.cleaned_data:

                if form:
                    image = form['image']
                    photo = Images(post=report, image=image)
                    photo.save()

            return HttpResponseRedirect('/')

        else:
            print(form.errors, formset.errors)


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


def find(request):

    group_list = Group.objects.all()

    current_group = request.GET.get('group')

    """current_group_name = 'Отдел:'"""

    role = get_role(request)

    start_date = request.GET.get('startdate')

    stop_date = request.GET.get('stopdate')

    input_text = request.GET.get('q')

    author = request.GET.get('author')

    author_name = 'Отчет от:'

    tag = request.GET.get('tag')

    author_list = User.objects.filter(groups__name=current_group)

    search_query = EngRec.objects.all()

    search_query_e = EngRec.objects.filter(text__icontains=input_text).order_by('-created_date')
    search_query_d = DirRec.objects.filter(text__icontains=input_text).order_by('-created_date')

    all_records_e = EngRec.objects.all().order_by('-created_date')
    all_records_d = DirRec.objects.all().order_by('-created_date')

    all_records = EngRec.objects.all()

    notes = None

    if role == 'Техдирекция':
        search_query = search_query_e
        notes = EngNotes.objects.order_by('-created_date')
        all_records = all_records_e

    elif role == 'Режиссеры':
        search_query = search_query_d
        notes = DirNotes.objects.order_by('-created_date')
        all_records = all_records_d

    elif role == 'Все отчеты':

        if 'Отдел:' not in current_group:   # Если отдел выбран

            if current_group == 'Техдирекция':
                search_query = EngRec.objects.filter(text__icontains=input_text).order_by('-created_date')
            elif current_group == 'Режиссеры':
                search_query = DirRec.objects.filter(text__icontains=input_text).order_by('-created_date')

            author_list = User.objects.filter(groups__name=current_group)
        all_records = list(chain(all_records_e, all_records_d))

    if role is None:
        return render(request, 'not_in_group.html')

    if start_date:
        search_query = search_query.filter(report_date__gte=start_date, report_date__lte=stop_date).order_by(
            '-report_date')
        search_query_e = search_query_e.filter(report_date__gte=start_date, report_date__lte=stop_date)
        search_query_d = search_query_e.filter(report_date__gte=start_date, report_date__lte=stop_date)

    if 'Отчет' not in author:   # Если автор выбран

        search_query = search_query.filter(author=author).order_by('-created_date')
        search_query_e = search_query_e.filter(author=author)
        search_query_d = search_query_d.filter(author=author)
        author_name = author_list.get(id=author)

    if role == "Все отчеты" and 'Отдел:' in current_group:

        search_query = list(chain(search_query_e, search_query_d))
        search_query.sort(key=attrgetter('report_date'), reverse=True)
        notes = list(chain(EngNotes.objects.all(), DirNotes.objects.all()))
        notes.sort(key=attrgetter('created_date'), reverse=True)


    current_group_name = current_group

    context = {'search_query': search_query, "notes": notes, "input_text": input_text, 'role': role,
               "author_name": author_name, "tag": tag, "author_list": author_list,
               "start_date": start_date, "stop_date": stop_date, "author": author, "all_records": all_records,
               'current_group': current_group, 'group_list': group_list, 'current_group_name': current_group_name}


    return render(request, 'search_result.html', context)









