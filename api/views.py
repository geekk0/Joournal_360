from rest_framework.generics import ListAPIView, ListCreateAPIView

from journal.models import Record
from rest_framework import viewsets
from rest_framework import permissions
from api.serializer import RecordSerializer


"""class RecordsViewSet(ListCreateAPIView):
        queryset = Record.objects.order_by('-created_date')[:days]
        serializer_class = RecordSerializer
        permission_classes = [permissions.IsAuthenticated]"""


class RecordViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        days = self.request.query_params.get('days')
        print(days)
        queryset = Record.objects.order_by('-created_date')[:days]
        return queryset

    def get_serializer_class(self):
        serializer_class = RecordSerializer
        return serializer_class

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated()]
        return permission_classes
