from rest_framework.generics import ListAPIView, ListCreateAPIView

from journal.models import Record
from rest_framework import viewsets
from rest_framework import permissions
from api.serializer import RecordSerializer


class RecordsViewSet(ListCreateAPIView):
    queryset = Record.objects.order_by('-created_date')[:3]
    serializer_class = RecordSerializer
    permission_classes = [permissions.IsAuthenticated]
