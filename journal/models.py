from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group


class Record(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               verbose_name='Отчет от')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата отправки')
    text = models.TextField(default='', verbose_name='Текст')
    report_date = models.DateField(blank=True, default=timezone.now,  verbose_name='За какое число')
    comments_count = models.IntegerField(default=0, editable=False, verbose_name='Количество комментов')
    author_group = models.CharField(blank=True, null=True, editable=False, verbose_name='Группа автора отчета', max_length=64)
    author_name = models.CharField(blank=True, null=True, editable=False, verbose_name='Имя и фамилия автора отчета', max_length=64)

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.report_date)+' '+str(self.author)

    def get_comments_count(self):
        self.comments_count = len(Comments.objects.filter(record_id=self.id))
        self.save()

    def get_author_group(self):
        auth_group = Group.objects.get(user=self.author)
        self.author_group = auth_group.name
        self.save()

    def get_author_names(self):
        author_firstname = User.objects.get(username=self.author).first_name
        author_lastname = User.objects.get(username=self.author).last_name
        self.author_name = author_firstname+' '+author_lastname
        self.save()

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class Notes(models.Model):
    message = models.TextField(default='', verbose_name='Текст заметки')
    created_date = models.DateField(default=timezone.now, verbose_name='Дата')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               verbose_name='от')

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.created_date)+' '+str(self.author)

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'


class Comments(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               verbose_name='Автор коммента')
    record_id = models.ForeignKey(Record, on_delete=models.CASCADE, verbose_name='К посту:')
    text = models.TextField(max_length=500, verbose_name='Текст коммента')
    created = models.DateField(default=timezone.now, verbose_name='')

    def publish(self):
        self.created = timezone.now()
        self.save()

    def __str__(self):
        return str(self.created)+' '+str(self.author)

    class Meta:
        verbose_name = 'Комменатрий'
        verbose_name_plural = 'Комментарии'


class Department(models.Model):
    groups = models.ManyToManyField(Group, blank=True)
    name = models.CharField(blank=True, verbose_name='Название отдела', max_length=64)

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'


class Images(models.Model):
    record = models.ForeignKey(Record, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='', verbose_name='Загрузить фото', blank=True, null=True)


def get_images(rec_name):
    return Images.objects.get(record=rec_name)









