from django.urls import include, path
from rest_framework import routers
from api import views

urlpatterns = [
    path('last_records/', views.RecordViewSet.as_view({'get': 'list'}),  name='последние_отчеты'),
    path('auth/', views.Subscribe.as_view({'get': 'list'})),
]
