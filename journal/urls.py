from django.urls import path
from . import views


urlpatterns = [
    path('', views.rec_list, name='rec_list'),
    path('регистрация/', views.RegistrationView.as_view(), name='регистрация'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('добавить заметку/', views.AddNoteView.as_view(), name='добавить заметку'),
    path('удалить запись/', views.delete_note, name='удалить запись'),
    path('фильтр/', views.find, name='фильтр'),
    path('отправить отчет/', views.send_report, name='отправить отчет'),
    path('редактировать запись/<int:note_id>', views.edit_note, name='редактировать запись'),
    path('добавить комментарий/<int:record_id>', views.AddCommentView.as_view(), name='добавить комментарий'),
    path('найти по дате/', views.find_by_date, name='найти по дате'),
    path('выбор отдела/<int:group_id>', views.find_by_group, name='выбор отдела'),
    path('выбор автора/<int:author_id>', views.find_by_author, name='выбор автора'),
    path('найти по тексту/>', views.find_by_text, name='найти по тексту')
]


