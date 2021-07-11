from django.urls import path
from . import views


urlpatterns = [
    path('', views.rec_list, name='rec_list'),
    path('запись/<str:role>/<int:rec_id>', views.record_full_text, name='запись'),
    path('регистрация/', views.RegistrationView.as_view(), name='регистрация'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.user_logout, name='logout'),
]
