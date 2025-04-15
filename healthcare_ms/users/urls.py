from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_list, name='user-list'),
    path('<uuid:guid>/', views.user_detail, name='user-detail'),
    path('<uuid:guid>/update/', views.user_update, name='user-update'),
    path('change-password/', views.change_password, name='change-password'),
    path('export-csv/', views.export_csv, name='export-csv'),
    path('me/', views.me, name='me'),
]
