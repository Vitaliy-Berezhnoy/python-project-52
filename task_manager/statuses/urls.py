from django.urls import path
from . import views

app_name = 'statuses'

urlpatterns = [
    path('', views.StatusesListView.as_view(), name='statuses'),
    path('create/', views.StatusCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.StatusUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.StatusDeleteView.as_view(), name='delete'),
]