import itertools
import datetime
import json


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import DetailView, View
from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django import forms



from itertools import *
from operator import *

from .models import Notes, Record, Images, Comments, Department
from .forms import LoginForm, RegistrationForm, AddNote, AddComment, ResetPassword


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


class ResetPasswordView(View):

    def get(self, request, *args, **kwargs):
        form = ResetPassword(request.POST or None)
        form.initial['username'] = request.user.username
        context = {'form': form}
        return render(request, 'password_reset.html', context)

    def post(self, request, *args, **kwargs):
        current_user = request.user
        form = ResetPassword(request.POST or None)

        if form.is_valid():
            current_user.set_password(form.cleaned_data['new_password'])
            current_user.save()
            return HttpResponseRedirect('/')
        return render(request, 'password_reset.html', {'form': form})


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


def add_comment(request, record_id):

    record = Record.objects.get(id=record_id)

    input_text = request.GET.get('input_text')

    comment = Comments.objects.create(author_id=request.user.id, record_id=record)

    comment.text = input_text
    comment.created = timezone.now()
    comment.save()

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
    else:
        render(request, 'login.html')


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
    else:
        render(request, 'login.html')


def send_report(request): # Преобразует заметки в записи

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


def detect_admin_groups():
    all_users = User.objects.all()

    group_names = []


    for user in all_users:
        if user.has_perm('journal.change_record'):
            group_name = Group.objects.get(user=user.id)
            group_names.append(group_name)
    return group_names


