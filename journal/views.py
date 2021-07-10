from django.shortcuts import render
from django.utils import timezone
from .models import Record


def rec_list(request):
    rec_list = Record.objects.all()
    return render(request, 'rec_list.html', {'rec_list': rec_list})


def record_full_text(request, rec_id):
    record_text = Record.objects.filter(id=rec_id)
    return render(request, 'record.html', {'record_text': record_text})
