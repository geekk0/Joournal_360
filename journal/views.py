import itertools
import datetime

from django.contrib.auth import authenticate, login, logout
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView, View
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist


from itertools import *
from operator import *

from .models import EngRec, DirRec, EngNotes, DirNotes, Notes, Record, Images, Comments
from .forms import LoginForm, RegistrationForm, SendEngReport, SendDirReport, AddNote, AddDirNote, ImageForm, AddComment


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


class AddNoteView(View):

    def get(self, request, *args, **kwargs):

        user = request.user.id

        if Notes.objects.filter(author=user).exists():
            return HttpResponseRedirect('/')

        else:

            form = AddNote(request.POST or None)
            context = {'form': form}

            return render(request, 'add_note.html', context)

    def post(self, request, *args, **kwargs):

        form = AddNote(request.POST or None)

        if form.is_valid():
            report = form.save(commit=False)

            report.author = request.user
            report.created_date = timezone.now()
            report.save()

            return HttpResponseRedirect('/')


class AddCommentView(View):

    def get(self, request, *args, **kwargs):

        form = AddComment(request.POST or None)
        context = {'form': form}

        return render(request, 'add_comment.html', context)

    def post(self, request, record_id, *args, **kwargs):

        form = AddComment(request.POST or None)

        if form.is_valid():
            comment = form.save(commit=False)

            comment.record_id = Record.objects.get(id=record_id)
            comment.author = request.user
            comment.created = timezone.now()
            comment.save()

            comments_count(request, record_id)

            return HttpResponseRedirect('/')


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


def get_roles(request):
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
            return roles


def send_report(request):           # Преобразует заметки в записи

    full_text = ''
    author = request.user
    created_date = timezone.now()

    for note in Notes.objects.all():
        full_text = note.message

    Record.objects.create(author=author, created_date=created_date, text=full_text)

    Notes.objects.all().delete()

    return HttpResponseRedirect('/')


def edit_note(request, note_id):

    note = Notes.objects.get(id=note_id)

    if request.method != 'POST':
        form = AddNote(instance=note, initial={'message': note.message})
        context = {'form': form}

        return render(request, 'edit_note.html', context)

    else:
        form = AddNote(instance=note, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

    context = {'note': note, 'index': index, 'form': form}
    return render(request, 'record.html', context)


def rec_list(request):

    roles = str(get_roles(request))
    user_groups = request.user.groups.all()

    print(user_groups)

    multirole = False

    if request.user.groups.all().count() > 1:
        multirole = True
    current_user = request.user
    match_authors_list = []
    for group in user_groups:
        for author in User.objects.filter(groups__name=group):
            match_authors_list.append(author)

    records = Record.objects.filter(author__in=match_authors_list).order_by('-created_date')

    notes = Notes.objects.filter(author__in=match_authors_list)

    comments = Comments.objects.all().order_by('-created')

    context = {'records': records, 'comments': comments, 'roles': roles, 'current_user': current_user, 'notes': notes,
               'multirole': multirole, 'group_list': user_groups}

    return render(request, 'rec_list.html', context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def delete_note(request):

    user = request.user.id

    Notes.objects.filter(author=user).delete()
    return HttpResponseRedirect('/')


def find(request):

    group_list = Group.objects.all()

    current_group = request.GET.get('group')

    current_group_name = 'Отдел:'

    role = get_role(request)

    comments = Comments.objects.all()



    input_text = request.GET.get('q')

    author = request.GET.get('author')

    author_name = 'Отчет от:'

    tag = request.GET.get('tag')

    author_list = User.objects.filter(groups__name=role)

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

            current_group_name = Group.objects.get(id=current_group)

            current_group_name = str(current_group_name)

            if current_group_name == 'Техдирекция':
                search_query = EngRec.objects.filter(text__icontains=input_text).order_by('-created_date')
            elif current_group_name == 'Режиссеры':
                search_query = DirRec.objects.filter(text__icontains=input_text).order_by('-created_date')

            author_list = User.objects.filter(groups__name=current_group_name)

        else:
            author_list = User.objects.all()

        all_records = list(chain(all_records_e, all_records_d))

    if role is None:
        return render(request, 'not_in_group.html')




    if role == "Все отчеты" and 'Отдел:' in current_group:

        search_query = list(chain(search_query_e, search_query_d))
        search_query.sort(key=attrgetter('report_date'), reverse=True)
        notes = list(chain(EngNotes.objects.all(), DirNotes.objects.all()))
        notes.sort(key=attrgetter('created_date'), reverse=True)



    context = {'search_query': search_query, "notes": notes, "input_text": input_text, 'role': role,
               "author_name": author_name, "tag": tag, "author_list": author_list, "author": author, "all_records": all_records,
               'current_group': current_group, 'group_list': group_list, 'current_group_name': current_group_name,
               'comments': comments}


    return render(request, 'search_result.html', context)


def comments_count(request, record_id):

    record = Record.objects.get(id=record_id)
    correct_count = len(Comments.objects.filter(record_id=record_id))
    print(type(correct_count))
    record.comments_count = correct_count
    record.save()


def find_by_date(request):
    group_list = Group.objects.all()

    current_group = request.GET.get('group')

    current_group_name = 'Отдел:'

    role = get_role(request)

    date = request.GET.get('date')

    author = request.GET.get('author')

    author_name = 'Отчет от:'

    tag = request.GET.get('tag')

    user_groups = request.user.groups.all()

    author_list = User.objects.filter(groups__name=role)

    if date:
        date = datetime.datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")

    else:
        return HttpResponseRedirect('/')

    match_authors_list = []
    for group in user_groups:
        for author in User.objects.filter(groups__name=group):
            match_authors_list.append(author)
    print(match_authors_list)

    records = Record.objects.filter(author__in=match_authors_list).order_by('-created_date')

    dated_records = records.filter(report_date=date)

    search_query = dated_records.order_by('-created_date')
    notes = Notes.objects.order_by('-created_date')
    comments = Comments.objects.all()

    all_records = records.order_by('-created_date')

    context = {'search_query': search_query, "notes": notes, 'role': role,
               "author_name": author_name, "tag": tag, "author_list": author_list,
               "date": date, "author": author, "all_records": all_records,
               'current_group': current_group, 'group_list': group_list, 'current_group_name': current_group_name,
               'comments': comments}

    return render(request, 'search_result.html', context)


def find_by_group(request):

    roles = str(get_roles(request))
    user_groups = request.user.groups.all()

    print(user_groups)

    multirole = False

    if request.user.groups.all().count() > 1:
        multirole = True
    current_user = request.user
    match_authors_list = []
    for group in user_groups:
        for author in User.objects.filter(groups__name=group):
            match_authors_list.append(author)

    records = Record.objects.filter(author__in=match_authors_list).order_by('-created_date')

    notes = Notes.objects.filter(author__in=match_authors_list)

    comments = Comments.objects.all().order_by('-created')







