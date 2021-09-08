from django.urls import path
from . import views


urlpatterns = [
    path('', views.rec_list, name='rec_list'),
    path('регистрация/', views.RegistrationView.as_view(), name='регистрация'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('добавить заметку/', views.AddNoteView.as_view(), name='добавить заметку'),
    path('удалить запись/', views.delete_note, name='удалить запись'),
    path('отправить отчет/', views.send_report, name='отправить отчет'),
    path('редактировать запись/<int:note_id>', views.edit_note, name='редактировать запись'),
    path('добавить комментарий/<int:record_id>', views.add_comment, name='добавить комментарий'),
    path('найти по дате/', views.find_by_date, name='найти по дате'),
    path('выбор автора/<int:author_id>', views.find_by_author, name='выбор автора'),
    path('найти по тексту/', views.find_by_text, name='найти по тексту'),
    path('добавить задачу/', views.add_objective, name='добавить задачу'),
    path('добавить статус/<int:objective_id>', views.add_status, name='добавить статус'),
    path('завершить задание/<int:objective_id>', views.finalize_objective, name='завершить задание'),
    path('добавить регулярное задание/', views.AddScheduledTask.as_view(), name='добавить регулярное задание'),
    path('добавить отчет/', views.new_edit_note, name='добавить отчет'),

    path('фильтр по отделу/<int:department_id>', views.sort_by_department, name='фильтр по отделу'),
    path('фильтр по группе/<int:group_id>', views.sort_by_group, name='фильтр по группе'),
    path('сменить пароль/', views.ResetPasswordView.as_view(), name='сменить пароль'),
    path('отправить email/', views.send_email, name='отправить email'),

    path('по дате мобильный/', views.by_date_view, name='по дате мобильный'),
    path('фильтр по отделу мобильный/', views.by_group_view, name='фильтр по отделу мобильный'),

]