@login_required
def rec_list(request, *device):

    admin_groups = detect_admin_groups()

    multirole = False

    roles = str(get_roles(request))
    user_groups = request.user.groups.all()

    user_departments_list = []

    for group in user_groups:

        deps = Department.objects.filter(groups=group)

        for dep_objects in deps:
            user_departments_list.append(dep_objects.name)


    if len(user_departments_list) > 1:
        multirole = True
    current_user = request.user
    match_authors_list = []

    user_departments = Department.objects.filter(groups__in=user_groups)

    for dep in user_departments:
        for group in Group.objects.filter(department=dep):
            for author in User.objects.filter(groups__name=group):
                match_authors_list.append(author)

    records = Record.objects.filter(author__in=match_authors_list).order_by('-created_date')

    notes = Notes.objects.filter(author__in=match_authors_list)

    comments = Comments.objects.all().order_by('-created')

    groups_authors_list = Group.objects.filter(department__in=user_departments).distinct().\
        exclude(name__in=admin_groups).order_by('id')

    shifts_dates = shifts_match()

    user_agent = request.META['HTTP_USER_AGENT']

    if 'Mobile' in user_agent:
        device = 'mobile'
    else:
        device = 'pc'

    context = {'records': records, 'comments': comments, 'roles': roles, 'current_user': current_user, 'notes': notes,
               'multirole': multirole, 'group_list': user_groups, 'author_list': match_authors_list,
               'user_departments': user_departments, 'groups_authors_list': groups_authors_list,
               'user_departments_list': user_departments_list, 'shifts_dates': json.dumps(shifts_dates),
               'device': device}



    return render(request, 'rec_list.html', context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def delete_note(request):

    user = request.user.id

    Notes.objects.filter(author=user).delete()
    return HttpResponseRedirect('/')


def comments_count(request, record_id):

    record = Record.objects.get(id=record_id)
    correct_count = len(Comments.objects.filter(record_id=record_id))
    record.comments_count = correct_count
    record.save()


def convert_date(date):

    set_year = date[:4]
    month = int(date[5:7])
    set_month = str(month - 1)
    set_day = date[8:10]

    set_date = set_year+', '+set_month+', '+set_day

    return set_date


def find_by_date(request):

    date = request.GET.get('date')

    multirole = False

    if request.user.groups.all().count() > 1:
        multirole = True

    admin_groups = detect_admin_groups()

    multirole = False

    roles = str(get_roles(request))
    user_groups = request.user.groups.all()

    user_departments_list = []

    for group in user_groups:

        deps = Department.objects.filter(groups=group)

        for dep_objects in deps:
            user_departments_list.append(dep_objects.name)

    if len(user_departments_list) > 1:
        multirole = True
    current_user = request.user.username
    match_authors_list = []

    user_departments = Department.objects.filter(groups__in=user_groups)

    for dep in user_departments:
        for group in Group.objects.filter(department=dep):
            for author in User.objects.filter(groups__name=group):
                match_authors_list.append(author)



    records = Record.objects.filter(author__in=match_authors_list).order_by('-created_date')

    groups_authors_list = Group.objects.filter(department__in=user_departments).distinct(). \
        exclude(name__in=admin_groups).order_by('id')

    if date:
        date = datetime.datetime.strptime(date, "%d.%m.%Y").strftime("%Y-%m-%d")


    else:
        return HttpResponseRedirect('/')

    for group in user_groups:
            for author in User.objects.filter(groups__name=group):
                match_authors_list.append(author)

    set_date = convert_date(date)

    all_records = Record.objects.filter(author__in=match_authors_list).order_by('-created_date')

    search_query = records.filter(report_date=date)

    notes = Notes.objects.order_by('-created_date')
    comments = Comments.objects.all()

    shifts_dates = shifts_match()

    context = {'search_query': search_query, 'comments': comments, 'roles': roles, 'current_user': current_user, 'notes': notes,
               'multirole': multirole, 'group_list': user_groups, 'author_list': match_authors_list,
               'set_date': set_date, 'user_departments': user_departments, 'groups_authors_list': groups_authors_list,
               'user_departments_list': user_departments_list, 'all_records': all_records,
               'shifts_dates': json.dumps(shifts_dates)}

    user_agent = request.META['HTTP_USER_AGENT']

    if 'Mobile' in user_agent:
        return render(request, 'search_result.html', context)

    return render(request, 'search_result.html', context)


def sort_by_group(request, group_id):

    shifts_dates = shifts_match()


    admin_groups = detect_admin_groups()

    multirole = False

    roles = str(get_roles(request))
    user_groups = request.user.groups.all()

    selected_group = Group.objects.get(id=group_id)

    user_departments_list = []

    for group in user_groups:

        deps = Department.objects.filter(groups=group)

        for dep_objects in deps:
            user_departments_list.append(dep_objects.name)

    current_user = request.user.username
    match_authors_list = []

    user_departments = Department.objects.filter(groups=selected_group)

    for dep in user_departments:
        for group in Group.objects.filter(department=dep):
            for author in User.objects.filter(groups__name=group):
                match_authors_list.append(author)


    records = Record.objects.filter(author__in=match_authors_list).order_by('-created_date')

    notes = Notes.objects.filter(author__in=match_authors_list)

    comments = Comments.objects.all().order_by('-created')

    groups_authors_list = Group.objects.filter(department__in=user_departments).distinct(). \
        exclude(name__in=admin_groups).order_by('id')


    all_records = Record.objects.filter(author__in=match_authors_list).order_by('-created_date')

    single_group = Group.objects.get(id=group_id)
    single_group_authors = User.objects.filter(groups__name=single_group)
    search_query = records.filter(author__in=single_group_authors).order_by('-created_date')

    comments = Comments.objects.all()

    context = {'search_query': search_query, 'comments': comments, 'roles': roles, 'current_user': current_user, 'notes': notes,
               'multirole': multirole, 'group_list': user_groups, 'author_list': match_authors_list,
               'user_departments': user_departments, 'groups_authors_list': groups_authors_list,
               'user_departments_list': user_departments_list, 'all_records': all_records, 'shifts_dates': json.dumps(shifts_dates)}

    return render(request, 'search_result.html', context)


def find_by_author(request, author_id):

    multirole = False

    if request.user.groups.all().count() > 1:
        multirole = True

    group_list = Group.objects.all()

    current_group = request.GET.get('group')

    current_group_name = 'Отдел:'

    role = get_role(request)

    roles = str(get_roles(request))

    date = request.GET.get('date')

    author = request.GET.get('author')

    tag = request.GET.get('tag')

    user_groups = request.user.groups.all()

    author_list = User.objects.filter(groups__name=role)

    match_authors_list = []
    for group in user_groups:
        for author in User.objects.filter(groups__name=group):
            match_authors_list.append(author)

    all_records = Record.objects.filter(author__in=match_authors_list).order_by('-created_date')

    search_query = Record.objects.filter(author_id=author_id).order_by('-created_date')

    comments = Comments.objects.all()


    context = {'search_query': search_query,  'role': role, "author_list": author_list,
               "author": author, "all_records": all_records, 'multirole': multirole, 'roles': roles,
               'current_group': current_group, 'group_list': group_list, 'current_group_name': current_group_name,
               'comments': comments}

    return render(request, 'search_result.html', context)


def find_by_text(request):

    admin_groups = detect_admin_groups()

    multirole = False

    user_groups = request.user.groups.all()

    input_text = request.GET.get('q')


    user_departments_list = []

    for group in user_groups:

        deps = Department.objects.filter(groups=group)

        for dep_objects in deps:
            user_departments_list.append(dep_objects.name)


    if len(user_departments_list) > 1:
        multirole = True
    current_user = request.user.username
    match_authors_list = []

    user_departments = Department.objects.filter(groups__in=user_groups)

    for dep in user_departments:
        for group in Group.objects.filter(department=dep):
            for author in User.objects.filter(groups__name=group):
                match_authors_list.append(author)

    records = Record.objects.filter(author__in=match_authors_list).order_by('-created_date')

    groups_authors_list = Group.objects.filter(department__in=user_departments).distinct().\
        exclude(name__in=admin_groups).order_by('id')

    search_query = records.filter(text__icontains=input_text).order_by('-created_date')

    all_records = records

    comments = Comments.objects.all().order_by('-created')

    groups_authors_list = Group.objects.filter(department__in=user_departments).distinct(). \
        exclude(name__in=admin_groups).order_by('id')

    shifts_dates = shifts_match()

    context = {'comments': comments, 'current_user': current_user, 'multirole': multirole,
               'group_list': user_groups, 'author_list': match_authors_list, 'search_query': search_query,
               'all_records': all_records, 'shifts_dates': json.dumps(shifts_dates),
               'groups_authors_list': groups_authors_list,}

    return render(request, 'search_result.html', context)


def sort_by_department(request, department_id):

    shifts_dates = shifts_match()

    admin_groups = detect_admin_groups()

    author_groups_list = Group.objects.filter(department=department_id)

    authors_list = User.objects.filter(groups__in=author_groups_list)

    records = Record.objects.filter(author__in=authors_list)

    user_groups = request.user.groups.all()

    current_user = request.user.username

    roles = str(get_roles(request))

    user_departments_list = []

    for group in user_groups:

        deps = Department.objects.filter(groups=group)

        for dep_objects in deps:
            user_departments_list.append(dep_objects.name)

    user_departments = Department.objects.filter(groups__in=user_groups)

    groups_authors_list = Group.objects.filter(department=department_id).distinct(). \
        exclude(name__in=admin_groups)

    comments = Comments.objects.all().order_by('-created')

    context = {'all_records': records, 'comments': comments, 'groups_authors_list': groups_authors_list,
               'current_user': current_user, 'roles': roles, 'user_departments': user_departments,
               'user_departments_list': user_departments_list, 'shifts_dates': json.dumps(shifts_dates) }

    return render (request, 'search_result.html', context)


def by_date_view(request):

    shifts_dates = shifts_match()

    context = {'shifts_dates': shifts_dates}

    return render(request, 'mobile_by_date.html', context)


def by_group_view(request):
    admin_groups = detect_admin_groups()

    multirole = False

    roles = str(get_roles(request))
    user_groups = request.user.groups.all()

    user_departments_list = []

    for group in user_groups:

        deps = Department.objects.filter(groups=group)

        for dep_objects in deps:
            user_departments_list.append(dep_objects.name)

    if len(user_departments_list) > 1:
        multirole = True
    current_user = request.user
    match_authors_list = []

    user_departments = Department.objects.filter(groups__in=user_groups)

    for dep in user_departments:
        for group in Group.objects.filter(department=dep):
            for author in User.objects.filter(groups__name=group):
                match_authors_list.append(author)
    groups_authors_list = Group.objects.filter(department__in=user_departments).distinct(). \
        exclude(name__in=admin_groups)

    user_agent = request.META['HTTP_USER_AGENT']


    context = {'groups_authors_list': groups_authors_list, 'current_user': current_user, 'multirole': multirole,
               'roles': roles, 'user_departments': user_departments}

    return render(request, 'mobile_by_group.html', context)


def create_shift_dates(start_date):

    shift_dates = []

    end_date = datetime.date(2024, 6, 15)

    delta = datetime.timedelta(days=4)

    while start_date <= end_date:
        shift_dates.append(str(start_date))

        start_date += delta
    return shift_dates


def check_dates_in_shifts(shift_dates, shift_name):

    start_check_date = datetime.date(2020, 6, 15)

    end_check_date = datetime.date(2024, 6, 15)

    shift_dates_dict = {}

    delta = datetime.timedelta(days=1)

    counter = 0

    while start_check_date <= end_check_date:

        if str(start_check_date) in shift_dates:
            shift_dates_dict.update({str(start_check_date): shift_name})
        start_check_date += delta
        counter += 1

    return shift_dates_dict


def shifts_match():
    shift_1_dates = create_shift_dates(datetime.date(2020, 6, 6))
    shift_2_dates = create_shift_dates(datetime.date(2020, 6, 7))
    shift_3_dates = create_shift_dates(datetime.date(2020, 6, 8))
    shift_4_dates = create_shift_dates(datetime.date(2020, 6, 9))

    match_dates_shift1 = check_dates_in_shifts(shift_1_dates, 'shift_1_dates')
    match_dates_shift2 = check_dates_in_shifts(shift_2_dates, 'shift_2_dates')
    match_dates_shift3 = check_dates_in_shifts(shift_3_dates, 'shift_3_dates')
    match_dates_shift4 = check_dates_in_shifts(shift_4_dates, 'shift_4_dates')

    match_dates_shift1.update(match_dates_shift2)
    match_dates_shift1.update(match_dates_shift3)
    match_dates_shift1.update(match_dates_shift4)

    all_shifts_match = match_dates_shift1

    return all_shifts_match




