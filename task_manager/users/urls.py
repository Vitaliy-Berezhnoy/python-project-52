from django.urls import path
from task_manager.users import views


urlpatterns =[
    path('', views.UsersIndexView.as_view(), name='users'),
]