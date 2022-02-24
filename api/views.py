import time
from itertools import chain

from journal.models import Record
from rest_framework import viewsets
from rest_framework import permissions
from api.serializer import RecordSerializer, AuthSerializer
from django.contrib.auth.models import User, Group


class RecordViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        days = self.request.query_params.get('days')

        authors = User.objects.filter(groups__department=1)
        queryset_eng = Record.objects.filter(author__in=authors).order_by('-created_date')[:int(days)]
        queryset_it = Record.objects.filter(author__in=User.objects.
                                            filter(groups__department=2)).order_by('-created_date')[:int(days)]

        if int(days) != 1:                                                          # Подписка сменных инженеров
            queryset = queryset_eng
            return queryset

        else:                                                                  # Подписка каждый день
            queryset = chain(queryset_eng, queryset_it)
            return queryset

    def get_serializer_class(self):
        serializer_class = RecordSerializer
        return serializer_class

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated()]
        return permission_classes


class Subscribe(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        user_group = Group.objects.get(user=user)
        print(user, user_group)
        user_switch_date = Record.objects.filter(author_group=user_group).latest('report_date').report_date
        print(user_switch_date)
        print(type(user_switch_date))
        if user.has_perm('journal.change_record') or user_group.objects.filter(name="Трудовые резервы"):
            sub_type = '1'
        else:
            sub_type = '3'
        context = {'user_switch_date': user_switch_date, "sub_type": sub_type}
        return context

    def get_serializer_class(self):
        serializer_class = AuthSerializer
        return serializer_class


