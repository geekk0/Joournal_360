from django.conf import settings
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify


class Record(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               verbose_name='Отчет от')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата отправки')
    text = models.TextField(default='', verbose_name='Текст')
    report_date = models.DateField(blank=True, default=timezone.now,  verbose_name='За какое число')
    comments_count = models.IntegerField(default=0, editable=False, verbose_name='Количество комментов')

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.report_date)+' '+str(self.author)

    def get_comments_count(self):
        self.comments_count = len(Comments.objects.filter(record_id=self.id))
        self.save()

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


"""def get_image_filename(instance, filename):
    title = instance.record__str__
    slug = slugify(title)
    return "record_images/%s-%s" % (slug, filename)"""


class Images(models.Model):
    record = models.ForeignKey(Record, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='', verbose_name='Загрузить фото', blank=True, null=True)


def get_images(rec_name):
    return Images.objects.get(record=rec_name)


class EngRec(Record):

    tag_list = [('Без замечаний', 'Без замечаний'), ('Прямой эфир', 'Прямой эфир'),
                ('Запись', 'Запись'), ('Прямой эфир + Запись', 'Прямой эфир + Запись')]

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
                ('Запись', 'Запись'), ('Прямой эфир + Запись', 'Прямой эфир + Запись')]
    tags = models.TextField(default='Без замечаний', max_length=50, choices=tag_list, verbose_name='Теги')

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.report_date)+' '+str(self.author)

    class Meta:
        verbose_name = 'Запись в журнал режиссеров'
        verbose_name_plural = 'Записи в журнале режиссеров'


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


class EngNotes(Notes):

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.created_date)+' '+str(self.author)

    class Meta:
        verbose_name = 'Заметка инженеров'
        verbose_name_plural = 'Заметки инженеров'


class DirNotes(Notes):

    def publish(self):
        self.created_date = timezone.now()
        self.save()

    class Meta:
        verbose_name = 'Заметка режиссеров'
        verbose_name_plural = 'Заметки режиссеров'


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



