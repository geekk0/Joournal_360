from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages

from .models import Images, Comments, Notes, Record, ScheduledTasks


class RegistrationForm(forms.ModelForm):

    phone = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Подтвердите пароль'
        self.fields['phone'].label = 'Номер телефона'
        self.fields['email'].label = 'Email'

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email=email).exists() and self.cleaned_data['email'] != '':
            raise forms.ValidationError('Данный Email уже зарегистрирован')
        return email

    def clean_username(self):

        username = self.cleaned_data['username']

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с данным именем уже зарегистрирован')
        return username

    def clean(self):

        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError('Пароли не совпадают')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password', 'email', 'phone']


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином {username} не зарегистрирован')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError(f'Неверный пароль')

        return self.cleaned_data

    class Meta:

        model = User
        fields = ['username', 'password']


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Изображение')

    class Meta:
        model = Images
        fields = ('image', )


class AddNote(forms.ModelForm):

    text = forms.Textarea()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].label = 'Текст записи'

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = Notes
        fields = ['message']


class AddComment(forms.ModelForm):
    text = forms.Textarea()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].label = 'Текст коммента'

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = Comments
        fields = ['text']


class ResetPassword(forms.ModelForm):

    old_password = forms.CharField(label='Введите старый пароль', widget=forms.PasswordInput)
    new_password = forms.CharField(label='Введите новый пароль', widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(label='Повторите новый пароль', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Введите старый пароль'
        self.fields['new_password'].label = 'Введите новый пароль'


    def clean(self):


        old_password = self.cleaned_data['old_password']
        new_password = self.cleaned_data['new_password']


        confirm_new_password = self.cleaned_data['confirm_new_password']

        if new_password == old_password:
            raise forms.ValidationError(f'Новый пароль не отличается от старого')

        if new_password != confirm_new_password:
            raise forms.ValidationError(f'Введенные пароли не совпадают')

        username = self.cleaned_data['username']
        user = User.objects.get(username=username)

        if not user.check_password(old_password):
            raise forms.ValidationError(f'Неверный пароль')

        validate_password(new_password, user=user, password_validators=None)

        return self.cleaned_data

    class Meta:

        model = User
        fields = ['username', 'old_password', 'new_password', 'confirm_new_password']


class AddScheduledTaskForm(forms.ModelForm):

    start_date = forms.DateField(widget=forms.SelectDateWidget)
    start_date.label = 'На какой день(дни) задание'
    CHOICES = [(0, 'Понедельник'), (1, 'Вторник'), (2, 'Среда'), (3, 'Четверг'), (4, 'Пятница')
               , (5, 'Суббота'), (6, 'Воскресенье')]
    week_days = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=CHOICES, required=False)
    week_days.label = 'Дни недели:'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = ScheduledTasks
        fields = ['departments', 'start_date', 'name', 'week_days', 'regularity', 'text']


