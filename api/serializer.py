from django.contrib.auth.models import User, Group
from rest_framework import serializers
from journal.models import Record


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ['author_name', 'text', 'report_date']