from django.urls import path
from . import views


urlpatterns = [
    path('', views.rec_list, name='rec_list'),
    path('запись/<str:role>/<int:rec_id>', views.record_full_text, name='запись'),
    path('регистрация/', views.RegistrationView.as_view(), name='регистрация'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('добавить запись инженеров/', views.SendEngReportView.as_view(), name='добавить запись инженеров'),
    path('добавить запись режиссеров/', views.SendDirReportView.as_view(), name='добавить запись режиссеров'),
    path('добавить заметку инженеров/', views.AddEngNoteView.as_view(), name='добавить заметку инженеров'),
    path('добавить заметку режиссеров/', views.AddDirNoteView.as_view(), name='добавить заметку режиссеров'),
    path('удалить заметку/<int:note_id>', views.delete_note, name='удалить заметку'),
    path('фильтр/', views.find, name='фильтр'),
    path('отправить отчет/', views.send_report, name='отправить отчет'),
    path('редактировать/<int:note_id>', views.edit_note, name='редактировать'),
]


