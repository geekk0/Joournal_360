from django.conf import settings
from django.db import models
from django.utils import timezone


class Record(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               verbose_name='Отчет от')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата отправки')
    text = models.TextField(default='', verbose_name='')
    report_date = models.DateField(default=timezone.now,  verbose_name='За какое число')





    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.report_date)+' '+str(self.author)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class EngRec(Record):
    tag_list = [('Без замечаний', 'Без замечаний'), ('Прямой эфир', 'Прямой эфир'),
                ('Запись', 'Запись')]
    tags = models.TextField(default='Без замечаний', max_length=20, choices=tag_list, verbose_name='Теги')


    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.report_date)+' '+str(self.author)

    class Meta:
        verbose_name = 'Запись в журнал инженеров'
        verbose_name_plural = 'Записи в журнале инженеров'


class DirRec(Record):
    tag_list = [('Без замечаний', 'Без замечаний'), ('Прямой эфир', 'Прямой эфир'),
                ('Запись', 'Запись')]
    tags = models.TextField(default='Без замечаний', max_length=20, choices=tag_list, verbose_name='Теги')


    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.str(self.report_date)+' '+str(self.author)

    class Meta:
        verbose_name = 'Запись в журнал режиссеров'
        verbose_name_plural = 'Записи в журнале режиссеров'


class EngNotes(models.Model):
    message = models.TextField(default='', verbose_name='Текст заметки')
    created_date = models.DateField(default=timezone.now, verbose_name='Дата')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               verbose_name='от')

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
