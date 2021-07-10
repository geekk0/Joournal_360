from django.urls import path
from . import views

urlpatterns = [
    path('', views.rec_list, name='rec_list'),
    path('запись/<int:rec_id>/', views.record_full_text, name='запись'),
]