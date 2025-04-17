from django.urls import path
from .views import (
    LoginView,
    RegisterView,
    user_list,
    user_detail,
    user_update,
    change_password,
    export_csv,
    me,
    delete_user
)

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', user_list, name='user-list'),
    path('<uuid:guid>/', user_detail, name='user-detail'),
    path('<uuid:guid>/update/', user_update, name='user-update'),
    path('change-password/', change_password, name='change-password'),
    path('export-csv/', export_csv, name='export-csv'),
    path('me/', me, name='me'),
    path('<uuid:guid>/delete/', delete_user, name='delete-user'),
]
