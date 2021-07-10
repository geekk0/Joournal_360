from django.conf import settings
from django.db import models
from django.utils import timezone


class Record(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    text = models.TextField(default='')

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class EngRec(Record):
    issue_category = models.TextField(default='')


    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись в журнал инженеров'
        verbose_name_plural = 'Записи в журнале инженеров'


class DirRec(Record):
    issue_category = models.TextField(default='', verbose_name='проблемы с записью\эфиром')


    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Запись в журнал режиссеров'
        verbose_name_plural = 'Записи в журнале режиссеров'