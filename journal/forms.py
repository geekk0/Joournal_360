from django import forms
from django.contrib.auth.models import User
from .models import Images, Comments, Notes, Record


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




